# 溪灯驿站 · HD2D 美术预览

本轮围绕驿站、石桥及周边树林做美术方向验证。保留青绿色尖屋顶和建筑轮廓，采用像素材质、像素树冠与立体光影。共用素材同步覆盖其他区域，但入口、河岸及遗迹尚未逐区完成新的构图定稿；本交付不宣称整张地图的最终美术已完成。

## 打开与对照

- 新预览：`res://scenes/lanternbrook_hd2d_preview.tscn`，已设为项目启动场景。
- 新地图：`res://world/maps/lanternbrook_hd2d/lanternbrook_hd2d.tscn`。
- 原版对照：`res://scenes/lanternbrook_map_preview.tscn`，原场景、源文件与碰撞资源保留。
- Blender：本目录 `Lanternbrook_HD2D_ArtPass.blend`；所有像素图已打包进文件。
- 实机截图：本目录 `renders/`，包含 1280×720、1920×1080 及左右旋转极限画面。

右键左右转向，中键平移，滚轮缩放，R 复位，Tab 隐藏界面，数字 1～5 切换区域。镜头俯角固定约 31.5°，左右各限制 12°，缩放范围 14～27。新版观察器独立于原版，修改不会破坏原自由旋转对照场景。

## 这轮的变化

- 木梁、木板、屋瓦、墙灰、石材、土地和砂砾使用项目原创的确定性像素纹理，以最近邻采样呈现；未套用整屏马赛克滤镜。
- 217 棵树使用带透明通道的像素树冠，四种色调、不同尺寸；树干缩进叶簇以内，碰撞独立保留。
- 去除均匀散布的三角草，改为道路旁有疏密的像素草簇；用 MultiMesh 合批。
- 道路边缘增加草色碎块过渡，墙面与石材保留安静的大色面，减少颗粒噪声。
- 降低整体日光、增强冷色环境光和局部暖灯，突出驿站；流水保留动画，减少大块镜面反光。
- 原地图实例位置、旋转，所有地面/桥面/障碍碰撞、导航与连接标记保持。
- 静态资源已保存为可编辑的分区场景；运行脚本仅控制镜头、风、水轮和遮挡。

## 检查与边界

`validation.json` 保存本轮碰撞、导航、镜头限制及性能记录。复用原版临时碰撞探针检查 1,524 个通路采样点，未加入正式角色。性能为 RTX 4060 Laptop、Forward+、各区域预热 30 帧后采集 90 帧的短测；不能代替接入人物后的玩法与长时间运行验收。

Blender 保留原可编辑模型，替换主要材质与树冠表现；Godot 场景是实时灯光、道路边缘混色、草簇合批和动态水流的最终依据。两者不同渲染器不会自动产生完全相同的画面。

## 素材来源与生成提示

表面纹理由 `tools/make_hd2d_textures.py` 原创像素绘制。树冠使用内置 imagegen 工具生成，最终资源存放于 `world/maps/lanternbrook_hd2d/textures/woodland_crown.png`，保留原始透明通道。以下是完整提示词，便于后续保持一致：

> Use case: stylized-concept. Production game asset for an original HD-2D forest inn environment. Generate ONE isolated deciduous tree CROWN ONLY, no trunk, no branches sticking out below, no ground, no scenery, no text. True transparent background. Crown fills centered square canvas with generous 6 percent transparent margin. Broad irregular organic canopy, layered billowing leaf clusters, asymmetric silhouette, small holes between clusters. Style: meticulous hand-placed retro JRPG pixel art with crisp square pixel clusters, visually about 160 by 160 source pixels, enlarged without smoothing; NOT low-poly, NOT painted blurry, NOT photoreal. Moss green and deep blue-green shadows, restrained sage and warm olive highlights on upper-left edges, dark teal undersides. Strong readable silhouette, rich clustered leaf detail with quiet shaded regions; avoid uniform scattered noise. View from a 35-degree downward three-quarter RPG camera, appropriate for a pixel tree crown suspended above a 3D tree trunk. Lighting gently from upper left, no glowing outline. Palette 12 to 18 muted woodland greens. Render actual alpha transparency.

## 重建

依次运行 `tools/make_hd2d_textures.py`、`tools/prepare_hd2d_water.py`、`tools/prepare_hd2d_observer.py`，让 Godot 重新导入纹理，再运行 `--headless --script res://tools/author_hd2d_pass.gd`。渲染检查用 `--script res://tools/validate_hd2d.gd`。Blender 用原 v1 源文件启动后运行 `tools/blender/author_hd2d_source.py`，另存本目录的新源文件。

上述重建会覆盖本轮生成资源；手工修改本轮文件后应先另存备份。原版地图和原版 Blender 源文件不会被这些重建脚本覆盖。
