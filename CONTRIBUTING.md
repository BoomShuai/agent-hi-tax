# 参与 Agent Hi Tax

> 发一句 `hi`，到底会消耗多少 token、积分、额度和时间？

Agent Hi Tax 是一个轻松但尽量可核验的观察项目。我们记录一句很小、内容完全确定的输入，通过一套真实 AI Agent 执行栈以后，外部能够看到多少消耗。

这不是模型智力 benchmark，也不是一张通用价格表。它测到的是整套系统共同产生的结果，包括 Agent harness、客户端版本、订阅或 API 计费通道、模型、effort、上下文、规则文件、工具、插件、中转站和工作区状态。

本项目的基本原则是：

> 脱离执行上下文的数字，只是一条轶事，不是一条可比较的测量记录。

## 文档语言与版本约定

当前贡献指南先以简体中文发布。未来英文版使用 `CONTRIBUTING.en.md`，与本页共用同一个 `protocol_version` 和同一套机器字段，不另造一套协议。

为了让中文和英文贡献能够被同一套程序校验：

- 面向人的说明、PR 正文和 `NOTES.md` 可以使用中文或英文；
- `manifest.yaml` 的字段名和枚举值固定使用英文；
- 输入本身的语言是实验变量，必须用 `prompt.language` 和不同的 case ID 区分；
- 将来中英文规则发生分歧时，以版本号更高的协议和 schema 为准，并在修订记录中说明差异。

## 当前阶段：人工试运行

仓库目前处于人工试运行阶段，还没有自动 runner，也没有最终版 schema 校验器。请先按照本页流程提交完整的 run package，并在 `NOTES.md` 中写清模板暂时无法表达的情况。

仓库维护者自己的样板测试也必须走同一流程：新建分支、准备证据包、填写清单、提交 PR、再按验收规则复核。不能因为是维护者自测，就直接把一个数字填进结果表。这样才能真正检验外部贡献流程是否可用。

## 一条结果代表什么

一个可区分的测试场景由下面这组变量共同确定：

`协议 × 输入 × Agent/载体/版本 × 认证/计费/订阅 × 路由 × 请求/观察到的模型 × 请求/观察到的 effort × 会话/工作区/harness 状态`

其中任何一项变化，都应视为另一个场景。例如：

- Codex CLI 与 Codex 桌面端是不同场景；
- 同一 Agent 的两个版本是不同场景；
- Plus、Pro、Max、API 按量计费是不同场景；
- `medium`、`high`、`xhigh` 是不同场景；
- 官方直连与第三方中转是不同场景；
- fresh session 与已有长对话的 resumed session 是不同场景；
- 空目录与带有大型 `AGENTS.md`、skills、MCP 的真实仓库是不同场景。

同一场景的独立重复测试非常欢迎。重复不是浪费，而是帮助观察波动、缓存、版本变化和偶然误差。

## 选择测试输入

第一个标准输入是：

- Case ID：`hi-en-v1`
- 编码：UTF-8
- 屏幕上输入的精确内容：`hi`
- 精确字节：`68 69`
- 不大写，不加标点，前后均无空白字符
- 在聊天界面中，Enter/Return 只负责提交，不算可见输入的一部分

欢迎测试其他输入，但必须遵守以下规则：

1. 每一种输入使用稳定且唯一的 case ID。
2. 把真正发送的内容原样保存到 `prompt.txt`。
3. 记录编码、语言、字节数和 SHA-256。
4. 不静默翻译、润色、补标点或添加说明。
5. 中文和英文版本属于不同 test case，不能共用同一个 case ID。
6. 如果 Agent 或中转站自动改写了输入，应把“用户输入”和“实际可观察到的发送内容”分开记录。

开始前先搜索仓库中已有的 runs 和 issues。独立复测永远欢迎；如果准备批量覆盖很多组合，或者准备认领一个长期缺失的组合，建议先开 issue，方便其他贡献者协调。

## 选择并披露环境类型

每次测试只能选择下面一种 `context.profile`。不同 profile 不得混进同一个比较组。

### `standard-clean`

