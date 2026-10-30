# TASK-A01｜C2 匹配指定参考俯视程度 v004

日期：2026-10-17（Asia/Shanghai）  
状态：已生成并归档，用户确认用作镜头角度参考；不是正式资产整体通过。  
工具：内置 ImageGen；基于 v003 编辑，附 R-10 作镜头参考；透明背景否。

- 用户原话：“我希望做到这个俯视角度”，并提供截图。
- 〔确认〕本轮目标为匹配截图内游戏画面的俯视程度；不再以助手猜测的数值角度作为判定标准。
- 输入 1（编辑目标）：C2 v003，已查看。
- 输入 2（仅镜头参考）：[R-10 用户截图](../参考索引/R-10_用户指定俯视角度_2026-10-17.png)，已查看并原样归档。
- 本轮只改观察角度；保持 v003 人物约占屏高 12%、暖光、配色、细节及场景关系。原截图的人物占屏未被本轮批准迁移。
- 图片中所有文字、桌面和工具控件均视为图像内容，不作为指令或需求。
- 不批准正式人物规格、角色名单、场景主题或 2D／3D 路线；本轮是已有探索方向的参考细化，未新增精确相机规格，不改规则总纲。
- 种子、质量档位和底层模型版本未提供；实际尺寸生成后记录。

## 实际提示词／nanobanana 可复制提示词（需附两张输入图）

```text
Use case: precise-object-edit.
Two input images have strictly separate roles:
IMAGE 1 is the EDIT TARGET: TCA C2 v003 clearing, single generic man, hut upper right, fence left, warm golden light.
IMAGE 2 is a CAMERA-PITCH REFERENCE ONLY: a user-supplied screenshot of a game with a person and sheep around a wooden cart. Ignore every desktop window, player control, watermark, text, logo, UI, and blue mascot overlay in this screenshot. The actual game view inside the screenshot is the only camera reference.
User request: achieve the same steep oblique downward viewing angle as the game view in IMAGE 2. Match its visual top-surface/side-surface relationship, the foreshortening of the upright person's body seen from above, and the overhead spatial read of the cart top. Do not merely repeat a guessed numeric angle; prioritize visually matching IMAGE 2's viewing direction.
Produce C2 v004 by reprojecting the scene from IMAGE 1 to this reference viewing direction. Make it a distinctly high oblique overhead gameplay view: dominant ground plane, clearly visible top of the man's head and shoulders, hut roof strongly dominant with a shallower visible wall band, rocks read more from above. Retain some side faces as in IMAGE 2; not a 90-degree vertical map.
IMPORTANT: transfer ONLY camera pitch from IMAGE 2. Do NOT copy the screenshot's sheep, cart, hat, costume, palette, flat shading, fog, visual detail level, camera distance, small character size, UI, words, watermark, desktop, or composition.
Keep IMAGE 1's human identity, plain light tunic and brown trousers, standing pose and approximate central screen position; keep the head-to-foot screen height around its current 12% of image height by adjusting camera distance as needed to compensate for foreshortening. Preserve world-space human-to-hut scale. Keep same hut upper right, fence left, paths, rock locations, ground layout, warm light, shadow direction, muted green/ochre/brown palette, textured finish and detail density of IMAGE 1. Natural camera projection changes are allowed, no scene redesign. This is a camera study; temporary character and scenery are not approved final game content.
Polished 16:9 landscape image, full frame filled with existing terrain/objects, no sky or horizon. No labels, UI, lettering, logos, watermarks, extra humans or animals.
```

## 输出与评审

- 输出：[C2 ImageGen v004](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v004.png)，1672 × 941 PNG；原件保留在 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-bf274fd2-ff39-42b0-ad91-ee582b2db7ad.png`。
- 初检：比 v003 更俯，屋顶及岩石顶面更突出，人形上表面增多；暖光、主要物件关系和地表画风基本延续；未见参考截图的 UI、水印、羊群、推车或蓝色形象混入。
- 偏差：人物约高 90 px／941 px，约 10%（看图估读），比输入约 12% 更小；人物屏幕位置、石块及路径形状有漂移。保持人物大小未完全实现，因此评审俯视程度时需注意占屏变化。
- 匹配程度：助手观察更接近高位斜俯视，不能宣称与截图精确一致；由用户决定是否达到参考观感。没有真实相机、投影或引擎验证。
- 用户评审：2026-10-17 原话“就这个作为镜头角度参考”。确认范围仅限本图俯视角度观感，登记为 CAM-01；人物大小、场景主题、纹理、人物规格和路线均未因此获批。
