# Claude Code Hi Tax 采集适配器

> 当前样板验证版本：Claude Code 2.1.220。其他版本可以使用，但必须记录版本、UI 和 transcript schema 差异。

本页把[通用贡献协议](../../CONTRIBUTING.md)映射成 Claude Code 的具体动作。保留贡献者既有的 wrapper、代理、sandbox 和账号安全设置；不要为了 Hi Tax 放宽安全边界。它们属于 harness，应在三次 attempt 中保持不变。

## 一、场景级预检，只做一次

macOS 示例：

```sh
command -v claude
claude --version
claude auth status
sw_vers
uname -m
date -u '+%Y-%m-%dT%H:%M:%SZ'
```

`claude auth status`、欢迎页和 `/status` 可能显示邮箱、组织、账号 ID、本地路径、代理和 Session ID。原图先保存在 Git 仓库外，公开前必须脱敏。

另外记录订阅档位、模型、effort、MCP connected 数量、plugins、skills、hooks、settings source、网络模式和 permission/footer mode。MCP 名称或私有设置正文无法公开时，保留数量与字段状态即可。

## 二、准备三个等价的空工作区

```sh
CLAUDE_HI_TAX_LAB="$HOME/agent-hi-tax-lab"
ATTEMPT="r1"  # 后续改为 r2、r3
RUN_DIR="$CLAUDE_HI_TAX_LAB/<scenario-slug>-$ATTEMPT"

mkdir -p "$RUN_DIR"
chmod 775 "$RUN_DIR"
cd "$RUN_DIR"
pwd
git rev-parse --show-toplevel
find . -mindepth 1 -maxdepth 1 -print
```

预期 `git rev-parse` 报告不是 Git 仓库，`find` 没有输出。截图和 transcript 副本不得放入这个工作区。

## 三、固定启动命令

2.1.220 可以显式传入 model 与 effort：

```sh
CLAUDE_MODEL="<exact-model-or-alias>"
CLAUDE_EFFORT="<exact-effort>"

claude --model "$CLAUDE_MODEL" --effort "$CLAUDE_EFFORT"
```

如果当前版本或 wrapper 不接受某个参数，可以在第一次模型请求前用本地 `/model` 或 `/effort` 设置，但三次必须采用同一种方式，并在 `launch-command.txt` 与 `protocol.deviations` 中说明。不要在 R1 设置默认值后，未经说明地让 R2/R3 继承。

## 四、每次会话内只做这些动作

1. 启动后使用一次 `/status`，私下记录 Session ID，同时确认版本、model、MCP、settings source、代理和工作区。
2. 确认欢迎页或 footer 的 effort 与 permission mode。三个 attempt 之间不要按 Shift+Tab 切换模式。
3. 输入精确的 `hi` 并提交。
4. 回复完成后，保存包含输入、完整回复、UI 延迟和 footer mode 的截图。
5. 正常退出；不要在被测 session 内运行 `/usage`，不要 resume 后继续采集。
6. 在 session 外读取 transcript。

`/status` 是本地观察动作，但仍应保持三次一致。若某次在 `hi` 前多执行了 `/model`、`/effort` 或其他命令，保留并登记偏差；确认它是否产生额外 assistant message，不能凭感觉认定“没有影响”。

## 五、退出后定位并去重 transcript

把 `/status` 中的 Session ID 只保存在本机变量中，先去掉复制时可能带入的换行：

```sh
CLAUDE_HI_TAX_SESSION_ID="<private-session-id>"
CLAUDE_HI_TAX_SESSION_ID="$(
  printf '%s' "$CLAUDE_HI_TAX_SESSION_ID" | tr -d '\r\n'
)"

CLAUDE_HI_TAX_TRANSCRIPT="$(
  find "$HOME/.claude/projects" \
    -type f \
    -name "$CLAUDE_HI_TAX_SESSION_ID.jsonl" \
    -print -quit
)"

test -n "$CLAUDE_HI_TAX_TRANSCRIPT" && echo "transcript found"
```

Claude Code 可能为同一个 assistant message 写入多条快照。不能逐行求和；按私有 `message.id` 分组，只保留 timestamp 最新记录：

```sh
jq -s -c '
  [
    .[]
    | select(
        .type == "assistant"
        and .message.id != null
        and .message.usage != null
      )
  ]
  | group_by(.message.id)
  | map(max_by(.timestamp))
  | map({
      timestamp,
      model: .message.model,
      usage: .message.usage,
      response: [
        .message.content[]?
        | select(.type == "text")
        | .text
      ]
    })
' "$CLAUDE_HI_TAX_TRANSCRIPT"
```

一个标准 `hi` attempt 应得到一个 logical assistant message。结果不为一个时，检查额外交互、hook、tool call 或重复记录；不要删除不方便解释的对象。公开事件必须移除 message ID、Session ID、邮箱、组织、用户名、主机名和绝对路径。

如果系统没有 `jq`，仍可提交视觉证据并标为 Level B；不要手工抄写一个声称来自机器日志的 Level A 事件。

## 六、Claude Token 关系

Claude Code 2.1.220 样板中的三个 input bucket 是相加关系：

```text
total_input_tokens
  = input_tokens
  + cache_creation_input_tokens
  + cache_read_input_tokens

context_total_tokens
  = total_input_tokens + output_tokens
```

不要把 cache creation/read 当作 `input_tokens` 的子集。原始 `iterations` 可能是数组；空数组应记录为原生观察，不能被解释成“没有推理”。这些 token 也不能直接换算成 Claude Max 的滚动窗口百分比。

## 七、提交前自查

- 三次都是新目录、新 session，没有 resume。
- model、effort、permission/footer mode、MCP、plugins、hooks、settings 和网络状态一致。
- transcript 已按 message ID 去重，没有逐行累加 usage。
- 每次都有精确回复文本与截图；机器记录拿不到时明确降为 Level B。
- 原图没有进入 Git，公开文件不含邮箱、组织 ID、Session ID 或绝对路径。
- 参考[Fable 完整样板](../../runs/2026-08-15/claude-code-2.1.220_claude-fable-5_high_hi-en-v1_as-used_mac-arm64/README.md)或[Opus 完整样板](../../runs/2026-08-15/claude-code-2.1.220_claude-opus-5_high_hi-en-v1_as-used_mac-arm64/README.md)填写结果。
