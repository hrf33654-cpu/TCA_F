# TASK-A01｜探索构图与人物尺度比较

**任务 ID／候选 ID：** TASK-A01／C1、C2、C3  
**任务版本／日期：** v0.1 · 2026-10-17（Asia/Shanghai）  
**任务状态：** 已立项，待用户生成  
**任务标题／负责人：** 探索斜俯视构图与人物可读尺度比较／用户生成，dsh 编写任务单、比较与记录  
**关联资产／角色：** 无正式资产 ID、无正式角色；本任务只产出比较图，不进入资产台账  
**依据文件与用户决定：** [资产开发指引清单 v0.1](../资产开发指引清单_v0.1.md) §9、§14；[总纲 R2](../../01_总纲/TCA_核心游戏设计总纲_v0.4_统一版_R2_2026-10-17.md) §01.4；[视觉参考记录 v0.2](../../05_视觉参考/探索视角与画风参考记录_2026-10-17.md)；用户 2026-10-17 选择“A和斜视角度”  
**用途／实际使用位置：** 首轮风格比较，用来定“探索画面里人物占多大、镜头多斜”；不是正式场景、不是角色设计、不是可发布素材  
**关联风格规范版本：** 尚无《美术风格规范》；本任务结果只作为候选方向  
**前置依赖与缺口：** 用户尚未确认出图界面能否上传参考图、能否选 16:9；任务单先按纯文字提示词编写，比例不可选时用最接近的横版比例并保持三张一致

## 1．任务背景

参考视频把人物压到画面高度的约 7%～8%，面部和衣纹基本不可读；TCA 是角色卡牌游戏，角色本身是内容。照搬这个尺度，角色在探索里只剩轮廓和配色可读；把人物放大，又会离开参考的观感。

用户选择 A（人物可读尺度）并要求把斜视角度一起纳入。本任务把**相机位置**作为唯一主动变量，让人物占屏与俯角一起变化，得到三个构图方向：

| 候选 | 一句话 | 人物占屏（目标） | 俯角（目标） | 画面重心 |
|---|---|---|---|---|
| **C1** | 远·高俯视，参考同款 | 约 7%～9% | 约 55°～60° | 场景与氛围 |
| **C2** | 中·中俯视，折中 | 约 14%～16% | 约 45° | 场景与角色并重 |
| **C3** | 近·低俯视，角色优先 | 约 22%～25% | 约 30°～35° | 角色 |

**重要限制：** 相机距离与俯角在真实镜头中是耦合的，所以这是一次“构图方向”比较，不是严格的单变量实验。选定方向后，再分别拆开验证俯角、距离、人物尺度和遮挡。

## 2．固定项（三张必须尽量一致）

| 项目 | 本任务固定为 | 说明 |
|---|---|---|
| 测试场景 | 简化低多边形草地空地：左侧低木栅栏，右后方圆锥顶小屋，散落石块与草丛 | **测试场景，不是 TCA 正式场景**；棚屋、围栏、草原不因此进入正式内容 |
| 测试人形 | 一个中性人形：素色短上衣与长裤、短发、面部细节最少、无元素符号／武器／配饰 | **比例尺，不是角色设计**；不进入正式名单 |
| 姿势 | 站立，手臂自然下垂，身体略朝镜头 | 三张保持一致 |
| 光照 | 左上方暖色低角度阳光，长而柔和的投影，远景轻雾 | 不新增昼夜或天气系统 |
| 色调 | 低饱和草绿、土黄、暖木棕 | 只作比较用色，不是正式色板 |
| 画幅 | 16:9 | 若工具只能出其他横版比例，三张必须一致，并在记录中注明 |
| 评审尺寸 | 1920 × 1080（评审约定，不是产品规格） | 生成图不足时放大到评审尺寸，或按比例并排查看 |
| 风格 | 风格化低多边形、简化几何、绘画性光照、不描边 | 视觉参考，不等于已选 3D 路线 |

## 3．本轮只改变

**相机位置**：距离与高度。由此同时改变人物占屏比例和俯角，不单独改人物身高、场景布局或光照方向。

## 4．提示词

### 4.1 公共前缀（英文，建议直接使用）

```text
Stylized low-poly game art, soft natural palette of muted grass green, ochre and warm wood brown, warm low-angle sunlight from the upper left, long soft shadows, light atmospheric haze, simplified geometric forms, clean large shapes, subtle surface texture, painterly lighting, no outlines. A small clearing with gently uneven grass, a low wooden fence on the left, a small hut with a conical roof in the back right, a few scattered rocks and grass tufts. One generic stylized human figure stands near the center: plain neutral tunic and trousers, short hair, minimal facial detail, no element symbols, no weapons, no accessories; the figure is only a scale reference, not a character design. The figure and the hut keep a consistent real-world scale relative to each other.
```

