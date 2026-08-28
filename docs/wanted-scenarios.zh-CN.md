# 待测场景清单

> 每一条都是一个可以独立认领、独立完成、独立提交 Pull Request 的任务。

本页更新于 2026-08-28。已完成的场景见 [Hi Tax Index](../RESULTS.md)；逐步操作方法见[实测指南](contributor-walkthrough.zh-CN.md)。

## 怎么用这个清单

1. 先盘点自己手头有什么：哪个 Agent 产品、什么订阅档位、什么操作系统。**不要为了完成任务去购买订阅**；挑和现有资源匹配的任务。
2. 在仓库开一个 issue 认领，标题写 `[认领] T-xx 一句话场景描述`，正文写明计划使用的 Agent 版本、模型、订阅档位和预计完成时间。没有合适任务也可以在 issue 里提出新组合。
3. 同一个任务允许多人认领：不同人、不同设备、不同账号的独立复测本身就是有价值的贡献，只要在 issue 和 PR 里写清楚即可。
4. 认领后按[实测指南](contributor-walkthrough.zh-CN.md)逐步执行；规则细节以[贡献指南](../CONTRIBUTING.md)为准。
5. 一个任务对应一个场景、一个 PR。个别对照类任务（标注"2 场景"）会产出两个场景包，就提交两个 PR。

**关于版本**：清单里引用的产品版本是现有样板采集时的版本。你实际装到的多半更新——这不影响任务成立：版本不同就是一个新场景，同样有观察价值。请如实记录你安装的精确版本，不要刻意降级。

**难度说明**：

- ★ 有现成采集适配器和完整样板可照抄，改动最小；
- ★★ 有适配器，但要改变一个场景变量并保持其余不变；
- ★★★ 没有现成适配器，需要自己摸清产品的 usage 暴露方式和脱敏点。

首次参与预留 2–4 小时；做过一次之后约 1.5–3 小时。

---

## A. 入门：独立复测现有场景（难度 ★）

复测是最好的第一个任务：样板、适配器、字段全部有现成参照，你只需要严格执行并如实记录。这也是检验"这套数据是否可复现"的唯一方式。

### T-01 复测：Codex CLI × gpt-5.6-sol × high

- **场景**：官方 Codex CLI（当前版本）× `gpt-5.6-sol` × `high` × ChatGPT 订阅 × fresh session × 空目录。
- **你需要**：任意档位的 ChatGPT 订阅（与样板的 Pro 20x 不同就如实记录）。
- **为什么优先**：现有样板只有维护者一人一机一次的观察；输入上下文是否稳定在约 13.95K tokens、缓存波动模式是否重现，都需要独立数据点。
- **参照**：[Codex CLI 适配器](adapters/codex-cli.zh-CN.md)、[现有样板](../runs/2026-08-14/codex-cli-0.147.0_gpt-5.6-sol_high_hi-en-v1_as-used_mac-arm64/README.md)。

### T-02 复测：Claude Code × Fable 5 × high

- **场景**：官方 Claude Code（当前版本）× `claude-fable-5` × `high` × Claude 订阅 × fresh session。
- **你需要**：Claude Pro 或 Max 订阅。
- **为什么优先**：验证"普通 input 仅 2 tokens + 约 25K cache creation"的结构是否在其他账号和配置下重现；注意三次 attempt 保持同一 permission mode。
- **参照**：[Claude Code 适配器](adapters/claude-code.zh-CN.md)、[现有样板](../runs/2026-08-15/claude-code-2.1.220_claude-fable-5_high_hi-en-v1_as-used_mac-arm64/README.md)。

### T-03 复测：WorkBuddy × Auto

- **场景**：WorkBuddy 桌面 IDE（当前版本）× `Auto` × fresh session × 独立空目录。
- **你需要**：WorkBuddy 账号（有积分显示）。
- **为什么优先**：Auto 路由的模型分布是逐次结果，样本越多越有意义；现有样板 3 次里出现了两个不同模型。这也是目前唯一做到 per-attempt 原生积分归因的产品，值得复现。
- **参照**：[WorkBuddy 适配器](adapters/workbuddy-desktop.zh-CN.md)、[现有样板](../runs/2026-08-15/workbuddy-5.3.13_auto_craft_hi-en-v1_as-used_mac-arm64/README.md)。

