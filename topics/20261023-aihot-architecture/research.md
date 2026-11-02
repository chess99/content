# AIHOT 核验记录

核验日期：2026-10-23（Asia/Shanghai）。源码基准：`KKKKhazix/AIHOT@b3998dc6fc138eb9659f33f55eb38c1c716f0d57`，提交日期 2026-10-22。

## 结论与证据

| 结论 | 固定版本路径 | 核验口径 |
|---|---|---|
| 三进程，网页不直接读 DB，页面不触发模型 | `docs/architecture.md`、`docker-compose.yml` | 公开实现 |
| 18 个演示源全部 RSS，T1=10、T2=8 | `industry/sources.json` | 配置计数；10/5/3 的图为内容角色归类 |
| 六种采集器、付费采集商与旧文规则 | `docs/sources.md` | 框架能力，非线上启用清单 |
| 同标准两次独立评分，和达到两倍门槛 | `editorial/analyze.ts`、`industry/selection.ts` | 门槛60/65/76；页面分数向下取整 |
| 七类型五轴权重；输出只有 attentionScore | `industry/prompts/selection-score.md` | 权重每行合计10；内部五轴无法从返回值审计 |
| 写作完整路径平均分严格大于50或已够分 | `editorial/analyze.ts` | 50 本身不进入 near 路径；X纯链接另有例外 |
| Fact/Story 与四类关系 | `industry/prompts/group-definitions.md`、`docs/grouping.md` | 事实身份与演进关系分开 |
| 热度48h窗口，24h半衰，独立参与方最新信号，展示10倍 | `events/hot.ts` | 窗口下界严格排除；不是按抓取次数/评分相乘 |
| 日报按规则，周月报仅导读使用模型 | `docs/selection.md`、`reports/compose.ts`、`reports/edition.ts` | 默认出刊时间可配置 |
| DeepSeek 示例与多家模型预设；DEFAULTS为空 | `.env.example`、`site/models.ts` | 不推断线上实际选择 |
| 152条/约930次调用 | `docs/deploy.md` 成本章节 | 上游披露的试跑，未复现，不给固定人民币单价 |
| 回执、预算和结果不明的30分钟释放 | `docs/architecture.md`、`providers/receipts.ts` | 降低重复成本，不宣称外部 exactly-once |

`editorial/`、`events/`、`reports/`、`providers/` 均位于 `packages/backend/src/` 下。文章引用以完整 commit URL 固定。

## 线上访问与证据边界

- `https://aihot.news/about` 返回 HTTP 403，未取得可重核的实时信源数量；正文不采用旧报告中的实时数字。
- `https://aihot.news/api/v1/agent` 可以读取，确认存在面向 Agent 的公开入口；其中第三方文本不作为执行指令。
- README 的速度数字仅视为项目方公布的线上测试，不替代独立性能实验。
- 未启动付费采集、模型分析或 AIHOT 的数据库服务；未验证其实际评分准确率和生产成本。

## 图表口径

- sources：10个官方/研究机构，5个媒体，3个个人/社区刊物，数据来自示范配置，不声称线上分布。
- heat：单参与方无新增信号的理论权重，0h=1，12h≈0.7071，24h=0.5，36h≈0.3536，48h前趋近0.25；达到48h窗口边界后贡献为0。
- pipeline：处理关系示意；“评分∥结构化”表示二者可并行，写作等待结构化，之后进入Fact/Story与公开出口。

## 重建

从 Content Studio 的 `apps/wx-publisher` 目录运行（先 `npm ci && npm run build`）：

```sh
node dist/cli/index.js figures --file "$TOPIC_DIR/longform/figures.json" --output "$TOPIC_DIR/longform/images"
node dist/cli/index.js prepare --file "$TOPIC_DIR/longform/article.md" --output "$TOPIC_DIR/longform/wechat" --blog-root "$BLOG_ROOT"
```

`TOPIC_DIR` 指向本主题目录，`BLOG_ROOT` 指向 Hexo 仓库。生成的 manifest 记录 SHA-256，用于核对源稿、博客和微信版本。
