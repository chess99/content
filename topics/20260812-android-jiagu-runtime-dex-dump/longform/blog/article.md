---
title: 静态反编译只剩 StubApp，我怎样从运行中的 360 加固 APK 抓回业务 DEX
date: 2026-08-12 22:54:51
tags:
  - Android
  - 逆向工程
  - DEX
  - JADX
categories: 技术
pid: 124
permalink: /posts/android-jiagu-runtime-dex-dump/
---

这次研究的样本是 BlockyTime 2.19.28。直接把 APK 丢给 JADX，业务代码几乎没有出现。Manifest 里的 Application 是 `com.stub.StubApp`，包里同时存在四个 ABI 的 `libjiagu`。最终我在 API 34 x86_64 userdebug 模拟器里让应用走到目标页面，从进程内存恢复出多份业务 DEX。合并反编译后共有约 18,027 个 Java 文件，其中 613 个位于应用自身命名空间。

恢复结果没有变回原始工程，JADX 仍报告 215 个错误。它已经足够回答这次复刻最棘手的问题。截图里，左侧时间标签和右侧时间块像一张网格，源码显示它们是两个独立触摸区。左侧 `TimeScrollView` 拖动小时窗口，右侧 `BlockLayout` 拖选时间块。把两者写进同一个手势控件，会得到一个外观接近、用起来完全不同的页面。

<!-- more -->

## 样本和研究边界

样本来自一台已授权测试设备。研究期间只创建合成记录，目标是理解兼容行为与交互状态机，再做独立重写。我没有触碰账号、支付、凭据或用户私有数据，也不会发布 APK、DEX、内存快照和反编译源码。

| 字段 | 值 |
|---|---|
| 包名 | `top.onepix.timeblock` |
| 版本 | `2.19.28` |
| versionCode | `72` |
| APK 大小 | `19,589,546` 字节 |
| SHA-256 | `24236856A84308C97E27838B938769C51EFE38E8B57BE5E95AF8162F0607BAD3` |

## 静态证据只能把问题指向壳

Manifest 中的 Application 为 `com.stub.StubApp`。APK 还带着 `libjiagu.so`、`libjiagu_a64.so`、`libjiagu_x86.so` 和 `libjiagu_x64.so`。常规 JADX 输出只留下壳类和少量工具类，这些特征与 360 加固风格吻合。

到这里可以确定业务代码没有以普通 `classes.dex` 的形式等待反编译。静态证据没有说明它何时解密、从哪里加载，也没有保证运行后一定能找到完整 DEX。下一步仍要靠运行环境验证。

## 从 VDEX 抽出来的还是壳

我先查了应用的 OAT 目录，找到一个 15,203,852 字节的 `runtime-base.vdex`。其中一段 DEX 从偏移 64 开始，头部声明的 `file_size` 为 15,203,540。按头部长度抽取后，文件可以被 JADX 打开，输出却只有约 4 个类和 190 个方法。

这个结果排除了一条看起来很省事的路线。文件大、带合法 DEX 头、能进反编译器，都不能证明业务方法在里面。后面从内存拿到的三份 15,203,540 字节 DEX 也是同一批壳内容。

## 先把运行环境弄对

最初的模拟器使用 Google Play production 镜像。执行 `adb root` 后只得到下面这行回复。

```text
adbd cannot run as root in production builds
```

这不是某个 dump 脚本的兼容问题。继续换脚本也无法获得 `/proc/<pid>/mem` 的读取权限。我随后下载 Google APIs x86_64 的 API 34 userdebug 镜像，校验包的 SHA-1 与官方 XML 一致。新环境显示 `userdebug/dev-keys`，`ro.debuggable=1`，`adb root` 可以把 adbd 提升到 root。

原版 APK 在这个 x86_64 环境里正常安装。通过隐私协议并进入完整记录页后，目标业务已经真实执行，延迟加载的类也有机会进入进程。壳是否支持当前 ABI、应用能否走到目标页面，这两项要在读内存前确认。否则得到一片空白时，很难分清是脚本错了，还是业务代码从未加载。

