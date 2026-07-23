你大概见过这个场景：agent 修一个 bug，前两轮还像在接近答案，后面越改越偏；你忍不住开一个新对话，把问题重新说一遍，它反而一次改对。

很多人把这类现象叫 `context rot`，上下文腐烂。这个词很好记，但它把两种机制很不一样的问题塞进了一个桶里：一种是上下文太长，模型开始走神；另一种是上下文不一定长，但里面已经混进了错误前提。


我会先把它们拆开。下面的 `distraction` 是本文为了方便诊断使用的操作性标签，不等同于 Chroma 报告里的 `distractor` 术语。

- `distraction`：长度问题。context 太长，信号被稀释。
- `poisoning`：真相问题。context 里有毒，错误假设被反复引用。

它们不是互斥分类器，更像两个优先级不同的排查方向。太长时，先压缩和摘要；太脏时，先清理和隔离。

## 太长：模型不是到上限才开始变笨

Chroma 的 Context Rot 报告 做过一组直观测试：给模型一段长文档，让它从里面找某句话，然后不断加长输入，看表现怎么变。它们测了 18 个主流模型，结论不太舒服：输入越长，模型越容易退化，而且退化通常发生在理论窗口上限之前。

这个问题很好理解。你把越来越多的信息塞进同一个 context，真正有用的信号会被淹没。模型仍然“看得到”那些 token，但注意力预算不是无限的。Anthropic 在 context management 里也用了类似思路：长任务需要 context editing、memory、progressive disclosure 这类机制，把注意力留给当前真正相关的信息。

这类问题的症状是：context 明显变长，模型开始漏掉约束，回答变得泛，工具调用和文件读取开始重复，但没有明显执着于某个错误方向。

这时候 `/compact`、summary、context folding、把局部任务交给新的 sub-agent，都可能有用。Anthropic 在同一篇文章里给过一组数据：context editing 加 memory 在一个 100 轮 web search evaluation 里把 token 消耗降了 84%，在 agentic search eval 上比 baseline 提升 39%。这只能说明，在 Anthropic 的长轮次搜索评测里，context editing 和 memory 有明显收益；放到 coding agent 修 bug 场景，还需要单独验证。

问题是，我们平时说“agent 越改越烂”，很多时候 context 并没有长到这种程度。一个修 bug 会话，可能才一两万 token。离长上下文严重稀释还远，但 agent 已经开始在同一个错误方向里打转。

## 太脏：错误前提进了 context

另一种病更像 `context poisoning`。

Google DeepMind 在 Gemini 2.5 技术报告 的 Gemini Plays Pokémon 讨论中使用了 `context poisoning` 这个说法。报告 Appendix 8.2 的 Additional Challenges 里提到，目标、summary 等 context 片段可能被游戏状态的错误信息污染，模型会执着于不可能或无关的目标，而且这种污染可能需要很长时间才能解开。

放到 coding agent 里，它大概长这样：

1. agent 第一次给了一个错误修复方案；
2. 这个方案、推理过程、工具输出都进入了 context；
3. 你说“不对，再改”；
4. agent 未必理解成“整个方向错了”，它更可能理解成“细节不对，沿着这个方向继续修”；
5. 每改一轮，最初那个错误假设就被再引用一次。

一个最小化例子：agent 先判断 bug 来自缓存，于是改缓存逻辑；测试失败后，用户只说“不对”。下一轮它没有重新验证根因，继续解释“缓存修复还需要补兼容层”。再下一轮，新报错也被吸收到缓存假设里。到这一步，它并没有忘掉信息；它把错误假设当成了必须维护的上下文。

这就是两种病的区别：

| 维度 | distraction | poisoning |
| --- | --- | --- |
| 根因 | context 太长 | context 里有错误前提 |
| 典型症状 | 漏重点、走神、摘要化 | 执着于错误方向、越修越偏 |
| 常见触发 | 长任务、长文档、多轮工具输出 | 早期错误判断、含糊的“不对”、失败路径被保留 |
| 第一反应 | compact、summary、folding、memory | 清理事实、隔离失败路径、必要时重开 |

`poisoning` 不是“模型能力差”的同义词。模型可能很强，但只要它把错误前提当成约束，后面的推理就会越走越窄。

## `/compact` 治的是长度，不一定治污染

很多人遇到 agent 变乱，第一反应是 `/compact`。

这在 `distraction` 场景里合理。context 太长，那就压缩，把当前任务需要的信息留下来。Claude Code、Cursor、很多 agent 框架都在做类似事情。

但 `poisoning` 麻烦在这里：错误前提看起来也很“重要”。

如果摘要器只是判断“哪些信息对后续有用”，那个最初的缓存假设很可能会被保留下来。它贯穿了整段对话，出现频率高，又和后续 diff、报错、解释都有关。旧会话摘要里一旦写出“当前排查集中在缓存层”，这个未验证根因就被换了个更正式的格式带进下一轮。

Claude Code 文档里有一个失败模式叫 Autocompact is thrashing：自动压缩刚成功，某个文件读取或工具输出又把 context window 填满，系统会停止重试以避免浪费调用。官方说的是 context refill 和循环问题，不是在直接定义 poisoning。但它提醒我们一件事：自动压缩并不理解所有语义风险。它能缩短 context，不等于能识别哪些内容应该被丢弃。

论文层面也有旁证。Contextual Drag 研究了错误 context 对 LLM 推理的拖拽效应，论文摘要里提到，错误尝试进入 context 后会诱发结构相似的后续错误，在严重情况下 iterative self-refinement 会退化成 `self-deterioration`。Latent Phase-Shift Rollback 更激进：它不让模型用 prompt 自我纠错，而是在内部 KV-cache 层面回滚；论文摘要称，在它的实验设置里，这种方法比 prompted self-correction 高 24.2 个百分点。

