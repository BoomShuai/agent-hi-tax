# Codex CLI 0.151.0-alpha.7.2 / GPT-5.6 Sol / medium

This package is a T-13 observation of Codex CLI with `gpt-5.6-sol` at `medium` reasoning effort on macOS arm64. It was preregistered in [Claim #49](https://github.com/aicodingresearch/agent-hi-tax/issues/49).

## Scenario

- Prompt: `hi-en-v1`, exactly `hi` as two UTF-8 bytes
- Agent: first-party OpenAI Codex CLI 0.151.0-alpha.7.2
- Model: `gpt-5.6-sol`
- Reasoning effort: `medium`
- Authentication and billing: ChatGPT subscription login; exact plan not exposed
- Route: first-party subscription, native protocol
- Session: three fresh sessions, sequentially executed
- Workspace: three separate empty non-Git directories, still empty after each run
- Valid-run surface: official `codex exec --json`
- Sandbox and approval: `workspace-write`, restricted filesystem/network, approval policy `never`
- Harness profile: `as-used`
- Harness inventory: one enabled MCP server (`node_repl`), 11 enabled plugins, 202 model-visible skill entries, an empty global `AGENTS.md`, and one local notification hook
- Evidence level: Level C; native machine event records are included, but visual evidence was unavailable

## Results

| Attempt | Input incl. cached | Cached input | Non-cached input | Output | Reasoning output | Context total | CLI total excl. cached | Latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | 20,421 | 11,008 | 9,413 | 14 | 0 | 20,435 | 9,427 | 1,727 ms |
| R2 | 20,421 | 11,008 | 9,413 | 14 | 0 | 20,435 | 9,427 | 3,761 ms |
| R3 | 20,421 | 11,008 | 9,413 | 14 | 0 | 20,435 | 9,427 | 1,883 ms |

All three valid runs produced the same visible reply:

> Hi! What would you like to work on?

The native input, cached input, non-cached input, output, reasoning output, and context total were identical across the three attempts. Latency varied and is retained only as descriptive metadata.

Codex reports cached input as a subset of input:

```text
non_cached_input_tokens
  = input_tokens_including_cached - cached_input_tokens

context_total_tokens
  = input_tokens_including_cached + output_tokens

cli_total_excluding_cached
  = non_cached_input_tokens + output_tokens
```

The CLI total is not interpreted as ChatGPT subscription quota cost. Subscription quota was not measured.

## Harness warning

Each `exec` run emitted the same local client warning: skill descriptions were shortened to fit the skills context budget. Codex reported that all skills remained visible with shortened descriptions. The warning is retained in every `result.yaml`; the target request still completed successfully, with one assistant message and no tool calls or approvals.

This is part of the measured `as-used` harness rather than a reason to discard the attempts. The full public-safe name inventory is in [available-skill-names.txt](evidence/available-skill-names.txt).

The preregistration and initial preflight recorded 199 skill names because the first public-safe parser truncated names at the first colon and collapsed three namespaced siblings. Post-run inspection of each retained rollout found the same 202 full names and the same inventory hash in R1–R3. This is a measurement-extraction correction, not a runtime configuration change; details are in [post-run-audit.txt](evidence/post-run-audit.txt).

## Evidence and deviations

The public package contains the exact prompt, launch command, preregistration record, public-safe preflight and harness inventory, workspace checks, sanitized event logs, result records, and hashes. Raw `exec` JSONL and rollout files remained outside Git. Public events retain only version, model, effort, the exact target `hi`, final reply, timestamps, and native usage.

An initial TUI preflight was cancelled before any target model request because the host PTY did not render a usable interface. It is preserved as `attempts/r0/result.yaml` and excluded from the three valid repetitions. Before R1, the valid-run surface was fixed to official `codex exec --json` and then held constant through R3.

No visual screenshot was available because local Computer Use safety controls denied access to both Terminal and the Codex host application. No screenshot was generated or reconstructed; visual fields are marked `not_provided` and package-level evidence is Level C.

## Comparison boundary

T-13 is intended to extend the effort axis from `high` to `medium`, but this contribution does not include a same-machine high-effort sibling package. Published high-effort packages also differ in harness inventory, version, OS, account, or capture time. Therefore this package establishes a reproducible medium-effort observation, but it does not by itself identify a token difference caused only by effort.
