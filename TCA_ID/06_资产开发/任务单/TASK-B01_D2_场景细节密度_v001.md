# TASK-B01｜D2 场景细节密度 v001

日期：2026-10-17（Asia/Shanghai）  
状态：已生成并归档，待用户过目。  
用途：阶段 B 风格比较，非正式游戏资产。  
用户原话：“D2”。对应“大形简洁，重点区域保留草、石头和木纹”。

## 范围与检查条件

- 〔确认：比较方向〕采用 D2 适度细节制作候选；不代表尚未生成的成图已通过。
- 输入：[C2 v004](../美术源文件/TASK-A01_探索构图与人物尺度/generations/tca_task_a01_c2_imagegen_v004.png)，已实际查看；编辑目标＋CAM-01 镜头参考。
- 保留：已确认的镜头角度、当前画幅／布局／临时人形／占屏、暖光、色彩关系、主要物体轮廓。
- 只改：场景表面细节密度及分布。大面积草地与土路安静，草石和木纹集中于屋门、台阶、道路边缘和物体接地处。
- 不改：人物规格、正式主题、正式角色名单、路线、玩法；屋门只作视觉重点，不据此批准交互机制。
- 工具：内置 ImageGen，基于 v004 编辑；透明背景否；其他设置未提供，不编造种子、质量档位或模型版本。
- 目标：有完成度的简化设计，不能用模糊、降分辨率或低完成度代替适度细节。
- 检查：俯角及人物大小有无漂移；是否减少满地碎石与草叶；局部细节能否形成主次；暖光和接地是否保留。生成无法严格控变量时如实记录。
- 四项验收：视觉待用户确认；技术、正式内容、来源尚未验收；内部比较材料。

## 实际编辑提示词／nanobanana 提示词（需附 C2 v004）

```text
Use case: precise-object-edit / style-transfer.
Edit the supplied TCA exploration reference into TASK-B01 D2 v001: MEDIUM ENVIRONMENT DETAIL DENSITY. The user selected D2: broad simple masses with carefully placed local detail. This is a highly finished game-art candidate, not a sketch, blur pass, or blockout.
HARD INVARIANTS: preserve EXACTLY the source's high oblique downward camera angle, framing, 16:9 composition, human head-to-foot on-screen size (about 10 percent of frame height), human screen position and pose, hut roof-to-wall projection, fence position, paths and major rock silhouettes. Preserve the same light-tunic/brown-trouser temporary human, warm light from upper left, long world-space shadow directions, overall green/ochre/brown colors and existing world layout. No change of camera, time of day, character design, physical proportions or environment theme.
ONLY CHANGE the distribution and density of environmental surface details:
1. Calm broad grass and earth color masses across the open clearing; make the ground around the central person clearly readable. Remove the blanket of tiny pebbles, speckles, dents, repeated little soil marks and individual grass blades across every open area. Keep gentle terrain variation and deliberate broad shading, no featureless plastic.
2. Grass is organized in spaced, intentional readable CLUMPS, mostly at road margins, fence bases, and rock bases, separated by substantial quiet ground. Remove the continuous noisy carpet of fine foliage. Do not add flowers.
3. Keep selective tactile detail near the hut entrance and steps: a few wood seams, clean step edges, small contact patches of grass, and a few stones at path edges. This is only a visual focal area in the test scene, not a claim that gameplay interactions are approved.
4. Hut roof: retain the conical form and large readable shingle sections, fewer seams and fewer individual chips/scratches; avoid a uniform covering of tiny woodgrain marks. Retain useful door/fence construction shapes and a small amount of woodgrain only at focal points.
5. Rocks: preserve existing positions and large silhouettes, express form with a few broad planes and quiet shading; remove dense fissures, mottling and fine noisy patches.
Maintain sharp deliberate edges and attractive sculpted warm lighting. The result should feel intentionally art-directed, simplified and refined with a hierarchy of detail, not like a lower-resolution or defocused copy. Keep high quality throughout, with focal areas richer and peripheral surfaces quieter.
Do not add objects, remove major props, alter the central character's detail, paste labels, add UI, text, watermarks, animals, extra people, sky or horizon. The only approved standard carried over is the camera-angle reference. Character, scene theme, palette and production route remain test conditions.
```

## 输出与反馈

- 输出：[D2 v001](../美术源文件/TASK-B01_场景细节密度/generations/tca_task_b01_d2_imagegen_v001.png)，1672 × 941 PNG；原件保留于 `C:/Users/Lenovo/.codex/generated_images/01a149ef-c266-7820-be94-8a2af2166f32/exec-9827b9b2-0628-4059-93ea-85e2673a077f.png`。
- 初检：镜头观感、人物大小与位置、主要场景布局基本保留；地面散碎石显著减少，草叶主要收拢到路径、栅栏和岩石附近。屋门和台阶仍有局部细节，暖光与长投影保留。
- 局限：草地仍有连续细碎表面纹样，木瓦和岩石的表面仍较密，局部简化程度可能不足；不能把“已选 D2”视为本图已通过。投影边缘和局部纹理有重绘变化，未精确测量相机一致性。
- 下一轮只判断当前细节量是否合适：接受此密度作参考／再简化草地纹理／稍恢复道路边缘细节。由用户过目选择。
- 用户对本图的选择：2026-10-17 回复“B”，选择再简洁一点，主要减少草地碎纹，保留屋门、台阶细节；v001 保留作修改依据，未作为细节密度通过版。
