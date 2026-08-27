# AI LeetCode 阶梯实验统计快照

本快照整理自 `D:\code\ai-leetcode-lab` 完成状态，用于给博客正文中的数字提供统一口径。原始事实保存在实验仓库的追加日志、逐题目录和自动统计中。

## 实验范围

- 题库同步时间为 2026 年 8 月 11 日
- 同步时题目总数 4406
- 免费实验集 3628
- 付费锁定题 778
- 简单题 949
- 中等题 1836
- 困难题 843

平台后来新增的题目不回写到本次固定样本。

## 执行阶梯

1. terra-medium
2. sol-medium
3. sol-high
4. sol-xhigh
5. sol-ultra

每个题目与 Profile 每轮最多进行 5 次远程试跑和 3 次正式提交，最多 2 轮。当前思路明显不值得继续时允许提前 defer，题目随后进入下一档。实验没有完整 Token 数据，不估算各档 Token 消耗。

高档可以继承低档留下的失败代码和分析。本结果衡量阶梯接力过程，不等同于各档模型从空白起步的独立盲测。

## 最终结果

| 指标 | 结果 |
|---|---|
| 远程 Accepted | 3628 / 3628 |
| 远程覆盖率 | 100% |
| 首次正式提交通过 | 3606 |
| 首投通过率 | 99.39% |
| 正式提交 | 3706 |
| 失败正式提交 | 78 |
| 正式提交整体通过率 | 97.90% |
| 当前代码与 Accepted 代码精确匹配 | 3628 |
| Accepted 哈希漂移 | 0 |
| candidate 哈希漂移 | 0 |
| 待复盘组合 | 0 |

## 首次成功档位与难度

| 首次成功档位 | 简单 | 中等 | 困难 | 合计 | 占全部题目 |
|---|---|---|---|---|---|
| terra-medium | 940 | 1820 | 807 | 3567 | 98.32% |
| sol-medium | 9 | 16 | 27 | 52 | 1.43% |
| sol-high | 0 | 0 | 4 | 4 | 0.11% |
| sol-xhigh | 0 | 0 | 1 | 1 | 0.03% |
| sol-ultra | 0 | 0 | 4 | 4 | 0.11% |

## 进入 high 及以上档位的九道题

| 档位 | 题目 |
|---|---|
| sol-high | LCP 76 魔法棋盘、LCP 58 积木拼接、3374 首字母大写 II、LCP 16 游乐园的游览计划 |
| sol-xhigh | LCP 82 万灵之树 |
| sol-ultra | LCP 49 环形闯关游戏、LCP 60 力扣泡泡龙、LCP 70 沙地治理、LCP 71 集水器 |

## 限制题校正

实验末期发现五道题的判题响应同时出现 Accepted 字样和 Violation of Restriction 展示状态。完成修复后，限制状态优先于 Accepted 文案，候选登记与远程提交前也会检查题目级禁用规则。

涉及的题为 371 两整数之和、705 设计哈希集合、706 设计哈希映射、912 排序数组、2635 转换数组中的每个元素。五道题随后带明确限制重新交给 terra-medium，最终都取得真实远程 Accepted。

完成提交为 `32195bab7fa8cd645ed62aa8fe8afe93a9368c71`。

## 数据来源

- `D:\code\ai-leetcode-lab\stats\summary.md`
- `D:\code\ai-leetcode-lab\stats\summary.json`
- `D:\code\ai-leetcode-lab\config\profiles.json`
- `D:\code\ai-leetcode-lab\data\attempts.jsonl`
- 实验完成提交 `32195bab7fa8cd645ed62aa8fe8afe93a9368c71`
