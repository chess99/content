---
title: DEX 拆出来以后，我把反编译源码恢复成了能跑的 Android 工程
date: 2026-08-29 14:30:00
tags:
  - Android
  - 逆向工程
  - JADX
  - Gradle
categories: 技术
permalink: /posts/android-decompiled-app-runnable-recovery/
---
上一篇文章里，我处理了一份 360 加固风格的 Android APK。静态 JADX 只能看到 6 个 Java 文件，业务代码要等应用运行起来以后，再从进程内存里找。最后拿到 11 份 DEX 候选，筛出 6 份相关文件一起反编译，JADX 总共生成约 18,027 个 Java 文件，目标业务包里有 613 个。

当时文章停在“代码已经可以阅读”。我还特意留了一句，如果准备修改后重新构建，相关方法必须继续回到 smali 或字节码里核验。

这次真的往下做了。

最后的结果是一套新的 Android 模块。它可以和原应用同时安装，能够从干净目录构建，在 Android 14 模拟器上清数据冷启动，显示协议弹窗，初始化本地数据库，再进入记录、总结、计划和统计等核心页面。总结编辑器也完成了输入、复制、清空、粘贴和保存回归。最后又在一台 Android 真机上同时安装原版与恢复版，两个包都保留，恢复版能够冷启动到系统权限页。

它依然有清楚的缺口。56 个外围 Activity 的入口还保留着壳层 native 声明，账号、支付、广告、推送和云服务也没有完整恢复。所以本文里的“能跑”，指核心离线功能已经能够独立运行。它不等于拿回了原始工程，更不等于整个应用已经恢复完整。

上一篇解决的是怎样从运行中的加固 APK 抓回业务 DEX。本文从那些 DEX 的反编译目录开始，讲讲后面的麻烦。

上一篇文章在这里。

