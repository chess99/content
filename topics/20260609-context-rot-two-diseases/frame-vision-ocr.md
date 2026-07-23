# 关键帧 Vision OCR（每 10 秒采样）

## [00:00] frame_0001

01 /HOOK
@：
炼云 AI
这个剧本，你大概演过
第1~5 次
开一个新对话
agent 越改越烂
一次就改对了
1/ 过去半年它被反复说
context rot 上下文腐烂
这事你大概遇到过
01/20

## [00:10] frame_0002

02/ 这期的重点
@
炼云 AI
读了过去半年的相关研究和大厂博客—
这个名字其实是个 陷阱
<shell>context rots/shell>
病•其一
病•其二
distraction
poisoning
长度的诅咒
毒性的诅咒
不把它们分开—你永远治不对
这个名字其实是个陷阱
LIANYUN
02 /20

## [00:20] frame_0003

02/ 这期的重点
@
炼云 AI
读了过去半年的相关研究和大厂博客—
这个名字其实是个 陷阱
<shell>context rots/shell>
病•其一
病•其二
distraction
poisoning
长度的诅咒
毒性的诅咒
不把它们分开—你永远治不对
这—期想跟你聊清楚的就是这件事
LIANYUN
02/20

## [00:30] frame_0004

03/ 起源•CHROMA 报告
Chroma 测了 18 个主流模型
// 给它们一段长文档，找某句话— 然后一边加长文档，一边看表现
GPT
Claude
Gemini
Qwen
退化
退化
退化
退化
没逃掉
性能 vs 输入长度
.~5 万 token 开始明显下滑少
100 万 token 窗口上限
不是到上限才崩—是远在上限之前，就开始悄悄变笨
他们选了 18个当时最强的模型
LIANYUN
03 / 20

## [00:40] frame_0005

03/起源• CHROMA 报告
@
炼云 AI
Chroma 测了18个主流模型
// 给它们一段长文档，找某句话— 然后一边加长文档，一边看表现
GPT
Claude
Gemini
Qwen
+14个其他模型，全部退化•一个都
退化
退化
退化
退化
没逃掉
性能 VS 输入长度
~5 万 token 开始明显下滑 」
100 万 token 窗口上限
不是到上限才崩—是远在上限之前，就开始悄悄变笨
比如说给你一段很长的文档
LIANYUN
03/20

## [00:50] frame_0006

03/ 起源•CHROMA 报告
Chroma 测了 18个主流模型
// 给它们一段长文档，找某句话— 然后一边加长文档，一边看表现
GPT
Claude
Gemini
Qwen
退化
退化
退化
退化
没逃掉
性能 vS 输入长度
，~5 万 token 开始明显下滑J
100 万 token 窗口上限
不是到上限才崩—是远在上限之前，就开始悄悄变笨
所有模型都会随着输入变长而退化
LIANYUN
03 /20

## [01:00] frame_0007

03/ 起源•CHROMA 报告
Chroma 测了 18 个主流模型
// 给它们一段长文档，找某句话— 然后一边加长文档，一边看表现
GPT
Claude
Gemini
Qwen
退化
退化
退化
退化
没逃掉
性能 vs 输入长度
，~5 万 token 开始明显下滑少
100 万 token 窗口上限
不是到上限才崩—是远在上限之前，就开始悄悄变笨
是远在上限之前 就始梢梢变笨
LIANYUN
03 /20

## [01:10] frame_0008

04/2025-09 ANTHROPIC 背书•但是
@
炼云 AI
2025-09• Anthropic 定调
这种病有个名字
attention budget• 注意力预算
distraction
EP1讲过—就是给这件事的解释
注意力被稀释
但你回想一下开头那个改 bug的场景—
你的 context
但模型就是越改越烂
1-2 万 token
这是为什么？
离稀释程度还远着呢
你遇到的，根本不是 distraction
上一期我们提到的attention budget 注意力预算
LIANYUN
04 / 20

## [01:20] frame_0009

