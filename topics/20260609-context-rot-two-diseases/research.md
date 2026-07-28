# 素材清单：Context rot 不是一种病

## 资料来源与提取说明

- **原始视频**：`~/Downloads/上下文腐烂 (Context rot) 其实是两种病 大家都在抱怨 agent 越改越烂、开一个新对话就一次改对了 —— 这件事过去半年被反复说,叫 context rot。但我读了一堆论文之后发现,这个名字其实.mp4`
- **视频元数据**：10 分 24 秒，1920x1080，30fps，单音轨。
- **提取方法**：
  - 用 `D:\code\content-studio\tools\transcribe_video.py` 调用 `whisper.cpp` + `ggml-small` 模型重新做语音转写，结果见 `shared/transcript-whisper.md`、`shared/transcript-whisper.srt`、`shared/transcript-whisper.txt`、`shared/transcript-whisper.json`。
  - 全画面每 10 秒采样一次，用 macOS Vision OCR 识别幻灯片文字，结果见 `shared/frame-vision-ocr.md`。
  - 底部字幕每 2 秒采样一次，用 macOS Vision OCR 识别口播字幕，去重后 230 行，结果见 `shared/subtitle-vision-ocr.md`。
  - Whisper 语音稿能还原口播节奏，但专有名词有错词（如 Anthropic、Claude、Cursor、poisoning、context 等），写作时需要和字幕 OCR、画面 OCR 交叉核对。
- **使用限制**：不要直接复用视频截图。需要配图时建议重画概念图或生成原创示意图。

## 视频内容复原

### 时间线

- **00:00-00:24 Hook 与主旨**：Agent 越改越烂，开新对话反而一次改对。过去半年这种现象被叫做 `context rot`，但视频认为这个名字是陷阱，因为它混合了两种不同机制。
- **00:30-01:08 Chroma 起源**：Chroma 测了 18 个主流模型，让模型在越来越长的文档里找某句话。视频结论是所有模型都会随输入变长退化，而且不是到窗口上限才崩，可能在 100 万 token 窗口里 5 万 token 已明显下滑。
- **01:10-01:48 Distraction**：Anthropic 用 `attention budget` 解释长上下文退化。视频把这种病称为 `distraction`：context 太长，注意力被稀释。但修 bug 会话往往只有 1-2 万 token，还没到严重稀释程度。
- **01:52-02:16 Poisoning**：视频引入第二种病 `context poisoning`，即上下文中毒。其定义来自 DeepMind Gemini 玩宝可梦的报告：上下文某些部分被错误信息毒化，而且很久才能解开，模型会执着于不可能或无意义的目标。
- **02:18-02:32 两种机制对比**：`distraction` 是 context 太长、信号被淹没；`poisoning` 是 context 不长但里面有毒，早期错误判断进入 context 后被反复引用，后续推理建立在错误上。
- **02:34-03:16 修 bug 场景拆解**：Agent 第一次给出错误修复方案；用户说“不对”，agent 可能理解成“细节不对，继续推进”；每改一次，错误假设都没有被清理，反而被再次引用和加强。到第五次，已经在错误地基上盖了五层楼，推倒重来很难。
- **03:18-03:44 LoCoBench-Agent**：视频说 Salesforce 11 月发布 LoCoBench-Agent benchmark，agent 跑超过 12 轮后会重复读文件、重复调用失败工具、生成无用摘要并陷入循环。
- **03:46-04:40 Consensus Inertia**：视频说 3 月论文把现象称为 `Consensus Inertia`，即错误轨迹被中间产物固定后，纠正成本随流程推进急剧上升。错误猜测、失败修复、新报错会凝固成约束，模型试图同时满足互相矛盾的约束，因此在方案间震荡。
- **04:42-05:24 Compact 与 summary 的边界**：视频认为 `/compact`、summary、Cursor 自动摘要、ByteDance context folding、Anthropic progressive disclosure 都主要治疗 `distraction`。Anthropic 的 context editing + memory 在 100 轮评测中降低 token 消耗 84%，agentic search 性能提升 39%。
- **05:26-05:48 Autocompact 反作用**：视频引用 Claude Code 文档中的 `Autocompact is thrashing`，说明压缩成功后文件读取或工具输出又把 context 填满。视频进一步推断：如果最初错误假设被压缩算法视为重要信息，它会在压缩后保留下来。
- **05:52-06:10 Contextual Drag**：视频引用 2026 年 2 月论文 `Contextual Drag`，称被污染 context 下让模型自我纠错，性能不仅没有回升，反而继续下降，论文称为 `self-deterioration`。
- **06:12-06:30 Latent Phase-Shift Rollback**：视频引用 2026 年 4 月论文 `Latent Phase-Shift Rollback`，说它绕过 prompt 层，在模型内部回滚 KV-cache；手动回滚比模型 prompt 自纠错强 24 个百分点。
- **06:32-06:52 结论**：context 被毒化后，让 agent 自己走出来基本无效；最有效方法仍是清空重开。新对话不是让 agent 变聪明，而是旧对话里的毒不存在了。
- **06:54-07:34 干净对比表**：`distraction` 是长度的诅咒，所有模型都会得，有 compact/folding/summary/skills 等解法；`poisoning` 是毒性的诅咒，和人类反馈方式有关，目前最有效的是清空重开。
- **07:36-08:00 架构挑战**：`distraction` 对应注意力机制的数学局限，可以用工程方法绕过；`poisoning` 需要元认知，即 agent 意识到自己某个前提可能是错的，并主动否定之前判断。视频认为当前架构基本不具备这种能力。
- **08:04-08:32 与“决策权下沉”的张力**：在 `distraction` 上，agent skills、context folding、ACE 等让 agent 自己管 context；但在 `poisoning` 上，不能把决策权交给一个意识不到自己被毒化的 agent。
- **08:34-09:00 诊断问题**：下次遇到 agent 越改越乱，先问：这个 context 是太长了，还是太脏了？太长就压缩、摘要、开 sub-agent 处理细节；太脏就别再勾兑，清空重开。
- **09:02-10:20 下一篇伏笔**：新开的 sub-agent 本质上是局部清空重开。视频把 Anthropic multi-agent system、Cursor 并行 sub-agent、Manus planner/executor、Claude Code `/agents`、OpenAI Codex `/agent` 切换放在同一趋势下：任务切片，每片用干净 sub-agent 跑，只把结果带回主线。但 Anthropic 说 multi-agent 比单 agent 性能提升 90%，Cognition 则写了 `Don't Build Multi-Agents`，两家公司得出相反结论。

