# WorkBuddy Desktop Hi Tax 采集适配器

> 当前样板验证版本：WorkBuddy 5.3.13（macOS）。其他版本可以使用，但必须记录 UI、SQLite 和 JSONL schema 差异。

本页把[通用贡献协议](../../CONTRIBUTING.zh-CN.md)映射成 WorkBuddy 桌面 IDE 的具体动作。WorkBuddy 的完整状态不能由命令行直接建立：终端只负责环境预检和空目录准备，目录选择、模型、场景、权限、新建会话和 prompt 提交都在 GUI 中人工完成。

## 一、场景级预检，只做一次

macOS 示例：

```sh
printf 'WorkBuddy version: '
plutil -extract CFBundleShortVersionString raw \
  /Applications/WorkBuddy.app/Contents/Info.plist

sw_vers
uname -m
date -u '+%Y-%m-%dT%H:%M:%SZ'

jq -r '
  .enabledPlugins
  | to_entries[]
  | select(.value == true)
  | "enabled_plugin=\(.key)"
' "$HOME/.workbuddy/settings.json"
```

另外保存一次能够证明账号计划、积分或计费模式的产品页面；拿不到时使用 `not_exposed` 或 `not_provided`，不从单次积分反推订阅档位。

截图原图先留在 Git 仓库外。终端 prompt、WorkBuddy 回复和设置页可能暴露用户名、主机名、home 路径、账号、Git identity、user ID 或 Session ID，公开前必须脱敏。

## 二、准备三个等价的空工作区

```sh
WORKBUDDY_HI_TAX_LAB="$HOME/agent-hi-tax-lab"
ATTEMPT="r1"  # 后续改为 r2、r3
RUN_DIR="$WORKBUDDY_HI_TAX_LAB/<scenario-slug>-$ATTEMPT"

mkdir -p "$RUN_DIR"
chmod 775 "$RUN_DIR"
cd "$RUN_DIR"
pwd
git rev-parse --show-toplevel
find . -mindepth 1 -maxdepth 1 -print
```

预期 `git rev-parse` 报告不是 Git 仓库，`find` 没有输出。截图、转录或证据文件不得放进被测目录。

## 三、在 GUI 中建立固定状态

对每个 attempt：

1. 在 WorkBuddy 中人工选择刚创建的目录。
2. 确认界面是空白新会话；如果显示旧对话，先新建会话，不能继续发送。
3. 固定 requested model，例如 `Auto` 或一个显式模型。
4. 固定 UI 场景，例如“日常办公”“代码开发”或“设计创意”。
5. 固定权限模式，例如“允许完全访问”。
6. 保存一张同时显示目录、requested model、UI 场景、权限和空白状态的启动截图。

把 submit method 记录为 `manual_gui`。`open -a WorkBuddy` 最多只是打开应用，不应被描述成能够自动建立上述状态的 launch command。

## 四、发送标准输入

只输入一次精确的 `hi` 并提交。等待任务完全结束，再保存包含下列信息的截图：

- 可见输入与完整回复；
- UI 显示耗时；
- 本次 WorkBuddy 积分；
- requested model 与实际路由模型；
- 没有额外对话或工具操作。

不要在同一个会话中继续追问，也不要复用到下一次 attempt。

## 五、会话外定位机器记录

WorkBuddy 5.3.13 的 session 元数据位于 `~/.workbuddy/workbuddy.db`，事件位于 `~/.workbuddy/projects/*/*.jsonl`。先用当前 cwd 定位私有 Session ID，但不要把 ID 输出到公开文件：

```sh
WORKBUDDY_RUN_DIR="$PWD"

WORKBUDDY_SESSION_ID="$(
  sqlite3 -readonly "$HOME/.workbuddy/workbuddy.db" \
    "SELECT id FROM sessions
     WHERE cwd='$WORKBUDDY_RUN_DIR'
     ORDER BY updated_at DESC LIMIT 1;"
)"

WORKBUDDY_TRANSCRIPT="$(
  find "$HOME/.workbuddy/projects" \
    -type f \
    -name "$WORKBUDDY_SESSION_ID.jsonl" \
    -print -quit
)"

test -n "$WORKBUDDY_TRANSCRIPT" && echo "transcript found"
```

不要加 `deleted_at IS NULL`：在 GUI 切换到下一目录后，上一条已完成 session 可能被软删除，但 JSONL 和用量记录仍然有效。路径不唯一时按 `updated_at` 取最新一条，并检查状态与时间是否对应本次 attempt。