[360 加固 APK 的识别、运行时 DEX 恢复与常见坑](https://blog.cearl.cc/posts/android-jiagu-runtime-dex-dump/)

<!-- more -->

本次命令都在 Windows PowerShell 中执行。实际环境为 JDK 17、Android Gradle Plugin 8.5.0、Gradle 8.7、compileSdk 34 和 API 34 x86_64 模拟器。Android SDK 已通过 `ANDROID_HOME` 配置，设备可以被 adb 正常识别。

## 613 个 Java 文件还不叫 Android 工程

拿到反编译目录以后，人很容易产生一种错觉。Manifest 有了，`res` 有了，Java 文件也有了，给它补一个 `build.gradle`，Android Studio 应该就能接手。

我第一次试着组装模块，构建甚至还没走到 Java 编译。AAPT2 先在 8 个 `.9.png` 上停了下来。

```text
drawable-hdpi/abc_list_divider_mtrl_alpha.9.png
drawable-xhdpi/abc_list_divider_mtrl_alpha.9.png
drawable-mdpi/abc_list_divider_mtrl_alpha.9.png
drawable-xxhdpi/abc_list_divider_mtrl_alpha.9.png
drawable-hdpi/abc_textfield_search_default_mtrl_alpha.9.png
drawable-hdpi/abc_textfield_search_activated_mtrl_alpha.9.png
drawable-mdpi/abc_textfield_search_activated_mtrl_alpha.9.png
drawable-mdpi/abc_textfield_default_mtrl_alpha.9.png
```

这些文件名带着 AppCompat 常见的 `abc_` 前缀。它们已经跟应用资源一起进入 APK，解码出来以后，却不再满足这次 AAPT2 对源 NinePatch 的检查。

这次的错误信号很明确。`:legacy-app:mergeDebugResources` 失败，输出逐一指向上面的 8 个文件，并没有报告应用自定义资源缺失。我把它们留在只读的 `recovered/` 里，只从 `legacy-app` 的资源副本中移除，再让 AppCompat AAR 提供对应资源。

```kotlin
dependencies {
    implementation("androidx.appcompat:appcompat:1.4.2")
}
```

```powershell
.\gradlew.bat :legacy-app:mergeDebugResources
```

下一次构建通过了资源合并，错误才继续向 Java 编译推进。这里不能看见 `abc_` 就整批删除。应用可能有意覆盖依赖中的同名资源。稳妥的做法是逐个确认资源来自公共 AAR，检查应用代码是否依赖它的自定义内容，再只修改可运行副本。

问题也由此露了出来。APK 里的 `res` 是构建后的合并结果。应用自己的资源、AndroidX 资源、Material 资源和第三方 AAR 资源已经放在了一起。反编译器能把它们按目录导出，却不会顺手还原当年的依赖声明和资源归属。

这类错误如果按文件逐个修，很快会走偏。今天重画 8 张 NinePatch，明天还会碰到重复 attribute、重复 style、旧资源 ID 和 SDK 自带 layout。文件能通过编译，也不说明资源边界恢复对了。

我先把最初的反编译结果固定下来，放进只读的 `recovered/`。随后新建 `legacy-app/`，所有为了构建作出的修改都放在这里。两份目录里的同名文件可以直接比较。前一份回答“当时从 DEX 和 APK 里拿到了什么”，后一份回答“为了让它运行，我们改了什么”。

这个分层后来很有用。反编译代码里一旦出现奇怪的类型转换或调用顺序，我还能回到原样文件核对，不会分不清那是 DEX 留下的证据，还是前一次修编译时引入的改动。

## 先让公共依赖回到构建系统

恢复工程的下一步不是把所有 Java 文件都塞进 `src/main/java`。

AndroidX、Kotlin 标准库、协程、Room、Navigation、Paging、OkHttp 这些公共依赖，本来就应该由 Gradle 提供。它们的反编译副本会带来重复类、不可见的 synthetic 方法和一批已经失去源码语义的 Java。AAR 还能同时提供自己的 Manifest、资源和 native library，这正好接住前面暴露的资源问题。

依赖坐标可以从几个方向交叉判断。

- 看类的完整命名空间和方法签名
- 看资源名前缀与 style 继承关系
- 看 Manifest 里的组件、Provider 和 metadata
- 看 DEX 中保留的版本字符串与 `BuildConfig`
- 用编译错误检查所选版本是否缺方法或类型不兼容

这里恢复的是一组兼容依赖，不是原项目的 Gradle 锁文件。APK 没有提供足够信息，让人证明每一个版本号都与原工程一致。

资源 ID 还有一处容易踩坑。反编译结果里带着大量 `R$drawable.java`、`R$string.java` 和 `R$styleable.java`，里面是原 APK 的数值 ID。新工程重新编译资源以后，AGP 会生成自己的 R 类。旧数值类继续参与编译，轻则重复类，重则让代码拿着旧 ID 去访问新资源表。

恢复模块直接排除了目标包下的旧 R 类。下面的片段放在 `legacy-app/build.gradle.kts`。本次目标包里只有 `R$*.java`，没有顶层 `R.java`。第二条排除让同一写法也能处理带顶层 R 文件的反编译目录。

```kotlin
import org.gradle.api.tasks.compile.JavaCompile

tasks.withType<JavaCompile>().configureEach {
    exclude("top/onepix/timeblock/R\$*.java")
    exclude("top/onepix/timeblock/R.java")
}
```

随后执行 `:legacy-app:compileDebugJavaWithJavac`。通过信号是目标包不再出现重复 R 类，业务代码引用的 R 由本次资源编译生成。如果错误变成某个资源名不存在，应当回到资源归属与依赖版本继续查，不能把缺失引用改成数值常量。

公共依赖之外还有一批应用自己的小型库，以及无法从公开坐标可靠重建的代码。这些部分继续留在恢复模块。账号、广告、推送和一键登录则换成独立的离线兼容层，让启动和本地数据流程不再等待服务端、厂商凭据或原签名。

兼容层必须诚实。广告占位实现只返回“不展示”，推送初始化只保留调用形状。它们的作用是隔离外围能力，不会伪造一个已经恢复的线上功能。

## 把壳入口换回业务 Application

依赖和资源能编译以后，应用仍然可能从错误的地方启动。

原 APK 的 Manifest 把 Application 指向 `com.stub.StubApp`。它负责接管进程、解密并加载业务代码。现在业务 DEX 已经进入普通构建，恢复工程不该再依赖这条启动过程。

运行时 DEX 里可以找到业务侧的 `MainApplication`。它的 `onCreate` 依次初始化日志、Activity 生命周期监听、网络、皮肤、数据库、通知渠道、语言和自动记录服务。Manifest 因此改回业务 Application，Launcher 继续指向 `SplashActivity`。

这一步还有个很实际的问题。恢复 APK 需要跟原应用同时装在测试设备上，方便左右对照。Android 在安装阶段并不理解“开发版”和“正式版”，它主要看 applicationId 与签名证书。

- applicationId 相同、签名相同，两个 APK 属于同一应用身份，新包会走更新路径，但仍受版本号等安装规则约束。
- applicationId 相同、签名不同，安装通常会因签名不兼容被拒绝，不会自动变成第二个应用。
- applicationId 不同，才具备作为两个应用共存的前提。

因此，只改签名不能解决共存问题。为了共存必须先改 applicationId；原签名不在研究材料里，则另外意味着恢复包也不能作为原应用的更新安装。两项限制要分开处理。

这不是一条只存在于文档里的提醒。一次真机安装后，原版不再出现在设备上。等到用 PackageManager 复查时，原版和当时准备验证的恢复包都不在，现场状态已经不足以证明中间究竟发生了覆盖、卸载，还是安装链路中的其他操作。所以这里不把事故原因写死。能确定的是，此前的验收少了一条硬断言：安装恢复包以后，必须再次确认原版包仍在，而不是看到恢复版能启动就算通过。

```kotlin
android {
    namespace = "top.onepix.timeblock"

    defaultConfig {
        applicationId = "top.onepix.timeblock.recovered"
        versionName = "2.19.28-recovered"
    }
}
```

只改 applicationId 还不够。Manifest 里的自定义权限、广播权限和 FileProvider authority 都是设备级名字，也要一起检查。第一版恢复工程虽然已经使用 `.recovered` 包名，却还声明着原版的 `top.onepix.timeblock.permission.PUSH_WRITE_PROVIDER`。模拟器中先装着这版恢复包，再安装原版，PackageManager 给出了明确错误。

```text
INSTALL_FAILED_DUPLICATE_PERMISSION:
Package top.onepix.timeblock attempting to redeclare permission
top.onepix.timeblock.permission.PUSH_WRITE_PROVIDER
already owned by top.onepix.timeblock.recovered
```

修复时，自定义权限和 Provider 都改用 Manifest placeholder。实验版的显示名也改成 `BlockyTime Recovered`，避免两个图标同名造成误操作。下面只列与命名隔离有关的属性，不是完整 Manifest 节点。

```xml
<permission
    android:name="${applicationId}.permission.PUSH_WRITE_PROVIDER"
    android:protectionLevel="signature" />

<provider
    android:name="top.onepix.timeblock.models.biz.ExportFileProvider"
    android:authorities="${applicationId}.fileprovider" />
```

这类遗漏不会都表现为“覆盖原版”。它也可能在安装阶段直接冲突，或者运行到分享文件时才发现 authority 仍指向另一个应用。

构建后可以先检查 APK，确认没有误装成原包名。

```powershell
$Apk = "legacy-app\build\outputs\apk\debug\legacy-app-debug.apk"
$Aapt = Get-ChildItem "$env:ANDROID_HOME\build-tools\*\aapt.exe" |
    Sort-Object FullName -Descending |
    Select-Object -First 1 -ExpandProperty FullName

& $Aapt dump badging $Apk |
    Select-String "^package:|^application-label:"
& $Aapt dump permissions $Apk |
    Select-String "top.onepix.timeblock.*permission"
```

预期结果里应当出现包名 `top.onepix.timeblock.recovered`、显示名 `BlockyTime Recovered`，自定义权限也都应位于 `.recovered.permission.*` 下。如果还是原包名，或者权限仍占用原版命名空间，先别安装。

修复后，我在模拟器上同时安装两版，再在真机上重复了一次。最后的通过信号不是桌面上看见两个相似图标，而是 PackageManager 同时列出两条记录。

```powershell
$Serial = "emulator-5554"
adb -s $Serial shell pm list packages |
    Select-String "^package:top.onepix.timeblock"
```

```text
package:top.onepix.timeblock
package:top.onepix.timeblock.recovered
```

真机上的恢复版随后完成冷启动，进入系统权限申请页，原版包仍然存在。安装前仍应先备份原版数据。包名隔离是防止误覆盖和命名冲突的措施，不是数据恢复方案；一旦误卸载原版，重新装回 APK 不会自动带回原来的应用沙箱数据。

## 编译器开始检查反编译质量

资源和依赖处理完，Java 编译器终于能看到业务代码。接下来的错误才开始碰到反编译质量。

一类问题来自 Kotlin 编译产物。原字节码会调用 `launch$default`、`async$default` 之类默认参数桥。它们在库里属于 synthetic 方法，JVM 字节码可以调用，恢复成 Java 源码后，`javac` 却会把这类调用挡在可见接口之外。

恢复工程为常用桥接写了一层 Java 可见适配，把 mask 还原成实际默认参数，再调用协程库的公开方法。少量已经展开的 suspend 调用，则通过 continuation 接收结果，并设置超时，避免恢复错误把主流程永久挂住。

另一类问题更直接。JADX 在 9 个业务文件中留下了 17 个 `Method not decompiled` 方法，调用就会抛出 `UnsupportedOperationException`。它们分布在时间统计、连续打卡、周月年总结、事件与标记图表、旧数据迁移和 Excel 导出里。

这些方法没有统一的自动修复办法。实际处理时，我会同时看几份材料。

1. 运行时 DEX 里的方法字节码
2. CFR 等另一套反编译器给出的控制流
3. 调用方传入什么，随后怎样使用返回值
4. Room DAO 和数据类怎样表达同一业务约束
5. 原应用在相同输入下显示什么结果

富文本编辑器是一个更典型的例子。它有 4 个复杂方法没有被 JADX 正常还原，涉及复制、粘贴、模板导入和模板 JSON 导出。光把方法写到不抛异常没有意义。恢复后还要输入一段文字，复制，清空编辑器，再粘贴回来，最后退出页面触发保存。日志和落盘 JSON 都对得上，这项回归才算过。

这里的数字口径需要分开。17 指目标业务包 9 个文件里的明确异常方法。富文本库的 4 个方法另外计数，不包含在 17 里面。它们都来自方法体没有正常恢复，统计对象却属于两组源码。

## 没有异常桩也不代表方法都在

17 个明确异常桩补完以后，源码搜索已经找不到 `Method not decompiled`。这时又出现了一个更隐蔽的缺口。

一批 Activity 的 `onCreate` 在反编译源码里只有 native 声明。

```java
protected native void onCreate(Bundle savedInstanceState);
```

这类方法不会命中 JADX 的异常桩扫描，Java 编译也允许 native 声明通过。页面一旦打开，运行时才会寻找对应的 JNI 实现。离开原加固环境以后，它自然找不到。

当前样本里还剩 56 个这样的外围入口。这个数字是补回 5 个核心入口以后的剩余量。已补部分包括打卡统计、目标详情、事件统计、标记统计和总结编辑。

恢复一个 Activity 入口时，类里已有的方法通常会给出大部分顺序。以事件统计页为例，类中已经保留了 `layout`、`initData`、`initViews` 和 `initEvents`，缺的是把它们接起来的入口。下面是示意代码，只保留调用形状，没有复制目标应用的方法体。

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(layout(this));
    initData();
    initViews();
    initEvents();
}
```

这里需要核对的是先后关系。有的页面必须先从 Intent 取参数，再创建布局。有的 adapter 依赖 `initData` 填好的列表。有的 listener 在 view 尚未加入页面时注册，会直接拿到 null。相邻页面、字段初始化、方法调用关系和原应用的实际打开过程，可以共同约束这个顺序。

入口保持 native 时，打开页面会在运行阶段暴露 `UnsatisfiedLinkError`，错误中带有 Activity 与 `onCreate` 签名。补回调用顺序以后，回归断言也很具体。事件统计页能打开，默认日期和图表容器完成初始化，切换统计条件不退出，目标进程日志不再出现对应的 native 方法错误。

剩下的 56 个入口没有全部填成空页面。空页面确实能让跳转不崩，却会把“入口缺失”伪装成“功能已经恢复”。研究工程宁愿留下清单，也不靠这种办法增加完成率。

## 原应用负责回答行为问题

编译器能检查类型、方法和资源引用，检查不了手势是否相同，也检查不了保存后的业务结果是否一致。

这次研究一开始就碰到过这种差别。记录页左边是时间刻度，右边是时间网格。早期实验把一整行都交给选择控件，结果在刻度上拖动时也会选中时间块。原应用没有这个问题。继续操作并回看源码后才确认，左侧刻度和右侧网格属于两个独立 View。左边拖动改变显示的时间窗口，右边拖动才负责选区。

这个例子后来成了恢复过程里的检查方法。静态代码用来提出一个可运行的候选实现，原应用则提供相同入口、相同操作和相同数据下的参照结果。

页面能显示只是第一步。统计页要切换日、周、月、年。目标详情要分别检查时长、次数和连续天数。总结编辑器要走复制、粘贴和保存。数据库要在清数据后重新创建。每条测试都对应一个具体结果，不能只拍一张主页截图就宣布恢复完成。

黑盒对照也有边界。它只能覆盖实际操作到的分支。账号服务器怎样校验、支付回调怎样签名、云端备份怎样兼容历史版本，都不可能只靠本地点击补出来。

## 我怎样验收一个恢复工程

“构建成功”在这里太宽了。我把验收拆成几层，每一层都有看得见的结果。

构建失败的位置也能帮助分流。AAPT2 指向图片、style 或 attribute 时先查资源归属。`duplicate class` 先查公共依赖与反编译副本是否同时参与编译。冷启动立即退出就检查 Application、Launcher 和 Manifest。只有打开某个页面才出现 JNI 错误，就查该组件是否还留着 native 入口。页面能显示，手势或数据结果却不对，再回到控制流和黑盒对照。

| 层级 | 动作 | 通过信号 |
|---|---|---|
| 源码编译 | 从干净目录执行 Java 编译 | 没有语法、类型和残缺方法编译错误 |
| APK 构建 | 执行 Debug assemble | 生成可安装 APK，资源与 native library 完成打包 |
| 安装隔离 | 检查包名、权限与 Provider 后同机安装 | PackageManager 同时列出原版和恢复版 |
| 冷启动 | 清除恢复应用数据后启动 Launcher | 协议弹窗正常出现，进程不退出 |
| 数据库打开 | 同意协议并进入主页 | Room 数据库及 WAL、SHM 文件创建 |
| 核心流程 | 逐页执行记录、总结、计划、统计和编辑保存 | 页面、数据和手势结果符合参照样本 |
| 日志检查 | 扫描目标进程日志 | 没有 FATAL、ANR、缺失 native library 或残缺方法异常 |

完整回归可以从下面这组 PowerShell 命令开始。

本机同时连接了真机和模拟器，所以命令显式指定 `emulator-5554`。只有一台 adb 设备时可以去掉 `-s $Serial`。

```powershell
$Serial = "emulator-5554"
$Package = "top.onepix.timeblock.recovered"
$Activity = "top.onepix.timeblock.activities.splash.SplashActivity"
$Apk = "legacy-app\build\outputs\apk\debug\legacy-app-debug.apk"