04 /2025-09 ANTHROPIC 背书•但是
@
炼云 AI
2025-09• Anthropic 定调
这种病有个名字
attention budget• 注意力预算
distraction
EP1讲过—就是给这件事的解释
注意力被稀释
但你回想一下开头那个改bug的场景—
你的 context
但模型就是越改越烂
1-2 万 token
这是为什么？
离稀释程度还远着呢
4 你遇到的，根本不是 distraction
都是这一种
LIANYUN
04 /20

## [01:30] frame_0010

04 /2025-09 ANTHROPIC 背书•但是
@
炼云 AI
2025-09• Anthropic 定调
这种病有个名字
attention budget• 注意力预算
distraction
EP1讲过—就是给这件事的解释
注意力被稀释
但你回想一下开头那个改bug的场景—
你的 context
但模型就是越改越烂
1-2 万 token
这是为什么？
离稀释程度还远着呢
你遇到的，根本不是 distraction
但是你回想一下我开头讲的那个改bug的场景
LIANYUN
04/20

## [01:40] frame_0011

04 /2025-09 ANTHROPIC 背书•但是
@ 炼云 AI
2025-09• Anthropic 定调
这种病有个名字
attention budget• 注意力预算
distraction
EP1讲过—就是给这件事的解释
注意力被稀释
但你回想一下开头那个改 bug的场景—
你的 context
但模型就是越改越烂
1-2 万 token
这是为什么？
离稀释程度还远着呢
4 你遇到的，根本不是 distraction
因为你遇到的根本就不是distraction
LIANYUN
04/20

## [01:50] frame_0012

05/ 第二种病•POISONING
@ 炼云 AI
这种病也有名字—
context poisoning
上下文中毒
// 最早是 DeepMind 让 Gemini 玩宝可梦的时候正式定义的
DeepMind• 原话
context 的某些部分被错误信息毒化，而且这种毒化要花很长时间才能解开。
结果就是，模型会执着于完成不可能或者无意义的目标。
上下文中毒
LIANYUN
05/20

## [02:00] frame_0013

05/ 第二种病• POISONING
@：
炼云 AI
这种病也有名字—
context poisoning
上下文中毒
// 最早是 DeepMind 让 Gemini 玩宝可梦的时候正式定义的
DeepMind• 原话
context 的某些部分被错误信息毒化，而且这种毒化要花很长时间才能解开。
结果就是，模型会执着于完成不可能或者无意义的目标。
context的某些部分被错误信息毒化
LIANYUN
05 / 20

## [02:10] frame_0014

05/ 第二种病• POISONING
@ 炼云 AI
这种病也有名字—
context poisoning
上下文中毒
// 最早是 DeepMind 让 Gemini 玩宝可梦的时候正式定义的
DeepMind• 原话
context 的某些部分被错误信息毒化，而且这种毒化要花很长时间才能解开。
结果就是，模型会执着于完成不可能或者无意义的目标。
不可能或者无意义的目标
LIANYUN
05/20

## [02:20] frame_0015

06/ 两种机制对比
@ 炼云 AI
完全不是一回事
distraction
poisoning
context 太长
context 不长•但里面有毒
信号被淹没
早期错误判断进 context
模型走神
一被反复引用
一所有推理建立在那个错误上
KEY
distraction 是长度问题•poisoning 是真相问题
poisoning是 contextt不长但里面有毒
LIANYUN
06 /20

## [02:30] frame_0016

07/ 场景解剖•CONTEXT 里发生了什么
@！
炼云 AI
每改一次，最初的错误假设都没被清理
反而被反复引用•反复加强
#1 agent给了错误修复方案
一进入 context
#2你说「不对」
—.
agent 听成「细节不对，继续推」
#3 再改细节
错误假设被再引用一次
#4 你再说「不对」
一 假设被再加强一次
#5 到了第五次
一 错误地基上已经盖了5 层楼
要它推倒重来—几乎不可能
你致bug那个场景
LIANYUN
07/20

## [02:40] frame_0017

07 / 场景解剖•CONTEXT 里发生了什么
@ 炼云 AI
每改一次，最初的错误假设都没被清理
反而被反复引用•反复加强
#1 agent给了错误修复方案
进入context
#2 你说「不对」
一 agent 听成「细节不对，继续推』
#3 再改细节
错误假设被再引用一次
#4 你再说「不对」
一 假设被再加强一次
#5 到了第五次
一 错误地基上已经盖了5 层楼
要它推倒重来—几乎不可能
你说不对 改
LIANYUN
07/20

