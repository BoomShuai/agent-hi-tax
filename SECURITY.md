# Security and privacy reporting

**English** | [中文](SECURITY.zh-CN.md)

This repository publishes screenshots, transcripts, and machine logs collected from real accounts. The most likely incident here is not a software vulnerability — it is **evidence that was published with something in it that should not have been**: a credential, an account email, a session identifier, a private path, or private repository content.

Report those privately. Do not open a public issue, do not comment on the PR, and do not paste the leaked value anywhere public.

## How to report

1. Use GitHub's private reporting: **Security → Report a vulnerability** on this repository (GitHub private vulnerability reporting). This creates a draft advisory visible only to you and the maintainers.
2. If that is unavailable to you, contact a maintainer listed in [.github/CODEOWNERS](.github/CODEOWNERS) through a private channel on GitHub and ask for a private channel before sending any detail.

In the report, include:

- the file path and, if you can, the commit;
- what kind of material is exposed (credential, email, session ID, private path, private content);
- **a description of where it appears, not the value itself** — for example "top-right corner of `evidence/status.png`", not the string.

## What happens next

- **Acknowledgement**: we aim to respond within 3 working days.
- **Containment**: for a live credential, rotation or revocation comes first — before any repository cleanup. A commit that removes a secret does not undo the exposure; anything pushed to a public repository must be treated as compromised.
- **Cleanup**: the affected files are corrected. Where the material is in Git history, an emergency history rewrite may be required. Before that rewrite, a maintainer temporarily and explicitly changes the admin ruleset bypass from `pull_request` to `always`, records the change in an auditable incident trail, and verifies the effective rules. The cleanup is then force-pushed; affected scenario packages have their `SHA256SUMS` regenerated and the results index rebuilt because the rewrite changes commit hashes. Immediately after cleanup, the maintainer restores the bypass to `pull_request` and rechecks the repository ruleset and the effective rules on `main`. The temporary `always` mode must never be left in place.
- **Disclosure**: an incident that affected published data is noted in the affected scenario package, without reproducing the exposed value.

Outside that temporary, explicit, and auditable emergency procedure, the admin bypass is PR-only. It cannot be used to directly push, force-push, or delete `main`.

## If you are the contributor who made the mistake

Report it yourself, quickly. Nothing bad happens to you for it, and the repository would rather fix a leak on day one than discover it a year later. Rotate the credential first, then tell us.

## Taking evidence down

If evidence of yours was published and you want it removed — your own screenshot, your account details, or content you did not intend to make public — request it through the same private channel, or open a **Data correction or takedown** issue if the request itself contains nothing sensitive. Removal requests about your own material are granted; the corresponding fields are then downgraded to `not_provided`, and the scenario record stays honest about what is no longer public.

## Software vulnerabilities

The scripts in this repository run locally and in CI over repository content; they are not a service and hold no secrets. Report anything you find in them (for example a path-handling flaw in the verification scripts, or a workflow injection in `.github/workflows/`) through the same private channel.

## Out of scope

- Product behaviour of the agents being observed. If a vendor's product exposes something it should not, report it to that vendor, not here.
- Disagreement with a published measurement. That is a normal issue or PR — see [CONTRIBUTING.md](CONTRIBUTING.md).
