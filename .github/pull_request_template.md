## 场景

- Scenario ID：
- 场景目录：`runs/YYYY-MM-DD/<scenario-id>/`
- Agent / 版本：
- Model / effort：
- 订阅或计费通道：
- Route / harness profile：

## Attempts

- 计划次数：
- 有效次数：
- 无效、错误或超时次数及原因：

## 证据

- 包级证据：Level A / B / C
- 视觉证据：public / private_evidence / not_provided
- 未暴露、未提供、自报或冲突字段：
- 原图是否始终留在 Git 仓库外：是 / 否

## 协议偏差与混杂变量

说明额外命令、权限或 footer mode 变化、MCP／plugin／hook 差异、共享额度污染，以及任何不能归因于模型的差异。没有则写“无”。

## 验证输出

粘贴下面命令的完整结果：

```text
./scripts/verify-run-package.sh runs/YYYY-MM-DD/<scenario-id>
python3 scripts/build-results-index.py
./scripts/verify-all.sh
```

## 提交前检查

- [ ] 本 PR 只包含一个场景及其全部 attempts。
- [ ] 至少有 3 次有效独立运行，且不是并行、resume 或挑选出来的最低值。
- [ ] Prompt、Agent 版本、模型、effort、路由、权限模式和 harness 在有效 attempts 中一致。
- [ ] 场景级环境证据只保留一份，每次 attempt 分别保留回复与 usage。
- [ ] 原生 usage 字段与派生公式均已注明，cached input 没有重复相加。
- [ ] 无效与异常 attempt 没有被静默删除。
- [ ] 公开文本和图片不含凭据、邮箱、账号 ID、Session ID、resume 命令、用户名、主机名、绝对 home 路径或私有内容。
- [ ] 视觉原图没有进入公开 Git 历史；脱敏图已逐张目视检查。
- [ ] `private_evidence` 只用于维护者已经实际核对过的原件。
- [ ] `SHA256SUMS` 在所有公开文件最终定稿后生成。
- [ ] 根级 `RESULTS.md` 已重新生成。
- [ ] `./scripts/verify-all.sh` 已通过。