## 从进程映射里找 DEX

root 环境下可以读取 `/proc/<pid>/maps`，每一行会给出地址范围、权限和映射来源。再按这些地址从 `/proc/<pid>/mem` 读取内容，就能检查 ART 当前持有的内存。

我的第一版脚本很粗暴。它把所有可读映射逐个写到磁盘，最终产生 1077 个文件，总量约 850,788,352 字节。路线因此得到验证，磁盘里也塞满了共享库、堆、字体和大量重复页。扫描时间与误报随之上升。

第二轮会按下面的顺序缩小范围。

1. 先处理路径或名称明确指向 DEX、VDEX、OAT 和 ART 的映射。
2. 再看应用私有目录、壳 so 附近和具有执行权限的匿名区域。
3. 目标页面操作一遍后，对比前后新增或变化的匿名可读映射。
4. 大映射分块读取，块与块之间保留至少一个 DEX 头长度的重叠，避免 magic 或头部跨边界。
5. 只有前面都没有结果时，才扩大到全部可读区域。

本次全量快照已经存在，我便直接在这些文件里找 `dex\n035\0` 和 `dex\n039\0`。magic 只能产生候选，后面还要校验 `header_size`、endian tag 与 `file_size`。最小扫描逻辑可以写成下面这样。

```python
import struct

DEX_MAGIC = (b"dex\n035\0", b"dex\n039\0")

def find_dex(blob):
    for magic in DEX_MAGIC:
        start = 0
        while True:
            offset = blob.find(magic, start)
            if offset < 0:
                break

            file_size, header_size, endian = struct.unpack_from(
                "<III", blob, offset + 0x20
            )

            if (
                header_size == 0x70
                and endian == 0x12345678
                and file_size >= 0x70
                and offset + file_size <= len(blob)
            ):
                yield blob[offset:offset + file_size]

            start = offset + 1
```

这段代码只演示已获授权进程内存快照的头部识别。实用脚本还要处理读取权限、不可读页、跨块边界、校验和、重复 DEX 与损坏头部。本次实际按 DEX signature 和 SHA-256 去重。

## 十一份候选里哪些是业务代码

扫描共切出 11 份文件。里面有重复壳 DEX，也有只有数百或数千字节的极小候选。六份主要文件的规模如下。

| 文件 | 大小 | DEX 版本 | classes | methods |
|---|---|---|---|---|
| dump-000 | 3,851,504 | 039 | 6,248 | 30,654 |
| dump-001 | 4,570,496 | 035 | 3,216 | 28,541 |
| dump-004 | 6,531,532 | 035 | 4,602 | 32,665 |
| dump-005 | 6,694,200 | 035 | 4,987 | 50,196 |
| dump-006 | 7,294,868 | 035 | 5,727 | 50,024 |
| dump-007 | 6,962,644 | 035 | 5,631 | 47,605 |

把这些 DEX 一起交给 JADX 后，输出约 18,027 个 Java 文件。`top.onepix.timeblock` 命名空间下共有 613 个，记录页相关的 `TimeScrollView`、`BlockLayout`、`LineBlockView`、`RecordController` 和 `DayDataHandler` 都能找到。

JADX 的 215 个错误主要说明部分方法无法可靠还原。排查交互时没有必要等到错误清零。类的字段、常量、触摸分支、回调接口与控制器调用能彼此印证，已经可以重建目标状态机。

## 一张网格其实有两个触摸区

复刻版曾遇到一个很直接的问题。手指在时间条上滑动时，控件开始选择时间块，那么用户还怎么拖动时间条。原版没有这种冲突。

恢复出的布局关系给出了答案。

```text
记录页横向触摸区
┌────────────────┬──────────────────────────────┐
│ TimeScrollView │ BlockLayout                  │
│ 左侧时间标签   │ 右侧时间块                   │
│ 纵向拖动       │ 拖动选择                     │
│ 调整 hours     │ 单格双击清除                 │
└────────────────┴──────────────────────────────┘
```