.\gradlew.bat :legacy-app:clean :legacy-app:assembleDebug
adb -s $Serial install -r $Apk
adb -s $Serial shell pm list packages |
    Select-String "^package:top.onepix.timeblock"
adb -s $Serial shell pm clear $Package
adb -s $Serial logcat -c
adb -s $Serial shell am start -W -n "$Package/$Activity"

$AppPidText = adb -s $Serial shell pidof $Package
if (-not $AppPidText) {
    throw "Recovered app process is not running"
}
$AppPid = ($AppPidText.Trim() -split "\s+")[0]
```

启动页显示以后，先手动完成协议流程和需要验证的核心操作。Debug 包可以通过 `run-as` 检查数据库是否真的创建。

```powershell
adb -s $Serial shell run-as $Package ls -l databases
```

本次全新启动后能看到 `tb_db_1`、`tb_db_1-wal` 和 `tb_db_1-shm`。这只能证明 Room 已经打开数据库，不能证明 schema、迁移和业务数据都正确。上层验证要另外执行一次读写。本次继续打开记录、总结、计划、统计和我的五个页签，再完成一条总结编辑与保存，检查页面结果和落盘 JSON。

最后扫一次日志。

```powershell
$CurrentAppPidText = adb -s $Serial shell pidof $Package
if (-not $CurrentAppPidText) {
    throw "Recovered app process exited during regression"
}
$CurrentAppPid = ($CurrentAppPidText.Trim() -split "\s+")[0]
if ($CurrentAppPid -ne $AppPid) {
    Write-Warning "Recovered app process restarted during regression"
}

