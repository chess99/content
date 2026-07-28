---
title: Codex CLI 速查手册：从交互对话到 CI 自动化的全部命令
date: 2026-05-19 00:00:00
tags:
  - Codex CLI
  - AI 工具
  - 开发效率
  - OpenAI
categories: 工具
permalink: /posts/codex-cheatsheet/
---

**TL;DR**：这是一份完整的 Codex CLI 命令速查手册，按使用场景排列。如果你用过 Claude Code，这篇文章是对照阅读的最好方式——两个工具的理念很像，但细节设计各有侧重。

<!-- more -->

---

上个月写了一篇 [Claude Code 速查手册](/posts/claude-code-cheatsheet/)。最近 AI coding 工具两家独大，Claude Code 和 Codex CLI 并列，superpowers 这类工具也开始把两者作为独立视角——Codex 作为"第二意见"审代码，Claude Code 负责执行。想亲手试试 Codex，顺手整理成手册。

结论先说：两个工具理念很像，但侧重不同。Claude Code 的 Hooks 和 Skills 生态更成熟，更适合深度定制工作流；Codex 在非交互执行和 CI/CD 集成上更顺手，而且有一个 Claude Code 暂时没有的特性——原生 Codex Cloud，让任务在云端异步跑，结果拉回来 apply。

下面按使用频率和学习顺序来讲。

---

## 第一组：搞清楚这三件事，再开始用

### 认证方式 — 先登录，再做别的

Codex 支持四种登录方式：

```bash
codex login                    # 浏览器 OAuth（ChatGPT 账号，最简单）
codex login --device-auth      # 设备码流，适合无头服务器
printenv OPENAI_API_KEY | codex login --with-api-key   # 直接用 API Key
codex login status             # 检查当前是否已登录
```

什么时候用哪种：日常开发用浏览器 OAuth，CI/CD 环境用 API Key 管道输入，远程服务器用设备码流。`codex login status` 是 CI 脚本的标准前置检查，它在已登录时退出码为 0。

---

### 沙箱策略 — 三档权限，按需选

这是 Codex 和 Claude Code 设计理念差异最明显的地方之一。Codex 把执行权限分成三档，在命令行显式声明：

```bash
codex --sandbox read-only          # 只读，只能看不能改
codex --sandbox workspace-write    # 可以读写工作目录（默认推荐）
codex --sandbox danger-full-access # 无限制访问
```

`workspace-write` 是大多数本地开发的正确选项。`danger-full-access` 字面意思就是警告，只有在专门隔离的 VM 或容器里才考虑用。还有一个快捷方式：

```bash
codex --yolo    # 等同于 danger-full-access + 跳过所有审批提示
```

`--yolo` 不是玩笑命名，官方文档的说明是"Only use inside an externally hardened environment"。

---

### AGENTS.md — 给项目的持久化说明书

Codex 读取项目里的 `AGENTS.md` 文件作为持久化指令（类比 Claude Code 的 `CLAUDE.md`）。内容写项目架构、编码规范、目录约定，Codex 每次启动自动读取。

用 `/init` 快速生成一个脚手架：

```bash
codex
# 然后在 TUI 里输入
/init
```

什么时候写：每次你发现自己重复告诉 Codex 同一件事，就把它写进 `AGENTS.md`。这个文件提交到 git，团队共享，也避免 onboarding 新成员时重复解释项目约定。

---

## 第二组：日常交互，TUI 里该知道的事

### 启动与基本输入

```bash
codex                          # 启动 TUI，不带初始 prompt
codex "解释一下这个 codebase"   # 带初始 prompt 启动
codex -i screenshot.png "这个错误怎么修"   # 附带图片
codex --model gpt-5.5          # 指定模型（默认推荐 gpt-5.5）
codex --cd /path/to/project    # 启动时指定工作目录
```

模型选择：目前 `gpt-5.5` 是推荐选项（规划、工具调用、多步任务都更强）；如果 `gpt-5.5` 还没开放，继续用 `gpt-5.4`。

---

### TUI 键盘操作速查

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+C` | 中断当前响应 |
| `Ctrl+L` | 清屏（不清除对话上下文，仅清终端显示） |
| `/clear` | 清屏 + 开始新对话 |
| `Ctrl+G` | 用外部编辑器（`$VISUAL`）编辑当前输入框 |
| `Ctrl+R` | 搜索历史 prompt |
| `Ctrl+O` | 复制最新的 Codex 输出 |
| `Tab`（任务进行中） | 排队下一条指令，当前任务完成后执行 |
| `Esc` 两次 | 回编辑上一条用户消息并 fork 会话 |
| `@` | 模糊搜索文件，Tab/Enter 插入路径到输入框 |
| `!` 前缀 | 直接在 TUI 里执行 shell 命令（结果算入对话） |

---

### 有用的 Slash 命令

Codex 的 slash 命令数量比 Claude Code 少，但常用的都有：

```
/model          — 切换模型，支持 /model gpt-5.3-codex-spark 等
/permissions    — 调整操作权限（Auto / Read Only / Full Access）
/review         — 让 Codex 审查当前工作树
/diff           — 查看 git diff，包括未跟踪文件
/status         — 当前会话配置：模型、权限策略、token 用量
/compact        — 压缩对话上下文，释放空间
/plan           — 切换到计划模式，先出方案再动代码
/fork           — 把当前会话分叉成新线程
/side           — 开一个临时侧边对话，不影响主线程
/clear          — 清屏 + 开始新对话
/exit           — 退出（`/quit` 同效果）
/mcp            — 查看已配置的 MCP 工具
/init           — 在当前目录生成 AGENTS.md 脚手架
/theme          — 选语法高亮主题，保存到 config
/skills         — 浏览和使用 skills
/memories       — 管理记忆（开关记忆读取和生成）
```

---

### 会话管理：resume / fork

```bash
codex resume                   # 打开历史会话列表
codex resume --last            # 直接恢复最近一次会话
codex resume <SESSION_ID>      # 按 ID 恢复指定会话
codex resume --last --all      # 不限当前目录，找最近会话

