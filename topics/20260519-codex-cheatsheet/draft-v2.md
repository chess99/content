---
title: Codex CLI 速查手册：从交互对话到 CI 自动化的全部命令
date: 2026-05-19 00:00:00
tags:
  - Codex
  - OpenAI
  - AI 工具
  - 开发效率
categories: 工具
permalink: /posts/codex-cheatsheet/
---

**TL;DR**：这是一份 Codex CLI 的实用命令速查手册，与博客里已有的 [Claude Code 速查手册](/posts/claude-code-cheatsheet/) 对应。如果你已经在用 Claude Code，这篇读起来会很熟悉——两个工具解决同一类问题，但设计哲学有几处明显不同。

<!-- more -->

---

## 第一组：基础操作，先跑起来

### 启动交互会话

直接敲 `codex` 进入全屏 TUI，或者带上初始 prompt：

```bash
codex "解释一下这个代码库的结构"
codex --model gpt-5.5 "帮我设计一个任务队列"
```

会话里常用的操作：
- 按 `Tab` 在 Codex 运行时排队下一条指令（不打断当前任务）
- 按 `Enter` 打断当前任务，立即注入新指令
- `@` 打开工作区文件模糊搜索，按 Tab 插入路径
- `Ctrl+R` 搜索历史 prompt
- `Ctrl+G` 用系统编辑器（`$VISUAL` 或 `$EDITOR`）编辑当前输入框内容，适合写较长的 prompt；用 VS Code 需要设 `export VISUAL="code --wait"`，`--wait` 确保编辑完后内容能回填
- 按两下 `Esc` 走进之前的消息重新编辑，按 `Enter` 从那里 fork

---

### 沙箱策略 `--sandbox`

Codex 有三档权限：

```bash
codex --sandbox read-only          # 只读，不执行任何命令
codex --sandbox workspace-write    # 只能改工作区内的文件（推荐日常使用）
codex --sandbox danger-full-access # 不受限（慎用）
```

日常推荐 `workspace-write`，加上 `--ask-for-approval on-request`：

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

这是最平衡的配置：Codex 可以自主改代码、执行命令，但跑出工作区范围或者你不放心的操作时会暂停等你确认。

如果需要额外的写入目录，用 `--add-dir` 扩展，而不是直接升到 `danger-full-access`：

```bash
codex --cd apps/frontend --add-dir ../backend --add-dir ../shared
```

---

### AGENTS.md — 给仓库的持久化说明

在项目根目录放 `AGENTS.md`，Codex 每次启动自动读取。写项目规范、目录约定、常用命令——和 Claude Code 的 `CLAUDE.md` 是同一个思路。

```bash
codex /init  # 让 Codex 生成 AGENTS.md 初始模板
```

什么时候用：项目刚开始就建。每次你发现自己重复告诉 Codex "我们用 pnpm"、"API 前缀是 /api/v2"，写进去。

---

## 第二组：会话管理，跨天接续工作

### 恢复与 Fork 会话

Codex 在 `~/.codex/sessions/` 里存储所有会话记录。

```bash
codex resume            # 打开 picker 选一个会话继续
codex resume --last     # 直接恢复最近一次（当前目录）
codex resume --all      # 搜索所有目录的会话
codex resume <UUID>     # 指定 ID 恢复
```

想从某个会话分叉出新分支、不影响原来的记录：

```bash
codex fork --last       # Fork 最近一次会话
```

TUI 里也可以用 `/resume` 和 `/fork`。

什么时候用：开发持续多天的功能时，每天用 `--last` 接着昨天进度。`fork` 适合"我想试试另一种实现，但不想丢现在的进度"。

---

### `/compact` — 手动压缩上下文

会话做了大量工作后，上下文会撑满。`/compact` 把对话压缩成摘要，释放 token 空间：

```
/compact
```

什么时候用：用 `/status` 看到 token 接近上限时，或者开始新的大型子任务之前。压缩后 Codex 仍记得做了什么，但不再保留每一轮的原文。

---

## 第三组：审批与安全，控制 Codex 能做什么

### 审批模式 `--ask-for-approval`

```bash
codex --ask-for-approval on-request   # 遇到不确定时暂停确认（推荐交互使用）
codex --ask-for-approval never        # 全自动不问（CI 里用）
codex --ask-for-approval untrusted    # 对不在信任列表里的命令都问
```

TUI 里用 `/permissions` 随时调整。

---

### Execpolicy — 规则文件精细控制命令权限