新会话、空工作区，不启用贡献者自己增加的项目规则、MCP、插件、skills 或 hooks；产品内置行为仍然保留。只有能够核实这些条件时，才使用这个标签。

### `as-used`

贡献者平时真实使用的配置。它很有现实价值，但必须尽量列出会影响运行的规则、工具、插件、skills、MCP、hooks 和工作区状态。

### `custom`

特意设计的固定 fixture 或配置。条件允许时，应提供公开 fixture 地址和不可变的 commit。

不要为了获得 `standard-clean` 标签而随意删除个人配置。无法确认全局配置时，就用 `as-used`，并披露已知信息。私有规则不必公开正文，只记录文件名、作用域、字节数和 SHA-256 即可。

## 标准测试流程

### 1. 先声明，后执行

执行前先完成以下事项：

- 生成基于 UTC 的 run ID；
- 选定 prompt case、环境 profile 和场景变量；
- 写下计划重复次数；
- 创建 run package 目录和初始 `manifest.yaml`。

如果预先计划重复多次，就应提交全部 attempts，不能只挑 token 最少、额度变化最小或回复最好看的一次。每个 attempt 使用独立 run ID 和独立目录。

### 2. 隔离测量窗口

暂停会共用以下资源的其他活动：

- 同一账号或订阅额度；
- 同一 API project 或组织额度；
- 同一个中转站余额；
- 同一个团队共享用量计；
- 会在后台继续运行的 Agent、自动任务或重试。

如果 before 与 after 之间发生了无关调用，或者无法排除延迟入账的旧请求，应填写 `quota.contaminated: true`，并解释原因。受到污染的 token 机器记录仍可能有效，但共享额度差值不能再归因于本次 `hi`。

### 3. 记录配置

在发送输入以前，记录并尽量截图证明：

- Agent 产品、使用载体和精确版本/build；
- Agent 是官方、社区还是第三方发行；
- 登录方式、订阅档位和计费方式；
- 请求经过官方订阅、官方 API、中转站还是自部署服务；
- 请求模型、界面或日志实际暴露的模型；
- 请求 effort、实际暴露的 effort、推理模式和 service tier；
- 操作系统、架构、locale；
- fresh/warm/resumed 会话状态；
- 工作区、规则文件、工具、插件、skills、MCP 和 hooks。

网页产品没有公开版本号时，填写 `not_exposed`，同时保留测试时间和能够看到的 build 信息。不要猜版本。

### 4. 记录运行前基线

发出输入前，记录产品能够显示的 token、积分、额度百分比、余额或 usage 页面，并保存带 UTC 时间的截图。

产品不提供某个数字时填写 `not_exposed`，不能拿 0 代替。只有界面或机器日志明确报告为零时，才填写数值 0。

### 5. 进入声明过的会话状态

按 manifest 写明的 fresh、warm 或 resumed 状态开始，并确认不存在未披露的历史轮次或工作区规则。

不要试图提取产品隐藏的 system prompt。无法观察的内置上下文统一写 `not_exposed`，以产品版本作为主要代理变量。

### 6. 只发送一次完全一致的输入

- 不额外添加寒暄、说明、system message 或追问；
- 从提交瞬间开始计时；
- 除非场景本来就要求人工操作，否则不要取消、重试、批准意外动作或中途交互；
- 意外的工具调用、错误、超时或拒绝本身也应保存为结果；
- 不要因为第一次结果不好看就悄悄重跑并只提交第二次。

### 7. 记录完成状态

保存以下内容：

- 可见回复原文；
- 完成时间、总延迟和首个可见输出时间；
- 工具调用和人工批准次数；
- 产品暴露的每一个原生 usage 字段；
- 运行后的积分、额度或余额；
- 错误信息或取消原因。

能够获取时，应分别记录 input、cached input、output、reasoning 和 total tokens。不要只留下自己相加的 total。

### 8. 观察延迟更新的用量计

如果测试订阅额度或积分：

1. 先记录运行刚结束时的值；
2. 条件允许时，再记录大约 +2 分钟和 +10 分钟时的值；
3. 每条记录都写实际 UTC 观察时间；
4. 保存到 `quota-observations.csv`。

