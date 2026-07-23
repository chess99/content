# 选题卡：Context rot 不是一种病

## 核心洞察（一句话）

Agent 越改越烂不一定是上下文太长；更常见的失败是早期错误假设污染了上下文，压缩只能治“太长”，清空重开才是在治“太脏”。

## 目标读者

经常使用 Codex、Claude Code、Cursor、Devin、Manus 等 coding agent 的工程师和技术管理者。读者已经遇到过“同一个会话越修越乱，新会话反而一次修好”的体验，但缺少一个可操作的诊断框架。

## 核心论点（3-5条）

1. “Context rot”这个名字容易误导：它至少混合了 `distraction` 和 `poisoning` 两种机制。
2. `distraction` 是长度问题：上下文太长、注意力被稀释、信号被淹没；压缩、摘要、folding、skills 等工程手段主要治这个。
3. `poisoning` 是真相问题：错误假设进入上下文后被反复引用，后续推理建立在错误前提上；越修越乱通常更像这个。
4. `compact/summary` 对 poisoning 可能保留甚至强化错误信息，因为错误假设往往会被摘要器识别成“重要上下文”。
5. 当前实用策略不是继续勾兑，而是隔离和重置：清空重开、开干净 sub-agent、只把结果带回主线，把过程丢掉。

## 推荐结构

1. 从“越改越烂，新会话一次修好”的具体经历开场。
2. 解释 context rot 这个词的问题：它把两种病混成一种。
3. 分别讲 `distraction` 和 `poisoning` 的机制、症状、证据。
4. 用 coding agent 修 bug 的过程拆解 poisoning 如何形成。
5. 讨论为什么 `/compact`、summary、memory 治不了所有问题。
6. 给一个实践诊断表：这个 context 是太长了，还是太脏了？

## 潜在问题

- 不能把视频里的所有论文名和数字直接当作事实；需要逐条核查。
- “poisoning 目前基本无解”应降级表达为“常规 prompt 自纠错不可靠，工程上最稳的是重置/隔离”。
- “所有大厂都在用同一招”容易过度拔高，建议写成“多个主流产品都在引入上下文隔离/并行 agent 的机制”。
- 多 agent 不是银弹，Anthropic 和 Cognition 的观点本身相互冲突，文章需要保留这个张力。

## 事实与素材风险

- 已核查：Chroma context rot 报告、Anthropic context management 数据、Gemini 2.5 报告中的 context poisoning、Contextual Drag、Latent Phase-Shift Rollback、Anthropic multi-agent 90.2%、Cognition Don't Build Multi-Agents。
- 部分核查：LoCoBench-Agent 存在且来自 Salesforce，但视频里的“12 轮后陷入循环”需要回到论文确认。
- 待核查：Consensus Inertia 作为具体论文/术语的来源；Cursor 并行 sub-agent、Manus planner/executor、OpenAI Codex `/agent` 切换这几个产品表述需要查官方文档。

## 渠道建议

- 技术深度版（博客/内部知识库）：适合。可以展开论文、产品机制和工程诊断框架。
- 轻量化版（公众号）：适合，但需要弱化论文堆叠，把重点放在“太长 vs 太脏”的判断表和实际操作建议。

## 选题结论

PASS_WITH_REVISION。选题有明确读者痛点和反直觉洞察，但初稿必须把视频口播材料和已核查来源区分开，避免把二手视频中的论文名、数字和产品能力直接写成确定事实。
