---
title: 360 加固 APK 的识别、运行时 DEX 恢复与常见坑
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

一个 APK 的 Manifest 把 Application 指向 `com.stub.StubApp`，JADX 只反编译出 6 个 Java 文件，包内还出现一组 `libjiagu`。静态分析到这里，基本可以判断业务 DEX 被壳接管了。下一步的难点有三个，先确认壳的家族特征，再触发业务代码加载，最后从一堆内存候选中找出能用的 DEX。

本文用一个 Android 14 样本走完这条路线。静态反编译只剩壳，直接从 VDEX 抽出的 15 MB DEX 仍然只有 4 个类。切换到 x86_64 userdebug 环境并读取运行进程后，共找到 11 份 DEX 候选。去掉重复壳和极小文件，再按包名识别业务与依赖，JADX 最终生成约 18,027 个 Java 文件，目标应用目录下有 613 个。

这套方法适用于业务代码会以标准 DEX 形态进入 ART 的样本。方法级解密、DEX 虚拟化和大规模 native 化可能不会留下可直接切出的完整文件，文末会单独说明边界。

<!-- more -->

```text
APK 静态信号
    ↓
确认壳家族与 ABI
    ↓
userdebug 环境触发代码加载
    ↓
/proc/<pid>/maps 定位可读映射
    ↓
/proc/<pid>/mem 扫描并按 file_size 回读
    ↓
头部校验与内容哈希去重
    ↓
class descriptor 分类
    ↓
JADX 与 smali 抽查恢复质量
```

## 先确认 APK 是否加壳

判断不能只看 JADX 有没有报错。正常 APK 也可能经过混淆，类名会变短，控制流会变难读，但 Manifest 组件、业务包和大量方法通常还在。壳接管入口后，常见现象是外层 DEX 很大，实际类数却极少，Application 也被替换为壳入口。

这个样本有四组相互印证的信号。

1. Manifest 中的 Application 为 `com.stub.StubApp`。
2. APK 内包含 `libjiagu.so`、`libjiagu_a64.so`、`libjiagu_x86.so` 和 `libjiagu_x64.so`。
3. 常规 JADX 输出只有 6 个 Java 文件，目标业务包没有展开。
4. 外层 DEX 后续统计只有 4 个 class definition 和 190 个 method ID，与 19.6 MB 的 APK 规模明显不相称。

`StubApp` 与 `libjiagu_*` 的组合符合 360 加固家族的常见特征，因此本文称它为 360 加固风格样本。仅靠这些文件名无法断定服务版本、加固选项和壳的具体构建号。需要精确识别时，还应继续比对 so 导出、字符串、壳入口实现与已知样本指纹。

静态分析仍然值得做。它可以确认包名、版本、组件、权限、资源、壳入口和支持的 ABI。尤其要把 `lib/<abi>/` 看清楚。动态环境的架构不在壳支持范围内时，应用可能安装成功却无法完成解密，后面的内存扫描自然也拿不到目标代码。

本次样本的基本信息如下。

| 字段 | 值 |
|---|---|
| 包名 | `top.onepix.timeblock` |
| 版本 | `2.19.28` |
| versionCode | `72` |
| APK 大小 | `19,589,546` 字节 |
| SHA-256 | `24236856A84308C97E27838B938769C51EFE38E8B57BE5E95AF8162F0607BAD3` |

记录样本哈希很重要。壳厂商、应用版本或渠道包只要变化，入口、so、加载时机和内存布局都可能跟着变化。没有哈希，后续复现实验时很容易把不同 APK 当成同一个样本。

## 合法 DEX 不等于业务 DEX

静态路线里最容易误判的是 OAT 与 VDEX。这个样本安装后在应用 OAT 目录生成了 `runtime-base.vdex`，大小为 15,203,852 字节。从偏移 64 处能读到合法 DEX 头，头部声明的 `file_size` 为 15,203,540。按这个长度截取后，JADX 也能正常打开。

结果只有 4 个 class definition 和 190 个 method ID，命名空间集中在 `com.stub` 与 `com.tianyu`。它仍然是壳。这里的 method ID 包含当前 DEX 定义的方法及其引用的外部方法，不能当成方法实现数量。

这一步给出了一个很实用的判断。DEX magic、合法头部、很大的文件体积和反编译器能打开，只能证明文件格式成立。判断业务代码是否已经恢复，还要继续看下面几项。

- `class_defs_size` 与 `method_ids_size` 是否匹配应用规模
- 目标包名是否出现在 type descriptor 与字符串池中
- Manifest 组件对应的类能否找到
- 是否出现 Activity、Fragment、Controller、Model 等业务层次
- 关键资源名、接口路径或领域词是否能与应用行为对应