---

## B. 补全对比：已有产品的单变量扩展（难度 ★★）

每条任务只改变现有场景的一个变量，其余全部保持不变，是最容易产生"干净差值"的观察。

### T-11 去混杂补测：同一 permission mode 下的 Fable 5 vs Opus 5（2 场景）

- **场景**：Claude Code × `high` × 同一 permission/footer mode 下分别测 `claude-fable-5` 和 `claude-opus-5`。
- **你需要**：Claude 订阅（Max 最好，可直接对照现有样板）。
- **为什么优先**：**这是当前数据集中最明确的待修复点。** 现有 Fable/Opus 对比被 footer mode 混杂（`bypass permissions on` vs `manual mode on`），342 tokens 的总输入差异目前不能归因于模型。把 mode 固定后重测两个模型，就能把这个混杂拆掉。
- **注意**：两个场景、两个 PR；manifest 里填写 comparison/confounder 字段。

### T-10 Claude Code × Sonnet 5 × high

- **场景**：Claude Code（当前版本）× `claude-sonnet-5` × `high` × fresh session。
- **你需要**：Claude 订阅。
- **为什么优先**：补上 Sonnet 之后，同一 harness 下三个模型档位的 footprint 就能放在一起看：模型选择是否改变 system prompt 和工具定义的注入量。注意保持 permission mode 与你对照的样板一致。

### T-12 effort 阶梯：Claude Code × Fable 5 × medium（或 low）

- **场景**：与现有 Fable 样板完全相同，只把 effort 从 `high` 换成 `medium` 或 `low`。
- **为什么优先**：effort 是产品明确暴露的档位，但它到底影响输入注入、输出长度还是仅影响推理，目前没有数据。

### T-13 effort 阶梯：Codex CLI × gpt-5.6-sol × medium

- **场景**：与现有 Codex 样板完全相同，只把 effort 换成 `medium`。
- **为什么优先**：同 T-12，Codex 侧。

### T-14 订阅档位对照：Claude Pro

- **场景**：与任一现有 Claude Code 样板同型，订阅从 Max 换成 Pro。
- **为什么优先**：预期 token footprint 与订阅档位无关——但"预期"需要证据。如果有差异，那是重要发现。

### T-15 订阅档位对照：ChatGPT Plus 或普通 Pro

- **场景**：与现有 Codex 样板同型，订阅从 Pro 20x 换成 Plus 或普通 Pro。
- **为什么优先**：同 T-14，Codex 侧。

### T-16 Windows 平台复测（任选一个现有场景）

- **场景**：任一现有场景，操作系统换成 Windows。
- **为什么优先**：全部现有数据都在 macOS arm64 上；harness 在不同平台注入的环境信息可能不同。预检命令用 Windows 等价物，其余流程不变。

### T-17 WorkBuddy 固定单一模型 vs Auto

- **场景**：WorkBuddy × 显式固定一个具体模型（如 GLM-5.2）× 其余与 Auto 样板相同。
- **为什么优先**：把"Auto 路由"和"模型本身"两个变量拆开；与 T-03 的 Auto 数据对照可以观察路由本身是否引入额外开销。

---

## C. 新产品：把更多 Agent harness 纳入观察（难度 ★★★）

新产品任务的价值最高，难度也最高：没有现成适配器，需要自己回答"这个产品把 usage 暴露在哪里、怎么脱敏"。先按[贡献指南](../CONTRIBUTING.md)的通用语义采集，把与三个现有适配器的差异写进 PR；欢迎顺手起草一份 `docs/adapters/<product>.zh-CN.md` 初稿。

各产品计量单位五花八门（token、积分、premium requests、额度百分比）——**保留原生单位，不要换算**。

### T-20 Gemini CLI

- **你需要**：Google 账号或 Gemini 订阅；确认产品暴露的 usage 字段。
- **为什么优先**：主流厂商中唯一完全缺席的一家；其免费/订阅额度模型与 token 暴露方式都值得首个样本。

### T-21 Cursor

- **你需要**：Cursor 订阅。
- **为什么优先**：典型的"积分/请求数"计费产品，IDE 载体，与 CLI 类产品的 harness 结构差异大。

