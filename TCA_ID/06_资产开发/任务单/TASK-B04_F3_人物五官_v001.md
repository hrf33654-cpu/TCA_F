# TCA｜TASK-B04 F3 人物五官 v001

日期：2026-10-17；阶段 B；状态：C／F3 方向已选，v001 成图待用户评审；用途：内部风格比较。

- 用户原话：“C”，对应精细动漫五官；只批准试做，成图仍由用户选择。
- 依据：指引 §5 B1／B4、§9；风格规范 CHR-01 比例方向、CHR-02 S3 着色、CHR-03 无描边，镜头及环境沿用 CAM-01／ENV-01／ENV-02；正式内容与总纲 R2 不变。
- 输入：`06_资产开发/美术源文件/TASK-B03_人物着色/generations/tca_task_b03_s3_imagegen_v001.png`；左侧为场景来源，右侧为临时人物观察来源。
- 唯一主变量：五官概括程度。大眼、可辨虹膜／瞳孔／眼睑，鼻口简洁，保留中性表情。临时沿用原人物发型、肤色与衣服，不将其作为正式身份设定；虹膜用现有低饱和深色范围作测试，不确定正式瞳色。
- 输出：上方同尺度同观察角度的原简化五官／F3 五官两幅头肩比较，下方既有俯视场景应用。上方为生成式观察稿，并非像素裁切或新探索镜头；下方须保留原占屏关系，不放大人物伪装五官可读。
- 检查条件：F3 眼形、虹膜和眼睑可辨；鼻口仍简洁；S3 与无外描边保持；临时人物整体观感连续；探索场景构图和环境不明显改变；如补绘／比例／材质偏移须记录，不宣称严格控变量成功。
- 工具：内置 ImageGen 编辑，透明背景否。种子、质量、底层模型版本未提供；尺寸以输出为准。下列提示词与同一输入可交给用户在 nanobanana 执行。
- 制作路线、正式人设／角色名单、战斗复用、动画和精确规格待定，无 Godot 操作。内部比较归档，不登记为生产成品。

## 实际提示词／nanobanana 可复用提示词

```text
Use case: precise-object-edit.
Create a TCA F3 detailed anime facial-feature STYLE CANDIDATE study based on the supplied reference presentation. The reference left section is the exploration scene, reference right section shows the same temporary figure. This figure is a placeholder, not a designed official character.
Change ONLY facial feature treatment: larger expressive anime-shaped eyes, clearly legible iris and pupil, controlled small eye catchlight, a clean upper eyelid shape and readable eyebrows; simplify nose and mouth. Preserve the existing neutral expression, short dark hair silhouette and color, skin tone, head size, compact body proportions, plain light shirt, belt, brown trousers and boots. Do not turn into a child or redesign hairstyle, identity or costume. Keep features tasteful, no makeup, ornamental lashes or additional accessories. Iris uses a subdued dark tone consistent with the existing placeholder palette, not a new character color identity.
Retain approved S3 broad but restrained light/shadow blocks and soft transitions on face and arms. NO ink outline around head, body, clothing or facial silhouette; eyelids and brows are local facial features, not a global outlining style. Avoid photorealistic skin detail, glossy doll skin and flat line-art cel illustration. Integrate detailed anime facial proportions into the existing soft volumetric game-art appearance.
Compose ONE landscape study sheet: upper half has TWO equal-size head-and-shoulder views at exactly the same mild three-quarter observation angle and magnification, LEFT the original simple-feature treatment from the supplied temporary figure, RIGHT the new F3 treatment. Keep the original face structure and expression as closely as possible; only increase facial feature detail and anime eye shape. These are freshly generated observation studies, not exact source crops. Match hair, lighting and shirt between both views.
Lower half: the COMPLETE exploration scene corresponding to the reference LEFT scene, with only the central figure's face updated to the same F3 treatment. Keep the approved HIGH OBLIQUE downward exploration camera, full scene framing and relative person height around 10–11 percent within that scene. Do not raise the head or enlarge the person to expose the face. Preserve the hut upper right, fence left, rocks, detailed ochre paths, broad smooth green grass without continuous microtexture, edge tufts, warm upper-left sun and long shadows. Tiny facial details should naturally become hard to see at exploration scale; never enlarge eyes unnaturally just for this panel.
Clean narrow neutral gutters only. No writing, letters, panel labels, UI, watermark, extra people, weapons or new objects. The upper observation camera is only for inspecting facial styling; it does not replace the approved exploration camera. All outcomes await user review; this sheet proves no precise anatomy, 3D consistency, engine or production readiness.
```

## 输出与评审

- 输出：[F3 v001 展示板](../美术源文件/TASK-B04_人物五官/generations/tca_task_b04_f3_imagegen_v001.png)；工具原件 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-c773aeef-7dda-4859-886e-868e410384f1.png`，原件保留。
- 版面：上左简化五官、上右 F3、下方探索应用。右上眼睛增大，有深色虹膜、瞳孔与眼睑线，鼻口较简洁；未新增人物外描边。
- 偏移：上左也是补绘，不是原图精确放大；两侧眉眼表情、脸部轮廓与衣纹存在变化，右侧略显年轻，不能称作严格只改眼睛或批准年龄。展示角度仍较俯，不能证明正面与跨视角设计一致。
- 场景应用：人物仍小，虹膜等细节不可清楚辨认；下方面板比例与取景发生变化，建筑／栅栏边缘与原参考不完全相同。只帮助观察风格融合，不作为新 CAM-01 或全景构图批准，也不代表真实设备尺寸验证。
- 用户下一步：A 保留右上五官方向／B 眼睛更大、动漫感更明显／C 眼睛稍收小，保留虹膜与眼睑细节。尚无成图选择，不进入后续人物设计决定。
- 视觉待用户确认；技术、正式内容与发布来源未验收。比例、着色和无描边继续以原已批准参考为准，不由本次偶然偏移覆盖。

- 实际输出尺寸：2017 × 780 PNG。

## 后续修改

- 用户回复“C”，要求眼睛稍收小但保留虹膜／眼睑；已另建 [v002 任务](TASK-B04_F3_人物五官_v002.md)，v001 未获批准，原图保留以便对照。