两个 View 从命中区域开始就分开了。手指落在左侧窄栏，事件进入 `TimeScrollView.onTouchEvent`。手指落在右侧网格，事件由 `BlockLayout` 的触摸监听器处理。原版没有在同一片区域里猜测用户想滚动还是想选择。

### 左侧时间栏怎样拖动

`TimeScrollView` 固定绘制 19 行。按下时保存 `downY`，移动时根据当前纵坐标和起点的差更新 offset，再换算 hours。hours 被限制在 1 到 6。松手或收到取消事件后，视图用动画吸附到最近一行，并通过 `hourChanged(hours)` 通知控制器。

它改变的是一天怎样投影到当前 19 行，不直接选择任何时间块。手势状态可以简化为下面这段伪代码。

```kotlin
when (event.actionMasked) {
    DOWN -> downY = event.y
    MOVE -> {
        offset = event.y - downY
        hours = (startHours - offset / itemHeight)
            .toInt()
            .coerceIn(1, 6)
        invalidate()
    }
    UP, CANCEL -> snapToRowAndNotify()
}
```

### 右侧网格怎样选择

`BlockLayout` 同样固定为 19 行，每一行是一个 `LineBlockView`。DOWN 保存起点，并让各行记录手势开始时的选区。MOVE 与 UP 调用 `toggleLineView`，把起点和当前位置转成矩形，再与每行、每格的矩形求交。

拖动跨越多行时，起始行从落点选到行尾，中间行全部覆盖，末行从行首选到终点。`LineBlockView` 用 `tempSelected` 保存初始选区，覆盖过程采用 toggle 语义。手指回拖时，格子能恢复手势开始前的状态，不会只增不减。

同一格连续点击还有单独分支。两次落点命中同一 block，时间间隔满足 40 毫秒到 300 毫秒，组件便调用 `onDoubleClickBlock`。控制器随后清除该块，并把操作加入撤销记录。填充事件后，`updateBlocks` 会调用 `cancelSelect` 清理临时选择。

### 十九行怎样表示二十四小时

`DayDataHandler` 把全天数据投影成 19 行。首行压缩午夜到 hours 之前的时段，中间固定展示从 hours 开始的 17 个小时，末行承接剩余时段。hours 在 1 到 6 之间变化，所以左侧拖动时，首尾压缩范围和右侧每格对应的全天索引都会一起变化。

`LineBlockView` 自己用 Canvas 绘制格子。单元间距为 1 dp，圆角为 4 dp，空块默认色为 `-3355444`。选择覆盖色为 `-7829368`，alpha 为 170，200 毫秒动画从格子中心向外扩散。相邻的同事件块会合并显示，宽度太小时省略文字。

这些常量适合拿来校正像素和动画，触摸分区与索引投影更早决定体验。若只照截图画 19 行，再让一个控件同时处理纵向滚动和块选择，后续怎样调手势阈值都会偏离原版。

## 下一次我会怎样缩短排查

遇到类似样本，我会先记录壳特征、ABI 与静态 DEX 的类数，避免把大文件误认成业务代码。随后准备可控制的 userdebug 环境，让应用走完目标功能，再按显式 DEX 映射、应用私有映射、变化的匿名映射这个顺序读取内存。每个候选都校验 DEX 头和边界，以 signature 去重，然后把多份 DEX 一起交给 JADX。

这条路线也有清楚的失效条件。方法级解密、虚拟化和大规模 native 化可能不会留下可直接切出的完整 DEX。内存快照也不会还原变量名、注释、原始 Kotlin 结构和构建工程。对这次样本而言，读到 `TimeScrollView.onTouchEvent` 与 `BlockLayout.toggleLineView` 已经够了。它们把一次模糊的手感差异变成了两个可以分别实现和测试的触摸状态机。
