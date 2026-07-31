---
captured: 2026-08-01
title: "Claude Code之父：每半年清空一次claude.md、skills和hooks，模型自己会想办法"
author: Tina
publisher: InfoQ
source: https://mp.weixin.qq.com/s/MEUMv2mJGNcS-rGl48f5FA
original_video: https://www.youtube.com/watch?v=qyPCVqFUyDo
---

# 与“Superpowers 流程税”相关的证据摘记

本文整理了 Claude Code 创始人 Boris Cherny 的访谈。以下仅保留与本主题有关的观点，不把文章全文复制入库。

## 模型升级与旧指令

- Boris 表示，每一代模型都很不同，三个月前为旧模型设计的内容，到下一代可能已经不再适用。
- Opus 5 发布后，Claude Code 团队删除了超过 80% 的系统提示词。
- 团队会先清空系统提示词，再逐行加回来，通过消融实验判断哪些内容仍有价值。

## 给用户的建议

- Boris 建议 Claude Code 用户每隔六个月删除一次 `CLAUDE.md`、Skills 和 Hooks，看看新模型自己会怎么做。
- 第一步是删除，下一步是实际使用；不要提前猜测模型需要什么指令。
- 只有模型反复在同一件事情上出错时，才应该把相应指令加回来。

## 对过度工程化的判断

- 对现代模型，用户更应该描述目标、约束和退出标准，而不是过度规定每一步。
- Boris 认为人们经常把 Agent 想得过于复杂，并进行过度工程化。
- Skill、MCP 或其他脚手架应针对实际暴露的问题补充，而不是预先堆满。

## 与本主题的关系

这些观点佐证了“模型进步会让一部分旧脚手架贬值，Skill 需要随模型重新验证”的方向，但它们不是针对 Superpowers 或 gstack 的直接实测，也不能证明所有 Skill 都应该每半年删除。
