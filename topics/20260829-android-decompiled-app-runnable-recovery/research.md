# 素材清单 DEX 拆出来以后怎样恢复成可运行 Android 工程

## 支撑单元一 上一篇结束时已经拿到了什么

### 支撑素材

- 上一篇公开文章记录了样本信息、运行时 DEX 获取方法和分类结果。样本为 BlockyTime 2.19.28，原包名 `top.onepix.timeblock`，versionCode 72，APK SHA-256 为 `24236856A84308C97E27838B938769C51EFE38E8B57BE5E95AF8162F0607BAD3`。来源 https://blog.cearl.cc/posts/android-jiagu-runtime-dex-dump/
- 动态扫描得到 11 份候选，其中 6 份为后续联合反编译使用的相关 DEX。JADX 总输出约 18,027 个 Java 文件，目标包目录有 613 个 Java 文件。`class definition` 与 Java 文件数口径不同，不能混写。来源为上一篇文章与 `D:\code\BlockyTime-Recovered\docs\RECOVERY.md`。
- 第一阶段仓库提交为 `8d16f4d chore: 整理 BlockyTime 动态恢复源码与研究工程`。该阶段把反编译结果放入只读 `recovered/`，另建小型 `app/` 验证时间网格手势，没有把恢复快照写成“可构建原工程”。

---

## 支撑单元二 为什么恢复快照不能直接构建

### 支撑素材

- 旧版 `docs/BUILD_STATUS.md` 记录了第一次把恢复输出临时组装为 Android 模块的结果。AAPT2 首先在 8 个 `.9.png` 上失败，文件名带 `abc_list_divider_mtrl_alpha` 和 `abc_textfield_*`，可识别为公共 UI 依赖资源。来源命令 `git -C D:\code\BlockyTime-Recovered show 8d16f4d:docs/BUILD_STATUS.md`。
- APK 中包含应用资源和依赖资源的合并结果。Android 官方资源文档说明构建会合并 main source set、build variant 与 library dependency 中的资源。来源 https://developer.android.com/studio/write/add-resources#resource_merging
- AAR 会携带 manifest、classes.jar、resources、assets 和 native libraries 等 Android 构建输入。能确认坐标的公共依赖应优先恢复为 AAR，而非编译其反编译副本。来源 https://developer.android.com/studio/projects/android-library
- 本次处理没有宣称精确找回原 Gradle 配置。`legacy-app/build.gradle.kts` 选择了一组能与反编译调用和资源共同工作的兼容版本，其中包含 Kotlin、AndroidX、Material、Room、Navigation、Paging、OkHttp、Jackson、图表、二维码、图片裁剪、支付和推送 SDK。
- 编译阶段排除了目标包中旧的数值 `R$*.java`。资源 ID 由本次 Android Gradle Plugin 重新生成，反编译得到的旧 R 常量不能继续充当新工程的资源索引。来源 `D:\code\BlockyTime-Recovered\legacy-app\build.gradle.kts`。

---

## 支撑单元三 依赖和资源应该怎样分层

### 支撑素材

- 仓库采用三层结构。`recovered/` 保持原样，`legacy-app/` 承担可运行化修改，`app/` 保存早期手势实验。这样可以随时比较“反编译证据”和“为编译运行作出的修复”，不会在第一次修语法时覆盖证据。来源 `D:\code\BlockyTime-Recovered\README.md`。
- 公共 AndroidX、Kotlin 与可识别 SDK 交给 Maven/AAR。目标应用自己的业务代码、布局、图片和无法从公共坐标重建的小型库保留在 `legacy-app`。推送、广告和一键登录等依赖服务端与凭据的外围代码通过独立离线兼容层隔离。来源 `legacy-app/build.gradle.kts` 与 `legacy-app/src/main/java/recovered/offline/`。
- 当前离线兼容层包含广告、推送、一键登录、Kotlin 合成调用和协程桥接。它的目标是让账号和厂商能力不阻塞离线核心链路，不伪装线上能力已经恢复。
- `RecoveredCoroutines` 处理了 Java 源码无法直接调用 Kotlin synthetic 默认参数桥的问题，并为少量恢复出的 suspend API 提供有超时的 continuation 等待。来源 `legacy-app/src/main/java/recovered/offline/coroutines/RecoveredCoroutines.java`。

---

## 支撑单元四 启动入口和包名隔离

### 支撑素材

- 原 Manifest 的 Application 指向 `com.stub.StubApp`。恢复工程将其改为业务代码里的 `top.onepix.timeblock.MainApplication`，主入口仍为 `SplashActivity`。来源 `recovered/src/main/AndroidManifest.xml` 与 `legacy-app/src/main/AndroidManifest.xml` 对比。
- `MainApplication.onCreate` 中能看到数据库、皮肤、通知、语言、网络和自动记录服务等真实初始化顺序。壳入口退出以后，这段业务 Application 才能成为进程初始化入口。来源 `legacy-app/src/main/java/top/onepix/timeblock/MainApplication.java`。
- 恢复工程使用 `top.onepix.timeblock.recovered` 作为 applicationId，显示名为 `BlockyTime Recovered`。自定义权限和 FileProvider authority 也按恢复包名隔离，允许与原应用并存比较。来源 `D:\code\BlockyTime-Recovered\README.md` 与 `docs/BUILD_STATUS.md`。
- Android 官方文档区分 namespace 与 applicationId，并说明 applicationId 是设备和商店识别应用的唯一标识。来源 https://developer.android.com/build/configure-app-module#set-application-id
- Manifest placeholder 可以注入 applicationId 等构建变量，适合处理 FileProvider authority 与自定义权限。来源 https://developer.android.com/build/manage-manifests#inject_build_variables_into_the_manifest

