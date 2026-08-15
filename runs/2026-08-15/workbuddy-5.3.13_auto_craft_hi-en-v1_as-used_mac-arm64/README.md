# 第四个标准样板：WorkBuddy 5.3.13 / Auto / craft

这是 Agent Hi Tax 的第四个标准样板，也是第一个桌面 IDE、自动模型路由和产品积分样板。

## 场景

- Prompt：`hi-en-v1`，精确内容为两个 UTF-8 字节 `68 69`
- Agent：腾讯 WorkBuddy 5.3.13 桌面 IDE
- 请求模型：`Auto`
- 实际模型：R1、R2 为 `glm-5.2`，R3 为 `deepseek-v4-flash`
- UI 场景：`日常办公`
- 原生数据库 mode：`craft`
- 权限：`fullAccess`，UI 显示“允许完全访问”
- 系统：macOS 26.5.2，arm64
- 会话：每次均为独立目录、空白 fresh session
- 提交方式：在 WorkBuddy IDE 中人工选择目录、确认状态并手工提交 `hi`
- Profile：`as-used`
- 计量：WorkBuddy 原生 Token 与产品积分

## 三次结果

| Attempt | 实际模型 | Input（含缓存） | Cached input | 非缓存 input | Output | Thinking | Context total | 积分 | 事件耗时 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| R1 | GLM-5.2 | 32,119 | 9,920 | 22,199 | 382 | 281 | 32,501 | 4.46 | 11.628 秒 |
| R2 | GLM-5.2 | 33,043 | 9,920 | 23,123 | 436 | 255 | 33,479 | 4.66 | 8.470 秒 |
| R3 | DeepSeek-V4-Flash | 33,193 | 8,960 | 24,233 | 631 | 469 | 33,824 | 0.74 | 7.893 秒 |

WorkBuddy 的缓存与总量关系为：

```text
non_cached_input_tokens
  = input_tokens_including_cached - cached_input_tokens

context_total_tokens
  = input_tokens_including_cached + output_tokens
```

`reasoning_output_tokens` 是 `output_tokens` 的子集，不能再次相加。三次都只有一个原生 message API 调用，没有工具调用、Web 调用或人工批准。

聚合值：

- Input 中位数 33,043，范围 32,119–33,193；
- Cached input 中位数 9,920，范围 8,960–9,920；
- 非缓存 input 中位数 23,123，范围 22,199–24,233；
- Output 中位数 436，范围 382–631；
- Context total 中位数 33,479，范围 32,501–33,824；
- 事件耗时中位数 8.470 秒，范围 7.893–11.628 秒；
- 积分中位数 4.46，范围 0.74–4.66。

完整机器明细见 [RESULTS.csv](RESULTS.csv)，场景变量见 [manifest.yaml](manifest.yaml)。

## Auto 本身就是实验对象

三次请求条件完全相同，但 WorkBuddy 的 `Auto` 在 R3 更换了底层模型。它说明“请求模型”和“实际模型”必须分层记录：本样板的固定场景变量是 `Auto`，逐次结果则是实际路由模型。

因此，0.74 与 4.46／4.66 的积分差不能解释成同一模型的随机波动，也不能拿来证明 DeepSeek 与 GLM 的一般价格关系。本样板测到的是 WorkBuddy Auto 路由在这三个时点作出的选择及其原生计量。

## 空目录不等于空上下文

三次工作区在启动前都为空且不是 Git 仓库，但回复仍暴露了全局 Harness 上下文：

- R2 主动引用了贡献者的 Git identity；公开文本与截图已用 `[REDACTED_GIT_IDENTITY]` 替换。
- R3 根据工作区 basename，把 `agent-hi-tax-lab` 误解成税务／报税相关实验室。

这两项都不来自可见的两个字符 `hi`。它们证明桌面 Agent 的首次请求可能注入身份、记忆、工作区元数据或其他全局上下文；“空目录”只能排除项目文件，不能自动得到裸模型请求。

## 视觉回复差异

R1 和 R3 使用中文，R2 使用英文；三次都没有工具调用，但都生成了较长的“建立长期基本设置”回复。R2 的语言差异发生在与 R1 相同的 GLM-5.2 路由下，因此不能只归因于底层模型切换。

本项目只记录这种观察，不从三个样本推断稳定语言偏好、人格或模型指纹。

## 机器记录与积分交叉核验

每次完成后，本机只读 watcher 从 WorkBuddy fresh-session JSONL 提取全部带 `providerData.rawUsage` 的调用，按私有 `messageId` 去重，再用 SQLite `session_usage.credit_json` 逐 request 交叉核验。

三次均为：

- 1 个唯一 API call；
- JSONL `rawUsage.credit` 与 SQLite 积分完全匹配；
- 0 个工具调用；
- 0 个 Web 调用；
- session 状态为 completed。

watcher 在回复完成后读取本地记录并发送通知，不参与 WorkBuddy 推理，也没有额外模型调用。

## 证据

公开包包含：

- 场景级[环境与插件预检截图](evidence/environment.redacted.png)；
- 三次空白启动截图：[R1](attempts/r1/start.png)、[R2](attempts/r2/start.png)、[R3](attempts/r3/start.png)；
- 三次完整回复截图：[R1](attempts/r1/response.png)、[R2](attempts/r2/response.png)、[R3](attempts/r3/response.png)；
- 场景级[预检转录](evidence/preflight.txt)和 [Harness 状态](evidence/harness.txt)；
- 三份最小脱敏事件：[R1](attempts/r1/events.sanitized.jsonl)、[R2](attempts/r2/events.sanitized.jsonl)、[R3](attempts/r3/events.sanitized.jsonl)；
- 私有原图与公开副本的[哈希登记](evidence/private-evidence.md)和[遮挡审计](evidence/redaction-audit.txt)；
- 所有公开文件的 SHA-256。

私有原图不进入 Git。环境图遮盖用户名、主机名和 home 路径前缀；R2 遮盖 Git identity。处理未缩放、未裁剪、未模糊、未生成式重绘，遮挡区域之外的 RGB 像素与全部 Alpha 像素保持一致。

## 已知边界

- 未取得 WorkBuddy 订阅档位、倍率或账户总余额，因此只记录逐次原生积分。
- WorkBuddy 没有 CLI 状态流程；空目录由终端准备，Agent 状态和 prompt 由 GUI 手工操作。
- 5.3.13 在 GUI 切换目录后可能软删除上一条 session，并使其 SQLite `session_usage` 不再可查；本样板的 watcher 在每次切换前已完成三次匹配核验。
- UI 的“日常办公”和数据库的 `craft` 同时保留，不假设二者是同一字段的翻译。
- Exact skills、MCP 和每次请求实际注入的 plugin/tool schema 未暴露。
- R2 回复文本因身份隐私做了一处公开替换；私有原文 SHA-256 已登记。
- `Auto` 路由使本场景不是单一底层模型的受控比较。