## [02:50] frame_0018

07 / 场景解剖•CONTEXT 里发生了什么
@
炼云 AI
每改一次，最初的错误假设都没被清理
反而被反复引用•反复加强
#1 agent给了错误修复方案
一进入context
#2 你说「不对」
一 agent 听成「细节不对，继续推』
#3 再改细节
错误假设被再引用一次
#4 你再说「不对」
一 假设被再加强一次
#5 到了第五次
一 错误地基上已经盖了5 层楼
要它推倒重来—几乎不可能
所以官在第一次错误方案的基础上改了一个细节
LIANYUN
07/20

## [03:00] frame_0019

07/ 场景解剖•CONTEXT 里发生了什么
@ 炼云 AI
每改一次，最初的错误假设都没被清理
反而被反复引用•反复加强
#1 agent给了错误修复方案
进入context
#2 你说「不对」
一 agent 听成「细节不对，继续推』
#3 再改细节
一 错误假设被再引用一次
#4 你再说「不对」
一 假设被再加强一次
#5 到了第五次
一 错误地基上已经盖了5 层楼
要它推倒重来—几乎不可能
反而被反复引用 反复加强
LIANYUN
07/20

## [03:10] frame_0020

07/ 场景解剖•CONTEXT 里发生了什么
@：
炼云 AI
每改一次，最初的错误假设都没被清理
反而被反复引用•反复加强
#1 agent给了错误修复方案
进入context
#2 你说「不对」
一 agent 听成「细节不对，继续推』
#3 再改细节
一 错误假设被再引用一次
#4 你再说「不对」
一 假设被再加强一次
#5 到了第五次
一 错误地基上已经盖了5 层楼
要它推倒重来—几乎不可能
它已经在一个完全错的地基上 盖了五层楼
LIANYUN
07/20

## [03:20] frame_0021

082025-11• LOCOBENCH- AGENT
@
炼云 AI
Salesforce 11 月发的一个 benchmark
结论很刺眼—
agent 跑超过
×！
重复读已经读过的文件
× 重复调用已经失败的工具
12
× 生成大段没有用的摘要
轮之后
陷入循环
12轮听起来不多吧？跟Cursor讨论一个稍复杂的bug—分分钟就到
Salesforce 11 月发了一个叫 LoCoBench-Agent 的
benchmark
LIANYUN
08 /20

## [03:30] frame_0022

082025-11• LOCOBENCH- AGENT
@
炼云 AI
Salesforce 11 月发的一个 benchmark
结论很刺眼—
agent 跑超过
×！
重复读已经读过的文件
重复调用已经失败的工具
12
* 生成大段没有用的摘要
轮之后
陷入循环
12轮听起来不多吧？跟Cursor讨论一个稍复杂的bug—分分钟就到
重复调用已经失败的工具
LIANYUN
08 /20

## [03:40] frame_0023

082025-11• LOCOBENCH- AGENT
@ 炼云 AI
Salesforce 11 月发的一个 benchmark
结论很刺眼—
agent 跑超过
*重复读已经读过的文件
×重复调用已经失败的工具
12
* 生成大段没有用的摘要
轮之后
陷入循环
12轮听起来不多吧？跟Cursor讨论一个稍复杂的bug—分分钟就到
12轮分分钟就到了
LIANYUN
08/20

## [03:50] frame_0024

092026-03•CONSENSUS INERTIA
@ 炼云 AI
Consensus Inertia 共识惯性
// 一条错误轨迹一旦被中间产物固定下来，纠正成本会急剧上升
错误的东西逐渐凝固成 agent 心目中的「约束」
C1 原始 bug
c2 失败的修复
c3 新的报错信息
C1 ^ C2 A C3 = o 试国同时满足一一數学上不可能
所以模型在不同方案之间雲荡
不是模型不行—是它在执行一个数学上无解的任务
共识惯性
LIANYUN
09 /20

## [04:00] frame_0025

