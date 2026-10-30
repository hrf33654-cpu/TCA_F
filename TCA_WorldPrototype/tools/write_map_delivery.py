"""Write the route diagram and measured delivery notes from actual map metadata."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/lanternbrook_map_v1'
data=json.loads((ROOT/'world/maps/lanternbrook/map_data.json').read_text(encoding='utf8'))
def xy(p):return (530+p[0]*8,420+p[2]*8)
def path(points):return ' '.join(('%s %.2f %.2f'%('M' if i==0 else 'L',*xy(p))) for i,p in enumerate(points))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="900" viewBox="0 0 1120 900">', '<rect width="1120" height="900" fill="#142824"/>', '<g font-family="Microsoft YaHei, sans-serif">', '<text x="54" y="56" fill="#f2e7c6" font-size="29" font-weight="bold">溪灯驿站 · 河谷环线</text>', '<text x="54" y="86" fill="#b0c7b9" font-size="15">第一版地图布局 / 100 × 80 米 / 地图本地坐标</text>', '<rect x="130" y="100" width="800" height="640" rx="28" fill="#344b37" stroke="#7b8e63" stroke-width="3"/>']
for x in range(-40,50,10):
    px=530+x*8;svg.append(f'<path d="M {px} 110 V 730" stroke="#ffffff" opacity=".05"/>')
for z in range(-30,40,10):
    py=420+z*8;svg.append(f'<path d="M 140 {py} H 920" stroke="#ffffff" opacity=".05"/>')
river=[]
for i in range(161):
    z=-40+i*.5;river.append([-3-.11*z-.55*math.sin(z*.26),0,z])
svg.append(f'<path d="{path(river)}" fill="none" stroke="#608e83" stroke-width="22"/>')
for i,route in enumerate(data['routes']):
    svg.append(f'<path d="{path(route)}" fill="none" stroke="{["#e4bc73","#8bc3b4","#e4bc73"][i]}" stroke-width="{10 if i<2 else 7}" stroke-linejoin="round" stroke-linecap="round"/>')
svg.append('<rect x="535" y="379" width="41" height="34" rx="3" fill="#78a69a" stroke="#f1dfb3" stroke-width="2"/>')
for z in [1.8,-18]:
    x=-3-.11*z-.55*math.sin(z*.26);px,py=xy([x,0,z]);svg.append(f'<rect x="{px-23}" y="{py-7}" width="46" height="14" rx="2" fill="#d4c3a0" stroke="#24382e" stroke-width="2"/>')
label_offsets=[(28,15),(35,55),(-155,50),(-165,-8),(-140,-58)]
for i,region in enumerate(data['regions']):
    px,py=xy(region['position']);dx,dy=label_offsets[i];tx,ty=px+dx,py+dy
    svg.append(f'<circle cx="{px}" cy="{py}" r="13" fill="#f0d8a0" stroke="#213a30" stroke-width="3"/><text x="{px}" y="{py+5}" text-anchor="middle" fill="#20382f" font-weight="bold" font-size="15">{i+1}</text>')
    svg.append(f'<path d="M {px} {py} L {tx} {ty}" stroke="#d5dcc1" opacity=".7"/><rect x="{tx-8}" y="{ty-23}" width="136" height="36" rx="6" fill="#172e28"/><text x="{tx}" y="{ty+1}" fill="#f4e9cc" font-size="18">{region["label"]}</text>')
svg.extend(['<path d="M 991 170 V 120 M 981 135 L 991 120 L 1001 135" fill="none" stroke="#e7debd" stroke-width="3"/><text x="982" y="108" fill="#e7debd" font-size="16">北</text>', '<text x="138" y="785" fill="#e4bc73" font-size="17">━ 主线：入口 → 驿站 → 石桥 → 河岸 → 遗迹</text>', '<text x="138" y="817" fill="#8bc3b4" font-size="17">━ 回路：遗迹 → 上游木桥 → 驿站东侧 → 庭院</text>', '<text x="138" y="855" fill="#b0c7b9" font-size="14">已配置碰撞、导航与入口标记；角色、互动、战斗与室内尚未接入。</text>', '</g></svg>'])
(OUT/'map_layout.svg').write_text('\n'.join(svg),encoding='utf8')
physics=json.loads((OUT/'physics_validation.json').read_text(encoding='utf8'))
perf=json.loads((OUT/'performance.json').read_text(encoding='utf8'))
export=json.loads((OUT/'export_report.json').read_text(encoding='utf8'))
report=['# 溪灯驿站 · 河谷环线 v1','', '2026-10-27。原创室外地图场景，已接入项目默认启动入口。人物、互动、战斗和建筑室内尚未接入；5～10 分钟仅是区域体量目标，未宣称游玩时长验收。','', '## 打开与操作','', '- 默认运行项目，或打开 `res://scenes/lanternbrook_map_preview.tscn`。','- 右键环视，中键平移，滚轮缩放，R 回驿站，Tab 隐藏界面。','- 1～5 跳转入口、庭院、石桥、河岸、遗迹。','- 原展示入口仍在 `res://scenes/main.tscn`；原 Blender 源文件未覆盖。新入口保留原地图实例的平移与旋转。','', '## 源文件与布局','', '- `Lanternbrook_Map_v1.blend`：可编辑完整地图，含分集合模型、五个区域相机及灯光。','- `map_layout.svg`：有标注的俯视布局；`renders/map_top.png`：实际 Godot 俯视截图。','- `renders/region_1_1280.png` 至 `region_5_1920.png`：五区域实机图；`*_reverse.png`：反向观察图。','- 全部环境模型、程序纹理和布局为本项目原创。延续原样板的 Blender MCP 工具及 MIT 许可记录，无新增第三方美术素材。','', '## 编辑与接入','', '正式内容入口为 `res://world/maps/lanternbrook/lanternbrook_map.tscn`。Art 下分为入口、庭院、石桥、河岸、遗迹、远景六个场景；可打开各 `art_*.scn` 编辑。重型几何与地面三角碰撞存为压缩二进制场景，主场景保留可读的节点与属性。','', '- `Collision/GroundAndDecks`：地面、桥面、台阶与遗迹平台，物理层 1。','- `Collision/Obstacles`：建筑、树干、岩石、柱子及主要道具；`RiverBoundary` 与 `MapBoundary` 阻止进入河流及地图外侧，均在物理层 2。草叶、花朵与树冠不阻挡行走。','- `WalkableRegion`：按真实地面和阻挡轮廓预烘焙导航；导航半径 0.5m、高度 1.6m、最大台阶 0.3m。后续接入角色时按正式体型复核。','- `Markers/Spawn`、`InnDoor`、`Exit`、`RuinsEntry`、`UpperBridge`：稳定名称的 Marker3D，位置均为地图本地坐标；接入者通过 `global_transform` 获取世界位置。门口与出口仅为连接标记。','- `Routes/MainRoute`、`ReturnRoute`、`InnApproach`：连续 Path3D；区域名称见 `Regions`。','- `environment_motion.gd`：水轮动画、遮挡渐隐。导出的 `focus_target` 可指向后续角色 Node3D；未指定时使用观察镜头的焦点。树冠、屋顶及前景边界岩石淡出，碰撞始终保留。','- `prototype/map_observer.tscn`：独立观察工具，可整段移除。其 `focus_target` 可接入跟随目标；输入动作全部使用 `world_map_` 前缀，复位沿用 `world_reset`。','- 水流材质继续使用 `world/environments/lanternbrook/river_material.tres`，风摆参数保存在各分区的 ShaderMaterial。','', '## 验证记录','', f'- 几何：{export["export_meshes"]} 个分区/材质网格，{export["export_triangles"]:,} 三角面。',f'- 主线、返回线与门口支线：{physics["samples"]} 次胶囊探测，半径 0.30m、高 1.6m，中心及左右偏移 0.70m，共检查约 2m 净宽；失败 {len(physics["failures"])} 次。', f'- 相邻采样支撑高度最大变化 {physics["maximum_adjacent_height_change"]:.3f}m；两座桥和遗迹缓坡通过。',f'- 导航：{len(physics["navigation"])} 段路径请求均返回路径；河流与四侧边界检查结果见 `physics_validation.json`。', f'- 镜头：{len(physics["camera_checks"])} 组区域、角度、俯仰及缩放检查；输入及复位结果见同一文件。','', '| 分辨率 | 区域 | 平均帧时间 | P95 帧时间 |','|---|---|---:|---:|']
for item in perf['measurements']:
    report.append(f'| {item["actual_size"]} | {data["regions"][item["region"]-1]["label"]} | {item["average_ms"]:.2f} ms | {item["p95_ms"]:.2f} ms |')
report+=['', '实测设备：'+perf['adapter']+'，Godot 4.6.2 Forward+。每区域预热 35 帧后采样 90 帧；两种分辨率均核对了实际截图尺寸。该结果是当前本机短时场景测试，尚未包含人物/玩法负载，也不是最低配置或长时间游玩验收。','', '## 重建与维护','', '1. Blender 打开旧样板源文件，经 `tools/blender/build_map_v1.py` 生成独立新地图；该步骤会重建新地图，应先另存手工修改。','2. 在新地图中运行 `tools/blender/export_map_v1.py`，更新 `map_art.glb` 与元数据。','3. 等 Godot 导入完成，执行 `godot --headless --path <项目目录> --script res://tools/bake_map_v1.gd`，生成分区、碰撞、灯光、导航与观察场景。','4. 执行 `godot --path <项目目录> --script res://tools/validate_map_v1.gd`，进行独立窗口验证与截图，再运行 `python tools/write_map_delivery.py` 更新本说明。','', '地图主题与遗迹装饰继续属于视觉候选，不自动新增正式剧情、任务或世界观规则。']
(OUT/'README.md').write_text('\n'.join(report)+'\n',encoding='utf8')
print('Map layout and delivery notes written.')
