# Claude Code 自定义 API 下 WebSearch/WebFetch 挂了怎么办

| 渠道 | 状态 | 发布时间 | 使用版本 | 链接 |
|---|---|---|---|---|
| 小红书 | 待发布 | - | `image-post/post.md` + `image-post/images/` (4 张) | - |
| 抖音 | 待发布 | - | `image-post/post.md` + `image-post/images/` (4 张) | - |

## 定位

- 系列：工具与工作流
- 读者：使用 Claude Code + 自定义 API 端点（火山引擎/DeepSeek 等），发现 WebSearch 和 WebFetch 工具不可用的开发者
- 问题：Claude Code 的 WebSearch/WebFetch 依赖 Anthropic 服务端，自定义 `ANTHROPIC_BASE_URL` 时这两个工具走不了
- 方案：Exa MCP 替代搜索 + 读网页，Firecrawl CLI 处理难抓页面，Chrome DevTools MCP 只做浏览器交互
- 一句话：一个命令补回联网能力