如果 DEX 有十几 MB，`class_defs_size` 却只有个位数，优先把它看成壳、填充文件或特殊容器，不要因为体积大就给它贴上业务 DEX 的标签。

## 动态环境先解决权限和 ABI

第一套实验环境使用 API 34 x86_64 Google Play production 镜像。执行 `adb root` 后，adbd 直接拒绝提权。

```text
adbd cannot run as root in production builds
```

这类镜像适合接近普通用户设备的行为测试，不适合直接读取其他进程的 `/proc/<pid>/mem`。换 Frida 脚本或调整 ADB 参数不会改变 adbd 的构建属性。

后来换成 Google APIs x86_64 userdebug 镜像，镜像包的 SHA-1 与官方仓库 XML 一致。启动后可以用下面几条命令确认环境。

```bash
adb root
adb shell id
adb shell getprop ro.build.type
adb shell getprop ro.debuggable
adb shell getprop ro.product.cpu.abi
```

本次环境返回 root、`userdebug`、`ro.debuggable=1` 和 `x86_64`。APK 中正好包含 x86 与 x86_64 对应的 `libjiagu`，应用能够通过启动流程并进入主要页面。

应用能启动还不够。很多壳会按需加载代码，应用自己的动态模块也可能延迟初始化。dump 前应当把准备研究的页面和功能实际操作一遍，再通过 `pidof` 确认目标进程仍在运行。如果应用有独立进程，还要检查 Manifest 中的 `android:process`，避免只盯着主进程。

## 从 maps 找范围，再从 mem 取内容

目标进程启动后，先拿 PID 和内存映射。

```bash
PACKAGE=top.onepix.timeblock
PID=$(adb shell pidof "$PACKAGE")
adb shell "cat /proc/$PID/maps" > maps.txt
```

`maps` 每行包含地址范围、读写执行权限、文件偏移和映射来源。一个典型范围类似下面这样。

```text
70000000-70400000 r--p 00000000 00:00 0
```

地址区间换算出起点和长度后，可以从 `/proc/<pid>/mem` 按范围读取。实验脚本需要跳过没有读权限的区域，同时限制单次读取大小。直接让 `dd` 把超大映射一次拉完，容易遇到读取失败、磁盘膨胀和后续扫描过慢。

本次第一版脚本把所有可读、大小在 0x70 到 64 MB 之间的映射都转储了。最终得到超过 1000 个文件，总量约 811 MiB。DEX 确实在里面，噪声也很可观，字体、共享库、堆页和重复映射占了绝大部分。

更合适的扫描顺序如下。

1. 优先处理路径或名称指向 `.dex`、`.vdex`、`.oat` 与 ART 的映射。
2. 检查应用私有目录和壳 so 附近的映射。
3. 在进入目标功能前后各保存一份 `maps`，关注新增或尺寸发生变化的匿名可读区。
4. 对大范围分块扫描，相邻窗口保留至少 0x70 字节重叠。命中合法头后，按 `file_size` 从候选虚拟地址重新读取完整 DEX。
5. 前面没有结果时，再扩大到全部可读映射。

匿名映射不能直接排除。壳可能把解密结果放进匿名内存，再通过 ART 接口加载。只扫描带 `.dex` 路径的行虽然省事，也可能恰好漏掉需要的那一份。

## DEX magic 之后还要校验头部

标准 DEX 头以 `dex\n035\0`、`dex\n039\0` 等 magic 开始。不同 Android 版本还会出现其他三位版本号，扫描器不应只写死本次样本里的 035 和 039。找到候选 magic 后，至少还要读取三个字段。

| 偏移 | 字段 | 本次校验 |
|---|---|---|
| `0x20` | `file_size` | 不小于 `0x70`，且切片不越界 |
| `0x24` | `header_size` | 等于 `0x70` |
| `0x28` | `endian_tag` | 等于 `0x12345678` |

下面的 Python 脚本直接读取已授权测试进程。它按 `maps` 中的可读范围分块扫描，发现合法头后再从原虚拟地址回读 `file_size` 指定的完整候选。运行前需要执行 `adb root`，并把应用操作到需要分析的功能。

