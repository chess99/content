# Vercel 还是 Cloudflare？独立开发者上站怎么选

Vercel 和 Cloudflare 都能部署一个现代网站。真正会改变答案的，是你用什么技术、流量从哪里来、文件有多少，以及服务器需要做多少计算。

如果只想快速查答案，可以先看这张表。

| 项目条件 | 优先考虑 |
|---|---|
| 标准 Next.js，且依赖 Workers 尚不支持的 Node.js API 或程序包 | Vercel |
| 静态资源占比高、动态逻辑轻 | Cloudflare Workers Static Assets |
| 图片、PDF、素材下载等文件存储与分发量大 | 优先评估 R2；应用部署平台另选 |
| 服务端需要较高内存、较长计算时间 | Vercel，重任务再考虑独立后端 |
| 后端主要调用数据库、支付和外部 AI API | 两者都可以 |
| 项目没有明显偏向 | 选与现有技术栈更匹配、自己更熟悉的那个 |

## 运行环境：先看项目实际依赖什么

Vercel Functions 可以直接运行 Node.js。官方文档明确写着支持全部 Node.js API，适合依赖 Node 运行时或需要更多内存和 CPU 的函数。涉及原生二进制模块时，仍要在目标构建和运行环境中实测。

Cloudflare Workers 使用自己的运行环境。它已经提供了相当完整的 Node.js 兼容层，也可以通过 OpenNext 部署 Next.js。Cloudflare 当前列出的支持范围包括 App Router、SSR、SSG、ISR、Server Actions、Streaming 和 Middleware 等大部分常用能力；Node.js Middleware 仍在未支持列表里。

因此，“Next.js 只能部署到 Vercel”已经过时，“Next.js 放到 Cloudflare 肯定更麻烦”也太笼统。可以用三个问题判断：

- 项目是否依赖 Workers 尚不支持的 Node.js API，或已经验证无法在 Workers/OpenNext 运行的程序包？
- 所用框架是否有成熟的 Workers 部署方式？
- 本地预览和线上运行时是否已经验证一致？

标准 Next.js 项目放到 Vercel，路径最直接。项目原本就按 Workers API 开发，Cloudflare 同样直接。只有现有代码明显依赖 Node.js，而部署目标又是 Workers 时，兼容性才会成为需要单独检查的工作。

## 费用：月费只是第一行

截至 2026 年 8 月，Vercel Hobby 免费，但官方将它限定为非商业的个人用途。商业项目通常要看 Pro：平台费每月 20 美元，包含一个可部署席位、20 美元的基础设施用量抵扣，以及每月 1 TB Fast Data Transfer 和 1000 万 Edge Requests。

Cloudflare Workers Paid 最低每月 5 美元，包含每月 1000 万次 Worker 请求和 3000 万 CPU 毫秒。超出后，每百万请求 0.30 美元，每百万 CPU 毫秒 0.02 美元。Workers 不另收数据传输或吞吐费用。由 Workers Static Assets 直接提供的静态资源请求免费且不限量；SSR 或配置为先执行 Worker 脚本的请求仍按 Workers 规则计算。

这些数字说明的是计费结构，不能单独证明某个平台一定更便宜。

一个访问量不大的商业 SaaS，Vercel 的固定起步费用更高，但 Pro 也包含用量抵扣、流量额度和预览部署等平台能力。一个静态页面多、请求量大、动态计算少的网站，Cloudflare 的静态资源规则更容易体现优势。

所以比较费用时，至少要分开看四项：固定月费、动态请求和计算时间、静态资源访问、文件存储及出口流量。

只比较“20 美元和 5 美元”，很容易把项目真正会产生的费用漏掉。

## 文件多时，Cloudflare 的优势更具体

如果产品会产生大量图片、PDF、音频、视频或下载文件，Cloudflare R2 值得单独看。

R2 Standard Storage 当前价格是每 GB-month 0.015 美元，免费层包含每月 10 GB-month。它直接向互联网传输文件时不收出口流量费，但存储、写入和读取操作仍有各自的计费规则。

这类产品常见的组合是：网站和 API 放在 Vercel 或 Cloudflare Workers，文件放在 Cloudflare R2，数据库根据业务另外选择。

选了 Vercel，并不需要把文件也放进 Vercel 的存储产品。反过来也一样，使用 R2 不要求应用必须运行在 Workers。