codex fork                     # 打开会话列表，选一个 fork
codex fork --last              # fork 最近一次会话成新线程
```

Claude Code 叫 `/resume`、`/branch`，Codex 叫 `codex resume`、`codex fork`，功能对应。Codex 还支持在 exec 模式下 resume：

```bash
codex exec resume --last "继续修那个 race condition"
codex exec resume <ID> "实现上次的计划"
```

这个组合特别适合 CI：第一个 job 做规划，第二个 job 接着执行。

---

## 第三组：非交互执行，脚本和 CI 里用

### codex exec — 非交互模式

```bash
codex exec "修复 CI 失败"                         # 基本用法
codex exec --sandbox workspace-write "重构 auth 模块"
codex e "快速别名"                                  # exec 的简写

# 从 stdin 读 prompt
echo "检查所有 .ts 文件的未处理 Promise rejection" | codex exec -

# 输出控制
codex exec --json "分析这个 codebase"              # JSONL 输出
codex exec -o result.md "生成架构文档"              # 最终消息写入文件
codex exec --json -o events.jsonl "审查这个 PR"    # 两个一起用

# 指定目录
codex exec --cd apps/backend "写单元测试"
```

`--output-last-message / -o` + `--json` 是 CI 里的标准组合：`--json` 给流水线用，`-o` 给下游步骤读最终结果。

对比 Claude Code 的 `claude -p`，`codex exec` 功能基本对应，但多了 `--output-schema`：

```bash
codex exec --output-schema schema.json "分析代码质量"
```

用 JSON Schema 约束输出格式，适合需要结构化结果的自动化场景。

---

### web search — 让 Codex 联网

```bash
codex --search "最新的 Node.js LTS 版本是多少"
# 或在 config.toml 里设置
# web_search = "live"   # 实时搜索
# web_search = "cached" # 缓存搜索（默认）
# web_search = "disabled"
```

默认是 cached 模式（OpenAI 维护的索引，不是实时抓取）。需要最新数据时用 `--search` 开启 live 模式。使用 `--yolo` 时默认变成 live。

---

### Hooks 和 execpolicy — 操作审批规则

Codex 的 execpolicy 让你可以定义哪些命令自动放行、哪些需要人工确认、哪些直接拒绝：

```bash
# 检查一条命令是否会被放行
codex execpolicy --rules ~/.codex/rules.toml --pretty git push

# 测试执行策略文件
codex execpolicy -r project.rules -r user.rules npm test
```

在 CI 里预先定义好 rules，配合 `--ask-for-approval never` 实现全自动运行，同时保留对危险命令的拦截：

```bash
codex exec --sandbox workspace-write --ask-for-approval never "重构这个模块"
```

---

## 第四组：远程运行和 Codex Cloud

### codex cloud — 在云端跑任务

这是 Codex 独有的特性，Claude Code 目前没有对应功能。任务在 OpenAI 的云环境里异步执行，完成后把 diff 拉回来应用到本地：

```bash
codex cloud                            # 打开任务列表 TUI
codex cloud exec --env ENV_ID "修复安全漏洞"
codex cloud exec --env ENV_ID --attempts 3 "重构 payment 模块"  # best-of-3

# 查看已有任务
codex cloud list
codex cloud list --env ENV_ID --limit 5 --json

# 把云端任务的 diff 应用到本地
codex apply TASK_ID
```

`--attempts` 是个有意思的参数：让 Codex 云端跑 N 次，选最好的结果。对于复杂重构或有多种合理实现方式的任务，这个选项值得试。

---

### 远程 TUI — 在另一台机器上控制

```bash
# 服务器端启动 app server
codex app-server --listen ws://127.0.0.1:4500

# 本地连接
codex --remote ws://127.0.0.1:4500

# 带认证的生产场景
TOKEN_FILE="$HOME/.codex/token"
openssl rand -base64 32 > "$TOKEN_FILE"
codex app-server --listen ws://0.0.0.0:4500 \
  --ws-auth capability-token \
  --ws-token-file "$TOKEN_FILE"