在 `~/.codex/` 下放 `.rules` 文件，定义哪些命令允许、哪些需要确认、哪些禁止：

```bash
# 测试一条命令在规则下的判决
codex execpolicy check --rules ~/.codex/my.rules -- git push
codex execpolicy check --rules ~/.codex/my.rules --pretty -- npm publish
```

什么时候用：在 CI 或者团队共享环境里给 Codex 划清操作边界，把规则文件提交到 git 里。

---

### `--yolo` — 跳过所有审批和沙箱

```bash
codex --yolo "fix the build"
```

只在已经做好硬隔离的环境里用（Docker、VM）。在本地机器上开 `--yolo` 等于告诉 Codex 它可以做任何事。

---

## 第四组：非交互模式，脚本和 CI 集成

### `codex exec` — 非交互执行

```bash
codex exec "修复 CI 里的测试失败"
codex exec --sandbox workspace-write "生成这次 PR 的 changelog"

# 从 stdin 读 prompt
git diff HEAD~1 | codex exec -
```

加 `--json` 输出 JSONL 事件流，方便下游处理：

```bash
codex exec --json "审查安全漏洞" | jq 'select(.type=="message")'
```

把最后的回复写到文件：

```bash
codex exec --output-last-message result.md "总结今天的代码改动"
```

---

### 恢复 exec 会话

非交互任务也支持续跑：

```bash
codex exec resume --last "继续完成之前的重构"
codex exec resume <UUID> "加上我刚才说的边界条件"
```

什么时候用：CI 里跑了一半失败了，或者非交互任务做到一半你想补充指令。

---

### `--output-schema` — 结构化输出

给 Codex 一个 JSON Schema，它会确保最终输出符合这个结构：

```bash
codex exec --output-schema schema.json "分析这些函数的复杂度"
```

什么时候用：把 Codex 嵌进数据流水线，需要它输出可编程消费的 JSON 时。

---

## 第五组：模型与配置

### 切换模型

```bash
codex --model gpt-5.5 "设计数据库 schema"
codex --model gpt-4.1-mini "把这段注释翻译成英文"
```

TUI 里用 `/model` 随时切换，也可以在 `~/.codex/config.toml` 里设默认：

```toml
model = "gpt-5.5"
```

复杂任务（规划、架构设计）用 `gpt-5.5`，简单任务用 `gpt-4.1-mini`，速度快、消耗少。

---

### 配置文件 `~/.codex/config.toml`

常用配置项：

```toml
model = "gpt-5.5"
web_search = "live"    # "cached"（默认）/ "live"（实时）/ "disabled"

[tui]
theme = "dracula"
vim_mode_default = true
```

命令行 `-c key=value` 可以临时覆盖配置：

```bash
codex -c web_search=live "有没有关于这个 API 的最新文档"
```

---

### Profile — 多环境配置切换

在 `config.toml` 里定义多个 profile，按场景切换：

```toml
[profile.ci]
model = "gpt-4.1-mini"
ask_for_approval = "never"

[profile.review]
model = "gpt-5.5"
ask_for_approval = "on-request"
```

```bash
codex --profile ci "修复测试"
codex --profile review "审查这次 PR"
```

---

### Feature Flags — 实验功能管理

```bash
codex features list                    # 看有哪些 feature flag
codex features enable unified_exec     # 开启
codex features disable shell_snapshot  # 关闭

# TUI 里用 /experimental 图形化管理
```

---

## 第六组：Web 搜索

Codex 内置 Web 搜索，默认用缓存索引。加 `--search` 或设置 `web_search=live` 获取实时结果：

```bash
codex --search "这个依赖最新的稳定版是多少"
```

什么时候用：需要查最新文档、库的 breaking changes、近期的 bug 修复记录时。Codex 会在 transcript 里显示 `web_search` 条目，可以看它查了什么。

---

## 第七组：MCP 扩展工具

### 管理 MCP 服务器

```bash
codex mcp list
codex mcp add my-tool -- npx my-mcp-server
codex mcp add my-http-tool --url https://my-tool.example.com/mcp
codex mcp remove my-tool
```

也可以直接在 `~/.codex/config.toml` 里配：

```toml
[[mcp_servers]]
name = "filesystem"
command = ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
```

Session 启动时 Codex 自动连接配置好的 MCP 服务器，工具直接出现在会话里。

---

### 把 Codex 自己变成 MCP Server

```bash
codex mcp-server
```

让另一个 Agent 来调用 Codex，Codex 通过 stdio 对外提供 MCP 接口。

---

