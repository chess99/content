# 公众号贴图发布准备

## 文件

- 图片：`topics/20260625-codex-reconnecting-image-post/wechat/poster.png`
- 配置：`topics/20260625-codex-reconnecting-image-post/wechat/manifest.json`

## 标题

Codex 重连修复

## 描述

Codex 每次回答前都 Reconnecting？可能不是模型慢，而是 WebSocket 传输层不稳。改用户级 config，让 Responses API 直接走 HTTPS。

## 创建草稿命令

```bash
node ../content-workflows/skills/wechat-image-post/scripts/wechat-image-post-draft.mjs \
  --manifest topics/20260625-codex-reconnecting-image-post/wechat/manifest.json
```

## 说明

- 真正的公众号“贴图”草稿需要通过微信公众号后台 UI 创建。
- 如果 Chrome CDP 或公众号登录态不可用，先按 `D:\code\content-workflows\skills\wechat-image-post\SKILL.md` 的说明完成浏览器准备。