### 可直接转化为文章的小标题

- Context rot 这个词，掩盖了两种病
- 太长的问题，和太脏的问题
- 为什么“再改一下”会把 agent 推进错误轨道
- `/compact` 治的是长度，不是真相
- 清空重开不是认输，是隔离污染
- Sub-agent 的本质：局部重置上下文

## 论点一：Context rot 至少混合了 distraction 和 poisoning 两种机制

### 支撑素材

- **视频素材**：00:10-00:24 明确提出“这个名字其实是个陷阱”，把 `context rot` 拆成 `distraction` 和 `poisoning`。
- **一手资料**：Chroma 的 `Context Rot: How Increasing Input Tokens Impacts LLM Performance` 报告测试 18 个模型，关注输入长度增加导致的性能退化。来源：https://www.trychroma.com/research/context-rot
- **一手资料**：Anthropic `Managing context on the Claude Developer Platform` 讨论长任务中的 context limits、context editing 和 memory。来源：https://www.anthropic.com/news/context-management
- **一手资料**：Gemini 2.5 技术报告提到 Gemini Plays Pokémon 中的 `context poisoning`。来源：https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf

### 反证/限制条件

- `context rot` 在很多文章里主要指长上下文退化；把 poisoning 纳入同一大词是本文的解释框架，不一定是所有论文的标准分类。
- 视频中的 “100 万 token 窗口可能 5 万 token 明显下滑”需要回到 Chroma 图表逐项确认，不宜直接写成普遍阈值。

### 来源风险

- Chroma、Anthropic、Gemini 报告可作为主来源。
- 术语二分法是视频作者的综合判断，文章应写成“更准确地说，我们至少要分两类”，不要写成学界定论。

---

## 论点二：修 bug 越改越烂，更像 poisoning，而不是 distraction

### 支撑素材