---

## 支撑单元五 编译错误暴露出的反编译缺口

### 支撑素材

- 恢复快照中有 9 个业务文件、17 个 `Method not decompiled` 方法。涉及统计、打卡、周月年总结、旧数据迁移和 Excel 导出。当前 `legacy-app` 已全部补回。清单来源 `D:\code\BlockyTime-Recovered\docs\DECOMPILATION_GAPS.md`。
- 富文本编辑器另有 4 个复杂方法需要从运行时 DEX、CFR 输出和字节码恢复，分别是复制、粘贴、模板导入和模板 JSON 导出。它们随后通过输入文字、复制、清空、粘贴、退出保存做了真实回归。
- 搜索 `Method not decompiled` 仍不足以判断完整度。当前源码中还有 56 个外围 Activity 的 `onCreate` 保留为 `native` 声明。核心离线路径手工恢复了 5 个入口，分别覆盖打卡统计、目标详情、事件统计、标记统计和总结编辑。
- 恢复入口时可以利用同类页面的初始化顺序、字段、`layout(context)`、`initData`、`initViews`、`initEvents` 以及原应用黑盒行为。5 个已恢复入口都遵循已有方法之间的依赖顺序，没有凭空重写整页。
- 本轮没有把剩余 56 个入口全部填成空页面。进入未恢复页面仍会失败，文档明确保留这一边界。

---

## 支撑单元六 原应用怎样充当行为参照

### 支撑素材

- 早期复刻曾把左侧时间刻度和右侧时间网格当作同一个手势区域，造成拖动刻度时触发选区。原应用黑盒操作与恢复源码共同确认两边属于不同 View，左侧拖动改变显示窗口，右侧拖动选择时间块。来源旧主题 `D:\code\content\topics\20260812-android-jiagu-runtime-dex-dump\research.md`。
- 可运行化阶段继续使用同一方法。静态代码给出候选调用顺序，原应用界面与恢复工程的实际结果负责验证页面是否真的成立。
- 总结编辑器的复制与粘贴不能只看返回 JSON。实际回归输入 `RecoveredNote123`，执行复制、清空、粘贴，再退出保存，并检查持久化 JSON 和日志。
- 黑盒参照只能验证已操作到的路径。它不能证明没有触发的分支正确，也不能补出服务端、签名或发布配置。

---

## 支撑单元七 怎样证明恢复工程已经能跑

### 支撑素材

- 当前构建环境为 Android Studio JBR 17、Android Gradle Plugin 8.5.0、Gradle 8.7、compileSdk 34、minSdk 21、targetSdk 33。来源 `D:\code\BlockyTime-Recovered\docs\BUILD_STATUS.md`。
- 最终执行 `:legacy-app:clean :legacy-app:compileDebugJavaWithJavac :legacy-app:assembleDebug`，干净构建成功。APK 输出为 `legacy-app/build/outputs/apk/debug/legacy-app-debug.apk`。
- 全新数据回归先安装 APK，再执行 `pm clear`。冷启动后协议弹窗出现，点击同意后进入记录主页，本地创建 `tb_db_1`、`tb_db_1-wal` 和 `tb_db_1-shm`。
- 记录、总结、计划、统计和我的五个底部页签逐一打开。进一步回归覆盖日周月年总结与统计、打卡详情、三类目标详情、事件统计、标记统计和总结编辑保存。
- 日志扫描没有出现 `FATAL EXCEPTION`、目标进程 ANR、`UnsatisfiedLinkError`、协程恢复超时或残缺方法异常。
- 当前仍有非阻塞构建警告，包括 Manifest 中 `extractNativeLibs` 提示、GIF native library 同时来自恢复文件与 Maven 依赖、三类 native library 无法 strip。这些警告没有在本次 API 34 x86_64 回归中造成核心路径失败，但后续升级 AGP 或覆盖其他 ABI 时需要重新处理。

---

## 补充素材

- 可用于文章的验证命令包括 Gradle 干净构建、`aapt dump badging` 检查包名、`adb install -r`、`adb shell pm clear`、`adb shell am start -W`、`run-as` 查看数据库，以及 logcat 关键字扫描。
- 最终恢复提交为 `3c99d6f feat: add runnable BlockyTime recovery module`，提交包含 3,087 个文件变化。这个数字主要来自代码与资源整体纳入恢复模块，不适合用来衡量手工恢复工作量，正文不使用。
- `legacy-app/src/main/jniLibs` 包含 10 个按 ABI 分布的 native library 文件。壳相关资产仍可能留在 APK assets 中，正文只陈述启动入口已脱离 `StubApp`，不写成所有壳二进制都已删除。

## 会改变结论的边界

- 当前成果是核心离线链路可运行，不能写成完整复刻或原始源码恢复。
- 仍有 56 个外围 Activity 入口未恢复。账号、云备份、支付、广告、推送和部分厂商能力依赖服务端、凭据或原加固运行时。
- 依赖版本是兼容性重建结果，没有证据证明与原工程逐项一致。
- 一个样本的方法不能直接覆盖方法级解密、DEX 虚拟化、大规模 native 化或资源深度混淆的应用。
- 公开文章只讲研究方法和验证结果，不附原 APK、DEX、恢复源码或签名材料。

## 待核查

- 无会阻断文章主线的待核查事实。文章写作时应继续区分本次样本观察、Android 官方机制和作者方法判断。
