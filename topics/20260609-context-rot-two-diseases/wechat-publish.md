# 公众号发布记录

## 文件

- 公众号稿：`topics/20260609-context-rot-two-diseases/wechat.md`
- 预览 HTML：`topics/20260609-context-rot-two-diseases/wechat-preview.html`
- 封面：`topics/20260609-context-rot-two-diseases/cover.jpg`

## 标题

Agent 越改越烂，不一定是 context 太长

## 摘要

Agent 越改越烂，可能不是上下文太长，而是错误前提进了 context。先判断太长还是太脏，再决定 compact、重开或隔离。

## 发布命令

```bash
node ~/code2/wx-publisher/dist/cli/index.js publish \
  --file topics/20260609-context-rot-two-diseases/wechat.md \
  --cover topics/20260609-context-rot-two-diseases/cover.jpg \
  --theme default \
  --title "Agent 越改越烂，不一定是 context 太长" \
  --digest "Agent 越改越烂，可能不是上下文太长，而是错误前提进了 context。先判断太长还是太脏，再决定 compact、重开或隔离。"
```

## 状态

- 最新草稿已成功创建：2026-06-10
- 最新 media_id：`bpB07u_8H2Ns8YJAsyxW3XVYHEEgu0gqVniAmrhq3MZJ0Gzh8BZvey7vACFLONAH`
- 主题：`default`
- 封面：本地封面已上传，未使用占位图；封面由 `1504x640` 候选图缩放为 `900x383` JPEG
- 正文图片：检测 0 张，上传 0 张
- 后续：到微信公众号后台草稿箱手动检查和发布
