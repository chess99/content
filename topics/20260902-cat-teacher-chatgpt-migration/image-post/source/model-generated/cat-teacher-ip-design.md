# 猫猫老师 IP 形象候选

## 当前状态

完整母标与封面小变体都仍是主题内候选。用户确认长期使用后，再迁入 `brand/assets/`。

## 核心母题

- 猫正在穿过一个有缺口的方框。
- 方框代表猫猫老师目前居住的聊天窗口。
- 身体跨过边界，代表它已经换过容器。
- 尾巴从缺口继续伸出去，代表聊天框不是终点。
- 炭黑是主体轮廓，暖橙只放在耳朵、眼睛、鼻子与尾尖，其中橙色尾尖是最稳定的识别点。

## 使用边界

- 小尺寸优先使用完整标记，不单独截取猫头。
- 保留方框缺口、穿框动作与橙色尾尖。
- 不加入机器人、芯片、线路、霓虹蓝、博士帽、眼镜、书本和教师指示棒。
- 不做宠物店式可爱 Logo，也不把猫改成幼猫或动漫角色。

## 本次封面小变体

- 文件：`cat-teacher-ip-cute-v1.png`
- 姿势：猫趴在一个看不见的边缘上，两只前爪垂下，尾巴向上弯起。
- 用法：只作为标题旁的附属视觉，可以轻微倾斜，不单独占一个展示区。
- 继承：保留黑色主体、橙色耳朵与橙色尾尖，让它能和完整母标互相认出来。
- 变化：去掉聊天框和穿框动作，让这张封面先读文字，再偶然发现猫。

## 整图生成版本

- 文件：`cover-integrated-v1.png`
- 参考：完整母标负责角色身份，小变体负责趴姿。
- 构图：标题是绝对主体；猫趴在第一行左上方，身体由字面支撑，两只爪子自然垂下。
- 结果：模型一次生成猫、标题与留白，不再把透明角色素材后期贴到文字附近。

### 整图提示词

```text
Use case: ads-marketing
Asset type: complete Xiaohongshu image-post cover, generated as one integrated composition rather than separate elements pasted together
Canvas: portrait 3:4, intended final delivery 1080 × 1440; must remain readable at 270 × 360
Input images: Image 1 is the established 猫猫老师 mascot identity reference; preserve its charcoal-black silhouette language, calm intelligent expression, warm orange inner ears and signature orange tail tip. Image 2 is a pose reference only: a cat resting with its front paws hanging down.
Primary request: create a minimal editorial cover where the text is unquestionably the main subject. Integrate a small cute variant of the referenced black cat naturally into the upper-left edge of the title. The cat is physically supported: its torso rests on the top edge of the first text line and both paws visibly drape over that edge. It must not float in empty space. The cat should feel like it belongs to the typography, not like a separate logo pasted above it.
Scene/backdrop: warm off-white empty background with generous breathing room
Visual structure: one bold two-line title, left aligned, occupying most of the visual weight; the small cat rests naturally at the upper-left of the first line. No other visual blocks or explanation.
Reading path: title first, cat discovered second
Text (verbatim, exactly these two lines):
“ChatGPT 现在可能”
“比我自己还了解我了”
Typography: very large heavy sans-serif, charcoal black, both lines identical font size and weight; the word ChatGPT must be fully visible and prominent; preserve every Chinese character exactly; no extra text
Color palette: warm off-white, charcoal black, very small amount of warm orange only on the cat
Constraints: generate the entire cover as one coherent image; cat small and secondary; clear believable contact/support between cat and title; clean normal anatomy; no floating pose; no watermark
Avoid: marketing poster styling, AI-tech aesthetics, neon blue, gradients, glows, circuits, robot cat, cards, frames, speech bubbles, decorative icons, random lines, author name, page number, logo showcase, shadows, 3D, anime, chibi, clutter, misspelled Chinese, missing characters, extra characters
```

### 小变体提示词

```text
Use case: logo-brand
Asset type: a tiny playful mascot attachment placed beside large Chinese title text on a Xiaohongshu cover
Primary request: create a cute lightweight variant of the established black cat mascot. The cat lies over an invisible edge with its chin and body resting above it, both front paws dangling below, and its tail curling upward.
Style/medium: minimal polished vector-like illustration, strong clean silhouette, expressive but restrained, suitable around 140 px
Color palette: charcoal black with warm apricot inner ears, eyes, nose and tail tip
Constraints: transparent RGBA background, no text, no frame, one cat, preserve the orange tail-tip signature, no watermark
Avoid: robot, circuitry, neon blue, hat, glasses, books, speech bubble, paw-print icon, anime, chibi proportions, 3D, background, shadow
```

## 内置图片工具提示词组

### 初始概念

```text
Use case: logo-brand
Asset type: a recurring IP mascot mark for 猫猫老师, used as a small visual signature on a Xiaohongshu cover and in future content
Primary request: design one original mascot symbol for a personal digital life that has moved across different AI systems. A calm adult cat crosses the boundary of a simple open chat-window frame. Its head and one forepaw emerge beyond the frame, while its long tail passes through a deliberate gap and continues outside.
Style/medium: minimal flat vector-like mascot mark, strong silhouette, restrained editorial design, friendly but not babyish
Color palette: charcoal black plus one muted warm apricot accent on a transparent background
Constraints: no text, one cat, readable around 80 px, original design, no watermark
Avoid: robot cat, circuitry, chips, glowing eyes, neon blue, graduation cap, glasses, books, generic speech-bubble logo, paw-print logo, anime, chibi, 3D, gradient, shadow
```

### 简化形状

```text
Radically simplify the mascot into a distinctive flat symbol while preserving the cat crossing an open frame and the tail continuing outside. Use 6 to 10 purposeful shapes, confident curves, strong negative space, tiny calm eyes, charcoal black and one muted warm apricot accent. Remove fur, realistic markings, browser buttons, large eyes, gradients, shadows and generic pet-brand styling.
```

### 表情修正

```text
Change only the cat's facial expression. Replace sharp intimidating eyes with two very small calm soft-almond eyes that feel observant, intelligent, patient and gently curious. Preserve the exact frame, gap, silhouette, body, paw, tail curve, orange tail tip, colors and composition.
```

### 背景提取

```text
Remove the entire checkerboard background and return a genuinely transparent RGBA background. Preserve the mascot exactly. Change only the background, with no halo, white box, shadow, text or watermark.
```
