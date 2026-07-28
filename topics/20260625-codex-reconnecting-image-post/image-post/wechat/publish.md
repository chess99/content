# 公众号贴图发布准备

## 文件

- 图片：`topics/20260625-codex-reconnecting-image-post/image-post/wechat/poster.png`
- 配置：`topics/20260625-codex-reconnecting-image-post/image-post/wechat/manifest.json`

## 标题

Codex 重连修复

## 描述

Codex 每次回答前都 Reconnecting？可能不是模型慢，而是 WebSocket 传输层不稳。改用户级 config，让 Responses API 直接走 HTTPS。

## 创建草稿命令

```powershell
npm --prefix D:\code\content-studio\apps\wx-publisher run dev -- publish-newspic `
  --title "Codex 重连修复" `
  --content "Codex 每次回答前都 Reconnecting？可能不是模型慢，而是 WebSocket 传输层不稳。改用户级 config，让 Responses API 直接走 HTTPS。" `
  --image "D:\code\content\topics\20260625-codex-reconnecting-image-post\image-post\wechat\poster.png"
```

## 说明

- 当前工具通过微信公众号官方接口创建“贴图”草稿，不再依赖浏览器 UI 自动化。
- 创建草稿属于外部写操作，执行前必须由用户确认标题、描述和图片。