状态字段可以在不公开 Session ID 的情况下读取：

```sh
sqlite3 -readonly -json "$HOME/.workbuddy/workbuddy.db" \
  "SELECT model, mode, permission_mode, source_mode,
          use_sandbox_cli, status, created_at, updated_at
   FROM sessions
   WHERE id='$WORKBUDDY_SESSION_ID';" \
| jq 'map(del(.id))'
```

## 六、提取并去重 rawUsage

一个 WorkBuddy turn 可能包含 message 和 function call 等多次 provider 调用。每条调用都可能带 `providerData.rawUsage`，必须按私有 `providerData.messageId` 去重，不能只取最终回复，也不能把重复快照相加：

```sh
jq -s -c '
  [
    .[]
    | select(
        .providerData.messageId != null
        and .providerData.rawUsage != null
      )
  ]
  | unique_by(.providerData.messageId)
  | map({
      timestamp,
      record_type: .type,
      model: .providerData.model,
      requested_model: .providerData.requestModelName,
      usage: {
        input_tokens_including_cached:
          (.providerData.rawUsage.prompt_tokens // 0),
        cached_input_tokens:
          (.providerData.rawUsage.prompt_cache_hit_tokens // 0),
        output_tokens:
          (.providerData.rawUsage.completion_tokens // 0),
        reasoning_output_tokens:
          (.providerData.rawUsage.completion_thinking_tokens // 0),
        total_tokens:
          (.providerData.rawUsage.total_tokens // 0),
        credit:
          (.providerData.rawUsage.credit // 0)
      }
    })
' "$WORKBUDDY_TRANSCRIPT"
```

标准 `hi` 如果没有工具调用，通常只有一个唯一 message call；如果结果不止一个，保留全部唯一调用并按调用聚合，不要删掉“不像预期”的记录。

积分还可以与 SQLite 交叉核验，不公开 request ID：

```sh
sqlite3 -readonly "$HOME/.workbuddy/workbuddy.db" \
  "SELECT credit_json FROM session_usage
   WHERE session_id='$WORKBUDDY_SESSION_ID';" \
| jq '{
    entries: (to_entries | length),
    total: ([to_entries[].value | tonumber] | add // 0)
  }'
```

这一步应在切换到下一个工作区之前立即执行。5.3.13 实测中，GUI 切换目录后上一条 session 可能被软删除，关联的 `session_usage` 也可能随之不可查；JSONL 仍然保留。SQLite 已缺失时保留 JSONL 原生积分并把交叉核验标成 `not_provided`，不要填成 0。

机器记录拿不到时仍可用截图提交 Level B。不要为了 Level A 运行不理解的脚本，也不要把原始 Session ID、message ID、request ID、JSONL 路径或完整私有日志提交到 Git。

## 七、WorkBuddy Token 关系

5.3.13 样板中的 `rawUsage` 关系为：

```text
non_cached_input_tokens
  = prompt_tokens - prompt_cache_hit_tokens

context_total_tokens
  = prompt_tokens + completion_tokens
```

`prompt_cache_hit_tokens` 是 `prompt_tokens` 的子集；`completion_thinking_tokens` 是 `completion_tokens` 的子集。两者都不能再次相加。

WorkBuddy credit 是独立的产品单位。除非产品公开精确换算公式，否则不要换算成 API 价格、订阅百分比或其他 Agent 的额度。

## 八、Auto 路由规则

如果三次固定选择 `Auto`，实际模型却不同，保持为同一个 Auto 场景：

- requested model 是场景变量；
- actual routed model 是逐次结果；
- 每次都必须保存实际模型；
- 不把不同实际模型的积分差解释成同一模型波动。

如果贡献者显式固定某个具体模型，模型变化才属于场景变化或执行错误。

## 九、提交前自查

- 三次都是新目录、空白新 session，没有继续旧对话。
- requested model、UI 场景、权限、plugins、settings 和网络状态保持一致。
- `Auto` 的实际路由模型按 attempt 单独记录。
- rawUsage 已按 message ID 去重，并与 SQLite 积分交叉核验。
- GUI 手工操作如实记录为 `manual_gui`。
- 公开文件不含账号、Git identity、用户名、主机名、绝对路径和各类 ID。
- 参考[WorkBuddy 完整样板](../../runs/2026-08-15/workbuddy-5.3.13_auto_craft_hi-en-v1_as-used_mac-arm64/README.md)填写结果。
