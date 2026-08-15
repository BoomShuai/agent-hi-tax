# 第三个标准样板：Claude Code 2.1.220 / Opus 5 / high

这是 Agent Hi Tax 的第三个三次重复样板，也是第二个 Claude Code 模型样板。

## 场景

- Prompt：`hi-en-v1`，精确内容为两个 UTF-8 字节 `68 69`
- Agent：官方 Anthropic Claude Code 2.1.220
- 模型：requested alias 为 `opus`，observed model 为 `claude-opus-5`
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
- Footer mode：三次回复截图均显示 `manual mode on`

## 三次结果

| Attempt | 原生 input | Cache creation | Cache read | 派生总输入 | 原生 output | Context total | UI 耗时 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | 2 | 24,835 | 0 | 24,837 | 14 | 24,851 | 5 秒 |
| R2 | 2 | 24,664 | 0 | 24,666 | 13 | 24,679 | 5 秒 |
| R3 | 2 | 24,598 | 0 | 24,600 | 13 | 24,613 | 4 秒 |

这里的“派生总输入”严格按 Anthropic 原生字段相加：

`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`

`context_total_tokens` 再加上 `output_tokens`。它与 Codex 样板中“cached input 是 input 子集”的口径不同，不能共用一个缓存公式。参见 [Anthropic 官方定价与 usage 字段说明](https://docs.anthropic.com/en/docs/about-claude/pricing)。

聚合值：

- 原生 `input_tokens`：三次均为 2；
- `cache_creation_input_tokens`：中位数 24,664，范围 24,598–24,835，均为 1 小时 ephemeral cache creation；
- 派生总输入：中位数 24,666，范围 24,600–24,837；
- `context_total_tokens`：中位数 24,679，范围 24,613–24,851；
- 原生 `output_tokens`：中位数 13，范围 13–14；
- UI 整秒耗时：中位数 5 秒，范围 4–5 秒；
- 三次均无 web search、web fetch 或其他工具调用；
- 原始 `iterations` 字段三次均为空数组。

完整机器明细见 [RESULTS.csv](RESULTS.csv)，场景变量见 [manifest.yaml](manifest.yaml)。

## 最有意思的观察

可见输入仍然只有 `hi`，原生非缓存 `input_tokens` 也只有 2，但 fresh session 首次请求同时创建约 24.6K–24.8K 的 1 小时缓存输入。这描述的是完整 Claude Code `as-used` harness 的首次请求足迹，不是两个可见字符直接调用裸模型的成本。

三次回复出现三个文本变体：

- R1：`Hi! What can I help you with today?`
- R2：`Hey! What can I help you with?`
- R3：`Hi! What can I help you with?`

可见文本与原生 output token 数分别为 14、13、13。本样板只记录这种对应关系，不把三次样本解释成稳定的模型风格。

三次原始 `iterations` 都是空数组。它与前一 Fable 样板记录的单 message iteration 不同，但产品没有公开该字段的稳定语义，因此不能把空数组解释为“没有推理”，也不能把差异直接解释成稳定的模型特征。

## 与 Fable 样板不能直接归因比较

紧邻的 Fable 样板总输入中位数为 25,008，本样板为 24,666，表面相差 342 tokens。但 Fable 回复截图显示 `bypass permissions on`，本样板显示 `manual mode on`。Footer mode 是一个未控制的 harness 变量，因此当前差值标为 `mode-confounded`，不能归因给 Fable 或 Opus。

如果要做模型隔离比较，应在完全相同的 permission/mode、MCP、plugins、hooks、settings、CLI 版本与时间窗口下重测。保留这一混杂样板仍有价值，因为它展示了视觉证据如何发现一个容易遗漏的变量。

这些 token 也不能直接换算成 Claude Max 订阅额度。本样板没有测量滚动窗口百分比，更没有把 API 缓存定价套到订阅计划上。

## Transcript 提取边界

贡献者在每次正常退出后，用当前空目录自动定位本地 transcript，再用 `jq` 按私有 `message.id` 分组、保留时间最新记录。三次输出均只有一个最终 assistant message。

维护者账号没有读取贡献者私有 Claude transcript 目录的权限，因此公开事件忠实重现贡献者粘贴的 post-exit `jq` 输出，而不声称维护者直接检查了原始 transcript 文件。消息 ID、Session ID 和绝对路径不进入公开包。

## 证据

公开包包含：

- 同批次复用的[环境与认证脱敏截图](evidence/environment.redacted.png)；
- Opus 专属的[模型、effort、版本与 MCP 状态截图](evidence/status.redacted.png)；
- 三次公开回复截图：[R1](attempts/r1/response.png)、[R2](attempts/r2/response.png)、[R3](attempts/r3/response.png)；
- 场景级[脱敏预检转录](evidence/preflight.txt)和[harness 状态转录](evidence/harness.txt)；
- 三份最小 transcript 事件：[R1](attempts/r1/events.sanitized.jsonl)、[R2](attempts/r2/events.sanitized.jsonl)、[R3](attempts/r3/events.sanitized.jsonl)；
- 三份精确回复文本与 SHA-256；
- 私有原图与公开副本的[哈希登记表](evidence/private-evidence.md)，以及可复核的[遮挡审计记录](evidence/redaction-audit.txt)；
- 所有公开文件的 SHA-256。

私有截图原件不进入 Git。公开副本只用固定坐标的纯黑矩形覆盖敏感区域，不缩放、不裁剪、不模糊、不生成式重绘；遮挡范围之外的解码 RGB 像素与原图完全一致，Alpha 通道也完全一致。包级为 Level A，视觉证据公开可复核。

## 已知偏差

- R1 在测试输入前使用本地 `/effort` 与 `/status`；R2 使用 `/status`；提取结果均只有一个 assistant message。
- R3 公开回复图保留启动横幅，但没有保留状态面板；模型和 effort 另由场景状态图与机器事件支持。
- 三次 footer 均为 `manual mode on`，与 Fable 样板不同。
- Claude Max 计划已验证，但具体 5x/20x 倍率未取得证据，标为 `not_provided`。
- UI 延迟只显示取整秒数，不具备事件时间戳的毫秒精度。
- MCP 只记录“3 connected”，没有取得名称清单。
- Plugins、skills 与 hooks 保留真实用户配置，但没有公开其私有正文。
- 为减少观察动作，本轮没有在被测 session 内执行 `/usage`；usage 在正常退出后从本地 transcript 提取。
