# 素材清单：怎么让 AI 写出好看的网页

## 论点一：好看的页面不是 prompt 里多写几个高级形容词，而是先讨论产品气质、信息层级、交互路径和视觉方向

### 支撑素材

- **案例**：`read.cearl.cc` 的迭代前后对比。旧版截图来自 `d72fb98`，新版截图来自当前最新 commit。两版都有继续阅读、搜索、最新上架和分类列表，但新版在纸张质感、卡片层级、横向书架、底部导航和图标系统上更统一。
- **案例**：用户提供的 brainstorming 截图，展示在实现前先讨论原型和交互，而不是直接让 agent 改 CSS。
- **引用**：Lovable 官方 prompting 文档强调先规划、按组件构建、使用真实内容，并指出模糊想法会产出模糊结果。来源：https://docs.lovable.dev/prompting/prompting-one

### 反例/质疑

- 对很小的 UI 修改，完整 brainstorm 可能显得重。主笔需要说明这套流程适合“页面整体质量提升”，不是每个按钮颜色都要开会。

---

## 论点二：`brainstorming` 的价值在于把“我要一个好看的页面”拆成可以讨论、取舍、验证的设计问题

### 支撑素材

- **引用**：superpowers `brainstorming` skill 要求先探索项目上下文、提问、提出 2-3 种方案、呈现设计并获得确认，再进入实现。来源：https://github.com/obra/superpowers
- **案例**：`ai-reading` 仓库中存在 `docs/superpowers/specs/2026-05-21-mobile-nav-redesign.md` 和对应 plan，说明移动端导航不是直接开改，而是先形成规格和实施计划。
- **图片**：`/images/ai-web-design-workflow/brainstorming-example.png`

### 反例/质疑

- brainstorming 不能替代审美判断。它只是把问题暴露出来，最后仍需要人选择方向。

---

## 论点三：`frontend-design` 提供审美约束，能减少默认 AI 味

### 支撑素材

- **引用**：本地 `frontend-design` skill 强调明确视觉方向，避免 generic AI aesthetics，关注 typography、color、motion、spatial composition、background details。
- **案例**：`ai-reading` 的 `4ec8bf5 feat: 统一视觉系统并优化页面层级`、`b30ec51 style: 增强品牌层次与视觉质感`、`04dfad2 feat: redesign reading interface` 都是视觉系统和阅读体验的集中迭代节点。

### 反例/质疑

- 如果只使用“luxury / premium / sleek”等形容词，仍然可能产出模板化页面。skill 的价值在于给出具体设计维度，而不是堆风格词。

---

## 论点四：`ui-ux-pro-max` 的位置更接近产品设计师，负责交互路径、状态完整性、可访问性和移动端体验

### 支撑素材

- **案例**：`ai-reading` 后续提交包括 `9b75f14 feat: wire BottomNav, mobile sidebar-off, book Header mode`、`390e731 refactor: simplify mobile home navigation`、`1d7a4c1 fix: keep reading back navigation in app`，说明设计不是静态截图，还包括移动端导航和返回路径。
- **案例**：移动端截图素材会突出新版不只是“更漂亮”，也把继续阅读、最新上架、分类浏览放到更符合阅读场景的位置。
- **引用**：`ui-ux-pro-max` 安装路径为 `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.5.0/.claude/skills/ui-ux-pro-max/`。它的 `SKILL.md` 定位是 UI/UX design intelligence，覆盖 UI structure、visual design decisions、interaction patterns、user experience quality control。
- **引用**：`ui-ux-pro-max` 的高优先级规则包括 Accessibility、Touch & Interaction、Performance、Style Selection、Layout & Responsive、Navigation Patterns。例如触摸目标最小 44×44 / 48×48、底部导航不超过 5 项、移动端不能横向滚动、返回行为必须可预测、核心内容移动端优先。

### 反例/质疑

- `ui-ux-pro-max` 是规则库，不会替你决定产品方向；它适合在方向确定之后，把移动端交互、可访问性、导航、状态反馈这些容易被工程师漏掉的东西系统扫一遍。

---

## 论点五：业界另一条路线是先在 AI 设计平台里完成高保真设计，再把设计系统和组件约束带回代码

### 支撑素材

- **引用**：Figma Config 2025 发布 Figma Make 和 Figma Sites，强调从 idea 到 production，把 prompt-to-code、网站发布、设计能力放进同一平台。来源：https://www.figma.com/blog/config-2025-press-release/
- **引用**：Figma Make GA 文章提到可导入现有 Figma library，以保持颜色、排版和核心样式一致。来源：https://www.figma.com/blog/figma-make-general-availability/
- **引用**：Google Labs Stitch 被定位为 AI-native software design canvas，可通过自然语言创建、迭代和协作高保真 UI。来源：https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/
- **引用**：Webflow AI Site Builder 会生成 style guide，并使用 Flowkit CSS Framework、utility classes、component patterns 和 design tokens。来源：https://help.webflow.com/hc/en-us/articles/38840145286035-Build-a-site-with-Webflow-s-AI-site-builder
- **数据**：Figma 2025 AI Report 中 78% 受访者认同 AI 提升效率，但只有 32% 认为可以依赖 AI 输出。来源：https://www.figma.com/blog/figma-2025-ai-report-perspectives/

### 反例/质疑

- 设计到代码仍不是无损闭环。Figma Make 的 functional version 不能直接进入 Figma Design，Design 里的图层改动也不会自动回写 Make。
- 设计平台能快速出方向，但品牌差异、信息架构、内容真实度、性能和可访问性仍需要人审。

---

## 补充素材（备用）

- `read.cearl.cc` 当前线上站点：https://read.cearl.cc/
- `ai-reading` 代码库：`~/Notes/ai-reading`
- 前后对比素材：用户已提供两张 389×843 移动端截图，旧版为 `d72fb98`，新版为当前最新 commit。
