# 选题卡：Codex Goal：长期任务要先写完成条件

## 核心洞察（一句话）

Codex 的 Goal 功能真正改变的是任务表达方式：长期任务的完成条件、验证方式和停止时机，从聊天里的临时约定变成线程级状态。

## 目标读者

已经在用 Codex CLI / Codex app 做代码修改、审查、迁移或前端实现的工程师。他们知道怎么 prompt Codex，但对新出现的 `/goal` 不确定：什么任务值得开 Goal，怎么写才不会失控，它和 Claude Code 的 `/loop`、Ralph Loop、`/goal` 是什么关系。

## 核心论点（3-5条）

1. Goal 适合“比一轮 prompt 大、但有明确验收条件”的任务，不适合开放式 backlog 或一堆无关小事。
2. 好 Goal 的关键在于写清楚完成条件、验证命令、边界和停止条件，少描述愿望。
3. Goal 与 Ralph Loop 相似之处是都让 agent 跨 turn 继续工作；差异是 Ralph Loop 主要靠 Stop hook 反复投喂同一 prompt，Codex Goal 是产品内置的线程状态和进度控制。
4. Goal 的效果取决于验证闭环：能跑测试、能看 diff、能截图验收的任务收益明显；只能靠主观判断的任务会更容易跑偏。
5. 对普通用户来说，最好的使用姿势是先 `/plan` 收敛任务，再 `/goal` 执行，避免一上来把大愿望丢给 Codex。

## 推荐结构

1. 从用户困惑切入：Goal 到底是不是“让 Codex 自己一直干”？
2. 解释 Goal 的产品语义：持久目标、线程状态、暂停/恢复/清除。
3. 给出“什么算好 Goal”的判断框架。
4. 对比 Codex Goal、Claude Code `/goal`、`/loop`、Ralph Loop。
5. 给出几个可直接改用的 Goal 模板。
6. 结尾落点：Goal 不替代工程判断，它要求你提前写清验收标准。

## 潜在问题

- 读者可能期待一篇“命令手册”，但这篇应该写成使用判断，不重复既有 Codex 速查手册。
- “效果如何”很容易写成主观吹捧，需要落到任务类型和验证条件，不能泛泛说提升效率。
- Claude Code 现在也有 `/goal`，不能只拿 Ralph Loop 对比，否则会误导。
- 不能声称 Codex Goal 的底层实现细节超出官方文档；缺少来源的地方要写成观察或推断。

## 事实与素材风险

- Codex Goal 已在 Codex app / IDE extension / CLI 可用，并在 2026-05-21 相关版本中不再实验，需要引用 OpenAI changelog。
- Codex `/goal` 的命令语义、4000 字符限制、pause/resume/clear 需要引用官方 CLI / app commands 文档。
- Codex “能工作数小时或数天”的说法可引用官方 use case，但文章表达要克制，不能推导成一定可靠。
- Ralph Loop 的 Stop hook、completion promise、max iterations 需要引用 Anthropic 插件页和 GitHub README。
- Claude Code `/goal` 也存在，并有独立 evaluator；需要引用 Claude Code docs，避免把 Codex Goal 错写成独有能力。

## 渠道建议

- 技术深度版（博客/内部知识库）：适合。读者需要的是判断框架和对比，不只是命令列表。
- 轻量化版（公众号）：适合改造成“Codex Goal 怎么写才不失控”，减少版本细节，保留模板和对比表。

## 选题结论

PASS_WITH_REVISION：选题成立，但不能写成“Codex 新范式”或“内置 Ralph Loop”的标题党。更稳的角度是“Goal 让完成条件变成状态”，把文章写给已经用 Codex 的工程师。
