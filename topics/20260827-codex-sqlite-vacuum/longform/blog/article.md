---
title: Codex 日志数据库占满 C 盘：用 VACUUM INTO 找回 26GB
date: 2026-08-27 00:00:00
tags:
  - Codex
  - SQLite
  - Windows
  - 磁盘清理
categories: 工具与工作流
permalink: /posts/codex-sqlite-vacuum/
---

**导语：** 用了几个月 Codex 后，C 盘突然红了。SpaceSniffer 一扫，`.codex` 目录占了 40GB，其中 `logs_2.sqlite` 一个文件就接近 27GB。更离谱的是，库中约 97% 的页都在 freelist 里；压缩后，数据库只剩 742MB。本文记录从发现问题到用 Claude Code 一条 prompt 安全回收 26.1GB 的全过程，也解释 SQLite 为什么会出现这种现象。

> 这是一次发生在 Windows 上的真实故障处理，数据来自 2026 年 8 月 27 日的本机快照。`logs_2.sqlite` 属于 Codex 当前版本的内部文件，路径和结构以后可能变化。下面采用的是 SQLite 层面的备份压缩方案；操作前要退出 Codex、保留原库，并完成前后校验。

<!-- more -->

---

## 背景

我一直用 Codex（OpenAI 的 AI 编程助手）做日常开发。几个月下来，C 盘开始频繁告警。用 SpaceSniffer 扫描后，发现占用大头是：

```text
C:\Users\zcs\.codex\   → 40GB
  └── logs_2.sqlite    → 27GB  ← 最大单项
```

![SpaceSniffer 扫描结果：用户目录中的 .codex 约占 40.5GB](/images/codex-sqlite-vacuum/spacesniffer-codex-40gb-crop.png)

在此之前，我对 SQLite 文件膨胀几乎没有概念——不就是个日志数据库吗，能大到哪去？

## 发现过程

第一步，用 SpaceSniffer 找到大文件。第二步，用 SQLite 工具读取内部状态：

```sql
PRAGMA quick_check;       -- ok
SELECT COUNT(*) FROM logs;
PRAGMA page_size;
PRAGMA page_count;
PRAGMA freelist_count;
PRAGMA auto_vacuum;
```

原库的实测结果如下：

```text
日志行数         144,249
page_size          4,096 bytes
page_count     7,041,670
freelist_count 6,833,529
auto_vacuum             2  （INCREMENTAL）
```

空闲页占比为：

```text
6,833,529 / 7,041,670 ≈ 97.04%
```

这比简单拿“文件大小 ÷ 日志条数”更能说明问题：27GB 主要是数据库保留的历史空间，不是当前 14 万行日志真实需要的体积。

还有一个更直接的证据：

```sql
SELECT MIN(id), MAX(id), COUNT(*) FROM logs;
```

```text
MIN(id)       988,031,822
MAX(id)       993,031,063
COUNT(*)          144,249
```

`id` 是自增主键。最高 ID 已接近 10 亿，而当前只保留 14.4 万行，说明这个库经历过大量写入，旧记录也在持续淘汰。具体清理周期不影响这次判断：真正占住磁盘的是淘汰后没有及时归还给文件系统的空间。

## 问题原因

Codex 会删除超限或过期日志，SQLite 则把不再使用的整页放进 freelist，供后续写入复用；这并不等于把空间归还给 Windows。这个库启用了 `auto_vacuum=INCREMENTAL`，但只有应用主动执行 `PRAGMA incremental_vacuum`，空闲尾页才会逐步从数据库文件中移除。

我另外核对了 Codex 是否执行过这条命令。本机应用版本为 `26.818.8289.0`；公开源码固定在 commit `2c4a95736bea64256a50f7b8506bd33c181cc85a`。源码会把可写连接设置为 `INCREMENTAL`，也会在日志超限及启动维护时执行删除，但仓库中没有 `incremental_vacuum` 的调用。本机保留的 SQL 执行日志同样记录了 `PRAGMA auto_vacuum = INCREMENTAL`，没有记录 `PRAGMA incremental_vacuum`。结合原库中 683 万个 freelist 页，可以判断：Codex 删除了旧日志，却没有主动把这些空闲页归还给文件系统。