建议字段为：

```text
observed_at_utc,phase,raw_value,unit,note
```

用量计可能取整或异步更新。不能仅凭“下降了 1%”反推出一个隐藏 token 数字，也不能把两个不同重置周期的百分比直接比较。

### 9. 脱敏、核对并生成哈希

删除凭据和无关隐私，但不得修改测量数值、事件顺序或关键时间。所有脱敏和最终修改完成以后，再生成 `SHA256SUMS`。

### 10. 一个 PR 只提交一个场景

同一场景预先声明的多次重复可以放在同一个 PR 中。成功、报错、取消、超时和额度未变化的结果都应保留。

## 必须记录的变量

本页末尾的 `manifest.yaml` 模板中，每个 key 都应保留。无法填写时使用下面的固定值：

- `unknown`：按理可以知道，但贡献者本次无法确定；
- `not_exposed`：产品没有暴露这个信息；
- `not_applicable`：这个变量不适用于当前场景；
- `0`：只有能够确认确实为零时才能填写。

| 变量组 | 必须记录的内容 |
| --- | --- |
| Run 身份 | schema/协议版本、run ID、UTC 时间、attempt、计划重复次数、被替代的旧 run |
| Agent harness | 产品、厂商、官方/社区/第三方发行、CLI/web/desktop/IDE/API 载体、精确版本/build、安装来源 |
| 账号与计费 | 认证通道、订阅档位、计费方式、额度共享范围；不得记录邮箱或账号 ID |
| 请求路由 | 官方订阅、官方 API、第三方中转或自部署，以及服务商、中转站和兼容协议 |
| 模型与推理 | requested/observed model、核实方式、requested/observed effort、推理模式、service tier、暴露的生成参数 |
| 上下文与 harness | fresh/warm/resumed、历史轮次、工作区/fixture、规则指纹、工具、插件、skills、MCP、hooks、网络和权限模式 |
| 输入 | case ID、原文文件、编码、语言、字节数、哈希、前后空白和提交方式 |
| 测量结果 | 回复、状态、各类 token、额度/积分前后值、延迟、计时方式、工具调用、批准次数、污染状态 |
| 证据 | 证据等级、文件、脱敏位置、日志清洗方式、文件哈希、所有协议偏差 |

保留各家产品的原生标签。例如，一个产品的 `high` 不能静默等同于另一个产品的 `high`。requested 和 observed 必须分开记录。

模型选择器里的名称通常只能证明“请求了什么”。只有 Agent 状态、事件日志或服务方回执能够独立确认时，才填写 `model.observed`；否则写 `not_exposed`。

## 官方产品、订阅、API 与中转站

Agent 的发行方和推理请求经过的路由是两个不同变量。例如：

- 官方 Agent 使用官方订阅：`agent.distribution: first-party`，`route.category: first-party-subscription`；
- 官方 Agent 使用官方 API key：`agent.distribution: first-party`，`route.category: official-api`；
- 官方 Agent 配置成经过中转站：`agent.distribution: first-party`，`route.category: third-party-gateway`。

路由必须四选一：

- `first-party-subscription`：消耗计入官方个人版或团队版订阅；
- `official-api`：由模型厂商官方 API 计量或付费；
- `third-party-gateway`：经过中转、转售、聚合平台或兼容接口；
- `self-hosted`：在贡献者能够控制的基础设施上完成推理。

中转站测试还应记录：

- 公开名称和公开域名；
- OpenAI-compatible、Anthropic-compatible 或其他协议；
- 所宣称的上游模型；
- 能够独立观察到的上游模型；
- 已知的缓存、fallback、路由或降级设置。

中转站返回的模型标签只能算声明，不能单独证明官方上游模型确实被调用。

只要适用，就应记录订阅档位；即使预期 Plus、Pro、Max 或其他档位结果相同也要记录。订阅档位是解释变量，不能仅凭相关性就断言它导致了差异。

## 只报告原生单位，不擅自换算

