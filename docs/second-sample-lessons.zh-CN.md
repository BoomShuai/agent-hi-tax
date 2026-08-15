# 第二个样板带来的流程修订

本页记录 2026-08-15 完成 Claude Code 2.1.220 / Fable 5 / high 样板以后，对协议和采集流程做出的第二轮修订。

## 标准化语义，不标准化具体命令

不同 Agent 暴露相同事实的方式并不相同：

| 语义字段 | Codex CLI 0.147.0 | Claude Code 2.1.220 |
| --- | --- | --- |
| 版本 | `codex --version` | `claude --version` |
| 会话身份 | `/status` 与退出后的 resume 提示 | `/status` 与本地 transcript 文件 |
| 模型与 effort | 启动参数、`/status`、事件日志 | 启动参数、欢迎页、`/status`、`/effort`、transcript |
| 原生 usage | rollout 事件与退出 UI | 本地 transcript 的 `message.usage` |
| 继续会话 | Codex resume 命令 | Claude resume 命令 |

协议应统一要求“取得并证明会话身份、模型、effort 和 usage”，但每个 Agent 使用自己的 adapter。把 Codex 的具体命令硬塞给 Claude Code，会增加操作又不提高证据质量。

公开包不保存原始 Session ID。需要连接截图、transcript 和 attempt 时，私下使用 Session ID；公开时只保留 attempt 编号、必要时间戳、脱敏事件和原件哈希。

## Token schema 必须保留厂商原生语义

Codex 首个样板的 input 已包含 cached input，cached 是其中的子集。Claude 本次 transcript 则把 `input_tokens`、`cache_creation_input_tokens` 和 `cache_read_input_tokens` 作为三个需要相加的输入桶。

因此模板升级为双口径：

- OpenAI/Codex 风格字段保留“包含 cached 的 input”及其子集；
- Anthropic 风格字段保留普通 input、cache creation 和 cache read；
- 只有明确写出公式的派生 `total_input_tokens` 与 `context_total_tokens` 才允许跨 attempt 汇总；
- 不把任何派生 total 自动叫作订阅成本。

校验脚本现在会分别检查两种算术关系，避免 cached input 重复相加或漏加 cache creation。

## Claude transcript 必须按消息去重

R1 transcript 对同一个 assistant message 写了两条 usage 相同的快照：先是空文本中间记录，再是带最终文本的记录。如果逐行求和，会把一次 `hi` 错算成两次请求。

Claude adapter 的固定规则是：

1. 只取 `type=assistant` 且存在 `message.id` 与 `message.usage` 的记录；
2. 按 `message.id` 分组；
3. 每组只保留 timestamp 最新的一条；
4. 在公开输出中删除 `message.id`；
5. 再检查 logical message 数量、iterations 和工具调用。

这项检查应自动化，不能要求贡献者肉眼判断重复行。

## 采集动作本身也可能成为观察变量

Claude Code 的 `/status` 是获取 Session ID 的现实入口，本轮 transcript 证明它没有产生第二个模型响应。为了保持三个 attempt 更一致，后续标准流程仍应只使用必要的本地命令：

1. 启动时用参数固定 model 与 effort；
2. 只运行一次 `/status` 取得私有 Session ID；
3. 发送唯一测试 prompt；
4. 截图后正常退出；
5. 在 session 外读取 transcript。

本轮没有在被测 session 内运行 `/usage`。这不是宣称 `/usage` 一定会调用模型，而是减少不必要的观察动作，使微小输入测试更容易复现。

R1 在 `hi` 前执行过 `/model`、`/effort` 和 `/status`；R2/R3 只执行 `/status`。R1 仍然有效，因为没有额外模型请求且显式启动参数没有改变，但它被登记为协议偏差。后续不再重复这些配置命令。

## 环境证据继续只采一次

本轮再次证明，版本、OS、订阅、路由和固定 harness 不需要每次截图。三次 attempt 各自只需要：

- 输入与完整回复；
- UI 显示延迟；
- 私有 Session ID；
- 退出后去重得到的最小 usage；
- 异常与工具调用。

场景级一次性采集：

- 版本、系统、架构、UTC 时间；
- 订阅与认证；
- 模型与 effort UI；
- MCP、plugins、hooks、settings、网络和权限模式；
- 空目录与非 Git 规则。

## 证据脱敏不能依赖临场手工

Claude 欢迎页同时展示模型、effort、订阅、组织和邮箱；`/status` 又同时展示模型、MCP、路径、邮箱和 Session ID。一个截图既很有证据价值，也很难直接公开。

当前样板选择：

- 原图留在仓库外；
- 公开 SHA-256 与未公开原因；
- 发布最小脱敏转录和 transcript 事件；
- 字段状态标为 `private_evidence`。

下一步适合开发确定性脱敏辅助工具：只做不透明遮挡、裁切、字段转录和哈希，不生成或重绘证据内容。工具必须保留原图哈希，并让维护者逐张目视验收。

## 下一个 harness 应该做成 Agent adapter

适合自动化的最小架构是：

`scenario protocol → agent adapter → private evidence → sanitizer → public package → validator`

Claude adapter 可以自动完成：

1. 采集版本与经过允许的环境字段；
2. 建立等长命名的 fresh 空目录；
3. 保存 Session ID 到私有清单；
4. 按当前工作区与时间定位 transcript；
5. 按 message ID 去重；
6. 提取 usage、response、model、service tier、speed、iterations 和 server tool use；
7. 生成公开事件、attempt YAML 和哈希；
8. 扫描邮箱、绝对路径、UUID 与 resume 命令。

交互式 TUI 与 `--print --output-format json` 不应混为同一场景。后者更容易自动化，但 surface 和 harness 可能变化，应作为独立场景测试。

## 第二个样板的主要结果

三个 fresh session 的原生普通 input 均为 2 tokens，同时创建了 25,006–25,441 tokens 的 1 小时 cache。派生 context footprint 为 25,045–25,473 tokens。R2 与 R3 的所有 token 字段完全一致；三次可见回复也完全一致。

这个结果很适合作为项目的第二个样板：它既展示了“两个字符背后约 25K harness”的趣味性，也证明不同 Agent 的缓存字段不能靠一个通用 total 草率比较。
