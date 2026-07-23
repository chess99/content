# 素材清单：Codex Goal：长期任务要先写完成条件

## 论点一：Goal 适合“比一轮 prompt 大、但有明确验收条件”的任务

### 支撑素材

- **官方定义**：OpenAI Codex use case 页面把 Goal 定义为“durable objective for long-running work”，建议在任务需要跨 turn 朝向“可验证停止条件”推进时使用。来源：https://developers.openai.com/codex/use-cases/follow-goals
- **适用场景**：官方列出的场景包括 code migration、大重构、deployment retry loops、experiments、games、side projects，以及需要清晰成功标准的长实验。来源同上。
- **反面边界**：官方明确说避免把 loose list of unrelated work 当作 goal。来源同上。
- **本机检查**：`codex --version` 输出 `codex-cli 0.133.0`；`codex features list` 中 `goals stable true`。这可作为作者环境说明，不当作普遍事实。

### 反证/限制条件

- 官方文档说 Codex 可以在 Goal 下独立工作数小时，但这不等于每个任务都适合无人看管。没有测试、没有截图验收、没有可运行检查的任务，Goal 只是把模糊目标保存得更久。
- Goal 不负责自动拆解任务。官方 app commands 建议先用 `/plan` shape it，再用 `/goal` 设置 refined goal。

### 来源风险

- 无风险：核心命令语义和适用场景有 OpenAI 官方文档。

---

## 论点二：好 Goal 的关键是完成条件、验证方式、边界和停止条件

### 支撑素材

- **官方写法建议**：OpenAI 建议一个好 Goal 要说明 Codex 应该达成什么、不应改什么、如何验证进展、何时停止。来源：https://developers.openai.com/codex/use-cases/follow-goals
- **设置步骤**：官方建议：命名一个 objective 和 stopping condition；指向必须先读的文件/日志/计划；定义证明进展的命令或 artifact；要求 checkpoint 和 progress log；用 `/goal` 查看状态；在完成、阻塞或变向时 pause/resume/clear。来源同上。
- **命令语义**：Codex CLI 文档写明 `/goal <objective>` 设置目标，`/goal` 查看，`/goal pause|resume|clear` 控制；目标非空且最多 4000 字符，长说明放文件里并让 Goal 指向文件。来源：https://developers.openai.com/codex/cli/slash-commands
- **App 行为**：Codex app 文档写明 Goal 是 persistent objective；active 时 app 会在 composer 上方显示进度，并可用按钮暂停、恢复、编辑或清除；仍然可以发 follow-up steer Codex。来源：https://developers.openai.com/codex/app/commands

### 反证/限制条件

- “写得长”不等于“写得好”。超过 4000 字符要放文件；更重要的是验收信号应该能进入 transcript 或文件系统，让 Codex可以自查。
- 对探索型任务，Goal 应该包含时间/turn/尝试次数边界，例如“最多尝试三种方案；若都失败，输出阻塞原因和证据”，否则可能变成成本不可控的循环。

### 来源风险

- 无风险：命令和写法均有官方文档。

---

## 论点三：Codex Goal 与 Ralph Loop 相似，但抽象层级不同

### 支撑素材

- **Ralph Loop 官方插件页**：Anthropic verified 的 Ralph Loop 插件描述为 iterative, self-referential AI development loops；Claude 反复处理同一任务直到完成。插件通过 stop hook 拦截 session exit，并自动重新投喂 prompt，同时保留文件修改和 git history。来源：https://claude.com/plugins/ralph-loop
- **Ralph README 实现描述**：Anthropic GitHub README 写明 Ralph 基于“continuous AI agent loops”，核心是 Stop hook 拦截 Claude 的退出尝试：Claude 工作、试图退出、Stop hook 阻止退出、同一 prompt 回灌、重复直到完成。来源：https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md
- **Ralph 使用方式**：`/ralph-loop "<prompt>" --max-iterations <n> --completion-promise "<text>"`，直到输出 completion promise 或达到 iteration limit。来源同上与插件页。
- **Codex Goal 产品语义**：Codex app / CLI 文档把 `/goal` 描述为 persistent target / task goal；它跟随 active thread，可 pause/resume/clear。来源：https://developers.openai.com/codex/app/commands 与 https://developers.openai.com/codex/cli/slash-commands