- 尽量保留每一个原生 token 字段；
- 积分、点数、请求、百分比或货币按界面原样记录，同时写单位和重置周期；
- 除非服务商公开了精确对应关系，否则不能把订阅额度百分比换算成 token；
- 取整后的额度变化不能当成精确 token 数进行比较；
- 如果其他会话、其他产品、团队成员、历史请求或后台任务可能共用用量计，填写 `contaminated: true`；
- 延迟必须标明测量方法，手工秒表、界面计时、本地事件时间戳和服务方时间戳不能混为一谈；
- 如果机器日志和 UI 数值冲突，两个都保留并说明，不要自行挑选更好看的一个。

## 证据等级与最低要求

请尽量提供产品能够支持的最高证据等级：

- **Level A — 机器记录 + 视觉证据：** 脱敏后的原生事件/usage 日志，加上运行前后截图和文件哈希；
- **Level B — 视觉证据：** 有运行前后截图或连续录屏，但没有可用的机器日志；
- **Level C — 自报数据：** 缺少足以独立检查的证据，只作为讨论线索或待复测场景，在补充证据以前不进入有证据支持的比较数据集。

Level A 或 B 至少要能把同一次 run 与以下信息对应起来：

1. Agent 及版本；
2. 请求模型与 effort，以及产品能够暴露的 observed 值；
3. 适用时的订阅、计费通道和请求路由；
4. 运行前 token、积分或额度状态；
5. 精确输入和可见回复；
6. 完成后的 token、积分、额度或其他被声明的结果；
7. 各证据文件之间可核对的时间或其他关联信息。

如果一张图同时展示多项信息，可以一图多用。为了保护隐私可以裁剪，也可以用不透明色块脱敏，但不能删掉判断结果所必需的上下文。所有重要脱敏都要在 manifest 中列出。

条件允许时，可在被测输入以外的位置展示 run ID，例如旁边打开的文本文件或终端窗口。不要把 run ID 塞进 `hi` 本身，因为那会改变输入。

截图和日志只能提高可审计性，并不是一次运行真实发生过的密码学证明。PR 被接受，表示证据包足够完整且内部一致，不表示维护者担保贡献者身份或所有上游声明。

## 隐私与安全

绝对不要提交：

- API key、access token、cookie、authorization header、会话导出或恢复码；
- 账号邮箱、账号 ID、支付信息或私有 dashboard URL；
- 完整的私人配置目录，或与测试无关的聊天/会话历史；
- 私有仓库内容、机密规则正文或敏感本地路径；
- 中转站凭据，或带 secret、签名参数的 endpoint URL。

截图脱敏优先使用完全不透明的色块，而不是模糊处理；脱敏后应展平图片，并重新检查最终文件。清洗日志时，应保留 usage 事件、时间戳、事件顺序和测量数值。私有规则只提交指纹，不提交正文。

Git 会保留历史。如果凭据进入了 commit 或 PR，不能只在下一次提交中删除：应立即轮换或吊销凭据，并联系维护者清理历史。

## Run package 目录

人工试运行阶段统一使用下面的结构：

```text
runs/
  YYYY-MM-DD/
    <run-id>/
      manifest.yaml
      prompt.txt
      response.md
      config.png                 # 配置证据；需要时提供
      before.png
      after.png
      events.sanitized.jsonl     # 产品能够导出时提供
      quota-observations.csv     # 测量额度或积分时提供
      NOTES.md                   # 偏离协议之处及补充上下文
      SHA256SUMS
```

run ID 不要包含敏感信息，例如：

```text
2026-08-14T120000Z_codex-cli_gpt-5.6-sol_medium_hi-en-v1_ab12
```

完成脱敏和最终编辑后，在 run 目录中生成哈希：

```sh
find . -maxdepth 1 -type f ! -name SHA256SUMS -exec shasum -a 256 {} \; | LC_ALL=C sort > SHA256SUMS
```

Linux 用户可以使用 `sha256sum`，并在 `NOTES.md` 中写明实际命令。任何文件发生变化后都要重新生成哈希。

