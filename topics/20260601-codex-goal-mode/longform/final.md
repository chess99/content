---
title: Codex Goal：长期任务要先写完成条件
date: 2026-06-01 00:00:00
tags:
  - Codex
  - AI 工具
  - AI Coding
categories: 工具
permalink: /posts/codex-goal-mode/
---

Codex 的 Goal 从实验功能转成稳定功能后，我的第一反应卡在一个问题上：这玩意儿到底该怎么用？

如果只是把一个大 prompt 存起来，那我直接写在 `AGENTS.md` 或 `docs/plan.md` 里不就完了。它和 Claude Code 的 `/loop`、Ralph Loop 到底有什么区别？什么任务配得上开 Goal，什么任务只是我懒得拆？

<!-- more -->

我查了一圈文档，也在本机确认了一下：`codex --version` 输出 `codex-cli 0.133.0`，`codex features list` 里 `goals` 是 stable。OpenAI 在 2026-05-21 的 [Codex changelog](https://developers.openai.com/codex/changelog) 里写到，Goal mode 不再是 experimental，Codex app、IDE extension 和 CLI 都能用。官方的描述很克制：Goal 是 thread 上的 persistent objective，用来让 Codex 朝一个具体目标持续推进，可以暂停、恢复、清除。

这句话比“让 Codex 一直工作”准确得多。Goal 的关键在于让目标持续可见，执行时间只是结果之一。

## Goal 解决的是哪种尴尬

平时用 Codex，最容易出问题的地方通常不在单条命令，而在长任务做到一半后目标漂移。

你让它“把登录模块迁到新 API”，它会读代码、改文件、跑测试、修错误。这个过程可能跨很多 turn。每一轮你都能纠偏，但也会遇到三个问题：

- 你前面说过的边界，后面不一定还足够显眼。
- Codex 做完一个局部步骤后，可能把“局部通过”当成“整体完成”。
- 你中途插入一句“顺便看下这个报错”，主线任务的完成条件会变得更松。

Goal 做的事，是把“这次到底做到什么才算完”从聊天内容里拎出来，变成一个线程级状态。你仍然可以继续发消息打断、补充、纠偏，但当前 Goal 会比散落在历史消息里的约束更显眼。

我会把 Goal 当成 agent 的验收条件，少写鼓励语。

## 什么算一个好 Goal

OpenAI 的 [Follow Goals](https://developers.openai.com/codex/use-cases/follow-goals) 文档给了一个很实用的判断：Goal 适合 long-running work，尤其是 code migration、大重构、deployment retry loops、实验、游戏、side project 这种需要跨 turn 的任务；不适合一串无关小事。

对工程实践来说，最值得关注的是迁移、重构、部署重试和带验证闭环的前端实现。

如果任务一轮就能完成，别开 Goal。如果任务没有结束标准，也别开 Goal。

“把前端优化一下”算不上好 Goal。Codex 可以优化到天荒地老，也可以随手改三处 CSS 就说完成。

“根据 `docs/redesign-plan.md` 改首页，只改 `src/pages/home` 和 `src/components/home`，每完成一个 section 跑一次 `pnpm build`，最终用 Playwright 截 1440px 和 390px 两张图，确认没有布局重叠后停止”更像一个 Goal。

它有四个东西：

- 要达成什么：改首页。
- 不要碰什么：只改两个目录。
- 怎么证明进展：按 section 做，跑构建和截图。
- 何时停：桌面和移动截图通过检查。

这四个东西能减少 Codex 把局部完成当整体完成的机会。Goal 不会让 Codex 突然更听话；它只是让你更难逃避验收标准。

## 我会怎么写 `/goal`

Codex CLI 文档里 [`/goal`](https://developers.openai.com/codex/cli/slash-commands) 的基本形态很简单：

```text
/goal <objective>
/goal
/goal pause
/goal resume
/goal clear
```

目标最多 4000 个字符。长计划不要硬塞进去，放到文件里，让 Goal 指向文件。Codex app 的 [commands 文档](https://developers.openai.com/codex/app/commands) 也写到，Goal active 时会在 composer 上方显示进度，你可以暂停、恢复、编辑或清除。

我更推荐先用 `/plan` 把任务收敛，再把确认过的目标设成 Goal：

```text
/plan 先阅读 docs/payment-migration.md，并给出迁移计划，不要先修改文件。
```

等 Codex 给出计划，我确认范围和顺序，再设 Goal：

```text
/goal 按 docs/payment-migration.md 的里程碑逐步实施。保持公共行为不变。仅修改 src/payments、tests/payments、docs/payment-migration-notes.md。每个里程碑完成后运行 pnpm test payments。当 pnpm test payments 返回 0 且 docs/payment-migration-notes.md 记录了已迁移调用点时停止。若需要产品决策，请 pause 并说明阻塞点。
```

这段不漂亮，但它有用。

我不想让 Codex 猜“什么时候算 done”。我也不想让它把“测试还没跑，但看起来差不多”包装成完成。Goal 里应该出现具体命令、具体文件、具体边界。没有这些东西，Goal 只是一个更持久的愿望。

## 它和 Ralph Loop 像不像

像，但相似点很浅。

[Ralph Loop](https://claude.com/plugins/ralph-loop) 是 Anthropic verified 的 Claude Code 插件。它的公开实现很直白：根据 [README](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md)，Ralph 用 Stop hook 拦截 Claude 试图结束 session 的动作，然后把同一个 prompt 再喂回去，让 Claude 继续干。你可以设置 `--max-iterations`，也可以设置 `--completion-promise`，比如“当你输出某句承诺时才算完成”。

这是一种循环机制。它的核心问题是：**下一轮什么时候开始？** Claude 要结束时，hook 把它拉回来。

Codex Goal 的公开语义不一样。OpenAI 文档没有把它描述成 hook，也没有说它会重放同一个 prompt。它更像是线程上的目标状态：Codex app 会在输入框上方显示进度，你可以 pause、resume、edit、clear；CLI 里也可以用 `/goal` 查看当前目标。它的核心问题是：**当前线程到底朝哪个完成条件推进？**

所以不能简单说 Codex Goal 就是内置 Ralph Loop。它们都在处理“多轮 agent 工作”，但抽象层级不同。

这里还有一个容易忽略的事实：Claude Code 现在也有官方 `/goal`。Anthropic 的 [goal 文档](https://code.claude.com/docs/en/goal) 写得比 OpenAI 更暴露机制：Claude 每个 turn 后会用一个 small fast model 检查 completion condition 是否满足；文档还说 `/goal` 是一个 session-scoped prompt-based Stop hook wrapper。Claude 的 [`/loop` 文档](https://code.claude.com/docs/en/scheduled-tasks) 则把它定位成 session 内按间隔重复运行 prompt 或 slash command 的能力，更适合轮询状态或提醒。

下面只按公开文档里的用户可见行为对比，不推断底层实现：

| 工具 | 下一轮靠什么触发 | 什么时候停 | 适合什么 |
| --- | --- | --- | --- |
| Codex Goal | 当前线程里的 persistent objective | 目标完成、阻塞、用户暂停/清除 | 有明确验收条件的长任务 |
| Claude Code `/goal` | 前一个 turn 结束后，独立 evaluator 检查 completion condition | evaluator 判断条件满足，或用户清除 | session 内持续推进一个可验证条件 |
| Claude Code `/loop` | 计时器到点后重新运行 prompt 或 slash command | 固定间隔 loop 需要用户停止或等 7 天过期；动态 loop 可以自行结束 | 轮询 CI、部署、PR 状态，或短期 session 内定时维护 |
| Ralph Loop | Stop hook 拦截退出后重放同一个 prompt | completion promise 命中，或达到 iteration limit，或用户取消 | 自我迭代、反复修复、实验性长跑 |

所以 `/loop` 和 `/ralph-loop` 没有新版旧版关系，也没有内置版和插件版的关系。`/loop` 是 Claude Code 的计划任务能力，核心是“隔一段时间再跑一次”；`/ralph-loop` 是插件命令，核心是“Claude 想停时，用 Stop hook 把同一个 prompt 再塞回去”。前者适合等外部状态变化，比如 CI、部署、PR 评论；后者适合让 Claude 在同一个任务上反复试错，比如写代码、跑测试、修失败、再跑测试。

这些细节不能倒推到 Codex，但它说明同一类产品都在补一个洞：只靠普通对话，很难稳定表达“继续做，直到这个条件成立”。

## Goal 的效果取决于验证闭环

我不太相信“开了 Goal，复杂任务就自动变稳”这种说法。长期 agent 任务真正怕的是缺少可验证反馈，任务长反而只是表象。

适合 Goal 的任务通常有这些信号：

- 测试能跑：`pnpm test payments`、`pytest tests/auth`、`go test ./...`。
- diff 能审：只允许修改某些目录，最终 `git diff --stat` 看得出来。
- 产物能看：截图、构建产物、迁移清单、benchmark 日志。
- 阻塞能定义：遇到产品决策、权限、外部服务失败时停下来报告。

长任务还要写失败预算，不然 agent 会把时间花在低质量重试上。比如“最多尝试三种修复路径；如果都失败，停下来给证据”，通常比“直到修好”更像工程约束。

不适合 Goal 的任务也很常见：

- “帮我把代码写优雅一点。”
- “研究一下这个方向有没有价值。”
- “把所有历史技术债处理掉。”
- “做一个看起来高级的页面。”

这些任务可以交给 Codex，但要先拆。比如“研究方向”可以拆成“阅读这 5 个链接，输出一页反方观点和三条可验证假设”。“页面高级”可以拆成“参考 `reference.png`，保持文案不变，改布局和视觉层级，截图对比 1440px/390px，不允许文字重叠”。

Goal 不会替你定义质量。它只会放大你已经定义好的质量标准。

## 我会用它替代什么

我不会用 Goal 替代 `AGENTS.md`。项目约定、目录结构、编码规范，仍然应该写在 `AGENTS.md`，因为它们是所有任务共享的背景。

我也不会用 Goal 替代计划文件。复杂迁移仍然应该有 `docs/plan.md`，里面写 milestone、风险、检查项。Goal 只负责把“按这个计划做到什么程度”挂到当前线程上。

我会用 Goal 替代三类脆弱操作。

第一类是“每隔几轮提醒 Codex 不要忘了主线”。Goal 本身就该保存主线。

第二类是“把大任务塞进一个超长 prompt”。长 prompt 读起来像规格书，但执行过程中很容易变成背景噪音。更稳的做法是规格写文件，Goal 写验收条件。

第三类是“手工催下一步”。在需要继续推进时，当前 Goal 能让“继续”指向同一套验收条件，比每轮都问“继续”更清楚。

## 三个可以直接改的模板

迁移任务：

```text
/goal 按 docs/auth-migration.md 的里程碑逐步实施。保留现有公共行为。仅修改 src/auth、tests/auth 和 docs/auth-migration-notes.md。每个里程碑后运行 pnpm test auth。当测试通过且 notes 文件列出已迁移入口时停止。若 API 行为存在歧义则 pause。
```

修 CI：

```text
/goal 修复 logs/ci-failure.txt 中对应的 CI 失败。先在本地复现失败。做最小的代码或测试改动来修复。再次运行同一失败命令。命令返回 0 时停止，或在三种不同失败方案都失败并有证据后 pause。
```

前端验收：

```text
/goal 实施 docs/home-redesign-plan.md。保持文案不变。每个检查点后用 Playwright 在 1440px 和 390px 分别截图。两张截图中都不再出现明显重叠、布局偏移或按钮文字裁剪时停止。
```

这些模板靠的是边界清楚，不靠堆长度：它们把 Codex 的自由度锁在任务需要的范围内。

## 真正的问题变成了“你怎么定义完成”

Goal 这个功能让我有点不舒服。它逼我把原本可以边做边想的验收标准提前写出来。

以前我可以丢一句“帮我重构一下”，然后边看边改。结果好坏，很多时候取决于我中途盯得够不够紧。Goal 逼我提前回答几个工程问题：哪些文件能动？哪些行为不能变？用什么命令验收？失败几次后该停下，避免继续消耗时间？

这个问题不只出现在 Codex。Claude Code 的 `/goal`、`/loop`、Ralph Loop 都在围绕同一个缝隙打补丁：agent 已经能连续工作了，但“连续工作”本身没有价值，除非它知道何时停。

所以我的结论很简单：不要把 Goal 当自动驾驶。它最有价值的用法，是把目标写成一张验收单。

当你能写出清楚的验收单，Goal 会让 Codex 更适合做跨 turn 的长期任务。当你写不出来，它只是把一个模糊 prompt 保存得更久。