### 反证/限制条件

- 不能把 Codex Goal 简单写成“OpenAI 内置 Ralph Loop”。两者都跨 turn 推进，但 Ralph 的主要公开机制是 Stop hook 和同 prompt 重放；Codex Goal 公开文档强调的是 persistent objective、进度 UI 和线程状态。底层是否也有类似 evaluator / hook 机制，OpenAI 文档未明确，不应臆测。
- Claude Code 现在也有官方 `/goal`，并不只有 Ralph Loop。

### 来源风险

- 中风险：Codex Goal 的底层机制没有像 Claude Code `/goal` 那样在公开文档里解释 evaluator，所以只写产品层语义。

---

## 论点四：Claude Code `/goal`、`/loop`、Ralph Loop 可以作为对照，帮助读者理解“下一轮何时开始、何时停止”

### 支撑素材

- **Claude Code `/goal`**：官方文档说 `/goal` 设置 completion condition，Claude 会跨 turn 工作直到条件满足；每个 turn 后由一个 small fast model 检查条件是否成立。来源：https://code.claude.com/docs/en/goal
- **Claude Code `/goal` 对比表**：Claude 文档明确比较三种方式：`/goal` 在前一轮结束后开始下一轮，停止于模型确认条件满足；`/loop` 在时间间隔到达后开始下一轮，停止于用户或 Claude 判断；Stop hook 在前一轮结束后触发，停止逻辑由脚本或 prompt 决定。来源同上。
- **Claude Code `/loop`**：官方 scheduled tasks 文档说 `/loop` 用于在 session 内重复运行 prompt、轮询状态或设置提醒；也提示如果想“turn after turn until a condition is met”，看 `/goal`。来源：https://code.claude.com/docs/en/scheduled-tasks

### 反证/限制条件

- Claude Code 的 `/goal` 文档细节不能倒推到 Codex Goal；只能作为对照理解。
- Ralph Loop 的插件页安装量等数字会变化，不建议写进正文，除非当天核查并声明时间。

### 来源风险

- 无风险：Claude Code `/goal`、`/loop`、Ralph Loop 均有官方/官方仓库资料。

---

## 补充素材（备用）

- OpenAI Codex changelog：2026-05-21，Codex app 26.519 提到 Goal mode 不再是 experimental，app / IDE extension / CLI 可用，可让 Codex 朝具体目标工作数小时甚至数天。来源：https://developers.openai.com/codex/changelog
- OpenAI Codex changelog：2026-05-21，Codex CLI 0.133.0 新功能说明 Goals 默认启用，dedicated storage，track progress across active turns。来源同上。
- 文章可用对照表：
  - Codex Goal：目标状态随 thread 存在；用户可 pause/resume/clear；适合有验证闭环的长任务。
  - Claude Code `/goal`：completion condition + small fast model evaluator；session-scoped；适合条件可由 transcript 证明的任务。
  - Claude Code `/loop`：按时间重复 prompt；适合轮询 deploy / CI / PR 状态。
  - Ralph Loop：Stop hook + same prompt replay + completion promise；适合连续迭代和自我修复。
- 可直接给读者的 Goal 模板：
  - `/goal Implement docs/PLAN.md. Work milestone by milestone, run npm test after each milestone, keep changes scoped to src/auth and tests/auth, and stop when npm test exits 0 and git diff contains only auth-related files.`
  - `/goal Migrate the old payment adapter to the new API. Read docs/payment-migration.md first. Preserve public behavior, run pnpm test payment after each checkpoint, and stop if a product decision is needed.`
  - `/goal Improve the landing page to match reference.png. Use Playwright screenshots at 1440px and 390px, keep copy unchanged, and stop when the screenshots match the reference within visible layout tolerance.`
