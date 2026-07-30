# 账号品牌资产

本目录保存跨主题、跨渠道复用的账号级品牌资产，不表示这些文件本身准备发布为笔记。

## 目录

- `BRAND.md`：工作流默认读取的唯一生效品牌入口；只记录当前已启用规则和未定状态。
- `strategy.md`：账号定位、栏目架构、主页与测试策略。
- `naming.md`：中文账号名候选评分、当前讨论状态和正式更名前检查。
- `identity.md`：Logo、字标、色彩、字体和使用规则。
- `cover-system.md`：封面母版、八类内容矩阵与 AI / 确定性版本的对照方法。
- `visual-comparison.md`：本轮 Logo 与四组封面对照的判断、限制和下一步。
- `research/xiaohongshu-benchmarks-20260728.md`：小红书对标账号、爆款笔记拆解与可执行选题。
- `assets/logo/`：AI 位图探索、SVG 母稿、头像预览和对比板。
- `assets/covers/ai/`：图片模型生成的完整构图探索稿。
- `assets/covers/deterministic/`：可精确控制中文、数据和真实素材的 SVG 样例。
- `assets/covers/cover-ai-vs-svg.*`：同题并排比较板。

## 边界

- 可编辑的母稿与最终品牌资产在这里维护一份。
- 工作流默认只读取 `BRAND.md`，再按其中的路由按需读取详细文件；研究稿和探索稿不会自动升级为正式规则。
- 所有 AI 位图均保留原始生成文件；发布时根据需要叠加确定性文字、Logo、真实 UI 与数据。
- 具体主题使用的最终封面仍放在相应内容形态目录，例如 `TOPIC_DIR/image-post/images/`。
- 通用渲染器、检查脚本和工作流放在 `D:\code\content-studio`，不放在本目录。
