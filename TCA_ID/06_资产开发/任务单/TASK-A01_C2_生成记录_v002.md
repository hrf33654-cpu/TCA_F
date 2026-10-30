# TASK-A01｜C2 修改记录 v002

日期：2026-10-17（Asia/Shanghai）  
状态：已生成并归档，待用户评审。  
执行工具：内置 ImageGen；任务类型：基于 v001 编辑。  
用户决定：回复“A”，选择提高镜头、缩小人物、简化场景，保留暖光和空间层次。

## 保留与修改范围

- 保留：v001 暖光、空间层次、临时人形身份、右后方小屋和左侧栅栏的基本关系。
- 修改：提高机位，画面由地面与场景物占据；移除天空、湖山远景；人物占屏高目标 14%～16%；简化植被、地表和建筑细节。
- 所有修改只用于本次构图候选；未批准正式人物规格、世界内容、色板或技术路线。
- 输入：[C2 v001](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v001.png)，已用看图工具查看。
- 参数：透明背景否；目标画幅 16:9；实际尺寸待输出记录。种子、质量档位、底层模型版本未提供。
- 俯角仅为视觉目标；概念图无法证明实际相机参数。

## 实际编辑提示词（也可交 nanobanana，需附 v001）

```text
Use case: precise-object-edit / stylized-concept.
Edit the supplied TCA TASK-A01 C2 v001 concept into C2 v002, a polished exploration-game composition candidate. User selected correction A: higher viewpoint, smaller figure, simpler environment; preserve warm light and spatial depth.
Reference image role: edit target. Preserve the same generic short-haired human in plain light tunic and brown trousers, standing relaxed near the center facing slightly right, same small conical-roof hut in the upper-right portion, same low wooden fence on the left, same muted green/ochre/wood-brown palette, warm upper-left illumination and long coherent ground shadows. These are temporary test fixtures, not approved character or world designs.
Change the CAMERA decisively: raise camera above the clearing and aim DOWN at about 45 degrees below horizontal. The image must read as an elevated oblique exploration gameplay view, with visible tops of the head, shoulders, roof and rocks. The entire frame is ground and objects resting on it: REMOVE visible sky, sun disk, horizon, distant lake, mountain panorama, and cliff vista. Continue the ground beyond the upper edge rather than showing a horizon. Keep natural mild perspective, avoid a vertical overhead map.
Pull back so the complete standing human from top of head to soles occupies 14–16% of image height, centered around 15%. Show more walkable ground around the figure. Keep believable human-to-hut scale by applying a consistent camera change to the entire scene.
Simplify scenery into confident broad geometric volumes: sparse grass clumps, a few large readable rocks, plain ground color masses, simplified hut roof and walls. Remove dense flower beds, individual foliage noise and foreground tree framing; no huge close foreground boulders. Retain gentle terrain changes, atmospheric separation and sculpted light/shadow; deliberate polished finish, not an unfinished blockout. Preserve long warm shadows without adding new objects or decorative motifs.
One 16:9 landscape frame. No text, labels, letters, UI, HUD, watermark, logos, extra characters, animals, weapons, element symbols, dramatic perspective distortion, shallow depth-of-field blur, or black outlines. Do not beautify back into a cinematic low-viewpoint landscape.
```

## 结果

- 输出：[C2 ImageGen v002](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v002.png)，1672 × 941 PNG；原件保留于 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-9a1e69f4-1e6d-4171-9b70-f80991137e48.png`。
- 初检：机位明显提高，天空、湖泊和山体消失，地面及屋顶可见；暖光、长投影、人形和小屋／栅栏关系基本保留。未见文字、水印或额外人物。屋顶顶端被上边缘裁切。
- 人物约高 120 px／941 px，约 13%（看图估读，非精确分割），略低于目标 14%～16%，不标为精确达标。
- 草叶、地面碎石、木瓦和岩石纹理仍偏密；低细节几何观感的修正只部分实现。俯角数值和真实相机参数未验证。
- 比较限制：本轮同时纠正镜头、占屏和细节，依据用户选择执行，是一组定向修改，不视为严格单变量实验。
- 下一轮只讨论：是否以 v002 的镜头与人物尺度作为 C1／C3 的比较基准；场景细节可另轮处理，不因选定构图而获批。
- 用户评审：2026-10-17 原话“就这个场视角挺好的，C，更俯视一点”。认可当前视角方向，并选择在维持人物占屏大小的前提下再增加俯视程度；不等同于精确相机参数、场景细节或正式风格全部通过。
