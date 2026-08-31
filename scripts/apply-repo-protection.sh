#!/bin/sh
# Check or apply the repository ruleset that protects the default branch.
#
# The classic branch-protection endpoint must remain unconfigured. This script
# refuses to continue if classic protection exists and never deletes it.
#
# Usage:
#   ./scripts/apply-repo-protection.sh [--check|--apply]
#
# --check is the default and never changes repository settings. --apply creates
# or updates the named repository ruleset and requires repository admin access.
set -eu

repo=${REPO:-aicodingresearch/agent-hi-tax}
branch=${BRANCH:-main}
# This exact existing name uses non-breaking hyphens. An ASCII lookalike must
# not silently create a second ruleset.
ruleset_name=${RULESET_NAME:-main‑branch‑protection}
mode=check

case ${1-} in
  ""|--check)
    ;;
  --apply)
    mode=apply
    ;;
  -h|--help)
    sed -n '2,12p' "$0"
    exit 0
    ;;
  *)
    echo "usage: $0 [--check|--apply]" >&2
    exit 2
    ;;
esac

if [ "$#" -gt 1 ]; then
  echo "usage: $0 [--check|--apply]" >&2
  exit 2
fi

for command_name in gh jq; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "required command not found: $command_name" >&2
    exit 1
  fi
done

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/agent-hi-tax-protection.XXXXXX")
trap 'rm -rf "$work_dir"' 0 HUP INT TERM

classic_response=$work_dir/classic-response.json
classic_error=$work_dir/classic-error.txt
ruleset_list=$work_dir/rulesets.json
effective_rules=$work_dir/effective-rules.json
expected_payload=$work_dir/expected.json
actual_payload=$work_dir/actual.json
expected_normalized=$work_dir/expected-normalized.json
actual_normalized=$work_dir/actual-normalized.json

check_classic_protection() {
  if gh api "repos/$repo/branches/$branch/protection" \
    >"$classic_response" 2>"$classic_error"; then
    echo "classic branch protection exists on $repo@$branch; refusing to continue" >&2
    echo "remove or reconcile it manually before managing the repository ruleset" >&2
    return 1
  fi

  if grep -q 'HTTP 404' "$classic_error" &&
    grep -q '"message":"Branch not protected"' "$classic_response"; then
    echo "classic branch protection: absent (expected)"
    return 0
  fi

  echo "could not verify that classic branch protection is absent" >&2
  sed -n '1,12p' "$classic_error" >&2
  return 1
}

write_expected_payload() {
  jq -n --arg name "$ruleset_name" '
    {
      name: $name,
      target: "branch",
      enforcement: "active",
      bypass_actors: [
        {
          actor_id: 5,
          actor_type: "RepositoryRole",
          bypass_mode: "pull_request"
        }
      ],
      conditions: {
        ref_name: {
          exclude: [],
          include: ["~DEFAULT_BRANCH"]
        }
      },
      rules: [
        {type: "deletion"},
        {type: "non_fast_forward"},
        {type: "creation"},
        {type: "update"},
        {
          type: "pull_request",
          parameters: {
            required_approving_review_count: 1,
            dismiss_stale_reviews_on_push: true,
            required_reviewers: [],
            require_code_owner_review: true,
            dismissal_restriction: {
              enabled: false,
              allowed_actors: []
            },
            require_last_push_approval: false,
            required_review_thread_resolution: true,
            require_extra_approval_for_unattributed_changes: true,
            allowed_merge_methods: ["merge", "squash", "rebase"]
          }
        },
        {
          type: "required_status_checks",
          parameters: {
            strict_required_status_checks_policy: true,
            do_not_enforce_on_create: false,
            required_status_checks: [
              {context: "verify"}
            ]
          }
        }
      ]
    }
  ' >"$expected_payload"
}

