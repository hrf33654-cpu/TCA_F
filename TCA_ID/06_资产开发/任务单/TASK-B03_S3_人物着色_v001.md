# TCA｜TASK-B03 S3 人物着色 v001

日期：2026-10-17；阶段 B；用途：内部风格比较；状态：用户已确认 v001 人物着色参考，不是完整资产验收。

- 用户原话：“我选3，另外目前都在文档指引下开发吧”。选 S3 分块＋柔和过渡，只批准试做方向。
- 依据：资产开发指引 §5 B1／B4、§9；风格规范 CAM-01、ENV-01、ENV-02、CHR-01；总纲 R2 与正式内容边界沿用。
- 工具：内置 ImageGen；编辑；透明背景否。实际底层版本、种子、质量参数未提供，不虚构。nanobanana 可复用下文提示词与同序参考，由用户执行。
- 输入 1（编辑目标）：`06_资产开发/美术源文件/TASK-B02_人物比例/generations/tca_task_b02_p2_imagegen_v001.png`。
- 输入 2（仅右侧比例方向）：`06_资产开发/美术源文件/TASK-B02_人物比例/generations/tca_task_b02_p2_comparison_generated_v001.png`；其补绘脸／服装不作为新设定。
- 保留：镜头、环境、P2 比例方向、临时人物姿态／服装／占屏、光源方向。本轮只调整人物着色。
- 输出：同一展示板左侧完整场景、右侧生成式局部展示。局部不是像素裁切，须检查重绘偏移；场景面板缩排也不等于目标设备实际显示尺寸。
- 验收条件：大明暗分区可读；少量转折柔化；两视图人物着色一致；已批准环境与比例方向无明显漂移；无新增人物设定；用户过目后才能登记着色参考确认。
- 路线、正式角色、动画、战斗复用、精确规格待定；无工程验收。当前产物按内部比较任务归档，正式资产台账不记作成品。

## 实际提示词／nanobanana 可复用提示词

```text
Use case: precise-object-edit.
Create a TCA exploration CHARACTER SHADING STUDY S3 using the supplied references. Image 1 is the scene edit target: preserve the high oblique camera, whole landscape composition, smooth broad green grass fields, sparse edge tufts, detailed ochre dirt path, hut, rocks, fence, warm upper-left light and long cast shadows. Image 2 is supporting proportion reference ONLY: use the RIGHT figure's moderately prominent head and compact adult body; ignore its left figure. Preserve the temporary short dark hair, plain light tunic with belt, brown trousers and boots, same relaxed pose facing slightly right. No identity redesign.
Change ONLY the character surface shading into S3: broad clearly designed light and shadow color groups on shirt, hair and trousers, restrained highlights, clean readable value separation; add a narrow gentle transition on the face, forearms and a few major turning planes. Most shading must remain broad color blocks, not continuous airbrushed gradients, not faceted polygon patches, not shiny plastic. Same warm scene lighting direction and contact shadow. No added outline, costume, facial detail, symbols or accessories.
Output a landscape presentation with TWO panels separated by a narrow neutral gutter. LEFT about 70 percent width: the COMPLETE scene from image 1, same framing and relative character height around 10–11 percent of scene height. RIGHT about 30 percent: a magnified local study of the SAME newly shaded character including head to boots and nearby ground, in exactly the same high oblique angle and pose; do not turn it into a frontal portrait. Both views must show the same proportions and S3 shading. The detail view is generated illustration for subjective inspection, not a pixel crop or measured anatomy proof.
Do not change background style, global palette, camera or grass/path detail. No text, labels, rulers, UI, watermark, extra characters, weapons or animals. This is a temporary style candidate awaiting the user's review, not a final approved character or a production-ready game asset.
```

## 输出与评审

- 已生成并归档：[S3 v001 展示板](../美术源文件/TASK-B03_人物着色/generations/tca_task_b03_s3_imagegen_v001.png)，2018 × 779 PNG。状态：人物着色参考已获用户确认。
- 原件：`C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-205ecc67-13c3-40d1-a664-69599f0c29a1.png`；原件保留，副本不覆盖历史图。
- 初检：上衣、裤腿与头发出现较清楚的明暗块面，脸／手臂保留过渡；当前仍偏柔和体积，分块效果较克制，需用户判断是否够清楚。
- 主要场景布局、俯视、草地与土路观感延续；生成有局部重绘，屋顶／地面纹理与人物姿态不能视为逐像素锁定。右侧为生成式局部展示，头身和衣纹有补绘偏移，不能证明精确比例或与左图完全一致。
- 展示板是排版比较，不能替代全屏实际尺寸／战斗或引擎验证。无新增人物、装备或正式设定批准。
- 用户成图选择：回复“A”，对应保留此版着色，已记入 CHR-02。保留克制明暗块面及脸／手臂柔和过渡；不批准其他偶然细节或人物设计。
- 视觉：人物着色参考通过；完整资产视觉验收不适用。技术／正式内容／发布来源未验收。下一项为人物轮廓与线条方向，尚未选择。