Codex 官方仓库已有对应的 [Issue #35823](https://github.com/openai/codex/issues/35823)，截至 2026 年 9 月 3 日仍处于开放状态。本文这套办法主要用于磁盘已经告急时应急回收空间；如果暂时没有空间压力，不必急着手工处理内部数据库，保持 Codex 更新并等待官方修复即可。

## 处理方式（一句话版）

当时 C 盘只剩约 3GB，不能在原盘执行普通 `VACUUM`。我改用 `VACUUM INTO` 在 D 盘生成紧凑副本，校验完整性和行数后，再替换原库。

---

## Prompt：让 Claude 帮你安全压缩

以下是经过实际验证的 prompt。可以直接复制，但要替换用户名、工具路径、日期和目标盘符：

```text
请帮我安全压缩 Codex 本地日志数据库，目标是释放 C 盘空间。

要求：

1. 先确认 Codex 已完全退出，以下进程都不存在：
   - codex.exe
   - codex-code-mode-host.exe
   如果仍有进程，不要强杀，先提醒我退出。

2. 数据库路径：
   C:\Users\<你的用户名>\.codex\logs_2.sqlite

3. SQLite 工具路径：
   <你的 sqlite3.exe 路径>
   如果找不到 sqlite3.exe，先停止并告诉我，不要换成未经确认的工具。

4. 不要直接删除数据库，也不要在 C 盘原地 VACUUM。

5. 先确认目标盘空间充足。保守起见，可用空间不要小于原数据库大小。
   压缩副本路径：
   D:\DiskCleanupBackup\<日期>\Codex\logs_2.compact.sqlite
   如果目标文件已经存在，停止并更换新文件名，不要覆盖。

6. 操作前记录以下结果：
   - PRAGMA quick_check;
   - SELECT COUNT(*) FROM logs;
   - PRAGMA page_size;
   - PRAGMA page_count;
   - PRAGMA freelist_count;
   - PRAGMA auto_vacuum;

7. 使用 SQLite 的 VACUUM INTO 在 D 盘生成压缩副本。随后对副本执行：
   - PRAGMA quick_check;
   - SELECT COUNT(*) FROM logs;
   确保完整性检查为 ok，且日志条数与原库完全一致。

8. 验证通过后：
   - 把原 logs_2.sqlite 移到备份目录；
   - 如果存在 logs_2.sqlite-wal 和 logs_2.sqlite-shm，也一起移走；
   - 把压缩副本移动到原来的 C 盘数据库路径。

9. 替换后再次执行 quick_check 和行数核对。任何一步失败，都保留或恢复原数据库。

10. 不要动 sessions、config.toml、认证文件、worktrees 等其他内容。
```

执行结果：27GB → 742MB，**释放 26.1GB**，当时的 144,249 条日志一条不少。原库也完整保留在 D 盘，随时可以回滚。

---

## 深入原理：SQLite 为什么会占住这么多空间？

### 1. SQLite 的存储模型：页（Page）

SQLite 把数据库文件划分为固定大小的页。本例的 `PRAGMA page_size` 返回 4096，也就是每页 4KB。表记录、索引和元信息都存储在页中，数据库文件大小大致等于页数乘以页大小。

```text
┌──────────────────────────────────────────────────────────────┐
│  SQLite 数据库文件（简化示意）                                │
│                                                              │
│  [Page 1]  [Page 2]  [Page 3]  ...  [Page N]                │
│   ↑         ↑         ↑               ↑                      │
│   含文件头   数据页    数据页           当前文件末尾            │
│                                                              │
│  本例文件大小 = 7,041,670 × 4KB ≈ 26.86GiB                  │
└──────────────────────────────────────────────────────────────┘
```

第 1 页的开头包含数据库文件头，后续页面用于保存表、索引和其他结构。

### 2. Freelist：删除数据不等于缩小文件

数据被删除后，已经完全不用的页可以进入 **freelist**（空闲页链表）。这些页仍在数据库文件内部，但后续写入可以再次使用。

```text
删除前：
[Page 1: used] [Page 2: used] [Page 3: used] [Page 4: used]

删除后：
[Page 1: used] [Page 2: FREE] [Page 3: FREE] [Page 4: used]
               └────────────── freelist ──────────────┘

文件仍有 4 页，但其中 2 页可以复用。
```

`freelist_count` 只统计完全空闲的页面。一个页面即使删掉了部分记录，只要还保存着有效内容，就不会计入 freelist。`VACUUM` 在重建数据库时还会整理这些未填满的页面，因此压缩结果通常比“总页数减去 freelist 页数”的估算更小。

`auto_vacuum=NONE` 会把空闲页留在文件中等待复用；`INCREMENTAL` 具备逐步回收文件尾部空闲页的能力，但要由应用主动触发。本例使用的是 `INCREMENTAL`，Codex 只启用了这种能力，没有执行实际回收所需的 `incremental_vacuum`。

### 3. 文件为什么没有跟着数据一起变小

`page_count` 对应数据库文件当前占用的页面总数。删除记录会增加 `freelist_count`，却不会直接减少 `page_count`。本例的变化过程可以概括为：

```text
持续写入日志
    ↓
数据库扩张到 7,041,670 页
    ↓
大量旧日志被淘汰
    ↓
6,833,529 页进入 freelist
    ↓
未见 Codex 执行 incremental_vacuum 回收尾页
    ↓
文件仍保持约 27GB
```

三种 auto-vacuum 模式处理空闲页的方式不同：`NONE` 保留空闲页供复用，`INCREMENTAL` 等待显式回收，`FULL` 在事务提交时尝试移动并截断尾部空闲页。本例虽然使用 `INCREMENTAL`，但 Codex 没有执行显式回收，文件因此停留在约 27GB。

### 4. Codex 日志场景为什么特别明显

从自增 ID 和保留行数看，这个库的工作负载可以概括为：

```text
高频写入日志
    +
Codex 删除旧记录
    +
未执行 incremental_vacuum
    =
当前数据不多，但数据库文件很大
```

直接成本是磁盘空间，同时整库复制、备份和安全扫描也会处理这个 27GB 文件。普通 B-tree 查询只访问相关页面，不会机械遍历全部 freelist；这里最突出的故障仍然是 C 盘被占满。

### 5. VACUUM 是怎么工作的

`VACUUM` 会重建数据库，把有效内容重新组织到一个紧凑文件中。它不仅能丢掉 freelist 页，还能整理部分填充的页，所以最终文件可能比简单计算“总页数减 freelist 页数”更小。

```text
VACUUM INTO 的概念示意：

  原库（27GB）                    新库（742MB）
  ┌──────────────┐                ┌──────────────┐
  │ Page 1: used │ ──重建──→       │ Page 1: used │
  │ Page 2: FREE │   跳过          │ Page 2: used │
  │ Page 3: FREE │   跳过          │ Page 3: used │
  │ Page 4: used │ ──重建──→       │ Page 4: used │
  │ ...          │                │ ...          │
  └──────────────┘                └──────────────┘
```

`VACUUM INTO` 会把逻辑内容写入一个全新的紧凑数据库，源库保持不变，因此也可以用于生成在线数据库备份。这次操作还包含行数核对、WAL/SHM 文件处理和原库替换。提前退出 Codex，可以避免校验期间产生新日志，也能确保不会替换一个仍在使用的数据库。

### 6. 三种空间回收方式对比

| 方案 | 原理 | 优点 | 局限 |
|------|------|------|------|
| **`VACUUM` / `VACUUM INTO`** | 重建数据库并压紧页面 | 回收彻底，也能整理部分填充页 | 大库耗时；原地 VACUUM 需要额外空间 |
| **`auto_vacuum=FULL`** | 每次事务提交时把空闲页移到文件末尾并截断 | 能持续归还尾部空闲空间 | 可能增加碎片；不会像 VACUUM 那样压紧部分填充页 |
| **`auto_vacuum=INCREMENTAL`** | 建立可移动页面所需的指针信息，再由 `incremental_vacuum` 分批回收 | 可控制单次回收量 | 不会自动执行；应用必须主动调用 |

`auto_vacuum` 模式通常在建表前确定；已有数据库也可以通过 `VACUUM` 重建后切换模式。Codex 管理着自己的内部数据库，手工改变模式可能与后续升级或应用逻辑冲突。对于这个已经使用 `INCREMENTAL` 的库，更合适的维护方式是：

1. 保持 Codex 更新，观察新版本是否改善回收行为；
2. 定期查看文件大小和 `freelist_count / page_count`，不要只看行数；
3. 只有当空闲页比例异常、磁盘压力明显时，才在退出 Codex 并完整备份后执行 `VACUUM INTO`；
4. 如果问题持续复现，向 OpenAI 反馈版本、文件大小和上述 PRAGMA 数据。

### 7. 为什么选 VACUUM INTO，而不是原地 VACUUM

普通 `VACUUM` 最坏可能需要相当于原数据库两倍的**额外可用空间**。对于一个 27GB 原库，保守估算可能还需要约 54GB 空闲空间；当时 C 盘只剩约 3GB，显然无法满足。

```text
C 盘原地 VACUUM：
  已有原库约 27GB
  最坏可能还需要约 54GB 可用空间
  当时 C 盘只剩约 3GB → 不适合

VACUUM INTO 'D:\...'：
  原库仍在 C 盘且保持不变
  紧凑副本直接生成到 D 盘
  主要新增占用发生在 D 盘
```

`VACUUM INTO` 会一直保留原库，直到新库通过校验。目标文件必须不存在或为空文件，因此每次操作都应使用新的备份文件名。

### 8. 总结

```text
┌──────────────────────────────────────────────────────────────┐
│  现象：27GB 数据库中约 97% 的页位于 freelist                 │
│                                                              │
│  原因：Codex 删除旧日志，但未见执行 incremental_vacuum      │
│                                                              │
│  处理：退出 Codex → VACUUM INTO 到 D 盘 → 校验 → 替换       │
│                                                              │
│  结果：27GB → 742MB，释放 26.1GB，并保留原库备份             │
│                                                              │
│  预防：监控空闲页比例；异常时备份后压缩，并向 OpenAI 反馈     │
└──────────────────────────────────────────────────────────────┘
```

这次留下了一套很实用的判断方法：**SQLite 文件大小不等于当前有效数据量；先测 page count 和 freelist，再决定怎么处理。**

下次 C 盘红了，别急着删文件——先看看是不是某个数据库在默默囤地。

---

## 参考资料

- [OpenAI Docs：Codex Local 的本地历史、SQLite 数据与日志](https://learn.chatgpt.com/docs/hipaa-configuration#configure-managed-requirements-and-defaults)
- [Codex 源码：SQLite 连接设置](https://github.com/openai/codex/blob/2c4a95736bea64256a50f7b8506bd33c181cc85a/codex-rs/state/src/sqlite.rs)
- [Codex 源码：日志写入、淘汰与启动维护](https://github.com/openai/codex/blob/2c4a95736bea64256a50f7b8506bd33c181cc85a/codex-rs/state/src/runtime/logs.rs)
- [Codex Issue #35823：logs_2.sqlite 未回收空闲页](https://github.com/openai/codex/issues/35823)
- [SQLite 官方文档：VACUUM](https://sqlite.org/lang_vacuum.html)
- [SQLite 官方文档：PRAGMA auto_vacuum](https://sqlite.org/pragma.html#pragma_auto_vacuum)
- [SQLite 官方文档：The Freelist](https://sqlite.org/fileformat.html#the_freelist)
