# 溪灯驿站 · 河谷环线 v1

2026-10-27。原创室外地图场景，已接入项目默认启动入口。人物、互动、战斗和建筑室内尚未接入；5～10 分钟仅是区域体量目标，未宣称游玩时长验收。

## 打开与操作

- 默认运行项目，或打开 `res://scenes/lanternbrook_map_preview.tscn`。
- 右键环视，中键平移，滚轮缩放，R 回驿站，Tab 隐藏界面。
- 1～5 跳转入口、庭院、石桥、河岸、遗迹。
- 原展示入口仍在 `res://scenes/main.tscn`；原 Blender 源文件未覆盖。新入口保留原地图实例的平移与旋转。

## 源文件与布局

- `Lanternbrook_Map_v1.blend`：可编辑完整地图，含分集合模型、五个区域相机及灯光。
- `map_layout.svg`：有标注的俯视布局；`renders/map_top.png`：实际 Godot 俯视截图。
- `renders/region_1_1280.png` 至 `region_5_1920.png`：五区域实机图；`*_reverse.png`：反向观察图。
- 全部环境模型、程序纹理和布局为本项目原创。延续原样板的 Blender MCP 工具及 MIT 许可记录，无新增第三方美术素材。

## 编辑与接入

正式内容入口为 `res://world/maps/lanternbrook/lanternbrook_map.tscn`。Art 下分为入口、庭院、石桥、河岸、遗迹、远景六个场景；可打开各 `art_*.scn` 编辑。重型几何与地面三角碰撞存为压缩二进制场景，主场景保留可读的节点与属性。

- `Collision/GroundAndDecks`：地面、桥面、台阶与遗迹平台，物理层 1。
- `Collision/Obstacles`：建筑、树干、岩石、柱子及主要道具；`RiverBoundary` 与 `MapBoundary` 阻止进入河流及地图外侧，均在物理层 2。草叶、花朵与树冠不阻挡行走。
- `WalkableRegion`：按真实地面和阻挡轮廓预烘焙导航；导航半径 0.5m、高度 1.6m、最大台阶 0.3m。后续接入角色时按正式体型复核。
- `Markers/Spawn`、`InnDoor`、`Exit`、`RuinsEntry`、`UpperBridge`：稳定名称的 Marker3D，位置均为地图本地坐标；接入者通过 `global_transform` 获取世界位置。门口与出口仅为连接标记。
- `Routes/MainRoute`、`ReturnRoute`、`InnApproach`：连续 Path3D；区域名称见 `Regions`。
- `environment_motion.gd`：水轮动画、遮挡渐隐。导出的 `focus_target` 可指向后续角色 Node3D；未指定时使用观察镜头的焦点。树冠、屋顶及前景边界岩石淡出，碰撞始终保留。
- `prototype/map_observer.tscn`：独立观察工具，可整段移除。其 `focus_target` 可接入跟随目标；输入动作全部使用 `world_map_` 前缀，复位沿用 `world_reset`。
- 水流材质继续使用 `world/environments/lanternbrook/river_material.tres`，风摆参数保存在各分区的 ShaderMaterial。

## 验证记录

- 几何：1552 个分区/材质网格，1,152,582 三角面。
- 主线、返回线与门口支线：1524 次胶囊探测，半径 0.30m、高 1.6m，中心及左右偏移 0.70m，共检查约 2m 净宽；失败 0 次。
- 相邻采样支撑高度最大变化 0.185m；两座桥和遗迹缓坡通过。
- 导航：31 段路径请求均返回路径；河流与四侧边界检查结果见 `physics_validation.json`。
- 镜头：180 组区域、角度、俯仰及缩放检查；输入及复位结果见同一文件。

| 分辨率 | 区域 | 平均帧时间 | P95 帧时间 |
|---|---|---:|---:|
| (1280, 720) | 林间入口 | 6.06 ms | 6.50 ms |
| (1280, 720) | 驿站庭院 | 6.06 ms | 6.54 ms |
| (1280, 720) | 溪上石桥 | 6.06 ms | 6.58 ms |
| (1280, 720) | 河岸小径 | 6.05 ms | 6.67 ms |
| (1280, 720) | 林中遗迹 | 6.06 ms | 6.66 ms |
| (1920, 1080) | 林间入口 | 6.05 ms | 6.30 ms |
| (1920, 1080) | 驿站庭院 | 6.06 ms | 6.60 ms |
| (1920, 1080) | 溪上石桥 | 6.06 ms | 6.55 ms |
| (1920, 1080) | 河岸小径 | 6.06 ms | 6.93 ms |
| (1920, 1080) | 林中遗迹 | 6.06 ms | 6.49 ms |

实测设备：NVIDIA GeForce RTX 4060 Laptop GPU，Godot 4.6.2 Forward+。每区域预热 35 帧后采样 90 帧；两种分辨率均核对了实际截图尺寸。该结果是当前本机短时场景测试，尚未包含人物/玩法负载，也不是最低配置或长时间游玩验收。

## 重建与维护

1. Blender 打开旧样板源文件，经 `tools/blender/build_map_v1.py` 生成独立新地图；该步骤会重建新地图，应先另存手工修改。
2. 在新地图中运行 `tools/blender/export_map_v1.py`，更新 `map_art.glb` 与元数据。
3. 等 Godot 导入完成，执行 `godot --headless --path <项目目录> --script res://tools/bake_map_v1.gd`，生成分区、碰撞、灯光、导航与观察场景。
4. 执行 `godot --path <项目目录> --script res://tools/validate_map_v1.gd`，进行独立窗口验证与截图，再运行 `python tools/write_map_delivery.py` 更新本说明。

地图主题与遗迹装饰继续属于视觉候选，不自动新增正式剧情、任务或世界观规则。
