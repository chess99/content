# 素材清单：Skill 的整洁之道

## 论点一：程序员 scope 扩张，时间分配变化

### 支撑素材
- **案例/数据**：
  - Andrej Karpathy（前 OpenAI、Tesla AI 负责人）提出 "vibe coding" 概念，描述程序员角色从"写代码"转向"指导 AI 写代码"
  - Kent Beck（TDD 发明者）："AI is making me 10x more productive... My job title hasn't changed but what I do all day has changed completely."
  - McKinsey "The economic potential of generative AI"（2023）：软件工程生产力提升 20-45%，同时指出"开发者时间重新分配到更高价值任务"
  - Simon Willison（Django 联合创始人）持续撰文记录个人使用 LLM 的工作方式变化，提出"LLM 是乘数，程序员变成架构师+验证者"

- **历史类比**：
  - 汇编 → 高级语言：Fortran/COBOL 出现后，程序员不再写机器指令，转而关注算法逻辑。当时也有"失业恐慌"，实际结果是需求爆炸式增长。
  - 手工运维 → DevOps/SRE：运维自动化使开发者承担了更多基础设施责任，scope 扩张的历史先例。

### 反例/质疑及回应
- **质疑**：scope 扩张也可能只是短期阵痛，最终 AI 会封装一切，程序员角色彻底消失
  - **回应**：历史类比——高级语言出现后程序员没有消失，而是 scope 上移。AI 是下一层抽象，上移规律成立。
- **质疑**：并非所有程序员都感受到 scope 扩张，初级程序员可能反而被边缘化
  - **回应**：文章聚焦的是高级工程师/架构师层面的 scope 扩张，初级程序员的处境是另一个话题，可在文章中注明边界。

---

## 论点二：SOLID 原则映射到 skill 设计

### 支撑素材
- **原始出处**：
  - Robert C. Martin（Uncle Bob），"Design Principles and Design Patterns"（2000）——SOLID 五原则系统整理
  - "Clean Architecture"（Robert C. Martin，2017）——明确将 SOLID 推广到组件和架构层面，超越 OOP 语境
  - SRP 权威诠释："A module should be responsible to one, and only one, actor."（利益相关方，而非"只做一件事"）

- **历史先例**：
  - Unix 哲学 "Do one thing and do it well"（Doug McIlroy，1978）——SRP 的前身，管道（pipe）机制是 skill 链式调用的历史原型
  - 微服务架构的 SRP 实践：Netflix、Amazon 将单体拆分为微服务，每个服务"只因一个业务原因变化"——与 skill 拆分逻辑完全一致

- **AI 特定**：
  - Anthropic 官方工具设计建议：工具应"窄而深"，职责清晰——与 SRP 吻合
  - OpenAI Function Calling 文档最佳实践：每个 function 职责单一，参数含义明确

### 反例/质疑及回应
- **质疑**：SOLID 是为 OOP 设计的，skill 是提示词驱动的，强行映射是牵强类比
  - **回应**：Uncle Bob 在 "Clean Architecture" 中已将 SOLID 推广到组件和架构层面，超越了 OOP 语境。原则的本质是"管理变化和依赖"，这在 skill 设计中同样成立。
- **质疑**：ISP 和 LSP 在 skill 场景中难以映射
  - **回应**：文章可选择性聚焦 SRP/OCP/DIP 三个映射最清晰的原则，坦承 LSP 映射较弱，这体现了诚实性。

---

## 论点三：Conway's Law 在 multi-agent 系统同样成立

### 支撑素材
- **原始出处**：
  - Melvin Conway，"How Do Committees Invent?"（1968，Datamation 杂志）原文
  - Fred Brooks 在《人月神话》中引用并传播的经典缩写版

- **经典案例**：
  - Amazon "Two-Pizza Team" 原则（Jeff Bezos）：每个微服务由一个小团队负责——组织结构决定服务边界
  - "Team Topologies"（Matthew Skelton & Manuel Pais，2019）——整本书都是 Conway's Law 的工程应用手册，提出"逆康威法则（Inverse Conway Maneuver）"
  - 哈佛商学院研究（MacCormack et al.，2008，Management Science）：对 Linux 和 Windows 内核的模块依赖图与组织架构相关性的实证研究

- **AI agent 特定**：
  - MetaGPT（2023，arXiv）：显式将 PM/Architect/Engineer/QA 等角色映射为 agent——软件公司组织结构直接映射为 agent 架构，是 Conway's Law 在 AI 场景的直接案例
  - Anthropic 的 Planner-Generator-Evaluator 架构：对应 PM-Dev-QA，三角分工
  - AutoGen（微软，2023）：agent 之间的通信结构决定任务分解方式——通信结构即架构

### 反例/质疑及回应
- **质疑**：agent 没有政治、职业利益、沟通摩擦等人类组织特性，Conway's Law 的根本机制不适用
  - **回应**：Conway's Law 更深层是"系统边界沿着信息流边界切割"。agent 的信息隔离（每个 agent 只看到部分上下文）同样产生这种效应。且设计者是人类，设计者的思维模型（往往是人类组织的映射）仍然影响架构。
- **质疑**：agent 重组成本接近零，所以 Conway's Law 的影响会消失
  - **回应**：成本低意味着可以更频繁地利用这个规律，而不是规律消失。

---

## 论点四：agent 团队重组成本接近零，架构决策频率提高

### 支撑素材
- **类比**：
  - 容器化（Docker/Kubernetes）使服务实例创建销毁成本极低，催生了微服务架构的大规模采用——低成本改变了最优架构形态
  - IaC（基础设施即代码）使云基础设施可随时替换，催生了 immutable infrastructure 范式
- **经济学视角**：
  - Ronald Coase，"The Nature of the Firm"（1937）：交易成本决定企业边界——agent 协调成本降低，细粒度分工变得合算
- **软件工程文献**：
  - Martin Fowler，"Refactoring"（1999）：重构成本低才使持续重构可行——agent 架构的"重构成本"远低于传统代码重构

### 反例/质疑及回应
- **质疑**：agent 重组成本并不接近零——修改 prompt、重新测试、验证行为稳定性都有成本
  - **回应**："接近零"是相对说法，相对于人类团队重组（招聘、培训、磨合）而言确实如此。更精确的表述是"成本量级差异巨大，决策频率可以提高一到两个数量级"。

---

## 论点五：具体范式

### 生成与验证分离
- Anthropic 官方博客的 Planner-Generator-Evaluator 架构（已有案例）
- TDD 的 Red-Green-Refactor：先写测试（验证器）再写实现（生成器）——逻辑同构
- "Constitutional AI"（Anthropic，2022）：生成-批判-修正循环
- Process Reward Models（OpenAI，"Let's Verify Step by Step"，2023）：步骤级验证器与生成器分离

### 渐进式细化
- XP（极限编程）的"Simple Design"原则：不过度设计，随需求明确逐步演进
- Fred Brooks，"Plan to Throw One Away"（《人月神话》第 11 章）：第一版必然是探索

---

## 补充素材（备用）

### 值得关注的潜在质疑
- **"SOLID 已经过时了"**：函数式编程社区认为 SOLID 是 OOP 时代的补丁。回应：skill 设计确实可以借鉴 FP 的纯函数思想（无副作用的 skill 更容易组合和测试），这是补充而非否定。
- **"prompt 工程无法像代码一样严格约束"**：自然语言的模糊性使 skill 边界比代码类的边界更难维护。这是真实挑战，需要强类型 schema、eval 测试套件等工程手段补偿。
