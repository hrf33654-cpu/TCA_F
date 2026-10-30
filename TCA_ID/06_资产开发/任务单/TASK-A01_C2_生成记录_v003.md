# TASK-A01｜C2 俯角微调 v003

日期：2026-10-17（Asia/Shanghai）  
状态：已生成并归档，待用户评审。  
工具：内置 ImageGen，基于 v002 编辑，透明背景否。  
用户原话：“就这个场视角挺好的，C，更俯视一点”。

## 本轮边界

- 〔确认〕用户认可 v002 视角方向，选择 C：保持人物大小，再更俯视一点。
- 唯一主要变化项：俯视程度。保持人物约占画面高 13%、姿势、位置、场景布局、暖光、配色和细节密度，允许随观察角度产生自然投影变化。
- 〔建议／本次候选条件〕提示词以比 v002 再增加约 8～10° 的视觉意图表达“更俯视一点”，并非用户批准的正式角度，也非可测量相机参数。实际变化由图像评审判断。
- 输入：[C2 v002](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v002.png)，已实际查看。
- 无新增正式人物规格、名单、场景主题或技术路线决定。屋顶等物体与画面边缘的关系可能随镜头编辑漂移，需检查。
- 目标画幅 16:9；实际输出尺寸待登记；种子、质量档位及底层模型版本未提供。

## 实际提示词（nanobanana 可用同文，需附 v002）

```text
Use case: precise-object-edit.
Edit the supplied exploration concept C2 v002 into C2 v003. This is a narrowly controlled CAMERA PITCH comparison, not a restyling.
Change ONLY the camera elevation/pitch to be modestly more top-down than the reference: rotate the viewing direction downward by approximately 8–10 degrees relative to the existing image, aiming for a clearly but gently steeper oblique gameplay view (rough visual target 55 degrees below horizontal). Make the hut roof and upper surfaces a little more visible, and the hut front wall a little less tall. Show a little more top of the standing person's head and shoulders. Keep an oblique view with readable side faces, not directly overhead.
Maintain the SAME standing human's on-screen head-to-sole height as in the reference, around 13% of total image height, centered close to the current position. Compensate camera distance/framing for the change in foreshortening rather than enlarging or shrinking the actual person. Preserve the same physical relative scales of human, hut, rocks and fence. Do not just crop or rotate the flat reference image.
Invariants: identical generic person with short dark hair, light plain tunic and brown trousers, same standing pose and facing; same hut upper right, fence left, footpath, rocks, grass and ground layout. Preserve warm sunlight from upper left, muted green/ochre/brown palette, long shadows cast in the same world-space direction, the current detail density, materials, rendering finish, and overall spatial character. Only perspective/projection changes naturally required by the camera pitch are allowed. Do not simplify textures, add decorations, change time of day, introduce new objects, alter character design, or redesign the hut.
Full 16:9 landscape image, polished consistent game concept finish. Entire frame filled by terrain and existing scene objects, no sky, horizon, lake or distant mountain view. No text, labels, UI, HUD, watermark, extra people or animals. This image is a temporary composition test, not a confirmed character specification, world theme, or technical production route.
```

## 输出与评审

- 输出：[C2 ImageGen v003](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v003.png)，1672 × 941 PNG。工具原件保留于 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-04773786-aded-4111-8020-1945e98e079e.png`。
- 初检：屋顶顶面比重增加、人物头顶更明显，视角较 v002 更俯；小屋、栅栏、道路、人形、暖光和长投影基本延续。未见新增人物、文字或水印。
- 比较限制：人物目测约高 110 px，占屏高约 12%，比 v002 约 13% 略小；保持大小未完全做到。边缘石块、草丛及屋顶构图有重绘漂移，不能当作同一相机的严格渲染对照。以上为看图估读，未验证真实相机数值。
- 视觉验收：待用户确认；技术、正式内容、来源验收未执行；仅作内部比较图。
- 用户选择：2026-10-17 提供截图并说“我希望做到这个俯视角度”。未批准 v003 为最终角度；改以 R-10 截图为直接参考制作 v004。