092026-03•CONSENSUS INERTIA
@
炼云 AI
Consensus Inertia：
共识惯性
// 一条错误轨迹一旦被中间产物固定下来，纠正成本会急剧上升
错误的东西逐渐凝固成 agent 心目中的「约束」
C1 原始 bug
c2 失败的修复
C3
新的报错信息
C1 ^ C2 ^ C3 =o 试图同时满足—一數学上不可能
所以模型在不同方案之间震荡
不是模型不行—是它在执行一个数学上无解的任务
错误的清测失败的修复错误的报错信息
LIANYUN
09/20

## [04:10] frame_0026

092026-03•CONSENSUS INERTIA
@
炼云 AI
Consensus Inertia 共识惯性
// 一条错误轨迹一旦被中间产物固定下来，纠正成本会急剧上升
错误的东西逐渐凝固成 agent 心目中的「约束」
C1 原始 bug
c2 失败的修复
C3
新的报错信息
C1 ^ C2 ^ C3 =o 试图同时满足—一數学上不可能
所以模型在不同方案之间震荡
不是模型不行—是它在执行一个数学上无解的任务
都是在试固同时满足这世约束
LIANYUN
09/20

## [04:20] frame_0027

092026-03•CONSENSUS INERTIA
@ 炼云 AI
Consensus Inertia 共识惯性
// 一条错误轨迹一旦被中间产物固定下来，纠正成本会急剧上升
错误的东西逐渐凝固成 agent 心目中的「约束」
C1 原始 bug
c2 失败的修复
C3 新的报错信息
C1 ^ C2 ^ C3 = o 试国同时满足—數学上不可能
所以模型在不同方案之间震荡
不是模型不行—是它在执行一个数学上无解的任务
原始bug失败的修复 新的报错全都共存
LIANYUN
09 /20

## [04:30] frame_0028

092026-03•CONSENSUS INERTIA
@
炼云 AI
Consensus Inertia 共识惯性
// 一条错误轨迹一旦被中间产物固定下来，纠正成本会急剧上升
错误的东西逐渐凝固成 agent 心目中的「约束」
C1 原始 bug
c2 失败的修复
C3
新的报错信息
C1 ^ C2 ^ C3 =o 试图同时满足—一數学上不可能
所以模型在不同方案之间震荡
不是模型不行—是它在执行一个数学上无解的任务
所以官在不同方案之间震荡
LIANYUN
09/20

## [04:40] frame_0029

1日/ 大厂现代 STACK•全在治 DISTRACTION
@
炼云 AI
那 /compact 呢？summary 呢？
/ 这些方案基本都在治 distraction，不是在治 poisoning
•1 /compact •压缩长 context
02 Cursor 自动摘要
03 ByteDance context folding
04 Anthropic progressive disclosure
Anthropic•100 轮评测
-84% +39%
context editing+ memory
token 消耗
agentic search
对 distraction 真有用—但对poisoning 不仅没用。 有时有反作用
那不是有 /compact 吗不是有 summary 吗
LIANYUN
10 / 20

## [04:50] frame_0030

10/ 大厂现代 STACK•全在治 DISTRACTION
@
炼云 AI
那/compact 呢？summary 呢？
// 这些方案基本都在治 distraction，不是在洽 poisoning
01 /compact •压缩长 context
|02 Cursor 自动摘要
03 ByteDance context folding
04 Anthropic progressive disclosure
Anthropic•100 轮评测
-84% +39%
context editing+memory
token 消耗
agentic search
对 distraction 真有用—但对 poisoning 不仅没用。 有时有反作用
不是在治 poisoning
LIANYUN
10/20

## [05:00] frame_0031

10/ 大厂现代 STACK•全在治 DISTRACTION
@
炼云 AI
那/compact 呢？summary 呢？
// 这些方案基本都在治 distraction，不是在治 poisoning
•1 /compact •压缩长 context
02 Cursor 自动摘要
03 ByteDance context folding
04 Anthropic progressive disclosure
Anthropic• 100 轮评测
-84% +39%
context editing+ memory
token 消耗
agentic search
| 对distraction 真有用—但对poisoning 不仅没用。有时有反作用
Anthropic 的 progressive disclosure
LIANYUN
10 /20

