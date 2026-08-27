# 素材清单：AI 刷完 3628 道 LeetCode，起步档模型解了 3567 道

## 支撑单元一：实验动机

### 支撑素材

- 用户亲历。一次面试包含在线手写编程题。题目内容、公司、时间和现场对话均未提供，不得补写。
- 用户当时的判断。常见 medium 题对 AI 已经没有明显压力，hard 题大多也能解，因此想知道 AI 在普通 LeetCode 题上的极限。
- 用户当前设想。如果面试要考察 AI 时代的编程能力，可以提供一道 AI 无法瞬间完成的陌生难题，让候选人现场配合 AI 解决，并观察拆解、验证和纠错。

---

## 支撑单元二：实验设计

### 支撑素材

- 固定实验集为同步时的 3628 道免费题。完整题库归档 4406 道，其中 778 道付费锁定。来源为 `D:\code\ai-leetcode-lab\stats\summary.md`。
- 实际执行阶梯为 `terra-medium → sol-medium → sol-high → sol-xhigh → sol-ultra`。来源为 `D:\code\ai-leetcode-lab\config\profiles.json`。
- 旧答案目录、官方题解、讨论区、搜索结果均在实验协议中明确禁止。来源为 `D:\code\ai-leetcode-lab\AGENTS.md`。
- 每个题目和 Profile 每轮最多 5 次远程试跑、3 次正式提交，最多 2 轮。当前档不值得继续时 defer，下一档获得完整尝试预算。来源为 `D:\code\ai-leetcode-lab\AGENTS.md`。
- 高档可以继承低档失败代码和分析，因此结果衡量阶梯接力，不是各模型从空白起步的独立盲测。来源为 `D:\code\ai-leetcode-lab\README.md`。

---

## 支撑单元三：最终结果与能力分布

### 支撑素材

- Accepted 3628 / 3628，覆盖率 100%。简单 949、中等 1836、困难 843。来源为 `D:\code\ai-leetcode-lab\stats\summary.md`。
- 首次成功归属为 terra-medium 3567、sol-medium 52、sol-high 4、sol-xhigh 1、sol-ultra 4。对应占比分别为 98.32%、1.43%、0.11%、0.03%、0.11%。
- terra-medium 首次解决 807 / 843 道困难题，占困难题 95.73%。两个 medium 档合计解决 834 / 843 道困难题，占 98.93%。
- 1836 道中等题全部在 medium 档解决，没有进入 high 及以上档位。
- 首次提交通过 3606 / 3628，首投通过率 99.39%。正式提交 3706 次，其中失败 78 次，整体通过率 97.90%。
- 完成时 LeetCode 个人页显示全站排名 95、已解答 3628、尝试中 0。截图为 `longform/leetcode-profile-3628.png`，页面链接为 https://leetcode.cn/u/funcsama/ 。

---

## 支撑单元四：九道进入 high 及以上档位的题

### 支撑素材

- sol-high 共 4 道困难题。LCP 76 魔法棋盘、LCP 58 积木拼接、3374 首字母大写 II、LCP 16 游乐园的游览计划。
- sol-xhigh 共 1 道困难题。LCP 82 万灵之树。
- sol-ultra 共 4 道困难题。LCP 49 环形闯关游戏、LCP 60 力扣泡泡龙、LCP 70 沙地治理、LCP 71 集水器。
- 九道题中八道为 LCP 题，一道为 SQL 困难题。它们覆盖状态压缩 DP、立方体表面精确覆盖、三角形枚举、构造与下界证明、虚树、平面区域图、minimax Dijkstra、子集 DP 和 SQL 边界规格等不同难点。来源为各题 `problem.md` 与 `approach.md`。
- LCP 82 的 sol-high 候选通过 112 / 114 用例后超时。sol-xhigh 用唯一平衡边分解与子集余数 DP 消除大量重复枚举，最终远程 Accepted。来源为 `D:\code\ai-leetcode-lab\problems\LCP-82-cnHoX6\approach.md`。
- 九题样本不足以比较 high、xhigh、ultra 的整体能力。高档还能看到低档失败产物，档位归属只能按阶梯过程解释。