```python
import hashlib
import re
import struct
import subprocess
import sys
from pathlib import Path

MAP_LINE = re.compile(
    r"^([0-9a-f]+)-([0-9a-f]+)\s+([r-][w-][x-][ps])\s+"
)
DEX_MAGIC = re.compile(rb"dex\n[0-9]{3}\x00")
CHUNK_SIZE = 8 * 1024 * 1024
MAX_DEX_SIZE = 256 * 1024 * 1024


def adb(serial, *args, binary=False, check=True):
    target = ["-s", serial] if serial else []
    result = subprocess.run(
        ["adb", *target, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )
    return result.stdout if binary else result.stdout.decode().strip()


def read_memory(serial, pid, address, size):
    command = (
        f"dd if=/proc/{pid}/mem bs=4096 "
        f"iflag=skip_bytes,count_bytes skip={address} count={size} "
        "2>/dev/null"
    )
    data = adb(
        serial, "exec-out", command, binary=True, check=False
    )
    return data if len(data) == size else None


def main(package, serial=None):
    if not re.fullmatch(r"[A-Za-z0-9_.]+", package):
        raise ValueError("invalid package name")

    pid_text = adb(serial, "shell", "pidof", package)
    if not pid_text:
        raise RuntimeError("target process is not running")
    pid = pid_text.split()[0]

    maps_text = adb(serial, "shell", f"cat /proc/{pid}/maps")
    Path("maps.txt").write_text(maps_text, encoding="utf-8")
    output_dir = Path("dex")
    output_dir.mkdir(exist_ok=True)

    seen_addresses = set()
    seen_hashes = set()

    for line in maps_text.splitlines():
        match = MAP_LINE.match(line)
        if not match or not match.group(3).startswith("r"):
            continue

        map_start = int(match.group(1), 16)
        map_end = int(match.group(2), 16)
        window_start = map_start

        while window_start < map_end:
            window_size = min(
                CHUNK_SIZE + 0x70, map_end - window_start
            )
            blob = read_memory(
                serial, pid, window_start, window_size
            )
            if blob is None:
                window_start += CHUNK_SIZE
                continue

            for magic in DEX_MAGIC.finditer(blob):
                address = window_start + magic.start()
                if address in seen_addresses:
                    continue
                seen_addresses.add(address)

                if magic.start() + 0x70 > len(blob):
                    continue
                file_size, header_size, endian = struct.unpack_from(
                    "<III", blob, magic.start() + 0x20
                )
                if not (
                    0x70 <= file_size <= MAX_DEX_SIZE
                    and header_size == 0x70
                    and endian == 0x12345678
                ):
                    continue

                dex = read_memory(serial, pid, address, file_size)
                if dex is None:
                    continue
                digest = hashlib.sha256(dex).hexdigest()
                if digest in seen_hashes:
                    continue
                seen_hashes.add(digest)
                output_dir.joinpath(f"{digest}.dex").write_bytes(dex)

            window_start += CHUNK_SIZE


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
```

保存为 `dump_runtime_dex.py`。只有一台 ADB 设备时，通过 `python dump_runtime_dex.py top.onepix.timeblock` 运行。多台设备同时连接时，再传入 serial，例如 `python dump_runtime_dex.py top.onepix.timeblock emulator-5554`。脚本会保存 `maps.txt`，并把按 SHA-256 命名的候选写进 `dex` 目录。

这仍是一份最小实现。它假设完整 DEX 可以从候选起始地址连续读取，也没有处理 DEX checksum 与 signature 修复、跨映射候选、CompactDex 和被壳改写的头部。校验失败不能立即说明候选无用，有些壳会故意破坏头字段。这时可以结合 map 范围、ART 对象和修复工具继续判断。

本次最初按 DEX header 内的 20 字节 signature 去重，最终仍切出三份内容完全相同的壳 DEX。进一步计算整文件 SHA-256 后，三份文件的哈希一致。原因很简单，去重表只在单轮扫描中生效，后续重复执行脚本时又生成了新编号。稳定工具应扫描现有输出并使用内容哈希做幂等去重。

## 十一份候选怎样分类

这次内存扫描得到 11 份候选。单看文件大小，很容易把六份 3.8 MB 到 7.3 MB 的 DEX 全部叫作业务 DEX。解析 `class_defs` 的 type descriptor 后，结构清楚得多。

| 文件 | 大小 | class defs | method IDs | 主要内容 |
|---|---|---|---|---|
| dump-000 | 3,851,504 | 6,248 | 30,654 | Chromium、Google、AndroidX |
| dump-001 | 4,570,496 | 3,216 | 28,541 | 百度与组件代码 |
| dump-004 | 6,531,532 | 4,602 | 32,665 | 目标包主体、Kotlin、OkHttp |
| dump-005 | 6,694,200 | 4,987 | 50,196 | Google、Jackson、Glide、百度、阿里 |
| dump-006 | 7,294,868 | 5,727 | 50,024 | Kotlin、华为、小米、Mob、腾讯 |
| dump-007 | 6,962,644 | 5,631 | 47,605 | AndroidX、Paging、Navigation、Fly |

`dump-004` 的 4602 个 class definition 中，有 2575 个位于 `top/onepix` 命名空间。其余大 DEX 没有目标包类定义，主要是框架和第三方 SDK。三份 15,203,540 字节文件的 SHA-256 完全相同，每份都只有 4 个 class definition 和 190 个 method ID，可以归为重复壳 DEX。另有 284 字节与 3580 字节的极小 DEX，class definition 数分别为 1 和 3。