## [05:10] frame_0032

10/ 大厂现代 STACK•全在治 DISTRACTION
炼云 AI
那/compact 呢？summary 呢？
// 这些方案基本都在治 distraction，不是在治 poisoning
•1 /compact •压缩长 context
02 Cursor 自动摘要
03 ByteDance context folding
04 Anthropic progressive disclosure
Anthropic• 100 轮评测
-84% +39%
context editing + memory
token 消耗
agentic search
」对distraction 真有用—但对 poisoning 不仅没用。有时有反作用
context editing + memory 在 100 轮评测里
LIANYUN
10/20

## [05:20] frame_0033

10/ 大厂现代 STACK •全在治 DISTRACTION
@
炼云 AI
那/compact 呢？summary 呢？
// 这些方案基本都在治 distraction，不是在治 poisoning
01 /compact •压缩长 context
02 Cursor 自动摘要
03 ByteDance context folding
04 Anthropic progressive disclosure
Anthropic• 100 轮评测
-84% +39%
context editing+memory
token 消耗
agentic search
对 distraction 真有用—但对 poisoning 不仅没用。 有时有反作用
这是真的有用
LIANYUN
10/ 20

## [05:30] frame_0034

11/ 反作用案例•ANTHROPIC 自己承认
@ 炼云 AI
Claude Code 文档里记录的失败模式
Autocompact is thrashing
压缩刚成功
一次文件读取/工具输出，立刻又把context 填满
-最初的错误假设，在压缩后还在里面
因为压缩算法判定它是「重要信息」
KEY 压缩不分毒不毒—毒性信息在被识别成「重要」后反被保留
Anthropic 自己在 Claude Code文档里都承认了一个失败模
式
LIANYUN
11 /20

## [05:40] frame_0035

11/ 反作用案例•ANTHROPIC 自己承认
@ 炼云 AI
Claude Code 文档里记录的失败模式
Autocompact is thrashing
压缩刚成功
- 一次文件读取/工具输出，立刻又把 context 填满
一最初的错误假设，在压缩后还在里面
因为压缩算法判定它是「重要信息」
KEY 压缩不分毒不毒—毒性信息在被识别成「重要」后反被保留
而且那个最初的错误假没在压缩之后还在里面
LIANYUN
11 /20

## [05:50] frame_0036

12 2026-02•CONTEXTUAL DRAG
@
炼云 AI
让毒化的模型自我纠错——结果呢？
// 2 月份一篇论文叫 Contextual Drag
模型准确率
预期：回升
论文给现象起的名字
self-
deterioration
自我恶化
让毒化模型自我纠错 丰能走出去。
反而沿原轨迹继续下沉
开始自纠错
实际：继续下降
更狠的是2月份一篇论文叫Contextual Drag
LIANYUN
12 / 20

## [06:00] frame_0037

12 2026-02•CONTEXTUAL DRAG
@
炼云 AI
让毒化的模型自我纠错—结果呢？
1/ 2 月份一篇论文叫 Contextval Drag
模型准确率
预期：回升
论文给现象起的名字
self-
deterioration
自我恶化
让毒化模型自我纠错 手能走出去。
反而沿原轨迹继续下沉
开始自纠错
实际：继续下降
结果性能不仅没口升 反而继续下降
LIANYUN
12 / 20

## [06:10] frame_0038

13 2026-04• LATENT PHASE- SHIFT ROLLBACK
@
炼云 AI
更狠的一篇—直接绕过prompt这层
1/ 在模型内部，手动回滚一段KV-cache
方案 A
方案 B
让模型自己 prompt 自己纠错
手动回滚 KV-cache
baseLine
绕过 prompt 层
B比A强
+24+308
让模型自己走出来—基本是无效的
叫 Latent Phase-Shift Rollback
LIANYUN
13/20

## [06:20] frame_0039