adb -s $Serial logcat -d -v threadtime --pid=$AppPid |
    Select-String "FATAL EXCEPTION|ANR in|UnsatisfiedLinkError|Method not decompiled|Recovered suspend call timed out"
```

这段命令只筛选启动时记录的目标 PID，并额外检查进程是否退出或重启。没有命中这些关键字仍然不能代替页面断言，不过它能抓到一批界面上不明显的失败。恢复协程若没有正常 resume、native library 若缺少当前 ABI、后台线程若在页面离开后崩溃，通常会在这里留下痕迹。

本次最终构建使用 Android Studio JBR 17、Android Gradle Plugin 8.5.0、Gradle 8.7 和 compileSdk 34。`clean`、Java 编译与 Debug assemble 全部通过，API 34 x86_64 模拟器上的核心回归没有出现 FATAL、ANR、`UnsatisfiedLinkError` 或协程等待超时。原版与恢复版的共存安装同时在模拟器和真机上通过，真机恢复版冷启动没有覆盖原版。

构建还有几条非阻塞警告。Manifest 中的 `extractNativeLibs` 需要后续按新版 AGP 处理。同一个 GIF native library 同时来自恢复文件和 Maven 依赖，当前 AGP 选择了应用内版本。另有三类 native library 无法 strip，最终按原样打包。这些问题没有挡住当前测试环境，换 AGP 或补测其他 ABI 时还得重新看。

## 这次恢复停在哪里

现在的仓库有三份内容。`recovered/` 保存原样反编译证据，`legacy-app/` 是可执行恢复工程，早期的 `app/` 继续保存时间网格实验。核心离线功能已经可以启动和操作，17 个明确业务异常桩与 4 个富文本残缺方法已经补回，5 个核心 Activity 入口也已经恢复。

缺口同样留在文档里。56 个外围 Activity 还没有入口实现，主要集中在账号、会员、支付、云数据、导入导出、权限设置、事件编辑、目标编辑和帮助页面。线上服务依赖的后端逻辑、凭据、签名与发布配置也不在 APK 里。

这套做法适合业务代码会以常规 DEX 进入 ART，反编译后还能看到类、字段和大部分调用关系的样本。遇到方法级解密、DEX 虚拟化、大规模 native 化或更深的资源混淆，后续工作会换成另一套问题。

如果你手里也有一份“JADX 已经能打开”的目录，可以先别急着逐个修红线。固定原样证据，重建公共依赖和资源边界，恢复真实启动入口，再让干净构建暴露控制流缺口。最后用清数据启动、数据库和核心操作去验收。走到哪一步，就写到哪一步。

反编译器输出了多少文件，只能说明拿回了多少材料。一个工程能不能运行，要让构建系统和设备回答。

## 参考资料

- [上一篇运行时 DEX 恢复文章](https://blog.cearl.cc/posts/android-jiagu-runtime-dex-dump/)
- [Android library 与 AAR 说明](https://developer.android.com/studio/projects/android-library)
- [Android 资源添加与合并规则](https://developer.android.com/studio/write/add-resources#resource_merging)
- [Android applicationId 配置](https://developer.android.com/build/configure-app-module#set-application-id)
- [Android Manifest 管理与占位变量](https://developer.android.com/build/manage-manifests#inject_build_variables_into_the_manifest)

*本文依据实际实验记录整理，使用 AI 辅助写作与审校。技术结论以本地源码、构建日志和设备回归结果核对。*
