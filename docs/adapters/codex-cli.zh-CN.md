# Codex CLI Hi Tax 采集适配器

> 当前样板验证版本：Codex CLI 0.147.0。其他版本可以使用，但必须记录版本与命令差异。

本页把[通用贡献协议](../../CONTRIBUTING.md)映射成 Codex CLI 的具体动作。它不是安全配置指南：不要为了测试关闭既有代理、sandbox、审批或账号安全措施；将它们作为 harness 变量如实记录。

## 一、场景级预检，只做一次

macOS 示例：

```sh
command -v codex
codex --version
sw_vers
uname -m
date -u '+%Y-%m-%dT%H:%M:%SZ'
```

另外保存订阅档位、模型、effort、路由、MCP、plugins、skills、hooks、权限模式和 settings source 的证据。命令输出或截图中的用户名、主机名、邮箱、账号 ID、绝对 home 路径和 session ID 不得进入公开包。

## 二、准备三个等价的空工作区

证据目录必须位于被测工作区之外。每次只创建当前 attempt 的目录：

```sh
CODEX_HI_TAX_LAB="$HOME/agent-hi-tax-lab"
ATTEMPT="r1"  # 后续改为 r2、r3
RUN_DIR="$CODEX_HI_TAX_LAB/<scenario-slug>-$ATTEMPT"

mkdir -p "$RUN_DIR"
chmod 775 "$RUN_DIR"
cd "$RUN_DIR"
pwd
git rev-parse --show-toplevel
find . -mindepth 1 -maxdepth 1 -print
```

预期 `git rev-parse` 报告不是 Git 仓库，`find` 没有输出。三个目录名除 `r1`、`r2`、`r3` 外保持一致，避免路径长度变化成为额外噪声。

## 三、固定启动命令

Codex CLI 0.147.0 的 `--model`、`--config`、`--cd` 和 `--no-alt-screen` 可用于显式固定模型、effort、工作区和终端滚动记录：

```sh
CODEX_MODEL="<exact-model>"
CODEX_EFFORT="<exact-effort>"

codex \
  --no-alt-screen \
  --model "$CODEX_MODEL" \
  --config "model_reasoning_effort=\"$CODEX_EFFORT\"" \
  --cd "$RUN_DIR"
```

如果场景还需要 feature、MCP、profile、sandbox 或审批参数，把它们写进 `launch-command.txt`，并在三次 attempt 中逐字保持一致。无法确认自己已经清空全局配置时，使用 `as-used`，不要声称是 `standard-clean`。

## 四、每次会话内只做这些动作

1. 启动后使用一次 `/status`，确认版本、模型、effort、工作区、权限模式和 `AGENTS.md` 状态。原始状态截图可能含账号与 Session ID，只能保存在 Git 仓库外。
2. 输入精确的 `hi` 并提交，不添加空格、标点或换行。
3. 回复完成后，保存一张同时包含输入和完整回复的截图。
4. 如需取得请求后的 context/usage UI，再使用一次本地 `/status`；不要发送第二条聊天消息。
5. 使用 `/quit` 正常退出并保存终端显示的 Token usage。不要 resume 这次会话继续测试。

Footer、权限模式或 collaboration mode 如果在三次之间变化，应拆场景或明确登记为混杂；不能只保留最接近预期的一次。

## 五、可选的机器记录提取

只有 UI 截图也可以提交 Level B。要提交 Level A，可以在退出后从本地 rollout 提取最小字段。Session ID 只用于本机定位，绝不能写入公开文件：

```sh
CODEX_SESSION_ID="<private-session-id>"
CODEX_ROLLOUT="$(
  find "$HOME/.codex/sessions" \
    -type f \
    -name "*$CODEX_SESSION_ID.jsonl" \
    -print -quit
)"

test -n "$CODEX_ROLLOUT" && echo "rollout found"
```

下面的 0.147.0 示例只输出版本、模型、effort、消息文本和原生 usage，不输出路径或标识符：

```sh
jq -s -c '
  {
    session_meta: (
      [ .[]
        | select(.type == "session_meta")
        | {timestamp, cli_version: .payload.cli_version}
      ] | last
    ),
    turn_context: (
      [ .[]
        | select(.type == "turn_context")
        | {timestamp, model: .payload.model, reasoning_effort: .payload.effort}
      ] | last
    ),
    messages: [
      .[]
      | select(.type == "response_item" and .payload.type == "message")
      | {
          timestamp,
          role: .payload.role,
          text: ([.payload.content[]?.text] | join(""))
        }
    ],
    token_counts: [
      .[]
      | select(
          .type == "event_msg"
          and .payload.type == "token_count"
          and .payload.info.last_token_usage != null
        )
      | {
          timestamp,
          usage: .payload.info.last_token_usage,
          model_context_window: .payload.info.model_context_window
        }
    ]
  }
' "$CODEX_ROLLOUT"
```

人工确认其中只有一个 `hi` 用户消息和一个最终 assistant 回复。若存在多个 token count，不要相加或挑最小值；先确认哪一个对应目标 turn，并在 `deviations` 中说明。原始 rollout 永远留在 Git 仓库外，公开包只保存核对过的最小事件。

## 六、Codex Token 关系

在 0.147.0 样板中：

```text
non_cached_input_tokens
  = input_tokens_including_cached - cached_input_tokens

context_total_tokens
  = input_tokens_including_cached + output_tokens

cli_total_excluding_cached
  = non_cached_input_tokens + output_tokens
```

Cached input 是 input 的子集，不能重复相加。CLI 显示 total 也不能直接解释成 ChatGPT 订阅额度成本。模型与 reasoning effort 应使用产品实际暴露的原生名称；当前模型能力与 effort 以[官方 OpenAI 模型指南](https://developers.openai.com/api/docs/guides/latest-model)为准。

## 七、提交前自查

- 三次都是新目录、新会话，没有 resume。
- launch command、模型、effort、权限模式和 harness 状态一致。
- 每次都有精确回复文本与截图；机器记录拿不到时明确降为 Level B。
- 公开文本和图片中没有 Session ID、resume 命令、邮箱、用户名、主机名或绝对路径。
- 参考[首个 Codex 完整样板](../../runs/2026-08-14/codex-cli-0.147.0_gpt-5.6-sol_high_hi-en-v1_as-used_mac-arm64/README.md)填写结果。
