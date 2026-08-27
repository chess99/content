# Codex 吃了我 40GB C 盘？用 Claude 一条 Prompt 找回 26GB

**导语：** 用了几个月 Codex 后，C 盘突然红了。SpaceSniffer 一扫，`.codex` 目录占了 40GB，其中 `logs_2.sqlite` 一个文件就接近 27GB。更离谱的是，库中约 97% 的页都在 freelist 里；压缩后，数据库只剩 742MB。本文记录从发现问题到用 Claude Code 一条 prompt 安全回收 26.1GB 的全过程，也解释 SQLite 为什么会出现这种现象。

> 本文记录的是 Windows 上一次真实故障处理，数据来自 2026 年 8 月 27 日的本机快照。`logs_2.sqlite` 是当前版本 Codex 的内部文件名，未来版本可能调整。OpenAI 官方文档确认 Codex 本地会保存 SQLite 数据和日志，但没有把本文的压缩流程列为官方维护步骤；因此，动手前一定要退出 Codex、保留原库，并做好校验。

---

## 背景

我一直用 Codex（OpenAI 的 AI 编程助手）做日常开发。几个月下来，C 盘开始频繁告警。用 SpaceSniffer 扫描后，发现占用大头是：

```text
C:\Users\zcs\.codex\   → 40GB
  └── logs_2.sqlite    → 27GB  ← 最大单项
```

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

`id` 是自增主键。最高 ID 已接近 10 亿，而当前只保留 14.4 万行，说明这个库经历过非常高频的写入和淘汰。至于 Codex 内部具体按什么周期、什么条件清日志，OpenAI Docs 没有公开说明；本文只描述从数据库快照能够确认的事实。

## 问题原因（一句话版）

删除日志后，SQLite 把不再使用的整页放进 freelist，供以后复用；这并不等于把空间立刻归还给 Windows。这个库虽然启用了 `auto_vacuum=INCREMENTAL`，但只有应用主动执行 `PRAGMA incremental_vacuum`，空闲尾页才会逐步返还给文件系统。实测的 683 万个 freelist 页说明，空间回收明显没有跟上日志淘汰。

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

SQLite 的页编号从 1 开始；第 1 页的开头包含数据库文件头，并不存在“Page 0”。

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

需要注意两点：

1. 不是每次 `DELETE` 或 `UPDATE` 都会释放完整页面；页面里可能只空出一部分。
2. `UPDATE` 也不能简单概括为“DELETE + INSERT”，SQLite 可能原地更新，也可能因为记录尺寸变化而搬移内容。

在 `auto_vacuum=NONE` 的数据库中，删除后文件通常保持原大小；空闲页只留在 freelist 中等待复用。本例不是 `NONE`，而是 `INCREMENTAL`，但它同样不会自动完成空间回收。

### 3. 文件页数：一个更准确的“高水位”类比

可以把数据库文件曾经扩张到的页数理解成一种“高水位”，但它只是帮助理解的类比，不是 SQLite 单独维护、永不回退的官方字段。

本例可以这样理解：

```text
持续写入日志
    ↓
数据库扩张到 7,041,670 页
    ↓
大量旧日志被淘汰
    ↓
6,833,529 页进入 freelist
    ↓
没有足量的 incremental_vacuum 回收尾页
    ↓
文件仍保持约 27GB
```

默认的 `auto_vacuum=NONE`、本例的 `INCREMENTAL`，以及 `FULL` 模式行为并不相同，所以“SQLite 文件永远只增不减”说得太绝对。更准确的表述是：**如果没有 `VACUUM`，也没有 FULL auto-vacuum 或显式的 incremental vacuum 把尾部空闲页截掉，删除数据通常不会让文件同步缩小。**

### 4. Codex 日志场景为什么特别明显

从自增 ID 和保留行数看，这个库的工作负载可以概括为：

```text
高频写入日志
    +
大量旧记录被淘汰
    +
空闲页回收速度没有跟上
    =
当前数据不多，但数据库文件很大
```

最确定的副作用是占满磁盘，同时增加整库复制、备份和安全扫描的成本。不能仅凭“文件有 27GB”就断言普通查询一定会扫描全部 27GB：B-tree 查询不会机械遍历每个 freelist 页，操作系统的内存映射也通常按需载入页面。

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

