#!/bin/sh
# Check or apply the repository security features used by SECURITY.md.
#
# Usage:
#   ./scripts/apply-repo-security.sh [--check|--apply]
#
# --check is the default and never changes repository settings. --apply may
# enable private vulnerability reporting, secret scanning, and push protection.
# It deliberately does not modify other security-and-analysis settings.
set -eu

repo=${REPO:-aicodingresearch/agent-hi-tax}
mode=check

case ${1-} in
  ""|--check)
    ;;
  --apply)
    mode=apply
    ;;
  -h|--help)
    sed -n '2,11p' "$0"
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

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/agent-hi-tax-security.XXXXXX")
trap 'rm -rf "$work_dir"' 0 HUP INT TERM

repository_response=$work_dir/repository.json
pvr_response=$work_dir/private-vulnerability-reporting.json
expected_state=$work_dir/expected.json
actual_state=$work_dir/actual.json

write_expected_state() {
  jq -n '
    {
      private_vulnerability_reporting: true,
      secret_scanning: "enabled",
      secret_scanning_push_protection: "enabled",
      dependabot_security_updates: "enabled",
      secret_scanning_non_provider_patterns: "disabled",
      secret_scanning_validity_checks: "disabled"
    }
  ' >"$expected_state"
}

read_actual_state() {
  gh api "repos/$repo" >"$repository_response"
  gh api "repos/$repo/private-vulnerability-reporting" >"$pvr_response"

  jq -n \
    --slurpfile repository "$repository_response" \
    --slurpfile pvr "$pvr_response" '
      {
        private_vulnerability_reporting: $pvr[0].enabled,
        secret_scanning: $repository[0].security_and_analysis.secret_scanning.status,
        secret_scanning_push_protection: $repository[0].security_and_analysis.secret_scanning_push_protection.status,
        dependabot_security_updates: $repository[0].security_and_analysis.dependabot_security_updates.status,
        secret_scanning_non_provider_patterns: $repository[0].security_and_analysis.secret_scanning_non_provider_patterns.status,
        secret_scanning_validity_checks: $repository[0].security_and_analysis.secret_scanning_validity_checks.status
      }
    ' >"$actual_state"
}

compare_states() {
  if cmp -s "$expected_state" "$actual_state"; then
    echo "repository security features: match expected state"
    return 0
  fi

  echo "repository security feature drift detected (expected vs actual):" >&2
  diff -u "$expected_state" "$actual_state" >&2 || true
  return 1
}

write_expected_state
read_actual_state

if [ "$mode" = check ]; then
  compare_states
  exit $?
fi

for guarded_field in \
  dependabot_security_updates \
  secret_scanning_non_provider_patterns \
  secret_scanning_validity_checks
do
  expected_value=$(jq -r --arg field "$guarded_field" '.[$field]' "$expected_state")
  actual_value=$(jq -r --arg field "$guarded_field" '.[$field]' "$actual_state")
  if [ "$actual_value" != "$expected_value" ]; then
    echo "$guarded_field is '$actual_value', expected '$expected_value'" >&2
    echo "this script does not modify that setting; refusing to continue" >&2
    exit 1
  fi
done

if [ "$(jq -r '.private_vulnerability_reporting' "$actual_state")" != true ]; then
  echo "enabling private vulnerability reporting"
  gh api -X PUT "repos/$repo/private-vulnerability-reporting" >/dev/null
fi

secret_scanning=$(jq -r '.secret_scanning' "$actual_state")
push_protection=$(jq -r '.secret_scanning_push_protection' "$actual_state")
if [ "$secret_scanning" != enabled ] || [ "$push_protection" != enabled ]; then
  echo "enabling secret scanning and push protection"
  gh api -X PATCH "repos/$repo" --input - >/dev/null <<'JSON'
{
  "security_and_analysis": {
    "secret_scanning": {"status": "enabled"},
    "secret_scanning_push_protection": {"status": "enabled"}
  }
}
JSON
fi

read_actual_state
compare_states
echo "repository security feature apply completed"
