<!-- 中文贡献者：可以用中文填写本模板；规则见 CONTRIBUTING.zh-CN.md -->
## Scenario

- Scenario ID:
- Scenario directory: `runs/YYYY-MM-DD/<scenario-id>/`
- Agent / version:
- Model / effort:
- Subscription or billing channel:
- Route / harness profile:

## Attempts

- Planned attempts:
- Valid attempts:
- Invalid, error, or timed-out attempts, with reasons:

## Evidence

- Package-level evidence: Level A / B / C
- Visual evidence: public / private_evidence / not_provided
- Fields that are not exposed, not provided, self-reported, or conflicted:
- Did original images stay outside the Git repository at all times: yes / no

## Protocol deviations and confounders

Describe extra commands, permission or footer mode changes, MCP / plugin / hook differences, shared-quota contamination, and any difference that cannot be attributed to the model. Write "none" if there are none.

## Verification output

Paste the complete output of the following commands:

```text
./scripts/verify-run-package.sh runs/YYYY-MM-DD/<scenario-id>
python3 scripts/build-results-index.py
./scripts/verify-all.sh
```

## Pre-submission checklist

- [ ] This PR contains exactly one scenario and all of its attempts.
- [ ] There are at least 3 valid independent runs, and they are not parallel, resumed, or cherry-picked minimums.
- [ ] The prompt, Agent version, model, effort, route, permission mode, and harness are consistent across the valid attempts.
- [ ] Exactly one copy of scenario-level environment evidence is kept, with the reply and usage kept separately for each attempt.
- [ ] Native usage fields and derived formulas are both documented, and cached input is not double-counted.
- [ ] Invalid and anomalous attempts have not been silently deleted.
- [ ] Public text and images contain no credentials, email addresses, account IDs, session IDs, resume commands, usernames, hostnames, absolute home paths, or private content.
- [ ] Original visual images have not entered public Git history; redacted images have been visually inspected one by one.
- [ ] `private_evidence` is used only for originals a maintainer has actually verified.
- [ ] `SHA256SUMS` was generated after all public files were finalized.
- [ ] The root-level `RESULTS.md` has been regenerated.
- [ ] `./scripts/verify-all.sh` has passed.
