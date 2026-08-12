# A 股巴菲特指标

- 创建日期：2026-07-26
- 主题：用巴菲特指标解释 A 股总市值与 GDP 的关系，并展示不同公开统计口径下的合理区间
- 内容形态：知识视频、小红书图文
- 状态：视频样片已完成，小红书图文已完成

## 资产

- `video/input/`：资料说明、来源登记、原始公开资料与图表数据。
- `video/brief.json`：视频定位与表达边界。
- `video/script.json`：结构化旁白脚本。
- `video/storyboard.json`：逐场景分镜。
- `video/config.json`、`video/config.fish.json`：两套配音与渲染配置。
- `video/publish/`：封面、字幕、来源说明、平台文案与本地最终成片。
- `research.md`：小红书图文使用的最新世界银行数据、口径与判断。
- `shared/world-bank-buffett-indicator-2006-2025.csv`：中美同口径年度数据。
- `shared/eastmoney-market-cap-snapshot-20260812.json`：2026 年 8 月 12 日沪深北股票总市值原始快照。
- `shared/current-buffett-calculation-20260812.json`：当下估值快照的 GDP 数据、算式和来源。
- `image-post/`：小红书正文、图片方案、模型原稿与最终发布图。

`video/publish/final.mp4` 作为本地最终资产保留，但按仓库大文件规则忽略，不进入普通 Git 历史。

## 发布记录

| 渠道 | 状态 | 发布时间 | 使用版本 | 链接 |
|---|---|---|---|---|
| 抖音 | 待发布 | — | `video/publish/final.mp4` + `video/publish/post-douyin.md` | — |
| 小红书视频 | 待发布 | — | `video/publish/final.mp4` + `video/publish/post-xiaohongshu.md` | — |
| 小红书图文 | 待发布 | — | `image-post/post.md` + `image-post/images/` | — |

## 生产方式

从 `D:\code\content-studio\apps\knowledge-video-factory` 调用视频工厂，并把本主题的 `video/` 作为外部项目目录传入：

```powershell
$videoDir = 'D:\code\content\topics\20260726-a-share-buffett\video'
node scripts/prepare-project.mjs --project-dir $videoDir
node scripts/render-project.mjs --project-dir $videoDir
node scripts/qa-video.mjs --project-dir $videoDir
```
