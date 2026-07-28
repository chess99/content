# 公众号发布准备

## 文件

- 公众号稿：`topics/20260624-ai-future-judgment/longform/wechat/post.md`
- 封面：`topics/20260624-ai-future-judgment/longform/wechat/cover.jpg`

## 标题

AI 普及后的未来判断：就业、分配、教育、资产与个体策略

## 摘要

AI 不会平均替代所有工作，而会先重写任务层、入门岗位和中产路径。真正要准备的，是可迁移现金流能力与更少单点依赖。

## 发布命令

```powershell
npm --prefix D:\code\content-studio\apps\wx-publisher run dev -- publish `
  --file topics/20260624-ai-future-judgment/longform/wechat/post.md `
  --cover topics/20260624-ai-future-judgment/longform/wechat/cover.jpg `
  --theme default \
  --title "AI 普及后的未来判断：就业、分配、教育、资产与个体策略" \
  --digest "AI 不会平均替代所有工作，而会先重写任务层、入门岗位和中产路径。真正要准备的，是可迁移现金流能力与更少单点依赖。"
```

## 状态

- 公众号稿已生成：Markdown 超链接已降级为纯文本，文末已集中保留完整 URL。
- 封面已由内置 image_gen 生成，并验证为 900×383 JPEG。
- `wx-publisher` 本地配置已写入 `D:\code\wx-publisher\.wxp.json`（该文件已被 wx-publisher 仓库忽略，不提交）。
- 草稿已成功创建：2026-06-25。
- 最新 media_id：`bpB07u_8H2Ns8YJAsyxW3QkhIieT618ccfLpANG1Z7PGLSwXs14aXZZEr5XwPrwh`
- 旧版 media_id：`bpB07u_8H2Ns8YJAsyxW3XAKLW9JD-HxsKOxCYG6JHa-WvXQTO4ZE1fGtV4Mlp5f`（已被新版草稿取代，勿发布）。
- 主题：`default`。
- 正文图片：检测 0 张，上传 0 张。
- 封面：使用本地 `wechat/cover.jpg`，未使用占位图。
- 后续：到微信公众号后台草稿箱手动检查和发布。