13 2026-04• LATENT PHASE- SHIFT ROLLBACK
@
炼云 AI
更狠的一篇—直接绕过prompt这层
// 在模型内部，手动回滚一段KV-cache
方案 A
方案 B
让模型自己 prompt 自己纠错
手动回滚 KV-cache
DaseLine
绕过 prompt层
B比A强
+24
个百分点
让模型自己走出来—基本是无效的
结果是手动回滚的效果
LIANYUN
13/20

## [06:30] frame_0040

14 / 把研究串起来•硬结论
◎ 炼云 AI
context 被毒化之后，最有效的方法是—
清空 重开
不是新对话里 agent 变聪明了一
是旧对话里那个毒，在新对话里不存在了
当 context 被毒化之后
LIANYUN
14 / 20

## [06:40] frame_0041

14 / 把研究串起来•硬结论
@
炼云 AI
context 被毒化之后，最有效的方法是—
清空 重开
不是新对话里 agent 变聪明了一
是旧对话里那个毒，在新对话里不存在了
这就是为什么你开新对话一次就好
LIANYUN
14 ½ 28

## [06:50] frame_0042

15/ 以后碰到-- 要识别是哪种
@：
炼云 AI
干净的对比
// 以后碰到— 识别是 distraction 还是 poisoning
distraction• 长度的诅咒
poisoning• 毒性的诅咒
症状
| context 太长•信号被稀释•模型走神
一
context 不长•错误假设被反复引用
谁会得
| 所有模型都会得
|跟人类反馈方式有关
解法
| compact•folding• summary• skills
清空重开
现状
|大厂现代 stack 主要在治这个
目前基本无解
讲到这里 我想把这两种病放在一起
LIANYUN
15 / 20

## [07:00] frame_0043

15 / 以后碰到-- 要识别是哪种
@
炼云 AI
干净的对比
1/ 以后碰到— 识别是 distraction 还是 poisoning
distraction• 长度的诅咒
poisoning
毒性的诅咒
症状
| context 太长•信号被稀释•模型走神
context 不长•错误假设被反复引用
谁会得
！ 所有模型都会得
|跟人类反馈方式有关
解法
| compact•folding• summary • skills
清空重开
现状
|大厂现代 stack 主要在治这个
目前基本无解
Context 太长信号被秸释模型走神
LIANYUN
15/ 20

## [07:10] frame_0044

15 / 以后碰到-- 要识别是哪种
@ 炼云 AI
干净的对比
1/ 以后碰到— 识别是 distraction 还是 poisoning
distraction • 长度的诅咒
poisoning• 毒性的诅咒
症状
| context 太长 •信号被稀释•模型走神
context 不长•错误假设被反复引用
谁会得
丨所有模型都会得
|跟人类反馈方式有关
解法
compact•folding• summary• Skills
清空重开
现状
|大厂现代 stack 主要在治这个
目前基本无解
有解 compact folding summary skills
LIANYUN
15/ 20

## [07:20] frame_0045

15 / 以后碰到-- 要识别是哪种
@ 炼云 AI
干净的对比
1/ 以后碰到— 识别是 distraction 还是 poisoning
distraction• 长度的诅咒
poisoning• 毒性的诅咒
症状
| context 太长 •信号被稀释•模型走神
context 不长•错误假设被反复引用
谁会得
丨所有模型都会得
|跟人类反馈方式有关
解法
|compact•folding• summary • skills
|清空重开
现状
|大厂现代 stack 主要在治这个
|目前基本无解
Context不长但里面有错误假设被反复引用
LIANYUN
15/20

## [07:30] frame_0046

15 / 以后碰到-- 要识别是哪种
@
炼云 AI
干净的对比
// 以后碰到— 识别是 distraction 还是 poisoning
distraction• 长度的诅咒
poisoning
毒性的诅咒
症状
| context 太长 •信号被稀释•模型走神
context 不长•错误假设被反复引用
谁会徥
所有模型都会得
|跟人类反馈方式有关
解法
| compact•folding• summary • skills
清空重开
现状
大厂现代 stack 主要在治这个
| 目前基本无解
目前基本天解最有效的方法是手动清空重开
LIANYUN
15 / 20

## [07:40] frame_0047