- **视频案例**：02:34-03:16 的修 bug 场景非常适合做文章开场：第一次错误修复进入 context，用户的“不对”被理解为“细节不对”，错误假设每轮被引用和加固。
- **论文**：`Contextual Drag: How Errors in the Context Affect LLM Reasoning` 研究错误尝试进入 context 后如何拖拽后续推理。论文摘要称错误 context 会导致结构相似错误，11 个模型、8 类任务上有 10-20% 性能下降，并且严重时 iterative self-refinement 会变成 `self-deterioration`。来源：https://arxiv.org/abs/2602.04288
- **论文**：`Latent Phase-Shift Rollback` 的摘要称 prompted self-correction 低于标准自回归生成，而 KV-cache rollback + steering 比 prompted self-correction 强 24.2 个百分点。来源：https://arxiv.org/abs/2604.18567
- **Gemini 报告**：context poisoning 的 Pokémon 案例说明错误目标写入 context 后，模型会追逐不可能目标。

### 反证/限制条件

- 真实 coding agent 越改越烂可能同时包含 distraction、tool failure、测试反馈缺失、用户反馈不清等因素，不能单因果归结为 poisoning。
- LPSR 是推理时内部状态干预，不等于产品层面的清空重开；它只能作为“prompt 自纠错不可靠”的旁证。

### 来源风险

- Contextual Drag 和 LPSR 已找到论文来源。
- 视频中的“Consensus Inertia”作为具体论文名或术语来源未找到可靠一手来源，需要继续核查。

---

## 论点三：Compact、summary、memory 主要治 distraction，不等于能治 poisoning

### 支撑素材

- **Anthropic 官方数据**：context editing + memory 在内部 agentic search eval 上比 baseline 提升 39%；100-turn web search evaluation 中 token consumption 降低 84%。来源：https://www.anthropic.com/news/context-management
- **Claude Code 官方文档**：`Autocompact is thrashing` 表示自动压缩成功后，某个文件或工具输出立即多次重新填满 context window，Claude Code 会停止重试以避免浪费 API 调用。来源：https://code.claude.com/docs/zh-TW/troubleshooting
- **视频推论**：如果错误假设被认为是“重要上下文”，摘要可能保留它，从而不能排毒。

### 反证/限制条件

- Anthropic 的 context editing/memory 数据不能反证 poisoning，它证明的是长任务 context 管理有效。
- `Autocompact is thrashing` 官方定义是 context refill/loop，不直接等于“毒性信息被保留”。视频把它用于 poisoning 需要写成推论。
- 好的人工 `/compact` 指令可能要求“只保留计划和 diff、丢掉失败路径”，因此不能笼统说 compact 一定有害。

### 来源风险

- Anthropic 数据和 Claude Code thrashing 文档可靠。
- “summary 会保留 poison”目前缺少直接实验来源，建议作为工程经验/推断表达。

---

## 论点四：清空重开和 sub-agent 的共同点，是隔离污染而不是提升智力

### 支撑素材

- **视频素材**：06:40-06:52：“不是新对话里 agent 变聪明了，是旧对话里的毒不存在了。”
- **Anthropic 多 agent 文章**：Anthropic 的 Research 功能使用 lead agent + subagents，称多 agent research system 在内部 research eval 中比单 agent Claude Opus 4 高 90.2%；文章也强调 subagents 有自己的 context windows，适合并行探索不同方向。来源：https://www.anthropic.com/engineering/built-multi-agent-research-system
- **Anthropic 限制条件**：同一篇文章明确说 multi-agent 会消耗大量 token，multi-agent systems 用量约为 chat 的 15 倍；并且 coding tasks 往往少于 research 的真正可并行任务。
- **OpenAI Codex 资料**：OpenAI Codex 页面称 Codex app 设计支持 multi-agent workflows，agents 可以在 worktrees/cloud environments 中并行工作。来源：https://openai.com/codex/
- **Cognition 反方**：Cognition 的 `Don't Build Multi-Agents` 反对过度构建 multi-agent 系统，强调 context passing 和协调问题。来源：https://cognition.ai/blog/dont-build-multi-agents

### 反证/限制条件

- Sub-agent 不天然解决 poisoning。如果主 agent 把错误前提作为任务说明传给 sub-agent，污染仍会传播。
- 多 agent 适合任务可分解、信息可并行探索、结果可压缩回传的场景；强依赖、共享状态多的 coding 任务可能不适合。

### 来源风险

