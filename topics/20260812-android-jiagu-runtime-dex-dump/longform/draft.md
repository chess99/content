# 静态反编译只剩 StubApp，我怎样从运行中的 360 加固 APK 抓回业务 DEX

这次研究的样本是 BlockyTime 2.19.28。直接把 APK 丢给 JADX，业务代码几乎没有出现。Manifest 里的 Application 是 `com.stub.StubApp`，包里同时存在四个 ABI 的 `libjiagu`。最终我在 API 34 x86_64 userdebug 模拟器里让应用走到目标页面，从进程内存恢复出多份业务 DEX。合并反编译后共有约 18,027 个 Java 文件，其中 613 个位于应用自身命名空间。

真正解决复刻问题的是几份记录页代码。截图里，左侧时间标签和右侧时间块像一张网格。源码显示它们是两个独立触摸区。左侧 `TimeScrollView` 拖动小时窗口，右侧 `BlockLayout` 拖选时间块。把两者写进同一个手势控件，会得到一个看起来接近、用起来完全不同的页面。

## 静态证据只能把问题指向壳

样本包名为 `top.onepix.timeblock`，版本号为 2.19.28，versionCode 为 72。APK 大小 19,589,546 字节，SHA-256 为 `24236856A84308C97E27838B938769C51EFE38E8B57BE5E95AF8162F0607BAD3`。

Manifest 和 `libjiagu.so` 等文件足以说明壳的风格。JADX 只输出壳类也符合预期。它们没有说明业务代码在哪个阶段、以什么形式进入 ART。

## 从 VDEX 抽出来的还是壳

应用 OAT 目录里有一个 15,203,852 字节的 `runtime-base.vdex`。内嵌 DEX 位于偏移 64，头部记录的文件大小是 15,203,540 字节。直接截取再反编译，结果只有约 4 个类和 190 个方法。

这个结果排除了一个诱人的捷径。大文件可能只是壳放进去的容器或占位内容，能被 JADX 打开也不能证明其中有业务方法。

## 可调试环境比工具名字重要

最初使用 Google Play production 镜像，`adb root` 明确拒绝。换成 SHA-1 与官方 XML 一致的 Google APIs x86_64 userdebug 镜像后，`ro.debuggable=1`，`adb root` 成功。原 APK 也能正常安装、通过隐私协议并进入记录页。

到这一步，进程已经实际执行了目标功能。读取 `/proc/<pid>/maps` 可以得到内存区域，再通过 `/proc/<pid>/mem` 取回映射内容。

第一次实现把所有可读映射都写到磁盘，产生 1077 个文件和约 850,788,352 字节数据。扫描有效，却很浪费。后续应先筛选 ART、DEX、匿名可执行区和应用私有映射，再分块查找候选头。

## DEX magic 后面还有三道检查

扫描器查找 `dex\n035\0` 与 `dex\n039\0`，再检查 `header_size`、endian tag 和 `file_size`。通过边界检查后切片，最后用 signature 或 SHA-256 去重。

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

这段示例只描述已获授权进程内存快照的头部识别。实用脚本还要处理不可读映射、跨块边界、校验和、重复 DEX 和部分损坏的头部。

本次得到 11 份候选。三份 15,203,540 字节的文件是重复壳 DEX，只有 4 个类和 190 个方法。六份主要业务 DEX 的大小在 3.8 MB 到 7.3 MB 之间。把它们一起交给 JADX，虽然出现 215 个反编译错误，记录页控制器和自定义 View 已经能读。

## 源码把一个交互误判讲清楚了

`TimeScrollView` 固定绘制 19 行。按下时记录纵坐标，移动时用位移调整 offset 与 hours，并把 hours 限制在 1 到 6。松手后它会吸附到最近一行，并通过 `hourChanged` 通知控制器。它只负责左侧时间窗口。

`BlockLayout` 位于右侧，同样固定 19 行，每行是一个 `LineBlockView`。按下时保存起点和原选区，移动时用矩形相交刷新覆盖范围。跨越多行时，首行选到末尾，中间行全选，末行从开头选到终点。

`LineBlockView` 保存 `tempSelected`，拖动采用 toggle 语义。两次点击位于同一格，间隔在 40 到 300 毫秒之间，还会触发双击清除。选择覆盖有 200 毫秒的中心扩散动画，单元间距为 1 dp，圆角为 4 dp。

`DayDataHandler` 解释了 19 行怎样映射全天。首行压缩午夜到 hours 之前的数据，中间固定展示 17 小时，末行承接余下小时。视觉网格只是投影，选择结果还要映射回全天底层 block。

```text
记录页
├─ 左侧 TimeScrollView
│  └─ 纵向拖动调整 hours
└─ 右侧 BlockLayout
   ├─ 19 个 LineBlockView
   ├─ 拖动选择与反选
   └─ 双击清除
```

黑盒观察能记录手势结果，很难稳定推断触摸分区、选择快照和索引映射。运行时代码提供了可以逐项复现的状态机。

## 以后再遇到类似样本

先确认壳特征和目标 ABI，再准备能控制进程的环境。应用必须走到目标功能，延迟加载的业务代码才有机会进入内存。扫描时先看显式 DEX 映射，再看匿名区。命中 magic 只是候选，头部、边界和去重缺一不可。JADX 有错误时也先搜索目标包名和业务名，关键状态机可能已经足够完整。

内存 dump 不能还原原始工程。变量名、内联结构、部分泛型和控制流会丢失，native 化或虚拟化方案还会让这条路线失效。本次研究也没有覆盖账号、支付、服务端协议和真实用户数据，恢复出的代码只用于理解兼容行为和独立重写。

这次最有用的产物不是某个万能脚本。真正起作用的是一段连续证据。静态文件确认壳，userdebug 环境让目标功能真实运行，内存映射给出 DEX，业务类再把手势冲突定位到两个独立 View。下一次遇到 StubApp，我会先沿这条证据链查下去。