## `manifest.yaml` 试运行模板

字段名和枚举值保持英文。请替换所有占位内容；值为 `unknown`、`not_exposed` 或 `not_applicable` 的 key 也不要删除。

```yaml
schema_version: "pilot-0.1"
protocol_version: "manual-hi-tax-0.1"

run:
  id: "<UTC>_<agent>_<model>_<effort>_<case-id>_<short-random-id>"
  captured_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
  planned_repetitions: 1
  attempt: 1
  supersedes: "not_applicable"

contributor:
  github_handle: "@your-handle"

agent:
  product: "<product name>"
  vendor: "<vendor or project>"
  distribution: "first-party|community|third-party"
  surface: "cli|web|desktop|ide|api|other"
  version: "<exact version or not_exposed>"
  build: "<exact build or not_exposed>"
  install_source: "<official download, package manager, URL, or not_exposed>"

environment:
  os: "<name>"
  os_version: "<version>"
  architecture: "<arm64, x86_64, etc.>"
  locale: "<locale>"
  timezone: "<IANA timezone>"

account:
  auth_channel: "subscription-login|official-api-key|gateway-account|local|other"
  subscription_plan: "<Plus, Pro, Max, Team, not_applicable, or not_exposed>"
  billing_mode: "included-quota|pay-as-you-go|credits|local-compute|unknown"
  quota_shared_scope: "<account, workspace, team, API project, gateway balance, or unknown>"

route:
  category: "first-party-subscription|official-api|third-party-gateway|self-hosted"
  provider: "<provider or not_applicable>"
  gateway_public_name: "<name or not_applicable>"
  gateway_public_domain: "<public domain only, or not_applicable>"
  protocol: "native|openai-compatible|anthropic-compatible|other|unknown"
  upstream_model_claimed: "<model or not_applicable>"
  cache_policy: "<disabled, enabled, unknown, or not_applicable>"
  fallback_policy: "<disabled, description, unknown, or not_applicable>"

model:
  requested: "<exact selector/config value>"
  observed: "<independently exposed value or not_exposed>"
  observation_method: "ui-status|cli-status|event-log|provider-receipt|not_exposed"

reasoning:
  effort_requested: "<native label or not_exposed>"
  effort_observed: "<native label or not_exposed>"
  mode: "<standard, thinking, extended-thinking, etc., or not_exposed>"
  service_tier: "<native label or not_exposed>"

generation_parameters:
  temperature: "not_exposed"
  top_p: "not_exposed"
  max_output_tokens: "not_exposed"
  other: {}

context:
  profile: "standard-clean|as-used|custom"
  session_state: "fresh|warm|resumed"
  prior_user_turns: 0
  workspace_type: "empty-directory|repository|none|other"
  fixture_url: "not_applicable"
  fixture_commit: "not_applicable"
  instruction_files: []
  tools_enabled: []
  plugins_enabled: []
  skills_enabled: []
  mcp_servers_enabled: []
  hooks_enabled: []
  network_mode: "enabled|disabled|restricted|not_exposed"
  permission_mode: "<native label or not_exposed>"
  built_in_hidden_context: "not_exposed"
  notes: ""

prompt:
  case_id: "hi-en-v1"
  file: "prompt.txt"
  sha256: "<hash>"
  bytes: 2
  encoding: "UTF-8"
  language: "en"
  leading_whitespace: false
  trailing_whitespace: false
  submit_method: "typed|pasted|api|other"

timing:
  started_at_utc: "YYYY-MM-DDTHH:MM:SS.sssZ"
  completed_at_utc: "YYYY-MM-DDTHH:MM:SS.sssZ"
  method: "event-log|provider-timestamps|screen-recording|manual-stopwatch|other"
  wall_time_ms: "<integer or not_exposed>"
  time_to_first_visible_output_ms: "<integer or not_exposed>"

result:
  status: "succeeded|error|cancelled|timed-out"
  response_file: "response.md"
  tool_calls: 0
  approvals: 0
  error: "not_applicable"

usage:
  source: "event-log|ui|provider-dashboard|gateway-dashboard|not_exposed"
  input_tokens: "<integer or not_exposed>"
  cached_input_tokens: "<integer or not_exposed>"
  output_tokens: "<integer or not_exposed>"
  reasoning_tokens: "<integer or not_exposed>"
  total_tokens: "<integer or not_exposed>"
  native_other: {}

quota:
  source: "<UI/dashboard name or not_exposed>"
  unit: "percent|credits|points|requests|tokens|currency|not_exposed"
  before: "<raw displayed value or not_exposed>"
  after: "<raw displayed value or not_exposed>"
  delta: "<calculated value or not_exposed>"
  reset_window: "<displayed window or not_exposed>"
  observation_times_utc: []
  contaminated: false
  contamination_notes: "not_applicable"

evidence:
  level: "A|B|C"
  files:
    - "before.png"
    - "after.png"
  machine_log_sanitization: "<description or not_applicable>"
  redactions: []
  hash_file: "SHA256SUMS"

protocol:
  parallel_activity_on_same_meter: false
  deviations: []
  notes: ""
```