16 / 更深一层•两种架构挑战
@ 炼云 AI
这两件事对应着—完全不同的架构挑战
distraction
poisoning
注意力机制的
需要的能力是
数学局限
元认知
很多聪明的工程方法可以绕过去
X 当前架构基本不具备
元认知• agent 要做到的事
意识到「我现在的某个前提可能是错的」•
主动否定自己之前的判断
distraction 是注意力机制的数学局限
LIANYUN
16/ 20

## [07:50] frame_0048

16 / 更深一层•两种架构挑战
@ 炼云 AI
这两件事对应着—完全不同的架构挑战
distraction
poisoning
注意力机制的
需要的能力是
数学局限
元认知
很多聪明的工程方法可以绕过去
X 当前架构基本不具备
元认知• agent 要做到的事
意识到「我现在的某个前提可能是错的」•
主动否定自己之前的判断
agent要能意识到
LIANYUN
16 / 20

## [08:00] frame_0049

17/ 回看 EP1 主线•一个张力
@
炼云 AI
EP1 的主线是
决策权正在下沉
distraction
agent skills• context folding • ACE—
V正在发生
让 agent 自己管自己的 context
poisoning
决策权下沉—还远远没到
X 还未到
决策权交不给—一个意识不到自己被毒化的 agent
这件事跟我上一期讲的决策权正在下沉
LIANYUN
17 /20

## [08:10] frame_0050

17/ 回看 EP1主线•一个张力
@ 炼云 AI
EP1 的主线是
决策权正在下沉
distraction
agent skills• context folding• ACE—
正在发生
让 agent 自己管自己的 context
poisoning
决策权下沉—还远远没到
X 还未到
| 决策权交不给—一个意识不到自己被毒化的 agent
决策权下沉确实在发生
LIANYUN
17/20

## [08:20] frame_0051

17 / 回看 EP1 主线•一个张力
@ 炼云 AI
EP1 的主线是
决策权正在下沉
distraction
agent skills•context folding• ACE —
正在发生
让 agent 自己管自己的 context
poisoning
决策权下沉—还远远没到
X 还未到
| 决策权交不给—一个意识不到自己被毒化的 agent
但在 poisoning 这件事上
LIANYUN
17/20

## [08:30] frame_0052

18/ 下次碰到•一个诊断问题
@ 炼云 AI
agent 越改越乱时—先停下来，问自己
这个context是太长了，还是太脏了？
太长一
太脏一
•压缩/摘要
•别再勾兑了
•新开 sub-agent处理细节
•清空，重开
都有用
其他手段基本无效
清空重开＋认输=当前架构下最理性的选择
所以下次你再碰到 agent越改越乱
LIANYUN
18 /20

## [08:40] frame_0053

18 / 下次碰到•一个诊断问题
@ 炼云 AI
agent 越改越乱时—先停下来，问自己
这个 context是太长了，还是太脏了？
太长一
太脏一
•压缩 /摘要
•别再勾兑了
•新开 sub-agent 处理细节
•清空，重开
都有用
其他手段基本无效
清空重开＋认输=当前架构下最理性的选择
如果是太太
LIANYUN
18/ 20

## [08:50] frame_0054

18 / 下次碰到•一个诊断问题
@ 炼云 AI
agent 越改越乱时—先停下来，问自己
这个 context是太长了，还是 太脏了？
太长一
太脏一
•压缩 /摘要
•别再勾兑了
•新开 sub-agent 处理细节
•清空，重开
都有用
其他手段基本无效
清空重开 ＋认输=当前架构下最理性的选择
如果是太脏别再勾兑了清空重开
LIANYUN
18/20

## [09:00] frame_0055

19/ 伏笔•2026 大厂共识
@ 炼云 AI
有没有觉得奇怪—
新开一个 sub-agent= 局部的清空重开
1/ 2026 所有大厂用同一招对抗 context 污染
Anthropic
multi-agent system
| Cursor
并行 sub-agent
Manus|
planner/executor
Claude Code /agents
OpenAI Codex /agent 切换
同一招
把任务切片•每片用一个干净的sub-agent 去跑•
只把结果带回主线，过程全部丢掉
我刚才反复提到一个词 sub-agent
LIANYUN
19/20

## [09:10] frame_0056

