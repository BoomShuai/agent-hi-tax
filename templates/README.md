# Templates

模板用于减少漏项，不是要求所有 Agent 伪装成同一种 schema。

## 选择顺序

1. 先复制 `scenario-manifest.yaml` 和 `attempt-result.yaml`。
2. 再打开与被测产品最接近的完整样板，复制它的 `RESULTS.csv` 列和 provider-native usage 字段。
3. 产品没有暴露的字段写 `not_exposed`；不适用于该厂商的字段写 `not_applicable`；不要填 `0` 代替缺失值。
4. `aggregate` 只汇总 `RESULTS.csv` 中确实存在、定义清楚的字段。
5. 不做跨场景比较时删除 `comparison` 模板块；存在权限模式、插件、账号或其他未控制变量时，保留该块并标记混杂。

## 当前参考样板

- [Codex CLI：OpenAI/Codex cached input 是 input 的子集](../runs/2026-08-14/codex-cli-0.147.0_gpt-5.6-sol_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [Claude Code Fable：Anthropic 三个 input bucket 相加](../runs/2026-08-15/claude-code-2.1.220_claude-fable-5_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [Claude Code Opus：记录跨样板 mode 混杂](../runs/2026-08-15/claude-code-2.1.220_claude-opus-5_high_hi-en-v1_as-used_mac-arm64/manifest.yaml)
- [WorkBuddy Auto：缓存为 input 子集，实际路由模型是逐次结果](../runs/2026-08-15/workbuddy-5.3.13_auto_craft_hi-en-v1_as-used_mac-arm64/manifest.yaml)

模板仍使用 `pilot-0.3`。新增的是可选记录字段和填写说明，没有改写既有样板的原始口径。