> 4.3～4.5 已经把这段展开成可直接复制的完整提示词；4.1 只用于你自行改写或调试前缀。

### 4.2 公共前缀（中文，便于核对，不必同时粘贴）

```text
风格化低多边形游戏美术，低饱和自然配色（草绿、土黄、暖木棕），左上方暖色低角度阳光，长而柔和的投影，远处轻微空气雾感；简化几何形体，大块面清楚，表面细节克制，偏绘画性的光照，不描边。一小片草地空地，地面略有起伏；左侧一段低木栅栏，右后方一间带圆锥形屋顶的小屋，散落几块石头和草丛。画面中央附近站着一个中性测试人形：素色短上衣与长裤，短发，面部细节最少，无元素符号、无武器、无配饰；它只是比例尺，不是角色设计。人形与小屋保持一致的现实尺度关系。
```

### 4.3 C1｜远·高俯视

```text
Stylized low-poly game art, soft natural palette of muted grass green, ochre and warm wood brown, warm low-angle sunlight from the upper left, long soft shadows, light atmospheric haze, simplified geometric forms, clean large shapes, subtle surface texture, painterly lighting, no outlines. A small clearing with gently uneven grass, a low wooden fence on the left, a small hut with a conical roof in the back right, a few scattered rocks and grass tufts. One generic stylized human figure stands near the center: plain neutral tunic and trousers, short hair, minimal facial detail, no element symbols, no weapons, no accessories; the figure is only a scale reference, not a character design. The figure and the hut keep a consistent real-world scale relative to each other.

Camera far away and high above the clearing, looking down at roughly 55–60 degrees, wide establishing shot; the figure is very small, about one-twelfth of the frame height; most of the frame is ground, fence, hut roof and long shadows.

Natural perspective camera, not orthographic, not isometric. 16:9, high quality game concept art, consistent lighting. No text, no UI, no watermark.
```

镜头句（中文核对）：相机远离并高置于空地上方，俯角约 55–60°，广角全景；人形非常小，约占画面高度的十二分之一；画面大部分是地面、栅栏、屋顶和长投影。

### 4.4 C2｜中·中俯视

```text
Stylized low-poly game art, soft natural palette of muted grass green, ochre and warm wood brown, warm low-angle sunlight from the upper left, long soft shadows, light atmospheric haze, simplified geometric forms, clean large shapes, subtle surface texture, painterly lighting, no outlines. A small clearing with gently uneven grass, a low wooden fence on the left, a small hut with a conical roof in the back right, a few scattered rocks and grass tufts. One generic stylized human figure stands near the center: plain neutral tunic and trousers, short hair, minimal facial detail, no element symbols, no weapons, no accessories; the figure is only a scale reference, not a character design. The figure and the hut keep a consistent real-world scale relative to each other.

Camera at a medium distance and medium height, looking down at roughly 45 degrees; the figure is about one-seventh of the frame height; the figure, the ground and the hut roof are all clearly visible.

Natural perspective camera, not orthographic, not isometric. 16:9, high quality game concept art, consistent lighting. No text, no UI, no watermark.
```

镜头句（中文核对）：相机处于中等距离和中等高度，俯角约 45°；人形约占画面高度的七分之一；人形、地面和屋顶都清楚可见。

### 4.5 C3｜近·低俯视

```text
Stylized low-poly game art, soft natural palette of muted grass green, ochre and warm wood brown, warm low-angle sunlight from the upper left, long soft shadows, light atmospheric haze, simplified geometric forms, clean large shapes, subtle surface texture, painterly lighting, no outlines. A small clearing with gently uneven grass, a low wooden fence on the left, a small hut with a conical roof in the back right, a few scattered rocks and grass tufts. One generic stylized human figure stands near the center: plain neutral tunic and trousers, short hair, minimal facial detail, no element symbols, no weapons, no accessories; the figure is only a scale reference, not a character design. The figure and the hut keep a consistent real-world scale relative to each other.

Camera closer and lower, looking down at roughly 30–35 degrees; the figure is about one-quarter of the frame height and is the main subject; the hut and fence recede into the background.

Natural perspective camera, not orthographic, not isometric. 16:9, high quality game concept art, consistent lighting. No text, no UI, no watermark.
```

镜头句（中文核对）：相机更近、更低，俯角约 30–35°；人形约占画面高度的四分之一，是画面主体；小屋和栅栏退到背景。

### 4.6 负面提示词

**英文：**

```text
text, letters, numbers, UI, HUD, watermark, logo, signature, multiple people, animals, extra limbs, deformed hands, photorealistic skin, dark horror, neon colors, busy clutter, fisheye, tilt-shift, orthographic, isometric, top-down map view
```