- Anthropic 和 Cognition 来源可靠。
- 视频列出的 Cursor 并行 sub-agent、Manus planner/executor、Claude Code `/agents`、OpenAI Codex `/agent` 切换需要进一步查官方文档；目前只能作为“视频声称/待核查”。

---

## 论点五：实用诊断框架是“太长”还是“太脏”

### 支撑素材

- **视频诊断问题**：08:34-09:00，“这个 context 是太长了，还是太脏了？”
- **太长的症状**：输入越来越长后模型开始遗漏重点、重复、摘要化、注意力被稀释。适合 compact、summary、context editing、memory、folding、skills、开 sub-agent 处理局部细节。
- **太脏的症状**：会话不长但越修越偏；agent 一直执着于早期错误假设；用户反复说“不对”后模型只改细节不换方向；错误修复、新报错、失败工具调用互相冲突。适合清空重开、明确重述事实、隔离失败路径、只带干净问题和必要证据进入新会话。

### 反证/限制条件

- 有些场景同时太长又太脏，建议先清理事实边界，再压缩。
- “清空重开”会丢失有价值的调查过程，需要保留可验证结果、测试输出、约束和最终 diff，而不是把失败轨迹原样带过去。

### 来源风险

- 这是本文的工程化框架，来源主要是视频综合、论文旁证和使用经验；应避免写成严格学术分类。

---

## 事实核查表

| 视频说法 | 核查状态 | 可用来源 | 写作建议 |
| --- | --- | --- | --- |
| Chroma 测 18 个模型，长 context 下都会退化 | 已核查 | https://www.trychroma.com/research/context-rot | 可写，但具体阈值需回图表确认 |
| Anthropic attention budget / context management 支持长任务 context 管理 | 已核查 | https://www.anthropic.com/news/context-management | 可写成官方 context management 数据 |
| context editing + memory 降 token 84%、agentic search +39% | 已核查 | https://www.anthropic.com/news/context-management | 可直接引用 |
| Gemini Plays Pokémon 中出现 context poisoning | 已核查 | https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf | 可写，引用时回 PDF 找原文页码 |
| LoCoBench-Agent 存在，来自 Salesforce | 已核查 | https://www.salesforce.com/blog/locobench-agent/；https://arxiv.org/abs/2511.13998 | 视频“12轮后陷入循环”需查论文细节 |
| Consensus Inertia 是 2026-03 论文/术语 | 待核查 | 暂未找到一手来源 | 初稿不要作为核心证据 |
| Contextual Drag 导致错误 context 拖拽后续推理，自纠错可能恶化 | 已核查 | https://arxiv.org/abs/2602.04288 | 可作为 poisoning 的强支撑 |
| LPSR 通过 KV-cache rollback 比 prompt 自纠错强 24pp | 已核查 | https://arxiv.org/abs/2604.18567 | 可作为“prompt 自纠错不可靠”的旁证 |
| Claude Code 有 Autocompact thrashing 失败模式 | 已核查 | https://code.claude.com/docs/zh-TW/troubleshooting | 可写，但不要过度外推 |
| Anthropic multi-agent 比 single agent 高 90.2% | 已核查 | https://www.anthropic.com/engineering/built-multi-agent-research-system | 必须同时写成本和适用边界 |
| Cognition 写 Don't Build Multi-Agents | 已核查 | https://cognition.ai/blog/dont-build-multi-agents | 作为反方材料 |
| OpenAI Codex 支持 multi-agent workflows | 已核查 | https://openai.com/codex/ | 可写“Codex app 支持 multi-agent workflows”，`/agent` 切换待核查 |

## 可生成的原创图片建议

- **诊断流程图**：标题“这个 context 是太长了，还是太脏了？”左路是压缩/摘要/skills，右路是清空重开/sub-agent 隔离。
- **两种病对比图**：`distraction = length problem`，`poisoning = truth problem`，用两列对比症状、原因、解法。
- **错误假设加固阶梯**：第 1 次错误修复进入 context，第 2-5 次被反复引用，最后形成“错误地基上的五层楼”。
- **Sub-agent 隔离示意图**：主线只接收结果，不接收完整失败轨迹，强调“过程丢弃、结论回传”。

## 备用标题

- Context rot 不是一种病
- Agent 越改越烂时，先问：太长了，还是太脏了？
- 为什么新开一个对话，Agent 突然又会了？
- `/compact` 治不了被污染的上下文
- 清空重开不是认输，是当前架构下的排毒