`instruction_files` 如需填写，建议采用下面的结构，不要提交私有正文：

```yaml
instruction_files:
  - scope: "global|project|directory"
    name: "AGENTS.md"
    bytes: 1234
    sha256: "<hash>"
```

## 提交 Pull Request

外部贡献者按普通 GitHub 流程操作：

1. Fork 仓库并创建新分支；
2. 按目录规范加入一个场景的 run package；
3. 完成脱敏、哈希和本页检查清单；
4. 提交 commit，并向本仓库发起 PR。

仓库维护者制作首批样板时也应新建分支并发起 PR，用同一套流程进行自测。

分支名建议为：

```text
run/<agent>-<model>-<effort>-<case-id>-<date>
```

PR 标题建议为：

```text
run: <agent> / <model> / <原生-effort> / <prompt-case> / <date>
```

PR 正文应说明：

- 测了什么，为什么测；
- 路由类型和证据等级；
- 计划和实际提交的重复次数；
- 所有偏离本协议的地方；
- 任何可能污染结果的因素；
- 这是新场景、独立复测，还是对旧结果的纠正。

## 提交前检查清单

- [ ] `prompt.txt` 与真正提交的输入完全一致。
- [ ] Agent、版本、订阅/计费路由、模型、effort 和会话状态均已记录。
- [ ] requested model/effort 和 observed model/effort 没有混为一谈。
- [ ] 观察窗口内没有未披露的活动共用同一个用量计。
- [ ] 预先计划的所有 attempts 均已提交，没有挑选最好看的结果。
- [ ] manifest、截图、日志和回复中的数值相互一致。
- [ ] 证据清晰、已脱敏，并已生成哈希。
- [ ] 不含密钥、个人标识符或无关私密内容。
- [ ] 中转站和 self-hosted 结果标签清晰，没有伪装成官方订阅结果。
- [ ] 所有不确定项、延迟更新和协议偏差均已披露。
- [ ] 本地执行 `git diff --check` 没有报错。

## 审核与纠错

维护者主要检查：

- 场景变量是否完整；
- 证据之间是否属于同一次 run；
- manifest、日志、截图和回复是否内部一致；
- 用量单位和 observed/requested 是否被正确区分；
- 是否存在隐私或凭据风险；
- 结果是否被放进正确的比较组。

维护者可以要求补充说明、降低证据等级、把字段改成 `unknown`、将结果拆到另一个比较组，或拒绝无法安全审查的证据包。

接受 PR 只代表它符合当前协议，不代表项目为某个厂商、模型、中转站或订阅背书，也不表示维护者对贡献者身份或上游模型声明提供绝对真实性担保。

已接受的 run package 应视为不可变的历史观察。如果确需纠正，请提交一个新 package，或做一次透明的 metadata 修正，填写 `run.supersedes` 并解释原因。不要为了让旧结果更好看而静默改写。

感谢你把一句小小的 `hi` 变成一条透明、可复核的观察记录，也感谢你帮助这个项目同时保持好奇、严谨和好玩。
