# 首个标准样板：Codex CLI 0.147.0 / GPT-5.6 Sol / high

这是 Agent Hi Tax 的第一个三次重复样板。

## 场景

- Prompt：`hi-en-v1`，精确内容为两个 UTF-8 字节 `68 69`
- Agent：官方 OpenAI Codex CLI 0.147.0
- 模型：`gpt-5.6-sol`
- Reasoning effort：`high`
- 认证：ChatGPT 订阅登录
- 订阅：ChatGPT Pro 20x，Billing UI 截图已验证
- 系统：macOS 26.5.2，arm64
- 会话：每次均为 fresh session
- 工作区：每次均为独立空目录、非 Git 仓库
- Profile：`as-used`
- Plugins：通过启动参数关闭
- MCP：四个已知用户 MCP 通过启动参数关闭
- Skills：全局 skills 仍会进入 harness
- Hooks：用户 hooks 保留；检查脚本后确认没有额外模型调用

## 三次结果

| Attempt | 全部输入 | Cached input | 非缓存输入 | 输出 | Context total | CLI total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | 13,950 | 5,888 | 8,062 | 14 | 13,964 | 8,076（由事件日志推导） |
| R2 | 13,950 | 0 | 13,950 | 13 | 13,963 | 13,963 |
| R3 | 13,950 | 9,984 | 3,966 | 14 | 13,964 | 3,980 |

聚合值：

- `context_total_tokens`：中位数 13,964，范围 13,963–13,964；
- `cli_total_excluding_cached`：中位数 8,076，范围 3,980–13,963；
- 回复事件延迟：中位数 3,561 ms，范围 3,308–3,657 ms；
- tool calls、approvals 和 reasoning output tokens：三次均为 0。

完整机器明细见 [RESULTS.csv](RESULTS.csv)，场景变量见 [manifest.yaml](manifest.yaml)。

## 如何解释

`input_tokens_including_cached` 三次完全一致，说明这套 harness 给两个字符的 `hi` 带来了稳定的约 13.95K 输入上下文。CLI total 的明显波动来自自动缓存，不来自用户输入长度变化。

这里不把 CLI total 称为“真实成本”，也不把 weekly limit 的变化归因于这三次运行。测试时同一账户还有其他任务，且 UI 明确提示额度数据可能延迟。

## 证据

公开包包含：

- 一张[场景环境截图](evidence/environment.png)；
- 一张 [ChatGPT Pro 20x Billing UI 截图](evidence/subscription.png)；
- 三次输入与回复截图：[R1](attempts/r1/response.png)、[R2](attempts/r2/response.png)、[R3](attempts/r3/response.png)；
- 三份精简事件日志：[R1](attempts/r1/events.sanitized.jsonl)、[R2](attempts/r2/events.sanitized.jsonl)、[R3](attempts/r3/events.sanitized.jsonl)；
- 所有公开文件的 SHA-256。

包含邮箱、本机用户名、完整路径或 Session ID 的原图没有进入 Git。其哈希与缺失说明见 [private-evidence.md](evidence/private-evidence.md)。

## 已知偏差

- R1 没有保存 `/quit` usage 截图；CLI total 由事件日志确定性推导。
- R2 的 session 在本次 token 记录之后出现过一个没有 token_count 的 aborted turn；它位于测量窗口之外，已在单次结果中登记。
- R1/R2 的空目录检查有终端文字和本地复核，但没有逐次公开截图；R3 保存过截图但因本机标识留在私有证据中。
- weekly limit 受到同账户并发任务污染，不进入结果指标。
- UI 在首次请求前显示 1M context window，事件日志报告 258,400；两个观察均保留。
- 测试使用 `as-used` 而非 `standard-clean`，因为全局 skills 与用户 hooks 仍存在。