SQLite 官方文档把 `VACUUM INTO` 描述为生成“逻辑内容相同、且已经完全 vacuum”的新数据库。源库不会被修改，新库直接写入指定路径。它不是针对源数据库的写操作，官方甚至把它列为生成在线数据库备份的一种方式。

不过，我们这里不只是生成备份，后面还要核对行数、搬走 WAL/SHM 文件并替换原库。为了避免校验期间又有新日志写入，也避免替换活跃数据库，仍然应当先完全退出 Codex。

### 6. 三种空间回收方式对比

| 方案 | 原理 | 优点 | 局限 |
|------|------|------|------|
| **`VACUUM` / `VACUUM INTO`** | 重建数据库并压紧页面 | 回收彻底，也能整理部分填充页 | 需要锁；大库耗时；原地 VACUUM 需要额外空间 |
| **`auto_vacuum=FULL`** | 每次事务提交时把空闲页移到文件末尾并截断 | 能持续归还尾部空闲空间 | 可能增加碎片；不会像 VACUUM 那样压紧部分填充页 |
| **`auto_vacuum=INCREMENTAL`** | 建立可移动页面所需的指针信息，再由 `incremental_vacuum` 分批回收 | 可控制单次回收量 | 不会自动执行；应用必须主动调用 |

另一个容易写错的点是：从 `NONE` 切换到 `FULL` 或 `INCREMENTAL`，通常要在建表前设置，或者通过一次 `VACUUM` 重建数据库；并非创建后永远不能改。

本例原库已经是 `INCREMENTAL`。因此，比“强行修改 Codex 数据库模式”更稳妥的做法是：

1. 保持 Codex 更新，观察新版本是否改善回收行为；
2. 定期查看文件大小和 `freelist_count / page_count`，不要只看行数；
3. 只有当空闲页比例异常、磁盘压力明显时，才在退出 Codex 并完整备份后执行 `VACUUM INTO`；
4. 如果问题持续复现，向 OpenAI 反馈版本、文件大小和上述 PRAGMA 数据。

### 7. 为什么选 VACUUM INTO，而不是原地 VACUUM

SQLite 官方文档说明，普通 `VACUUM` 最坏可能需要相当于原数据库两倍的**额外可用空间**。因此，对一个 27GB 原库，保守估算可能还需要约 54GB 空闲空间；当时 C 盘只剩约 3GB，显然无法满足。

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

`VACUUM INTO` 的另一个安全优势是：在校验新库之前，原库一直保留。需要注意，目标文件必须不存在或是空文件；因此脚本不应静默覆盖旧备份。

### 8. 总结

```text
┌──────────────────────────────────────────────────────────────┐
│  现象：27GB 数据库中约 97% 的页位于 freelist                 │
│                                                              │
│  实测：auto_vacuum=INCREMENTAL，但空间回收没有跟上日志淘汰   │
│                                                              │
│  处理：退出 Codex → VACUUM INTO 到 D 盘 → 校验 → 替换       │
│                                                              │
│  结果：27GB → 742MB，释放 26.1GB，并保留原库备份             │
│                                                              │
│  预防：监控空闲页比例；异常时备份后压缩，并向 OpenAI 反馈     │
└──────────────────────────────────────────────────────────────┘
```

这次最大的教训不是“看到 SQLite 就定期 VACUUM”，而是：**SQLite 文件大小不等于当前有效数据量；先测 page count 和 freelist，再决定怎么处理。**

下次 C 盘红了，别急着删文件——先看看是不是某个数据库在默默囤地。

---

## 参考资料

- [OpenAI Docs：Codex Local 的本地历史、SQLite 数据与日志](https://learn.chatgpt.com/docs/hipaa-configuration#configure-managed-requirements-and-defaults)
- [SQLite 官方文档：VACUUM](https://sqlite.org/lang_vacuum.html)
- [SQLite 官方文档：PRAGMA auto_vacuum](https://sqlite.org/pragma.html#pragma_auto_vacuum)
- [SQLite 官方文档：The Freelist](https://sqlite.org/fileformat.html#the_freelist)

*本文所述操作于 2026 年 8 月 27 日完成，使用 Claude Code 执行。原数据库 27GB，压缩后 742MB，释放约 26.1GB C 盘空间。原库备份保留在 `D:\DiskCleanupBackup\2026-08-26\Codex\original\`。*
