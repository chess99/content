# Superpowers 流程税：研究记录

## 1. 触发案例

- 用户让 Codex 制作小红书内容时，Codex 自动触发 Superpowers，并把写作任务带入计划、拆任务和 TDD 流程。
- 这只能证明流程和任务发生过明显错配，不能单独证明 Superpowers 对代码任务无效。
- 原吐槽帖：[一篇小红书文案，Codex 给我做起了 TDD](https://www.xiaohongshu.com/explore/6a5e2ac00000000011005d02?xsec_token=ABMwGJ8oNplCPGrB2lortq4CUSEIU8iciVC0Zh_2TAZdk=&xsec_source=pc_user)

## 2. 用户反馈中的隔离 A/B

证据截图：`shared/evidence/superpowers-ab-test.png`

反馈者自述使用 `gpt-5.6-sol`、`xhigh` 和官方 Superpowers v6.1.1：

- 三项任务隐藏评测：基线 3/3，Superpowers 3/3，没有测出正确率差异。
- 两项完整计量任务合计：Superpowers 耗时为基线的 3.61 倍，input token 为 8.98 倍，output token 为 2.74 倍。
- 并发 bug 修复：基线 139.08 秒、133,390 input tokens；Superpowers 551.81 秒、1,570,275 input tokens。
- 原子账本功能：基线 101.83 秒、120,156 input tokens；Superpowers 316.70 秒、707,782 input tokens。
- 仅暴露 14 个技能、尚未加载正文时，初始输入已增加 10.1%。

### 证据边界

- 这是单个用户提供的小样本，不是独立复现或大规模 benchmark。
- 隐藏评测的任务、评分细节和完整运行日志尚未公开入库。
- 结果支持“这组任务中成本显著上升、正确率未测出提升”，不能外推为“Superpowers 对所有任务都无效”。

## 3. Superpowers 的强制调用规则

官方 `using-superpowers` skill 写明：只要认为某个 skill 有哪怕 1% 的适用概率，就“绝对必须”调用；相关 skill 需要在任何回复或行动之前调用。

来源：

- [Superpowers 仓库](https://github.com/obra/superpowers)
- [`using-superpowers/SKILL.md`](https://github.com/obra/superpowers/blob/main/skills/using-superpowers/SKILL.md)

这个规则能降低漏用流程的概率，也会扩大误触发成本。文案任务进入 TDD，正是后一种风险的直观案例。

## 4. “快 50%、便宜 60%”的口径

轮播图和文案采用的证据边界是：该数字比较 Superpowers v6 与旧版，而不是 Superpowers 与裸模型。原始发布链接尚未入库，补齐前不把它当作独立验证过的效果数据。

## 5. 当前可支持的判断

现有材料更适合支持一个克制的结论：

> Superpowers 并非简单地“失效”，而是它的强制流程在通用智能体和非代码任务中可能产生明显的流程税。是否值得，取决于任务风险、模型基础能力和流程成本之间的比例。

仍需补充：

- 更多独立用户在同模型、同任务、同推理档位下的复现。
- 对代码任务和非代码任务分别统计，避免混在一起。
- gstack 的同类公开实测与版本变化。
- Superpowers v6 性能声明的原始链接和测试口径。
