# 图片方案：Vercel 还是 Cloudflare？

## 形式

- 平台：小红书
- 数量：2 张
- 尺寸：1080×1440，3:4
- 类型：确定性排版的信息概要卡
- 视觉：暖纸白底、墨黑正文、工具与工作流蓝色强调；少装饰，不使用 Logo、作者名、页码和口号。
- 事实口径：2026-08-12；卡片不放容易过时的价格数字，正文保留核对日期。

## 第 1 张：关键差异

### 作用

让读者在一张图内理解两家的关键倾向。

### 文案

标题：

```text
Vercel 还是 Cloudflare？
先看项目需要什么
```

Vercel：

```text
Next.js 原生平台
完整 Node.js 支持更直接
更高的函数内存上限

常见场景
标准 Next.js / 完整 Node.js 依赖 / 服务端计算较重
```

Cloudflare：

```text
Workers 边缘运行环境
静态资源请求免费且不限量
R2 免互联网出口流量费

常见场景
静态资源多 / 动态逻辑轻 / 文件流量 / 多站
```

底部：

```text
两家都能上站，项目条件决定选择
```

### 证据

- Vercel Node.js Runtime、Functions Limits
- Cloudflare Workers Static Assets、R2 Pricing

## 第 2 张：决策卡

### 作用

把公众号中的场景判断压缩为可直接保存的选择表。

### 文案

标题：

```text
按这 5 个条件选
```

```text
依赖 Workers 不支持的 Node.js API
→ 先看 Vercel

静态资源多 / 动态逻辑轻
→ 先看 Workers Static Assets

图片 / PDF / 下载文件多
→ 先看 R2，应用平台另选

本地重计算 / 高内存
→ Vercel 或独立后端

主要调用数据库、支付、外部 AI API
→ 两边都可以
```

底部：

```text
没有明显偏向：选与现有代码更匹配的
```

### 证据

- `research.md` 中运行环境、文件和计算上限资料