normalize_payload() {
  jq -S '
    {
      name,
      target,
      enforcement,
      bypass_actors: (
        .bypass_actors
        | map({actor_id, actor_type, bypass_mode})
        | sort_by([.actor_type, .actor_id, .bypass_mode])
      ),
      conditions: (
        .conditions
        | .ref_name.exclude |= sort
        | .ref_name.include |= sort
      ),
      rules: (
        .rules
        | map(
            if .type == "pull_request" then
              {
                type,
                parameters: {
                  required_approving_review_count: .parameters.required_approving_review_count,
                  dismiss_stale_reviews_on_push: .parameters.dismiss_stale_reviews_on_push,
                  required_reviewers: (
                    (.parameters.required_reviewers // []) | sort_by(tojson)
                  ),
                  require_code_owner_review: .parameters.require_code_owner_review,
                  dismissal_restriction: {
                    enabled: (.parameters.dismissal_restriction.enabled // false),
                    allowed_actors: (
                      (.parameters.dismissal_restriction.allowed_actors // [])
                      | sort_by(tojson)
                    )
                  },
                  require_last_push_approval: .parameters.require_last_push_approval,
                  required_review_thread_resolution: .parameters.required_review_thread_resolution,
                  require_extra_approval_for_unattributed_changes: .parameters.require_extra_approval_for_unattributed_changes,
                  allowed_merge_methods: (.parameters.allowed_merge_methods | sort)
                }
              }
            elif .type == "required_status_checks" then
              {
                type,
                parameters: {
                  strict_required_status_checks_policy: .parameters.strict_required_status_checks_policy,
                  do_not_enforce_on_create: .parameters.do_not_enforce_on_create,
                  required_status_checks: (
                    .parameters.required_status_checks
                    | map({context, integration_id: (.integration_id // null)})
                    | sort_by([.context, (.integration_id // -1)])
                  )
                }
              }
            else
              .
            end
          )
        | sort_by(.type)
      )
    }
  ' "$1"
}

compare_payloads() {
  normalize_payload "$expected_payload" >"$expected_normalized"
  normalize_payload "$actual_payload" >"$actual_normalized"

  if cmp -s "$expected_normalized" "$actual_normalized"; then
    echo "repository ruleset: matches expected policy"
    return 0
  fi

  echo "repository ruleset drift detected (expected vs actual):" >&2
  diff -u "$expected_normalized" "$actual_normalized" >&2 || true
  return 1
}

check_classic_protection
write_expected_payload

gh api "repos/$repo/rulesets?includes_parents=true&per_page=100" >"$ruleset_list"
gh api "repos/$repo/rules/branches/$branch" >"$effective_rules"

inherited_rule_count=$(jq '
  [
    .[]
    | select(.ruleset_source_type != "Repository")
  ]
  | length
' "$effective_rules")

if [ "$inherited_rule_count" -gt 0 ]; then
  echo "organization or inherited rules apply to $repo@$branch; refusing to continue" >&2
  jq -r '
    .[]
    | select(.ruleset_source_type != "Repository")
    | "  type=\(.type) source_type=\(.ruleset_source_type) source=\(.ruleset_source) ruleset_id=\(.ruleset_id)"
  ' "$effective_rules" >&2
  exit 1
fi

repository_count=$(jq --arg repo "$repo" '
  [.[] | select(.source_type == "Repository" and .source == $repo)] | length
' "$ruleset_list")
matching_count=$(jq --arg repo "$repo" --arg name "$ruleset_name" '
  [
    .[]
    | select(
        .source_type == "Repository"
        and .source == $repo
        and .name == $name
      )
  ]
  | length
' "$ruleset_list")

if [ "$matching_count" -gt 1 ]; then
  echo "multiple repository rulesets named '$ruleset_name'; refusing to choose one" >&2
  exit 1
fi

if [ "$repository_count" -ne "$matching_count" ]; then
  echo "unexpected additional repository rulesets exist; the target policy requires exactly one" >&2
  jq -r --arg repo "$repo" '
    .[]
    | select(.source_type == "Repository" and .source == $repo)
    | "  id=\(.id) name=\(.name) enforcement=\(.enforcement)"
  ' "$ruleset_list" >&2
  exit 1
fi

if [ "$matching_count" -eq 0 ]; then
  if [ "$mode" = check ]; then
    echo "repository ruleset '$ruleset_name' is missing" >&2
    exit 1
  fi

  echo "creating repository ruleset '$ruleset_name'"
  gh api -X POST "repos/$repo/rulesets" --input "$expected_payload" >"$actual_payload"
else
  ruleset_id=$(jq -r --arg repo "$repo" --arg name "$ruleset_name" '
    .[]
    | select(
        .source_type == "Repository"
        and .source == $repo
        and .name == $name
      )
    | .id
  ' "$ruleset_list")
  gh api "repos/$repo/rulesets/$ruleset_id" >"$actual_payload"

  if [ "$mode" = check ]; then
    compare_payloads
    exit $?
  fi

  rollback_dir=$(mktemp -d "${TMPDIR:-/tmp}/agent-hi-tax-ruleset-rollback.XXXXXX")
  rollback_payload=$rollback_dir/ruleset-$ruleset_id.json
  jq '{name, target, enforcement, bypass_actors, conditions, rules}' \
    "$actual_payload" >"$rollback_payload"
  chmod 600 "$rollback_payload"
  echo "rollback payload saved to a temporary directory: $rollback_payload"

  echo "updating repository ruleset '$ruleset_name' (id=$ruleset_id)"
  gh api -X PUT "repos/$repo/rulesets/$ruleset_id" \
    --input "$expected_payload" >"$actual_payload"
fi

compare_payloads
echo "repository ruleset apply completed"
