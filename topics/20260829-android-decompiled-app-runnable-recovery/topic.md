# DEX 拆出来以后怎样恢复成可运行 Android 工程

## 主题定位

- 目标读者为已经拿到运行时 DEX 或 JADX 输出，准备继续做可运行化恢复的 Android 研究者与开发者。
- 文章承接上一篇《360 加固 APK 的识别、运行时 DEX 恢复与常见坑》，不重复内存扫描与候选 DEX 分类。
- 核心问题是反编译源码为什么不能直接构建，以及怎样重建依赖、资源、Manifest、方法体和验证链路。
- 主系列为工具与工作流。
- 研究边界为已授权设备上的兼容性和交互研究，不分发原 APK、运行时 DEX、签名文件或原版源码。

## 渠道计划

| 渠道 | 状态 | 发布时间 | 使用版本 | 链接 |
|---|---|---|---|---|
| 博客 | 博客稿已完成，待发布 | 待定 | `longform/blog/article.md` | 待补 |

## 关联内容

- 上一篇文章 https://blog.cearl.cc/posts/android-jiagu-runtime-dex-dump/
- 本轮恢复工程 `D:\code\BlockyTime-Recovered`
