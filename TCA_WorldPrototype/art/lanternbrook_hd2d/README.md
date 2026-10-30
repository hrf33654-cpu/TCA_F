# 溪灯驿站 · HD2D 完整室外地图

> 2026-10-27 景深 v4：在六区域景深基础上，加强远景并补充柔和的上沿虚化，修正上方明显弱于下方的问题。按 **D** 循环比较新版 / 原版 / 关闭。最新截图与验证见 [景深调整说明](research/depth_of_field_v4/README.md)；[v3 记录](research/depth_of_field_v3/README.md) 与本页下方原 `renders/`、性能表保留为历史证据。

已将认可的驿站像素质感扩展至整张约 100×80 米的室外地图，并逐区完成入口、庭院、石桥、河岸、遗迹及返回支路。保持青绿尖屋顶与暖灯，林地转冷、遗迹以青色微光收尾。人物、任务、战斗、互动和室内未接入；本交付完成地图内容及接入基础，不宣称已完成正式游玩验收。

## 打开与交付

- 项目启动 / 实机预览：`res://scenes/lanternbrook_hd2d_preview.tscn`。
- 正式地图：`res://world/maps/lanternbrook_hd2d/lanternbrook_hd2d.tscn`。
- 完整可编辑源文件：本目录 `Lanternbrook_HD2D_Complete.blend`；纹理与树冠图片已打包。
- 本目录 `map_layout.svg` 为带区域、环线与接入点的俯视布局示意。
- 本目录 `renders/` 包含六区域的 720p / 1080p Godot 实机截图、左右转向极限截图及整图鸟瞰。鸟瞰为交付用镜头，不改变正式观察模式的缩放限制。
- 原版对照：`res://scenes/lanternbrook_map_preview.tscn`；之前认可的 Blender 美术样板仍为 `Lanternbrook_HD2D_ArtPass.blend`。

## 区域内容

| 区域 | 内容 |
|---|---|
| 林间入口 | 青瓦门架、告示板、手推车、暖灯与路标；前景林带和低岩石收住边界。 |
| 驿站庭院 | 保留青绿屋顶、建筑轮廓、门廊与水轮，统一像素木纹、墙灰、石材和暖色灯光。 |
| 溪上石桥 | 连续桥面、两端通行空间、河岸碎石与流水，连接庭院和西侧林路。 |
| 河岸小径 | 垂柳、芦苇、蕨类、木平台、休息长椅与钓具；增加可以走到平台的支路。 |
| 林中遗迹 | 开阔石阶与露台、石拱、残柱、星仪环、青色核心、石刻与薄雾；前景树冠缩低以完整呈现地标。 |
| 林间归途 | 上游木桥、桥头灯、长椅、石路标与零散旧石，连回庭院形成环线。 |

森林包含 217 棵像素树冠，另有 2264 丛合批路边草与 331 组蕨类、芦苇、蓝花。新增 130 个区域美术构件，保存为可编辑场景节点。

## 控制与后续接入

右键左右转向、中键平移、滚轮缩放、R 回到庭院、Tab 隐藏界面。数字 1～6 分别查看入口、驿站、石桥、河岸、遗迹和归途。俯角 20°，镜头距离 96，长焦透视；庭院默认垂直视角约 9.53°，左右各限制 12°，有效取景尺寸范围 14～27。树冠、屋顶与前景岩石保留独立遮挡淡出；碰撞不随视觉淡出改变。本轮材质 v2、新镜头及轻景深已重新完成全区域检查、720p/1080p截图与性能采样。

- `Art/art_*.scn` 对应原始分区，`complete_*.scn` 对应本轮各区域新增内容，`pixel_woodland.scn` 对应树冠、树干及路边草。所有内容在编辑器中持久保存，运行时不重新搭建地图。
- `Collision/GroundAndDecks` 与 `Collision/RegionDetails/LookoutDeck` 为可走地面，物理层 1；`Obstacles`、`RegionDetails` 其余阻挡及河流、地图外缘为物理层 2。草、花、树冠、薄雾不阻挡行走。
- `Collision/CameraSurfaces` 在物理层 3（位掩码 4），仅供镜头及画面边缘探测远景地形和水面；不纳入行走导航。正式人物碰撞掩码使用层 1、2，镜头避让使用层 1、3。
- `WalkableRegion` 使用本轮重烘焙的 `complete_walkable.tres`；角色参考半径 0.5m、高 1.6m、最大台阶 0.3m，正式角色接入时按实际体型复核。
- `Markers` 保留 Spawn、InnDoor、Exit、RuinsEntry、UpperBridge，新增 RiversideLookout、Observatory、ReturnJunction；通过标记 `global_transform` 获取世界位置。
- `Routes` 保留 MainRoute、ReturnRoute、InnApproach，并新增 LookoutApproach。`complete_data.json` 是完整路线、区域与标记数据。
- 观察镜头和环境遮挡脚本的 `focus_target` 可接入后续角色；地图实例原有位置、旋转完整保留，所有路线与视觉效果使用地图本地坐标。