### T-22 GitHub Copilot（CLI 或 IDE Chat）

- **你需要**：Copilot 订阅（个人或教育版均可，如实记录）。
- **为什么优先**：premium requests 是又一种原生计量单位；教育版账号也很普及，取材方便。

### T-23 自选：你日常在用的其他 Agent

- **场景**：Cline、Qwen Code、iFlow、Trae 或其他你真实使用的 Agent 产品。
- **为什么优先**：真实用户的 as-used 配置最有现实意义。先开 issue 描述组合，确认按[场景身份规则](../CONTRIBUTING.md#什么算同一个场景)是一个新场景即可开工。

---

## D. Harness 变量专题：直接给 harness 的组成部分"称重"（难度 ★★）

如果你的研究方向是 Agent harness 本身，这一组任务和研究最直接相关：同一产品、同一模型下做一组开/关对照，**差值直接对应 harness 某个具体组件的边际 token 成本**。背景见[实测指南·为什么值得做](contributor-walkthrough.zh-CN.md#二为什么值得做)。

### T-31 MCP 开 / 关对照（2 场景）

- **场景**：同一产品、同一模型和 effort，分别在"配置了某个 MCP server"和"移除该 MCP"两种状态下各做 3 次。选工具数量多的 MCP server 效果更明显。
- **为什么优先**：MCP 工具定义即使从未被调用，也会进入上下文影响 input tokens——这是"工具定义成本"的直接测量，harness 研究里最常被引用的问题之一。

### T-32 规则文件有 / 无对照（2 场景）

- **场景**：空目录 vs 只含一份内容固定、公开可复现的 `AGENTS.md`（或 `CLAUDE.md`）的目录，其余不变。规则文件 fixture 随 PR 公开，harness profile 用 `custom`。
- **为什么优先**：测量规则文件注入的边际成本，以及产品是否原文注入、截断或改写。

### T-30 standard-clean vs as-used 同机对照（2 场景）

- **场景**：同一台机器、同一产品和模型：先在你的真实配置（`as-used`）下做 3 次；再构造一个可核实的干净环境（如新建系统用户，确认无全局规则、MCP、插件）做 3 次 `standard-clean`。
- **为什么优先**：差值近似等于"你个人 harness 配置的全部固定开销"。
- **注意**：`standard-clean` 的门槛较高——[贡献指南](../CONTRIBUTING.md#三种-harness-profile)要求确实核实过才能用这个标签。无法完全确认就诚实用 `as-used`，或改做 T-31/T-32 这类单开关对照。

### T-33 fresh vs resumed 会话（2 场景）

- **场景**：同一产品和模型：一组正常 fresh；另一组先建立一个只含一次 `hi` 往返的会话、退出后 resume 再发 `hi`。
- **为什么优先**：观察会话恢复时历史注入和缓存读取的行为，目前完全没有数据。

### T-34 干净的额度归因（任选载体）

- **场景**：任选一个现有场景重做，测试期间暂停同账号、同额度池的一切其他用量，记录每次 attempt 前后的额度/百分比显示。
- **为什么优先**：现有 Codex 样板的额度归因是 `contaminated`，Claude 样板是 `not_measured`。对订阅百分比额度做出首个干净的 per-attempt 归因，就能开始回答项目最初的问题："一句 hi 到底吃掉多少额度"。WorkBuddy 样板的积分归因可作方法参照。

---

## E. 新输入 case（先开 issue 与维护者对齐）

### T-40 hi-zh-v1：中文「你好」

- **场景**：任一已有 harness × 新输入 case「你好」。
- **注意**：新输入属于协议层变更——要先定义精确原文、编码、字节序列和 SHA-256，新建 `prompts/` 文件并确定 case ID。**先开 issue 讨论定稿，再开始测**；不要直接按自己的理解发一句中文就提交。
- **为什么优先**：输入语言是否影响 harness 注入（如语言检测、回复长度），是中英双语用户直接关心的问题。

---

## 想做清单之外的场景？

欢迎。开一个 issue 描述你的组合（产品 × 版本 × 模型 × effort × 订阅 × 路由 × 会话状态 × harness），对照[场景身份规则](../CONTRIBUTING.md#什么算同一个场景)确认它是一个新场景即可。清单会随认领和完成情况持续更新。
