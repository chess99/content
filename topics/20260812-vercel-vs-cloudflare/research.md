# 素材清单：Vercel 还是 Cloudflare？独立开发者上站怎么选

> 核对日期：2026-08-12。价格与平台能力会更新，发布前需复查。

## 论点一：两家的运行环境不同，但不能直接推导出谁更难用

### 支撑素材

- Vercel 官方说明 Node.js Runtime 支持全部 Node.js API，适合需要较大 RAM、CPU 或完整 Node.js 兼容性的函数。  
  来源：https://vercel.com/docs/functions/runtimes/node-js
- Cloudflare 官方说明 Next.js 可通过 OpenNext adapter 部署到 Workers；App Router、SSR、SSG、ISR、Server Actions、Streaming、Middleware 等大部分能力已支持。Node.js in Middleware 仍列为未支持。  
  来源：https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/
- Cloudflare 的 Next.js 部署需要 `@opennextjs/cloudflare`、`nodejs_compat` 和兼容日期。  
  来源：https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/

### 反证/限制条件

- 原生按 Workers API 开发的项目不存在“把 Node 项目兼容到 Workers”的前提。
- 采用 Next.js 不代表只能选择 Vercel；Cloudflare 官方支持面已经较完整。
- 具体 npm 包是否可用仍需逐项验证，不能从运行环境名称直接推出结论。

### 来源风险

无风险，均为官方文档；框架支持表变化较快，发布前复查。

---

## 论点二：费用差异来自计费结构，不只是月费

### 支撑素材

- Vercel Hobby 免费，但官方公平使用规则将其限制为非商业、个人用途。Pro 平台费为每月 20 美元，含一个部署席位和每月 20 美元基础设施用量抵扣；另含每月 1 TB Fast Data Transfer 和 1000 万 Edge Requests。  
  来源：https://vercel.com/docs/plans/hobby  
  来源：https://vercel.com/docs/plans/pro-plan
- Cloudflare Workers Paid 最低每月 5 美元，包含每月 1000 万次请求与 3000 万 CPU 毫秒；超出后每百万请求 0.30 美元、每百万 CPU 毫秒 0.02 美元。Workers 不额外收取数据传输或吞吐费用。  
  来源：https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare Workers Static Assets 的静态资源请求免费且不限量，也不额外收取 Assets 存储费。  
  来源：https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/

### 反证/限制条件

- Vercel Pro 的平台费包含用量抵扣和资源额度，不能简单写成“20 美元只买部署”。
- Cloudflare 的动态 Worker 请求和 CPU 仍计费；缓存命中是否调用 Worker 会改变账单。
- 具体费用取决于地区、调用方式、套餐和流量结构，本文不做统一账单测算。

### 来源风险

无风险，均为官方文档；价格必须标注核对日期。

---

## 论点三：文件和静态流量会明显改变选择

### 支撑素材

- Workers Static Assets 的静态资源请求免费且不限量。  
  来源：https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/
- R2 Standard Storage 为每 GB-month 0.015 美元，免费层含每月 10 GB-month；R2 直接向互联网传输不收出口流量费。操作次数单独计费。  
  来源：https://developers.cloudflare.com/r2/pricing/
- Vercel Functions 单次 request 或 response body 的最大载荷为 4.5 MB，官方建议大文件使用客户端直传等方案绕开函数。  
  来源：https://vercel.com/docs/functions/limitations

### 反证/限制条件

- R2 并非“完全免费”：存储、Class A 写操作和 Class B 读操作都有计费。
- 文件可以放 R2，应用继续部署在 Vercel；这不是平台二选一问题。
- 工程上即使使用 Cloudflare，也通常应让浏览器直传对象存储，避免文件经过函数中转。

### 来源风险

无风险，均为官方文档。

---

## 论点四：轻后端两边都能跑，重计算需看资源上限

### 支撑素材

- Vercel Node.js Functions 的最大内存：Hobby 2 GB，Pro/Enterprise 4 GB；Pro/Enterprise 一般最大运行 800 秒，特定版本的扩展上限为 1800 秒（beta）。函数按 active CPU 和 provisioned memory 计费，等待外部 I/O 不计入 active CPU。  
  来源：https://vercel.com/docs/functions/limitations
- Cloudflare Workers 每个 isolate 的内存上限为 128 MB；Paid 的 HTTP 请求 CPU 默认 30 秒，可提高到 5 分钟。网络请求、KV 和数据库等待不计入 CPU 时间。HTTP Worker 在客户端保持连接时没有硬性 wall-clock duration 上限。  
  来源：https://developers.cloudflare.com/workers/platform/limits/

### 反证/限制条件

- 128 MB 不等于所有 AI 应用都不适合 Workers。调用 OpenAI 等外部 API 时，大量时间属于网络等待。
- Vercel 的更高内存也不代表适合视频转码、浏览器自动化等所有重任务；此类任务可能更适合独立后端或专门计算服务。
- Cloudflare 的 CPU 上限与 wall-clock duration 是两个不同概念，正文必须区分。

### 来源风险

无风险，均为官方文档。

---

## 论点五：平台可以组合使用

### 支撑素材

- R2 提供 S3-compatible API，应用可以从其他平台调用；其对象存储和应用部署没有必须同平台的限制。  
  来源：https://developers.cloudflare.com/r2/api/s3/api/
- Vercel 支持连接外部数据库和存储，文章可以把“Vercel 应用 + R2 文件”作为架构建议，而非平台官方推荐。  
  来源类型：通用架构能力与作者建议。

### 反证/限制条件

- 跨平台会增加账号、权限、日志和费用管理入口；项目很小时不必为了理论优化强行拆分。
- 混合方案只作为文件流量明显时的选择，不设为默认架构。

### 来源风险

“组合更实用”属于作者判断，正文使用条件化表达。

---

## 原始讨论中未采用的内容

- 不提具体建站模板或产品。
- 不展开 TanStack 等框架路线。
- 不使用“Vercel 一定更省心”“Cloudflare 一定需要更多平台知识”这类无法普遍成立的判断。