## 实测记录

- 胶囊通路探针：1593 次采样，中心与左右各 0.70m，半径 0.30m、高 1.6m；阻挡失败 0。
- 导航：34 段路径请求，34 段返回路径；重烘焙导航 2021 个多边形。
- 区域镜头检查 54 组；地图边缘画面四角对地形/水面射线 216 次，未找到可见表面 0 次；镜头上下限及第 6 区快捷键检查见 `validation.json`。
- 全部检测使用临时探针；探针没有作为正式角色交付。场景保存后重新加载亦已检查。

| 分辨率 | 区域 | 平均帧时间 | P95 帧时间 |
|---|---|---:|---:|
| (1280, 720) | 林间入口 | 6.05 ms | 6.36 ms |
| (1280, 720) | 驿站庭院 | 6.07 ms | 6.63 ms |
| (1280, 720) | 溪上石桥 | 6.06 ms | 6.31 ms |
| (1280, 720) | 河岸小径 | 6.06 ms | 6.54 ms |
| (1280, 720) | 林中遗迹 | 6.06 ms | 6.50 ms |
| (1280, 720) | 林间归途 | 6.06 ms | 6.42 ms |
| (1920, 1080) | 林间入口 | 6.06 ms | 6.45 ms |
| (1920, 1080) | 驿站庭院 | 6.06 ms | 6.29 ms |
| (1920, 1080) | 溪上石桥 | 6.06 ms | 6.37 ms |
| (1920, 1080) | 河岸小径 | 6.06 ms | 6.74 ms |
| (1920, 1080) | 林中遗迹 | 6.06 ms | 6.30 ms |
| (1920, 1080) | 林间归途 | 6.06 ms | 6.34 ms |

设备：NVIDIA GeForce RTX 4060 Laptop GPU，Godot 4.6.2 Forward+。每区域预热 30 帧后记录 90 帧，截图实际尺寸已核对。该结果是本机短时场景测试，未包含人物、玩法与长时间运行负载。

## 可编辑源文件与重建

完整 Blender 源文件保留原始建筑/地形/道具可编辑模型，新增区域按集合组织，附六区域相机与入口标记。Godot 是导航、碰撞、实时光照、雾、水流、道路边缘混色和风动的最终依据，两种渲染器画面不会完全一致。

生成顺序：制作原始表面与林下细节后，运行 `make_texture_pass_assets.py` 制作 v2 辅助纹理；保留已生成的三张 handpainted_v2 图片及其 .import 导入设置（必须启用 mipmaps）。准备水流及观察器后重新导入，然后在有渲染的 Godot 中运行 `--script res://tools/author_hd2d_pass.gd`，不要给该制作步骤加 --headless：无渲染后端会丢失 MultiMesh 变换缓冲。制作器调用 complete_hd2d_regions.gd 与 texture_finish.gd，最后只打包一次各分区。检查与实机截图用 --script res://tools/validate_hd2d.gd。

Blender 打开 `Lanternbrook_HD2D_ArtPass.blend`，运行 `tools/blender/complete_hd2d_source.py`，另存为完整源文件。重建会覆盖本轮生成资源，手工编辑后先另存；原 v1 地图与原源文件不被覆盖。

## 本轮质感调整

木梁、木平台与石材换为原创生成的精细纹理，瓦面、灰泥、土路和林地表面重新绘制；材质按种类区分粗糙度与微凹凸，增加墙脚潮痕、河岸湿色、自然路缘与322片树下落叶。地被替换为成簇草叶，调整局部暖光与窗灯层次。具体素材来源、提示词、前后对照和回退备份见 research/TEXTURE_PASS_V2.md。

## 素材来源

建筑、道具、地形与像素表面为项目原创。橡树冠、垂柳冠使用内置 imagegen 生成并保留透明通道，文件为 `textures/woodland_crown.png` 与 `textures/river_willow.png`。橡树冠完整提示见 `ART_PASS_RECORD.md`；以下为本轮垂柳的完整提示：

> Production pixel-art asset for an original HD-2D woodland river map. ONE isolated weeping WILLOW TREE CROWN ONLY without trunk, without ground, without text, transparent background with real alpha. Broad irregular domed top with hanging leafy tendrils and scalloped trailing lower silhouette, several asymmetrical lobe clusters, small openings for light. View from fixed RPG three-quarter camera looking downward about 32 degrees. Meticulous crisp JRPG pixel art, around 160x160 logical pixels, enlarged with sharp square pixels and no smoothing. Rich clustered leaves, clear large light/shadow masses. Muted jade and sage highlights upper-left, deep teal blue-green shadows under hanging branches. Restrained olive accent but no bright neon. Same visual family as a quiet warm lantern inn in a cool forest. Crown centered with 7 percent transparent margin, fully contained, no roots, no scenery, no outlined border. Must read as drooping willow foliage rather than round oak. No polygonal 3D faces.

遗迹、告示及星仪均为环境美术，不自动引入正式剧情、任务或互动规则。
