# Claude Code 的 WebSearch/WebFetch 挂了？一个命令补回来

如果你用的是火山引擎 / DeepSeek 的自定义 API 端点，WebSearch 和 WebFetch 返回空是正常的——这两个工具走 Anthropic 服务端，你的自定义 API 根本管不到它们。

**一个命令搞定：**

```bash
claude mcp add --transport http exa https://mcp.exa.ai/mcp
```

重启 Claude Code，Exa 会自动接管搜索和读网页。免费额度每月 $10，日常够用。

**如果有些网页 Exa 抓不下来（JS 动态站、需要交互的），再加 Firecrawl：**

```bash
npx -y firecrawl-cli@latest init --all
```

**Chrome DevTools MCP 不要删，但它只用来做浏览器交互（登录、点击、表单），不要用它来搜索和读网页。**

---

装完记得在 `~/.claude/settings.json` 里把原生工具禁掉，避免每次撞墙：

```json
"permissions": { "deny": ["WebSearch", "WebFetch"] }
```

然后在 `~/.claude/CLAUDE.md` 加一句：

```text
联网搜索和读网页用 Exa MCP。难抓的页面用 Firecrawl。
浏览器交互才用 Chrome DevTools MCP。
```

---

总结：

| 干什么 | 用什么 |
|---|---|
| 搜索、读普通网页 | Exa |
| JS 动态站、整站爬取 | Firecrawl |
| 登录、点击、表单 | Chrome DevTools |

别折腾修 WebSearch 了，自定义 API 端点的兼容性 bug 修不完。

#ClaudeCode #AI工具 #开发工具 #Claude #MCP #联网搜索