**中文：** 文字、字母、数字、UI、HUD、水印、标志、签名、多人、动物、多余肢体、畸形手、写实皮肤、恐怖暗黑、霓虹色、杂乱细节、鱼眼、移轴、正交、等距、纯俯视地图视角。

如果界面没有独立的负面提示词栏，把这段并入正文末尾，并在前面加 “Avoid:”。

## 5．生成顺序

1. **先只跑 C2。** 检查场景、人物、光照是否接近预期；如果 C2 已经明显偏离，先改公共前缀，不要急着跑 C1／C3。
2. **再用 C2 作参考跑 C1 与 C3**（如果你的界面支持参考图／图片编辑）。这样场景与人物更接近，比较“相机位置”才有效。
3. **如果界面不支持参考图**，用同一段公共前缀分别跑 C1／C2／C3，并在记录里注明“三张场景细节不完全一致，比较以构图与人物占屏为主”。

**第一轮只用一个工具**（gptimage2.5 或 googlenanobanana，选你更顺手的那个）。选定方向后，再用另一个工具跑同一张，作为工具差异对照；不要第一轮两个工具各跑三张，否则 6 张图里同时有工具和构图两个变量。

## 6．保存与命名

原始输出放入：

`06_资产开发/美术源文件/TASK-A01_探索构图与人物尺度/generations/`

建议命名：

```text
tca_task_a01_c1_<tool>_v001.<ext>
tca_task_a01_c2_<tool>_v001.<ext>
tca_task_a01_c3_<tool>_v001.<ext>
```

- `<tool>` 用 `gptimage` 或 `nanobanana`；`<ext>` 用实际格式（png／jpg／webp）。
- 同一候选重跑用 `v002`、`v003`，不要覆盖上一版。
- 保留原始输出，不要只在聊天工具里留着；聊天记录会丢。
- 如果图片在工具里被自动压缩，尽量下载原图；同时记录界面显示的实际尺寸。

## 7．用户回填区

```text
实际使用工具与界面：
生成日期与操作者：
界面可选比例／实际输出尺寸：
是否使用参考图（是／否，哪一张）：
C1 实际文件：
C2 实际文件：
C3 实际文件：
生成中遇到的问题：
主观第一印象（哪张最接近你想要的感觉，为什么）：
```

## 8．检查与比较方法

收到三张图后，dsh 会做：

1. **并排对照**：统一到 1920 × 1080 或同一缩放比例，按 C1／C2／C3 排列。
2. **人物占屏测量**：量出人物从脚底到头顶的像素高度，换算成画面高度百分比，记录实际值与目标值的偏差。
3. **缩小检查**：在 100% 和 50% 两种查看比例下，检查人物朝向、姿势、轮廓是否还能读出来。
4. **斜视角度检查**：屋顶、栅栏侧面、地面是否同时可见；有没有变成纯俯视地图或接近平视。
5. **一致性检查**：三张是否像同一个地方、同一套光照、同一个人形；偏差写进“比较限制”，不强行对齐冒充同一场景。
6. **记录三类反馈**：保留什么／改变什么／无法判断什么，分别对应到 C1／C2／C3。

## 9．本任务明确不决定

- 不决定人物头身比、五官、发型、服装、描边、着色方式或细节量。
- 不决定 TCA 的正式场景主题、建筑风格、地区、昼夜或天气系统。
- 不决定 2D／3D／混合制作路线。
- 不决定首个测试角色、14 人名单、牌表或配方。
- 不把 C1／C2／C3 中的任何一张登记为正式资产或可发布素材。

## 10．验收条件

1. 三张图都有，画幅一致，无文字、UI、水印、签名。
2. 三张都只有一个中性人形，没有多人、动物、多余肢体或明显解剖错误。
3. 三张的场景元素、人物姿势、光照方向基本一致；不一致处已记录为比较限制。
4. 人物占屏大致落在 C1 7%～9%、C2 14%～16%、C3 22%～25%；偏差超过 ±3 个百分点时记录实际值，不假装达标。
5. 斜视角度可辨：三张能看出“更远更高 → 更近更低”的连续变化。
6. 用户能据此说出“哪个方向更接近想要的感觉”，或明确指出“都还不对，缺什么”。

## 11．下一轮

- 用户选定 C1／C2／C3，或提出混合方向（例如“C2 的尺度 + C1 的俯角”）。
- 若选混合方向，下一轮拆成单变量任务：先固定尺度比俯角，或先固定俯角比尺度。
- 选定后再进入人物比例与剪影比较；到那时才引入更具体的临时角色设计。

---

**参考索引：** R-01 视频仅作风格参考，不复刻其中角色、建筑或构图；R-01～R-03 不可作为发布素材。详见[参考索引 v0.1](../参考索引/参考索引_v0.1.md)。