export CODEX_REMOTE_TOKEN="$(cat "$TOKEN_FILE")"
codex --remote wss://remote-host:4500 --remote-auth-token-env CODEX_REMOTE_TOKEN
```

SSH 端口转发场景（在服务器跑代码，本地看 TUI）是这个功能最自然的使用场景。

---

## 第五组：MCP、配置和周边

### MCP 管理

Codex 用 `codex mcp` 管理 Model Context Protocol 服务，配置存在 `~/.codex/config.toml`：

```bash
codex mcp list                                    # 列出已配置的 MCP
codex mcp add my-db -- npx my-db-server           # stdio 方式
codex mcp add my-api --url https://api.example.com/mcp  # HTTP 方式
codex mcp remove my-db
codex mcp login my-api                            # OAuth 认证（HTTP 服务器）
```

配置好的 MCP 服务在每次 Codex 启动时自动连接，工具暴露给 Codex 使用，用 `/mcp` 查看当前可用工具列表。

---

### 配置文件和 Profiles

Codex 的配置存在 `~/.codex/config.toml`，支持 profiles 让不同项目用不同配置：

```bash
codex --profile ci-strict     # 使用 ci-strict profile
codex exec --profile fast "快速任务"

# 功能标志管理
codex features list
codex features enable unified_exec
codex features disable shell_snapshot
```

命令行 `-c key=value` 可以覆盖单次运行的配置，不修改文件：

```bash
codex -c model=gpt-5.4 -c web_search=disabled "分析这段代码"
```

---

### Shell 补全

```bash
codex completion bash >> ~/.bashrc
codex completion zsh > "${fpath[1]}/_codex"
codex completion fish > ~/.config/fish/completions/codex.fish
```

zsh 用户如果遇到 `command not found: compdef`，在 `.zshrc` 里在 eval 之前加 `autoload -Uz compinit && compinit`。

---

### codex sandbox — 隔离执行任意命令

不只是 AI 任务，Codex 的沙箱可以直接包裹任意 shell 命令：

```bash
# macOS（Seatbelt）
codex sandbox mac -- npm install

# Linux（Landlock + seccomp）
codex sandbox linux -- python script.py

# 带权限 profile
codex sandbox mac --permissions-profile strict --cd /project -- make build
```

这对于想用 Codex 的沙箱机制运行不完全信任的脚本很有用，即使不涉及 AI 任务。

---

## 快捷键速查表

| 快捷键 | 功能 |
|--------|------|
| `Esc`×2 | 回编辑上一条消息，从那个点 fork 会话 |
| `Ctrl+C` | 中断当前响应 |
| `Ctrl+L` | 清屏（不开新对话） |
| `Ctrl+O` | 复制最新 Codex 输出 |
| `Ctrl+R` | 历史 prompt 搜索 |
| `Ctrl+G` | 用外部编辑器编辑输入框 |
| `Tab`（任务中） | 排队下一条指令 |
| `@` | 文件模糊搜索，插入路径 |
| `!cmd` | 在 TUI 里直接执行 shell 命令 |

---

## 组合使用示例

**开发新功能的标准流程：**
```
1. 确认 AGENTS.md 里有最新的项目规范
2. codex 启动 TUI，/plan 先出方案
3. 确认后执行，途中用 Tab 排队追加指令
4. 不满意用 Esc×2 fork 到上一个节点重来
5. 完成后 /review 做一次代码审查
6. codex resume --last 下次接着昨天的进度
```

**CI 自动审查 PR：**
```bash
# .github/workflows/review.yml
- name: Codex Code Review
  run: |
    git diff origin/main...HEAD | \
    codex exec --sandbox read-only \
      --ask-for-approval never \
      -o review.md \
      - "审查这个 PR，重点关注安全问题和潜在 bug，输出 Markdown"
    cat review.md >> $GITHUB_STEP_SUMMARY
```

**云端 best-of-N 重构：**
```bash
# 让 Codex Cloud 跑 3 次，选最好的重构方案
codex cloud exec --env $ENV_ID --attempts 3 \
  "重构 auth 模块，确保测试全部通过，遵循项目里的 AGENTS.md 规范"

# 审查结果后应用
codex apply $TASK_ID
```

---

## 和 Claude Code 的主要差异

如果你两个工具都在用，这些差异值得注意：

| 特性 | Codex CLI | Claude Code |
|------|-----------|-------------|
| 持久化指令文件 | `AGENTS.md` | `CLAUDE.md` |
| 非交互执行 | `codex exec` / `codex e` | `claude -p` |
| 会话恢复 | `codex resume` | `/resume` |
| 会话分叉 | `codex fork` | `/branch` |
| 上下文压缩 | `/compact` | `/compact` |
| 云端任务 | `codex cloud` + `codex apply` | 暂无 |
| 远程 TUI | `codex app-server` + `--remote` | `/remote-control` |
| 沙箱策略 | `--sandbox` 命令行显式声明 | `/permissions` 交互式设置 |
| 输出格式约束 | `--output-schema` | 无内置支持 |

没有哪个"更好"，取决于你的工作流。本地交互式开发我两个都用；CI 里需要云端异步任务时 Codex 有优势；需要深度集成到项目工作流的定制化场景，Claude Code 的 Hooks 和 Skills 生态更成熟。
