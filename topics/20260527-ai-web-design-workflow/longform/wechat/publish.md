# 公众号发布准备

## 文件

- 文章：`topics/20260527-ai-web-design-workflow/longform/wechat/post.md`
- 封面：`topics/20260527-ai-web-design-workflow/longform/wechat/cover.jpg`

## 标题

让 AI 写出好看的网页，不是多写几个高级形容词

## 发布命令（在有白名单权限的环境执行）

```powershell
npm --prefix D:\code\content-studio\apps\wx-publisher run dev -- publish `
  --file topics/20260527-ai-web-design-workflow/longform/wechat/post.md `
  --cover topics/20260527-ai-web-design-workflow/longform/wechat/cover.jpg `
  --theme warm-tech `
  --title "让 AI 写出好看的网页，不是多写几个高级形容词" `
  --digest "一次晨笙阅读移动端改版复盘：用 brainstorming 定方向，用 frontend-design 管审美，用 ui-ux-pro-max 打磨交互。"
```

> 注意：`wechat/post.md` 已把 Markdown 超链接降级为纯文本，并在文末增加「参考资料」URL；发布前把相对图片路径解析为本地绝对路径，便于 `wxp publish` 上传到微信素材库；`final.md` 保留博客用链接和 `/images/...` 路径。

## 状态

- `wechat/cover.jpg` 已生成并验证为 900×383。
- `wx-publisher` 工具位置：`D:\code\content-studio\apps\wx-publisher`
- ✅ 草稿已成功创建（2026-05-28）
- media_id: `bpB07u_8H2Ns8YJAsyxW3cYnK3jOAoSBhwrZPoEH6opgggdgwnQBuo055cdvhwBW`
- 主题：`warm-tech`
- 摘要：`一次晨笙阅读移动端改版复盘：用 brainstorming 定方向，用 frontend-design 管审美，用 ui-ux-pro-max 打磨交互。`
- 正文图片：检测 2 张，成功上传 2 张。
- 待在微信公众号后台「草稿箱」手动发布。