## 第八组：云端任务

### Codex Cloud

在云端跑任务，本地用命令查看和操作结果：

```bash
codex cloud                                # 交互式 picker 浏览任务
codex cloud exec --env ENV_ID "分析 bug"   # 提交任务
codex cloud list --env ENV_ID              # 查看任务列表
codex apply TASK_ID                        # 把云端 diff 应用到本地
```

加 `--attempts 3` 让 Codex 并行跑 3 次，取最好的结果：

```bash
codex cloud exec --env ENV_ID --attempts 3 "重构这个模块"
```

什么时候用：任务耗时长，不想占用本地机器；或者想用 best-of-N 来提高复杂任务的成功率。

---

## 快捷键速查表

| 快捷键 | 功能 |
|--------|------|
| `Tab`（任务运行时） | 排队下一条指令，不打断当前任务 |
| `Enter`（任务运行时） | 打断当前任务，立即注入新指令 |
| `Ctrl+R` | 搜索历史 prompt |
| `Ctrl+G` | 用外部编辑器（`$VISUAL` / `$EDITOR`）编辑当前输入 |
| `Ctrl+O` | 复制最近一次 Codex 输出 |
| `Ctrl+L` | 清屏（不重置会话） |
| `@` | 文件路径模糊搜索 |
| `Esc` 两下 | 编辑之前的消息，`Enter` 从那里 fork |
| `!` 开头 | 执行本地 shell 命令 |

---

## TUI 常用 Slash 命令速查

| 命令 | 功能 |
|------|------|
| `/model` | 切换模型 |
| `/permissions` | 调整审批和权限 |
| `/plan` | 先出计划再执行 |
| `/review` | 审查当前工作区改动 |
| `/diff` | 查看 git diff |
| `/compact` | 压缩上下文 |
| `/clear` | 清屏 + 新会话 |
| `/new` | 新会话（不清屏） |
| `/fork` | Fork 当前会话 |
| `/side` | 开临时分支会话，做完回主线 |
| `/resume` | 从 picker 恢复历史会话 |
| `/status` | 查看模型、token 用量、权限配置 |
| `/mcp` | 查看当前 session 里可用的 MCP 工具 |
| `/theme` | 换语法高亮主题 |
| `/vim` | 开关 Vim 输入模式 |
| `/fast` | 开关 Fast 服务层（如果当前模型支持） |
| `/search` | 开关实时 Web 搜索 |
| `/feedback` | 给 Codex 提 bug |
| `/quit` | 退出 |

---

## 组合使用示例

**开发新功能的标准流程：**
```
1. 确认项目里有 AGENTS.md，写好规范
2. codex --sandbox workspace-write --ask-for-approval on-request
3. /plan 描述功能需求，确认后开始执行
4. Codex 执行时用 Tab 排队下一条指令，不要打断它
5. codex resume --last 第二天接续进度
6. /review 上线前检查改动
```

**CI 里的自动化示例：**
```bash
# GitHub Actions 里自动生成 PR 描述
- name: Generate PR description
  run: |
    git diff origin/main...HEAD | \
    codex exec --sandbox read-only \
               --ask-for-approval never \
               - "根据这个 diff 生成 PR 描述，包含：改了什么、为什么改、怎么测试"
```

**让 Codex 并行跑多个方案：**
```bash
# 跑 3 个实现，选最好的一个
codex cloud exec --env my-env --attempts 3 \
  "给这个 API 加速，目标是 p99 延迟低于 50ms"
```

---

## 和 Claude Code 的关键差异

用过 Claude Code 的人看这篇会有几个地方觉得"不太一样"：

**审批模型不同。** Claude Code 的权限是白名单式（`/permissions` 配规则），Codex 是三档沙箱策略（`read-only / workspace-write / danger-full-access`）加上 execpolicy 规则文件。Codex 的沙箱是操作系统级隔离（macOS Seatbelt / Linux Landlock+seccomp / Windows 原生沙箱），Claude Code 的是应用层控制。

**会话 Fork 更突出。** Codex 把 `fork` 做成了一等公民——`codex fork`、`/fork`、双击 Esc 编辑历史消息然后 Enter fork——探索多种实现路径的工作流比 Claude Code 流畅。

**云端任务原生支持。** `codex cloud` 和 `codex apply` 让本地 CLI 和云端任务无缝联动，Claude Code 目前没有对应能力。

**配置用 TOML 不用 JSON。** `~/.codex/config.toml` vs `~/.claude/settings.json`，格式不同，但概念一一对应。