19/ 伏笔•2026 大厂共识
@ 炼云 AI
有没有觉得奇怪—
新开一个 sub-agent= 局部的清空重开
// 2026 所有大厂用同一招对抗 context 污染
Anthropic multi-agent system
Cursor
并行 sub-agent
Manus
planner/executor
Claude Code /agents
OpenAI Codex /agent 切换
同一招
把任务切片•每片用一个干净的sub-agent 去跑•
只把结果带回主线，过程全部丢掉
那一个新开的 sub-agent
LIANYUN
19/20

## [09:20] frame_0057

19/ 伏笔•2026 大厂共识
@ 炼云 AI
有没有觉得奇怪—
新开一个 sub-agent= 局部的清空重开
// 2026 所有大厂用同一招对抗 context 污染
Anthropic
multi-agent system
| Cursor
并行 sub-agent
Manus|
planner/ executor
claude Code /agents
OpenAI Codex /agent 切换
同一招
把任务切片•每片用一个干净的sub-agent 去跑•
只把结果带回主线，过程全部丢掉
Anthropic的 multi-agent system
LIANYUN
19/20

## [09:30] frame_0058

19/ 伏笔•2026 大厂共识
@ 炼云 AI
有没有觉得奇怪—
新开一个 sub-agent= 局部的清空重开
// 2026 所有大厂用同一招对抗 context 污染
Anthropic
multi-agent system
| Cursor
并行 sub-agent
Manus|
planner/ executor
claude Code /agents
OpenAI Codex /agent 切换
同一招
把任务切片•每片用一个干净的sub-agent 去跑•
只把结果带回主线，过程全部丢掉
OpenAI Codex 的 /agent 切换
LIANYUN
19/20

## [09:40] frame_0059

19/ 伏笔•2026 大厂共识
@ 炼云 AI
有没有觉得奇怪—
新开一个 sub-agent= 局部的清空重开
// 2026 所有大厂用同一招对抗 context 污染
Anthropic multi-agent system
Cursor
并行 sub-agent
Manus
planner/ executor
Claude Code /agents
OpenAI Codex /agent 切换
同一招
把任务切片•每片用一个干净的sub-agent 去跑•
只把结果带回主线，过程全部丢掉
跑完只把结果带回主线过程全部丢掉
LIANYUN
19/20

## [09:50] frame_0060

2日/ 但有个争议•EP3
题眼
@ 炼云 AI
但这件事有个隐藏的争议—
Anthropic 说
Cognition 反驳•文章标题
multi-agent 比单 agent
Don't Build
Multi-Agents
+90%世糖摄升
sub-agent 不是在解决问题•
是在制造问题
同样在做最前沿 agent的两家—完全相反的结论
NEXT•EP3 题眼
为什么2026所有大厂都在做sub-agent—但他们其实在赌两种完全相反的未来
1/ 有想法的评论区聊聊
比单 agent 性能提升 90%
LIANYUN
20 / 20

## [10:00] frame_0061

20/ 但有个争议•EP3 题眼
但这件事有个隐藏的争议—
Anthropic 说
Cognition 反驳• 文章标题
multi-agent 比单 agent
Don't Build
Multi-Agents
+90%性膳提升
sub-agent 不是在解决问题•
是在制造问题
同样在做最前沿 agent的两家—完全相反的结论
NEXT•EP3 题眼
为什么2026所有大厂都在做sub-agent—但他们其实在赌两种完全相反的未来
// 有想法的评论区聊聊
说sub-agent不是在解决问题 是在制造问题
LIANYUN
20/2日

## [10:10] frame_0062

2日/ 但有个争议•EP3 题眼
但这件事有个隐藏的争议—
Anthropic 说
Cognition 反驳•文章标题
multi-agent 比单 agent
Don't Build
MuLti-Agents
+9日%性糖摄升
sub-agent 不是在解决问题•
是在制造问题
同样在做最前沿 agent的两家—完全相反的结论
NEXT• EP3 题眼
为什么2026所有大厂都在做sub-agent—但他们其实在赌两种完全相反的未来
1/ 有想法的评论区聊聊
下期我想聊清楚这件事
LIANYUN
20 / 20