这两篇论文不能直接推出“所有 coding agent 都应该清空重开”。它们只能作为机制旁证：错误已经写进上下文后，让模型靠同一个上下文把自己救出来，可靠性并不高。

## 先问：太长了，还是太脏了

我现在会先问一个问题：

> 这个 context 是太长了，还是太脏了？

这不是严格分类器，只是一个使用 agent 时的启发式判断。

如果是太长，症状通常是“漏”。它忘了你前面说过的约束，找不到关键文件，回答开始变泛。这个时候可以压缩、摘要、拆子任务、让 agent 重新读取最相关文件。

如果是太脏，症状通常是“执着”。它记住了太多错误路径，并且一直试图解释那些错误路径为什么还能成立。你会看到它反复围绕同一个错误假设修补，哪怕测试和报错已经暗示方向不对。

| 现场信号 | 更像哪种 | 处理方式 | 不要带什么 |
| --- | --- | --- | --- |
| 会话很长，模型开始漏掉约束 | 太长 | compact、summary、重新列约束 | 无关工具日志 |
| 会话不长，但 agent 一直沿着错误方向改 | 太脏 | 停止迭代，重述问题，开新上下文 | 未验证根因 |
| 工具输出很多，但没有明确错误前提 | 太长 | 把工具结果整理成最小事实集 | 完整过程噪音 |
| 失败修复已经被反复解释和维护 | 太脏 | 丢掉失败路径，只带测试、现象、约束 | 失败 diff 和它的解释 |
| 需要探索多个方向 | 两者都可能 | 用 sub-agent 隔离探索过程，只回传结论 | 子任务的绕路过程 |

清空重开不是把所有东西都丢掉。比较好的做法是只带三类材料进新会话：当前真实现象、明确约束、已验证事实。最危险的是把旧会话完整总结成“背景”，那很可能只是把毒换了个格式带过去。

## Sub-agent 的价值可能在隔离失败路径

很多人谈 multi-agent，会先谈并行、速度、覆盖面。这些当然重要。Anthropic 在 一篇工程文章 里说，它们的 multi-agent research system 在内部 research eval 中比单 agent Claude Opus 4 高 90.2%。同一篇文章也说得很克制：multi-agent 很吃 token，任务必须真的可并行；coding 任务往往不像 research 那样天然适合拆很多独立方向。

我更关心另一个角度：sub-agent 可以隔离污染。

你让一个 sub-agent 去查“是否缓存导致”，它可以读文件、跑命令、犯错、绕路。最后主线只接收一个短结论：缓存不是根因，证据是某个测试和某个日志。探索过程不必完整带回主线。

这和“新开对话一次改好”的体验很像。新会话并没有让模型突然变聪明，它只是没有继承旧会话里的错误假设。

当然，sub-agent 不是银弹。Cognition 有篇文章标题就很直接：Don't Build Multi-Agents。它反对的重点之一，是多 agent 系统会制造协调和 context passing 的新问题。这个提醒很有价值：如果你把主线里的错误假设原样塞给 sub-agent，它照样会被污染。

所以 sub-agent 的用法不是“多开几个 agent 就会更聪明”。更稳的用法是：给它一个窄问题，不给它旧会话里的失败推理，让它返回证据和结论，主线只吸收验证过的信息。

## 我会怎么改自己的 agent 使用习惯

遇到 agent 越修越乱，我以前会继续催：“不对，再看看。”“还是不行，换个办法。”现在我会更早停下来。

如果只是 context 太长，我让它压缩当前事实，重新列任务边界。如果已经出现错误前提反复自我维护，我直接开新会话。如果不确定根因，我开一个干净 sub-agent 做独立排查，不把旧会话里的猜测带过去。

新会话的 prompt 不要写“刚才你试过 A、B、C 都失败了，所以现在继续”。这句话很容易把 A、B、C 的错误地基带过去。

更好的写法是：

```text
现象：运行 pnpm test auth 时，AuthProvider refresh token 用例失败。
约束：保持 public API 不变；先不要改 test。
已验证事实：请求已发出，服务端返回 401；本地 storage 中 refresh token 存在。
任务：重新定位根因。先列出 3 个可能原因和验证命令，再动代码。
```

如果要把旧会话压缩后继续，也可以明确要求：

```text
请只保留已验证事实、当前失败命令、不可改变的约束。
不要保留任何未验证的根因猜测、失败修复方案、或基于失败方案的后续解释。
```

这比单纯 `/compact` 更接近“排毒”。

我最后真正想带走的规则只有一条：下一轮 prompt 只带现象、约束、已验证事实；不带未验证根因、失败 diff、基于失败 diff 的解释。

`context rot` 这个词的问题，是它听起来像一种病。我现在更愿意把它拆成两个诊断问题：太长，还是太脏。

太长的时候，压缩和摘要是正经药。太脏的时候，继续勾兑通常只会让错误前提更难清理。重开一个干净上下文，只带事实和约束，不带失败路径，反而是当前 agent 架构下更稳的工程选择。

## 参考资料

1. Context Rot 报告：https://www.trychroma.com/research/context-rot
2. context management：https://www.anthropic.com/news/context-management
3. Gemini 2.5 技术报告：https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf
4. Autocompact is thrashing：https://code.claude.com/docs/zh-TW/troubleshooting
5. Contextual Drag：https://arxiv.org/abs/2602.04288
6. Latent Phase-Shift Rollback：https://arxiv.org/abs/2604.18567
7. 一篇工程文章：https://www.anthropic.com/engineering/built-multi-agent-research-system
8. Don't Build Multi-Agents：https://cognition.ai/blog/dont-build-multi-agents
