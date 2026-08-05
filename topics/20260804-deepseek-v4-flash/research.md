# DeepSeek V4 Flash｜事实与编辑底稿

- 日期：2026-08-04
- 状态：完成，可用于本主题
- 风险：模型版本、价格、排行榜和竞品会快速变化；必须标注日期，并区分官方规格、厂商自报跑分、独立评测和编辑判断

## 1. 这期要回答什么

DeepSeek V4 Flash 0731 的真实定位是什么：它是否已达到旗舰模型水平，强项是否集中在代码 Agent，超低价格有没有隐藏成本，哪些人值得把它设为默认模型？

本期不做“国产模型吊打谁”的情绪化结论，也不把单个榜单等同于所有真实任务。

## 2. 编辑结论

> DeepSeek V4 Flash 0731 已进入一线快模型与开放生态第一梯队，代码 Agent 和单位成本尤其突出；但它并非综合旗舰平替，事实可靠性、输出冗长、文本单模态和本地部署门槛仍是明确短板。

推荐把它作为低成本代码 Agent、批量任务和 API 后端的优先候选；不推荐在无搜索、无引用、无人复核的情况下独立承担投资、医学、法律、新闻等高风险事实任务。

## 3. 事实台账

| 事实 | 来源与检查时间 | 可支持的结论 | 不能支持的结论 |
|---|---|---|---|
| DeepSeek 官方定价页在 2026-08-04 显示 `deepseek-v4-flash` 当前模型版本为 `DeepSeek-V4-Flash-0731` | DeepSeek API Docs，2026-08-04 | 官方一方 API 已切换到 0731 版本 | 不能据此推断所有第三方供应商都已同步相同版本 |
| 官方 API 支持思考/非思考、1M 上下文、最大 384K 输出、JSON、工具调用、Responses API 与 Anthropic API | DeepSeek API Docs，2026-08-04 | 适合长上下文和 Agent 集成，接口兼容性较强 | 1M 窗口不等于能对 1M token 中每个细节无损召回与推理 |
| 官方价格为缓存命中输入 $0.0028/M、未命中输入 $0.14/M、输出 $0.28/M；峰谷双倍价格政策尚待正式生效公告 | DeepSeek API Docs，2026-08-04 | 单 token 价格极低，缓存重复上下文的任务尤其有优势 | 不能只按 token 单价断言所有真实任务都比竞品便宜；输出长度和缓存命中率会改变总成本 |
| V4 Flash 架构为 284B 总参数、每 token 激活约 13B，支持 1M 上下文；原始 V4 Flash 权重采用 MIT 许可 | DeepSeek V4 官方发布、Hugging Face 模型卡；2026-08-04 检查 | 13B 激活带来计算效率，但模型容量来自 284B MoE | 不能称它为普通“13B 小模型”，也不能据此预期单张消费级显卡可完整部署 |
| Artificial Analysis 对 0731 的 Max 推理版本给出 Intelligence Index 50，比 4 月版 40 高 10 分 | Artificial Analysis，2026-07-31 | 0731 在该综合测试框架中有显著进步 | 不能把 50 分解释为所有领域统一强 25%，也不能跨不同测试版本机械比较 |
| 同一评测中，0731 与 Gemini 3.6 Flash 同为 50，距 GLM-5.2 约 1 分，距 Kimi K3 约 7 分 | Artificial Analysis，2026-07-31 | 可把它定位在一线快模型附近、最强开放权重模型之下 | 不能写成“全面等于 Gemini”或“全面只差 Kimi 7 分”；这是特定综合指数和 Max 推理配置 |
| GDPval-AA v2 从 1189 提升至 1559；Terminal-Bench 2.1 提升 17 个百分点至 79%；τ³-Banking 提升至 31% | Artificial Analysis，2026-07-31 | Agentic real-world work、终端与工具任务是 0731 的主要提升方向 | 不能直接外推到任意 Claude Code、Codex、OpenCode 或自定义 Harness；提示词、工具协议和推理强度都会影响结果 |
| AA-Omniscience Index 为 -16，准确率约 37%，该测试中的 hallucination rate 为 84%，比旧版下降约 12 个百分点 | Artificial Analysis，2026-07-31 | 它在不知道答案时仍有较强的错误作答倾向，事实任务应配搜索与引用 | “84%”不等于日常回答有 84% 是错的；这是特定知识可靠性评测中对未知问题响应行为的指标 |
| 独立测试显示输出速度约 113.5 token/s；完成 Intelligence Index 使用约 210M 输出 token，高于约 100M 的中位数 | Artificial Analysis，2026-08-04 检查 | 官方 API 较快，但推理版本偏冗长，真实成本和耗时会被输出量部分抵消 | 不能把 113.5 token/s 当作所有地区、所有负载和所有第三方供应商的固定速度 |
| 0731 当前是文本输入、文本输出模型 | Artificial Analysis；DeepSeek 的 Copilot 集成文档明确视觉由其他模型代理，2026-08-04 | 图片理解和视觉工作流需要配其他模型 | 不能写成原生多模态旗舰 |
| 4 月版 V4 Flash 模型权重已在 Hugging Face 提供；Artificial Analysis 在 7 月 31 日文章中称 0731 的完整权重预计随后数周发布 | Hugging Face；Artificial Analysis，2026-07-31 | API 的 0731 和公开仓库中的旧版权重需要按版本区分 | 在未再次核实前，不应写“0731 精确权重已经完整开源并可下载” |

