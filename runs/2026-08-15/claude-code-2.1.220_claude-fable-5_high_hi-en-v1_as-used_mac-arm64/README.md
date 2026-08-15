# 第二个标准样板：Claude Code 2.1.220 / Fable 5 / high

这是 Agent Hi Tax 的第二个三次重复样板，也是第一个 Claude Code 样板。

## 场景

- Prompt：`hi-en-v1`，精确内容为两个 UTF-8 字节 `68 69`
- Agent：官方 Anthropic Claude Code 2.1.220
- 模型：requested 与 observed 均为 `claude-fable-5`
- Effort：requested 与 UI observed 均为 `high`
- 认证：Claude.ai 官方订阅登录
- 订阅：Claude Max；本次没有取得可证明具体倍率的页面
- 系统：macOS 26.5.2，arm64
- 会话：每次均为 fresh session
- 工作区：每次均为独立空目录、非 Git 仓库
- Profile：`as-used`
- MCP：状态页显示 3 个 connected，名称未采集
- Plugins 与 hooks：保留用户真实配置
- 网络：保留既有 wrapper 强制代理与安全预检
- 权限界面：`bypass permissions on`

## 三次结果

| Attempt | 原生 input | Cache creation | Cache read | 派生总输入 | 原生 output | Context total | UI 耗时 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | 2 | 25,441 | 0 | 25,443 | 30 | 25,473 | 5 秒 |
| R2 | 2 | 25,006 | 0 | 25,008 | 37 | 25,045 | 8 秒 |
| R3 | 2 | 25,006 | 0 | 25,008 | 37 | 25,045 | 6 秒 |

这里的“派生总输入”严格按 Anthropic 原生字段相加：

`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`

`context_total_tokens` 再加上 `output_tokens`。Anthropic 的公开用量说明也采用这三个输入桶相加的方式；它与 Codex 首个样板中“cached input 是 input 子集”的口径不同，不能共用一个缓存公式。参见 [Anthropic 官方定价与 usage 字段说明](https://docs.anthropic.com/en/docs/about-claude/pricing)。

聚合值：

- 原生 `input_tokens`：三次均为 2；
- `cache_creation_input_tokens`：中位数 25,006，范围 25,006–25,441，均为 1 小时 ephemeral cache creation；
- 派生总输入：中位数 25,008，范围 25,008–25,443；
- `context_total_tokens`：中位数 25,045，范围 25,045–25,473；
- UI 整秒耗时：中位数 6 秒，范围 5–8 秒；
- 三次可见回复完全一致；
- 三次均为一个 logical message iteration，web search、web fetch 和其他工具调用均为 0。

完整机器明细见 [RESULTS.csv](RESULTS.csv)，场景变量见 [manifest.yaml](manifest.yaml)。

## 最有意思的观察

可见输入只有 `hi`，原生非缓存 `input_tokens` 也只有 2，但 fresh session 首次请求同时创建了约 25K 的 1 小时缓存输入。这个数字描述的是完整 Claude Code `as-used` harness 的首次请求足迹，而不是两个可见字符直接调用裸模型的成本。

R2 与 R3 的输入字段完全一致；R1 的 cache creation 多 435 tokens。R1 在 `hi` 前执行过本地 `/model`、`/effort` 和 `/status` 命令，R2/R3 只执行 `/status`。Transcript 表明这些本地命令没有产生额外模型请求，但现有证据不足以把 435 tokens 的差异归因给其中某一个命令，因此只记录差异，不解释原因。

三次可见回复完全相同，但原生 `output_tokens` 为 30、37、37。产品没有暴露可把这些 token 与可见文本逐项对应的明细，因此不能把差值武断解释成某一种隐藏推理。

这些 token 也不能直接换算成 Claude Max 订阅额度。本样板没有测量滚动窗口百分比，更没有把 API 缓存定价套到订阅计划上。

## Transcript 提取

Claude Code 的本地 transcript 可能为同一个 assistant message 写入中间快照和最终快照。R1 原始文件中出现了两条 usage 相同、相隔 2 ms 的记录：第一条没有可见文本，第二条包含最终回复。

公开数据先按私有 `message.id` 分组，再保留时间最新的一条。消息 ID 本身属于会话连接键，不进入公开包。三次去重后都只有一个逻辑 assistant message。

## 证据

公开包包含：

- 场景级[脱敏预检转录](evidence/preflight.txt)；
- [harness 状态转录](evidence/harness.txt)；
- 三份去重后的最小 transcript 事件：[R1](attempts/r1/events.sanitized.jsonl)、[R2](attempts/r2/events.sanitized.jsonl)、[R3](attempts/r3/events.sanitized.jsonl)；
- 三份精确回复文本与 SHA-256；
- 私有视觉证据的[哈希登记表](evidence/private-evidence.md)；
- 所有公开文件的 SHA-256。

原始截图同时含有邮箱、组织名、本机路径、用户名或 Session ID，因此没有进入 Git。包级为 Level A，但视觉部分的字段状态明确标为 `private_evidence`，不能把私有哈希夸大为公开证明。

## 已知偏差

- R1 在测试输入前执行了额外本地 slash commands；没有观察到额外模型请求。
- R2、R3 只在测试输入前执行本地 `/status`。
- Claude Max 计划已验证，但具体 5x/20x 倍率未取得证据，标为 `not_provided`。
- UI 延迟只显示取整秒数，不具备事件时间戳的毫秒精度。
- MCP 只记录“3 connected”，没有取得名称清单。
- Plugins、skills 与 hooks 保留真实用户配置，但没有公开其私有正文。
- 为减少观察动作，本轮没有在被测 session 内执行 `/usage`；usage 在正常退出后从本地 transcript 提取。
