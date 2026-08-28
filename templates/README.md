# Templates

**English** | [中文](README.zh-CN.md)

Templates exist to reduce omissions, not to force every agent to masquerade as the same schema.

## Selection order

1. First copy `scenario-manifest.yaml` and `attempt-result.yaml`.
2. Then open the complete reference sample closest to the product under test, and copy its `RESULTS.csv` columns and provider-native usage fields.
3. Write `not_exposed` for fields the product does not expose; write `not_applicable` for fields that do not apply to that vendor; do not fill in `0` in place of a missing value.
4. `aggregate` should only aggregate fields that actually exist in `RESULTS.csv` and are clearly defined.
5. Delete the `comparison` template block when making no cross-scenario comparison; when permission modes, plugins, accounts, or other uncontrolled variables are present, keep the block and mark the confounding.

## Current reference samples

- [Codex CLI: OpenAI/Codex cached input is a subset of input](../runs/2026-08-14/codex-cli-0.147.0_gpt-5.6-sol_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [Claude Code Fable: Anthropic's three input buckets are additive](../runs/2026-08-15/claude-code-2.1.220_claude-fable-5_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [Claude Code Opus: recording a cross-sample mode confound](../runs/2026-08-15/claude-code-2.1.220_claude-opus-5_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [WorkBuddy Auto: cache is a subset of input; the actually routed model is a per-run result](../runs/2026-08-15/workbuddy-5.3.13_auto_craft_hi-en-v1_as-used_mac-arm64/manifest.yaml)

The templates still use `pilot-0.3`. What is new are optional record fields and fill-in notes; the raw semantics of existing samples have not been rewritten.
