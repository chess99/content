# BlockyTime 动态拆壳研究记录

## 研究目的

为独立重写 BlockyTime 的核心记录页补足静态反编译拿不到的业务状态机。研究对象运行在已授权的测试设备与本地模拟器中，只创建合成记录，不触碰账号、支付、凭据或用户私有数据。

## 样本信息

| 字段 | 值 |
|---|---|
| 包名 | `top.onepix.timeblock` |
| 版本 | `2.19.28` |
| versionCode | `72` |
| 文件大小 | `19,589,546` 字节 |
| SHA-256 | `24236856A84308C97E27838B938769C51EFE38E8B57BE5E95AF8162F0607BAD3` |

静态证据包括 Manifest 中的 `com.stub.StubApp`，以及 APK 内的 `libjiagu.so`、`libjiagu_a64.so`、`libjiagu_x86.so`、`libjiagu_x64.so`。常规 JADX 输出只剩壳类和少量工具类，特征符合 360 加固风格。

## 动态环境

- 第一套环境为 API 34 x86_64 Google Play production 镜像，`adb root` 返回 `adbd cannot run as root in production builds`。
- 后来使用官方 Google APIs x86_64 userdebug 镜像，下载包为 `x86_64-34_r14.zip`，SHA-1 与官方 XML 一致。
- 新镜像显示 `userdebug/dev-keys`，`ro.debuggable=1`，`adb root` 成功。
- 原 APK 在 x86_64 环境安装并进入完整记录页，说明壳与业务代码都能在该架构运行。

## 失败路线与转折

### VDEX 仍然是壳

应用的 OAT 目录中存在 `runtime-base.vdex`，大小为 `15,203,852` 字节。内嵌 DEX 从偏移 `64` 开始，头部声明的 `file_size` 为 `15,203,540`。抽取后再次交给 JADX，仍只有约 4 个类和 190 个方法。文件很大不能证明业务代码已经落在显式 DEX 中。

### 全量转储噪声过大

第一次读取 `/proc/<pid>/maps` 后，把所有可读映射逐个从 `/proc/<pid>/mem` 写到磁盘。结果得到 1077 个文件，总量约 `850,788,352` 字节。它帮助验证了路线，却不适合作为稳定工具。后续应优先筛选与 ART、DEX、匿名可执行区及应用私有映射相关的区域，再按块扫描。

## DEX 扫描方法

候选文件同时检查以下条件。

- magic 为 `dex\n035\0` 或 `dex\n039\0`
- `header_size` 等于 `0x70`
- endian tag 等于 `0x12345678`
- `file_size` 大于头部且没有越过当前内存快照
- 使用 DEX signature 或 SHA-256 去重

实际得到 11 份文件，其中有三份重复的大型壳 DEX，也有极小候选。六份体积较大的有效 DEX 统计如下。它们不能统称为业务 DEX，按 class descriptor 统计后，只有 `dump-004` 包含目标包主体，其余主要承载框架与第三方依赖。

| 文件 | 大小 | DEX 版本 | class defs | method IDs |
|---|---:|---:|---:|---:|
| dump-000 | 3,851,504 | 039 | 6,248 | 30,654 |
| dump-001 | 4,570,496 | 035 | 3,216 | 28,541 |
| dump-004 | 6,531,532 | 035 | 4,602 | 32,665 |
| dump-005 | 6,694,200 | 035 | 4,987 | 50,196 |
| dump-006 | 7,294,868 | 035 | 5,727 | 50,024 |
| dump-007 | 6,962,644 | 035 | 5,631 | 47,605 |

按前两级包名统计 class descriptor 后，主要结果如下。

| 文件 | 目标包类定义 | 主要命名空间 |
|---|---:|---|
| dump-000 | 0 | `org/chromium`、`com/google`、AndroidX |
| dump-001 | 0 | `com/baidu`、`com/component`、`com/style` |
| dump-004 | 2,575 | `top/onepix`、Kotlin 协程、Kotlin 反射、OkHttp |
| dump-005 | 0 | Google、Jackson、Glide、百度、阿里、支付宝 |
| dump-006 | 0 | Kotlin 反射、华为、小米、Mob、腾讯 |
| dump-007 | 0 | AndroidX、Fly、Paging、Navigation |

这里的 2,575 是 DEX `class_defs` 中目标命名空间的数量，包含内部类、合成类及其他不会逐一生成顶级 Java 文件的定义。JADX 最终在 `top.onepix.timeblock` 目录生成 613 个 Java 文件，两种统计口径不应混用。

所有 dump 一起输入 JADX 后生成约 18,027 个 Java 文件，`top.onepix.timeblock` 命名空间下有 613 个。JADX 报 215 个错误，核心记录页的类仍可阅读。表中的 method ID 来自 DEX `method_ids_size`，包含方法定义及外部方法引用，不代表方法实现数量。

## 核心业务证据

### TimeScrollView

- 左侧时间标签是独立 View。
- `ACTION_DOWN` 记录纵坐标。
- `ACTION_MOVE` 用位移更新 offset 和 hours，hours 被限制在 1 到 6。
- `ACTION_UP` 和 `ACTION_CANCEL` 对齐到最近一行，再调用 `hourChanged(hours)`。
- 视图固定绘制 19 行，首尾两行承担压缩时段。

### BlockLayout

- 右侧网格是另一个 View，内部固定 19 个 `LineBlockView`。
- DOWN 保存起点并把当前选区交给每一行。
- MOVE 与 UP 都会通过矩形相交刷新选择。
- 跨行拖动时，起始行选到行尾，中间行全选，末行从行首选到终点。
- 选择采用 toggle 语义，`tempSelected` 保存手势开始前的状态。
- 同一格两次点击间隔在 40 到 300 毫秒内会触发双击回调。

### LineBlockView 与 DayDataHandler

- 单元间距为 1 dp，圆角为 4 dp。
- 空块默认色为 `-3355444`，选择覆盖色为 `-7829368`，覆盖 alpha 为 170。
- 选择动画持续 200 毫秒，从单元中心扩散。
- `DayDataHandler` 将全天底层数据投影为 19 行。首行压缩午夜到 hours 之前的时段，中间显示 17 个小时，末行承接剩余时段。
- hours 在 1 到 6 之间变化，界面上的选中索引会映射回全天底层 block 索引。

## 对复刻工作的直接结论

记录页在视觉上像一张完整时间网格，触摸区实际分成左右两个 View。左侧纵向拖动只调整可视时间窗口，右侧拖动只负责选择时间块。若复刻版把整行交给一个选择控件，滚动和选择必然争夺同一手势，无法还原原版体验。

## 局限

- 内存 DEX 恢复不等于得到原始工程，变量名、泛型、内联结构和部分控制流会丢失。
- 本次没有覆盖 native 业务逻辑、资源混淆还原或服务端行为。
- 更强的虚拟化、方法级解密或 native 化方案可能无法用同一路线处理。
- 临时目录内的 APK、内存快照、DEX 与反编译产物不进入内容仓库，也不公开分发。