## 4. 架构与本地部署口径

### 13B 激活是什么意思

MoE 模型会为每个 token 选择部分专家参与计算，因此 V4 Flash 每次推理约激活 13B 参数；但完整模型仍有 284B 参数，所有专家权重仍需存储和调度。

适合公开表达：

> 计算量接近更小模型，但存储与部署并不会缩成普通 13B。

不采用：

- “一张 24GB 显卡就能跑。”
- “它就是一个 13B 模型。”
- “13B 做到了旗舰能力。”

Hugging Face 上原始 V4 Flash Base 仓库显示 FP8 权重约 295GB。量化可以降低内存需求，但普通个人电脑仍不属于舒适部署范围；具体需求还取决于量化格式、并行方案、KV Cache 和上下文长度。

## 5. 独立评测该怎么解释

Artificial Analysis 的 50 分来自 Reasoning、Max Effort 配置，其综合指数包含 Agent、终端、科学推理、知识可靠性和长上下文等多项测试。

可用表述：

- “独立综合指数进入一线快模型附近。”
- “Agent 和终端能力是最明显的提升。”
- “仍落后最强开放权重与顶级闭源模型。”

避免：

- “综合能力已经超过 V4 Pro。”虽然同一指数中 0731 高于 4 月测试的 V4 Pro，但版本时间、后训练和测试配置不同，不能据此宣布产品线永久倒挂。
- “接近某旗舰，所以日常效果完全一样。”综合分数接近不代表风格、知识、视觉、指令遵循和长链路稳定性相同。
- “Terminal-Bench 接近某模型，所以代码能力全面相等。”单项终端测试不覆盖所有软件工程任务。

## 6. 适用场景

### 优先推荐

1. 代码 Agent、终端操作、仓库阅读、批量改代码和生成测试；
2. 大量并行子 Agent，先用低成本模型完成大部分执行；
3. API 产品后端、结构化输出、工具调用和高并发任务；
4. 大文档、长仓库和长会话的整理与初步推理；
5. 需要低成本反复迭代的独立开发和内容生产工作流。

### 需要加验证层

1. 新闻、政策、价格、软件版本等实时信息；
2. 投资、医学、法律和安全相关结论；
3. 冷门事实、人物履历、引用和精确数字；
4. 超长上下文中的细节召回与跨段推理；
5. 无人值守、执行后果不可逆的 Agent 操作。

### 不适合作为唯一模型

1. 图片、视频和复杂视觉理解；
2. 普通消费级设备的完整本地部署；
3. 对事实正确率要求极高、又没有搜索和数据库支持的问答；
4. 需要最强长链路自主规划、且失败代价高的任务。

## 7. 推荐架构

更合理的产品用法不是只押 V4 Flash：

```text
V4 Flash 负责低成本执行
→ 搜索、测试和规则引擎做验证
→ 失败或高风险任务升级到更强模型
→ 人工确认不可逆操作
```

这比简单说“平替某旗舰”更接近它真正的价值。

## 8. 发布前逐项检查

- 标题不写“吊打”“封神”“全面超越”；
- 所有比较注明 Artificial Analysis、Max Effort 和日期；
- 84% 只写成特定评测中的 hallucination rate，并明确不是所有回答错误率；
- 价格注明官方 API、美元/百万 token 和截至日期；
- 13B 前必须出现“激活”，同时给出 284B 总参数；
- 说明 0731 API 与公开权重版本可能存在时间差；
- 说明文本单模态；
- 说明 1M 是上下文窗口规格，不是无损理解承诺。

## 9. 资料

### 官方

- DeepSeek API Models & Pricing：https://api-docs.deepseek.com/quick_start/pricing/
- DeepSeek V4 Preview Release：https://api-docs.deepseek.com/news/news260424/
- DeepSeek Thinking Mode：https://api-docs.deepseek.com/guides/thinking_mode
- DeepSeek V4 Flash 模型卡：https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
- DeepSeek V4 Flash Base 文件页：https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base/tree/main
- DeepSeek 接入 Claude Code：https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code
- DeepSeek 接入 GitHub Copilot：https://api-docs.deepseek.com/quick_start/agent_integrations/github_copilot

### 独立评测与报道

- Artificial Analysis 0731 分析：https://artificialanalysis.ai/articles/deepseek-v4-flash-0731-scores-50-on-the-artificial-analysis-intelligence-index-10-points-above-previous-deepseek-v4-flash
- Artificial Analysis 模型页：https://artificialanalysis.ai/models/deepseek-v4-flash
- Reuters 低成本报道：https://www.reuters.com/business/retail-consumer/deepseeks-new-ai-model-is-by-far-cheapest-well-known-models-run-research-firm-2026-08-03/