文件上传还要注意函数入口限制。Vercel Functions 当前的 request 或 response body 最大为 4.5 MB。大文件通常应该由浏览器通过签名地址直传对象存储，避免先经过函数再转存。这个做法在两家平台上都适用。

## 轻后端两边都行，重计算要看资源上限

很多 AI 产品的服务端工作很轻：验证用户、查数据库、调用支付接口、等待 OpenAI 或其他模型返回结果。网络等待不算 Cloudflare Workers 的 CPU 时间；Vercel 的活跃 CPU 时间计费同样不计算等待外部 I/O 的时间。这样的后端放在两边都成立。

差异会在服务器自己干重活时放大。

Cloudflare Workers 每个隔离实例（isolate）的内存上限是 128 MB。Paid 方案中，单次 HTTP 请求的 CPU 时间默认是 30 秒，可调高到 5 分钟。HTTP 请求的墙钟时间，也就是包含等待在内的总耗时，没有固定硬上限，只要客户端仍保持连接。它不适合被当作可靠的无限长任务机制：连接中断、运行时更新以及 CPU、内存上限仍可能终止执行。

Vercel Node.js Functions 的上限更接近传统服务器函数：Hobby 最大 2 GB 内存，Pro 和 Enterprise 最大 4 GB。Pro 的常规最长运行时间可以配置到 800 秒；特定 Node.js 和 Python 运行时可配置到 1800 秒，这项扩展能力仍处于 beta。

如果服务端需要本地处理大图、加载大量数据、生成复杂 PDF，Vercel 的空间更大。视频转码、浏览器自动化和持续占用大量 CPU 的任务，即使能塞进函数，也未必适合这两种 Web 函数平台；独立后端或专门的计算服务通常更合适。

## 一个混合案例：Next.js 应用加文件产品

假设你做的是标准 Next.js 应用，某个支付或鉴权依赖已经确认需要完整 Node.js 运行时，同时产品会生成大量图片和 PDF。

应用可以放在 Vercel，浏览器通过签名地址把文件直接上传到 R2，下载也从 R2 提供。这个组合分别满足了运行环境和文件分发的条件。它也会增加一个账号和一套权限管理，所以文件量还很小时，没有必要提前拆分。

## 用五个问题结束选择

打开你的项目，逐项回答：

1. 是否明确依赖 Workers 尚不支持的 Node.js API，或已有程序包经过验证无法在 Workers/OpenNext 运行？
2. 访问主要命中静态页面，还是每次都要执行动态逻辑？
3. 是否会长期保存和分发大量图片、PDF、音视频或下载文件？
4. 服务端主要等待外部 API，还是自己做高内存、长时间计算？
5. 现在维护一个产品，还是准备维护一组结构相似的小站？

第一项很突出，先看 Vercel。第二项更突出，先看 Workers Static Assets；第三项更突出，优先评估 R2，应用平台仍按运行环境选择。第四项如果属于外部 API 等待，两边都能选；如果属于本地重计算，优先检查 Vercel 的资源上限，再判断是否需要独立后端。维护多个小站时，再把统一管理和总体费用纳入判断。

平台选择也可以暂时不做满。先部署应用，文件用量上来后再接 R2；或者先用 Cloudflare 承载内容站，把少量复杂计算交给其他服务。

项目还没有真实用户时，选一个与当前代码匹配的平台上线。等流量、账单和故障真的出现，再用数据调整。

> 文中价格和限制核对于 2026-08-12。平台规则更新较快，做最终决定前请再查看官方文档。

## 参考资料

- Vercel：Using the Node.js Runtime with Vercel Functions  
  https://vercel.com/docs/functions/runtimes/node-js
- Vercel：Functions Limits  
  https://vercel.com/docs/functions/limitations
- Vercel：Pro Plan  
  https://vercel.com/docs/plans/pro-plan
- Vercel：Hobby Plan  
  https://vercel.com/docs/plans/hobby
- Cloudflare：Workers Pricing  
  https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare：Workers Limits  
  https://developers.cloudflare.com/workers/platform/limits/
- Cloudflare：Next.js on Workers  
  https://developers.cloudflare.com/workers/framework-guides/web-apps/nextjs/
- Cloudflare：Static Assets Billing and Limitations  
  https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/
- Cloudflare：R2 Pricing  
  https://developers.cloudflare.com/r2/pricing/