---

## 支撑单元五：长期任务工作流

### 支撑素材

- 题面归档、代码模板、题目目录、候选登记、试跑、正式提交、统计均由仓库统一管理。来源为 `D:\code\ai-leetcode-lab\README.md`。
- 本地解题可以并行，远程动作通过共享锁串行，提交间隔至少 13 秒。连续 HTTP 429 指数退避，并有保守的滚动 24 小时 500 次提交门禁。来源为 `README.md` 与 `AGENTS.md`。
- 候选必须记录证明、复杂度与验证等级。送判队列只接受 candidate-ready 哈希与工作区代码一致的题。
- 每次远程动作向 `data/attempts.jsonl` 追加题目、Profile、时间、判题状态和代码 SHA-256。历史校正只能追加注释，不能改写旧事实。
- 最终审计显示当前代码与 Accepted 代码哈希精确一致 3628 题，Accepted 漂移 0，candidate 漂移 0，待复盘组合 0。

---

## 支撑单元六：五道假成功与校正

### 支撑素材

- 用户提供的远程限制错误包括 `Array.prototype.map` 禁用、一元减号触发禁止减法、禁止 Python set、禁止 Python dict、禁止 `sorted()`。
- 涉及 371 两整数之和、705 设计哈希集合、706 设计哈希映射、912 排序数组、2635 转换数组中的每个元素。
- 判题状态中出现 `Accepted` 字样，同时 `status_display` 为 `Violation of Restriction`。旧解析只认前者，造成假成功。完成提交为 `32195bab fix: enforce restrictions and complete free problem ladder`。
- 修复加入题目级源码限制检查，并让限制状态覆盖 Accepted 文案。五题带明确限制后重新从 terra-medium 解题、远程送判并达到 SOLVED。
- 测试补充了五类限制的提交前拦截，以及 `Violation of Restriction` 覆盖 Accepted 状态的用例。来源为完成提交 `32195bab` 中的 `ai_leetcode/restrictions.py` 和 `tests/test_runner.py`。

---

## 支撑单元七：结论边界与面试讨论

### 支撑素材

- 强证据。固定 3628 题全部拥有可追溯的远程 Accepted 终态，Profile 归属、代码哈希和最终统计可下钻复核。
- 中等强度证据。在这条允许逐档继承的实验流程里，中档模型足以完成绝大多数公开 LeetCode 免费题。
- 不支持的外推。实验不能区分模型独立推理与训练记忆，不能代表未公开的新题，也不能证明人类学习算法没有价值。
- 作者判断。常规公开算法题若允许 AI，单独用它区分工程候选人的信息量已经很低。若工作目标本身允许 AI，面试可以更关注候选人怎样拆问题、约束 AI、设计验证、定位失败和收尾长期任务。

## 补充素材（备用）

- 账号页的 3718 次提交全部来自本轮实验。追加日志中共有 3718 次非基础设施远程判题，其中 10 次限制违规和 2 次提交封装错误经 `result_annotation` 排除，正式模型统计因此为 3706 次。6 次 remote test 不进入账号提交数。
- 实验统计生成时间为 2026-08-18T16:04:02Z，完成提交时间为 2026-08-19 00:06:59 +0800。
- 实时题库后来新增题目，不应混入固定的 3628 题实验集。

## 会改变结论的边界（如有）

- LeetCode 题目和大量题解长期公开，训练材料污染足以改变对“纯推理能力”的解释。
- 档位间并非独立盲测，高档继承低档失败代码和分析。
- high、xhigh、ultra 只有 4、1、4 道样本，无法精确比较三个高档的相对能力。
- LeetCode 难度标签衡量平台题目难度，不是专门为模型设计的能力刻度。

## 待核查（如有）

- 无。正文只使用用户亲历、实验仓库、远程判题记录和公开账号页能够支持的事实。