分类时可以直接解析 DEX，也可以先用 JADX、`dexdump` 或字符串搜索粗筛。最可靠的依据仍是 type descriptor，因为业务包名可能只以普通字符串形式出现在某个 SDK 里，单次文本命中会造成误判。

目标包的 DEX 也可能同时带着 Kotlin 标准库、协程或网络库，不能要求一个文件只出现业务命名空间。判断重点是目标包的 class definition 是否成规模，Manifest 组件能否对应上，以及包内是否形成可理解的结构。

本次把有效 DEX 一起交给 JADX 后，输出约 18,027 个 Java 文件。目标目录下有 613 个 Java 文件，主要分布如下。

| 目录 | Java 文件数 |
|---|---|
| `fragments` | 220 |
| `models` | 106 |
| `activities` | 105 |
| `views` | 78 |
| `utils` | 63 |
| `network` | 18 |

DEX 中目标命名空间有 2575 个 class definition，JADX 只生成 613 个目标目录 Java 文件，两者没有矛盾。前者会计算内部类、匿名类、合成类和 Kotlin 编译产物，后者经常把这些定义合并进顶级源码文件。

JADX 最终报告 215 个反编译错误。这不代表整批 dump 无效。审查恢复质量时，可以分三层看。

- 类名、字段、继承关系、注解和字符串通常最先恢复
- 方法签名、调用关系与普通控制流可以抽样核验
- 报错方法、复杂协程状态机和反编译器标出的 bad code 需要回到 smali 或其他反编译器交叉检查

若目标只是确认架构、组件关系或定位一段逻辑，部分方法报错往往可以接受。若要修改后重打包，每个相关方法都要继续下钻，不能把 JADX 生成的 Java 当作可直接编译的原始源码。

## 常见失败怎样定位

### JADX 只剩几个壳类

先比较 APK 大小、DEX 类数与目标包是否存在，再检查 Manifest Application 和 native 库。确认加壳后停止在静态 Java 里硬找业务方法，把精力转到加载时机和运行环境。

### VDEX 很大，反编译内容却很少

读取 DEX header 中的 class 与 method 数量，并检查目标 type descriptor。体积只能说明容器大，不能说明业务代码多。

### 内存里搜不到 DEX magic

依次检查 ABI、应用是否完整启动、目标功能是否触发、PID 是否正确、是否存在独立进程、读取范围是否过窄。上述条件成立后仍没有结果，再考虑头部被抹除、compact dex、方法级解密、虚拟化或 native 化。

### 找到很多 DEX，不知道哪份有用

先按整文件哈希去重，再统计 `class_defs_size`、`method_ids_size` 和前两级包名。目标包成规模出现的文件优先，依赖 DEX 留着一起反编译，重复壳与极小空文件单独归档。

### JADX 报错很多

不要只看错误总数。先抽查目标包中的 Manifest 组件、控制器、模型和一个关键调用链。Java 无法还原的方法回到 smali，必要时用其他工具交叉反编译。错误集中在第三方依赖时，对业务分析的影响可能很小。

## 一份可以复用的操作清单

拿到新的 APK 后，可以按下面的顺序排查。

1. 计算 APK 哈希，记录包名、版本、渠道和文件大小。
2. 解出 Manifest，检查 Application、组件和独立进程。
3. 列出 `lib/<abi>/`，比对壳特征与计划使用的运行架构。
4. 统计外层 DEX 的 class definition、method ID 与目标包，区分混淆和壳接管。
5. 安装到可控环境，验证 root、build type、debuggable 与 ABI。
6. 启动应用并实际触发目标功能，重新确认所有相关 PID。
7. 保存 `/proc/<pid>/maps`，按显式 DEX、应用私有映射、变化的匿名映射逐步扩大范围。
8. 从 `/proc/<pid>/mem` 分块扫描，命中头部后按 `file_size` 回读完整候选。
9. 扫描 DEX magic，校验头部与边界，使用整文件哈希去重。
10. 解析 class descriptor，区分壳、业务、框架和第三方 SDK。
11. 联合反编译所有相关 DEX，抽查组件、调用关系与 smali。
12. 记录没有恢复的部分，判断是否存在延迟加载、头部破坏、方法级解密或虚拟化。

这份样本最终停在标准 DEX 恢复阶段，业务包、组件层、数据层和依赖关系都已经出现。遇到同时带有 `StubApp`、`libjiagu_*` 等特征，并且业务代码以标准 DEX 进入 ART 的样本时，可以把这套顺序作为排查起点。壳文件名给出方向，运行时内存给出候选，DEX 结构和包分布负责确认结果。
