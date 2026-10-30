# TASK-B02｜P2 约 5 头身临时人形 v001

日期：2026-10-17（Asia/Shanghai）  
状态：用户选择局部对照右侧 P2 比例方向作为参考。局部对照含重绘，不是精确裁切或测量证据；不代表正式人物规格全面通过。  
用户原话：“2”，对应 P2 约 5 头身；确认先试该候选，不是批准正式人物规格。

## 范围与检查

- 编辑目标：[TASK-B01 D2 v003](../美术源文件/TASK-B01_场景细节密度/generations/tca_task_b01_d2_imagegen_v003.png)，已实际查看。
- 只改临时人形的头部与身体相对比例；约 5 头身是站直时冠顶到脚底的解剖比例意图，不以高俯视投影的可见长度直接相除断言达标。
- 固定：CAM-01 镜头、人物约占屏高 10% 及脚底位置、短发／素上衣／棕裤／靴／姿态、ENV-01 草地、ENV-02 土路、场景布局与暖光。人物服装等只是控变量条件，非正式设定。
- 人形无元素身份、正式角色 ID 或名单归属；不依据“二次元”标签附加大眼、描边或特定着色方案。
- 检查：头部是否相对突出、四肢适度紧凑但仍为成人印象；人物总占屏不增大；背景及已确认镜头／地表不明显漂移；小尺寸能否读出比例差别。
- 局限：实际原图人形仅约 90px 高，高俯视角存在缩短，难以精确验证 5 头身；必要时另制明确标注的比例设计图，不能以场景图假称规格达标。
- 工具：内置 ImageGen 编辑，透明背景否；目标 16:9；实际尺寸待输出登记；质量／种子／底层模型版本未提供。
- 本任务为内部比例比较，无技术、正式内容或来源验收通过声明。

## 实际提示词／nanobanana 提示词（需附 D2 v003）

```text
Use case: identity-preserve / precise-object-edit.
Edit ONLY the single temporary human in the supplied TCA exploration image into a FIVE-HEAD-TALL stylized adult proportion study (P2). Five-head-tall refers to the anatomical unprojected standing body from crown to soles being about five head-heights, NOT five visible heads stacked in this oblique camera projection. Keep an adult impression; do not turn into a child or toddler.
Make the head moderately larger relative to the torso and limbs than in the reference, with a compact body and appropriately shortened limbs so total anatomy is about five head units. Preserve the same short dark hair, minimal facial design, plain light neutral tunic, brown trousers, simple boots, bare hands and relaxed standing pose facing slightly right. No new eyes style, accessories, weapons, emblems or character lore. This is a generic temporary scale figure, not a named or approved character.
Maintain the SAME overall screen-space head-to-sole height, about 10 percent of the full image height, same central ground contact point and similar center position. Do NOT enlarge the whole person to make the head readable. No chibi 2-head body, no 7–8-head fashion proportions.
LOCK the entire background and camera: same approved high oblique downward view, 16:9 landscape frame, same hut roof projection and position, fence left, paths and boulders, smooth broad green lawn WITHOUT continuous microtexture, isolated edge grass tufts, existing detailed ochre dirt path, warm upper-left sunlight, same long shadows and palette. Change the person's shadow only as naturally required for the new proportions, retain its direction and grounded contact.
Finished coherent stylized game concept rendering. Preserve the source rendering and lighting on the figure, no restyling to ink outlines, no changing face or clothes to an anime costume. No text, labels, comparison dividers, rulers, UI, watermark, extra people or animals. Output the full scene, not a portrait or close-up. User must review this proportion candidate; no final design approval is implied.
```

## 输出与评审

- 输出：[P2 场景候选 v001](../美术源文件/TASK-B02_人物比例/generations/tca_task_b02_p2_imagegen_v001.png)，1672 × 941 PNG；工具原件保留于 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-2f56ede3-241f-4c57-85e6-342db40554f2.png`。
- 初检：头部较输入略突出，身体较紧凑，短发、素上衣、棕裤和姿态基本保留；已确认的镜头、草地／土路观感和主要布局延续。
- 偏差与限制：人形约高 100px，占屏约 11%（看图估读），比输入约 10% 略大，控变量不完全成功；人物与背景有轻微重绘，变化较细微。高俯视场景图不能精确证明约 5 头身；不把提示词目标写为已验证规格。
- 补充对照：已用内置 ImageGen 制作 [生成式局部对照](../美术源文件/TASK-B02_人物比例/generations/tca_task_b02_p2_comparison_generated_v001.png)，左为原人形、右为 P2。生成过程补绘了脸、发型、衣纹和局部材质，不是原像素精确放大；只帮助观察候选方向，不用于证明精确头身比，也不批准补绘细节。
- 对照原件：`C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-3565e5db-718a-4310-bd18-d80a17119bda.png`，保留原件。

## 生成式局部对照实际提示词

```text
Create a simple two-panel magnified visual comparison of the central standing human in the two supplied images. LEFT panel = human from image 1 (previous figure), RIGHT panel = human from image 2 (P2 candidate). Both are local zoom views from the SAME high-oblique scene angle, NOT new frontal character illustrations. Crop a small equal-size region around each figure including head, feet, nearby ochre ground, and the start of their cast shadow, then enlarge to equal viewing magnification, placing side by side. Preserve each source figure's actual apparent head/body proportions and pose, hair, face detail, clothing, lighting and nearby ground; do not invent face features, redraw a more attractive character, normalize away the difference, add anatomy or change camera to front view. Preserve the slightly larger total person screen height of image 2 if present, rather than misleadingly matching heights. Neutral narrow divider only. No rulers, numbers, labels, text, UI or watermark. This is a generated zoom comparison for subjective visual inspection, not anatomical measurement evidence. High fidelity to the two original local human appearances is the priority.
```

输入依次为 D2 v003、P2 场景 v001；透明背景否。输出 1536 × 1024（图像展示尺寸），未进行精确比例测量。实际结果出现补绘，按上文限制使用。
- 用户成图选择：2026-10-17 回复“A”，保留右侧 P2 比例方向，记入 CHR-01。确认头部适度突出、身体紧凑的观感；精确 5 头身、脸部／发型／服装、人物占屏、正式身份及技术路线未因此批准。
