# 溪灯驿站 · Lanternbrook

2026-10-27，TCA 世界探索视觉样板。原创 3D 环境，为斜视镜头与后续像素角色结合而制作；本批次只含场景，不含角色。

## 看图与打开文件

- `renders/Lanternbrook_final.png`：2400 × 1500 主视角，Blender Cycles 渲染。
- `renders/Lanternbrook_reverse_view.png`：1800 × 1350 另一侧视角，可见水轮与门廊。
- `renders/Godot_final.png`：Godot 4.6.2 Forward+ 的实际运行截图，和离线成图分别保留。
- `Lanternbrook_HD2D.blend`：可编辑源文件。建筑、地形、植被、桥路、水体、道具与光照按集合组织。
- `../../world/environments/lanternbrook/lanternbrook.glb`：引擎资源，包含内嵌贴图。
- `../../world/environments/lanternbrook/lanternbrook.tscn`：Godot 展示场景，已接到项目默认入口。

## 视觉设计

用青绿色瓦顶与溪水串起画面，以暖色窗灯形成视觉中心。拱桥、步道与门口构成连贯动线；前景树木、河岸、建筑和远处岩壁分出空间层次。瓦片、木梁、窗框、石桥、草木、藤蔓、蕨类、炼金招牌、瓶罐、木桶、水轮与门廊均为实际几何。

主相机为正交斜视，宽度约 28.2 个场景单位，焦点位于房屋和桥之间。源文件内保留可调景深、体积薄雾、冷色环境补光与黄昏暖光。

## 在 Godot 查看

用 Godot 4.6.2 打开本项目并运行默认场景。右键拖动环视，滚轮缩放，R 复位，Tab 隐藏说明。水面采用沿弯曲河道向下游平移的动态高光、水面起伏与岸边碎泡；静态白色水纹模型在实时预览中隐藏。流速与高光强度可在 `river_material.tres` 调节。所有操作均为场景观察工具；本批次未加入人物、移动碰撞、寻路、剧情、交互或战斗逻辑。

实时版本将几何按区域与材质合并为 62 个网格，约 38.2 万三角面。GLB 内含原创建模与打包的程序生成材质贴图，不依赖 Blender 的程序节点才能显示颜色。实际运行使用 RTX 4060 Laptop、Vulkan Forward+；已验证导入、场景启动与截图，未进行持续帧率或最低配置验收。

源文件的 Cycles 灯光、薄雾与景深与实时展示使用不同渲染流程，两者各有截图，不能将离线成图当作实时渲染结果。

## 素材与工具来源

全部场景几何、配色与材质纹理均在本任务中创建，无外部模型、商业素材包或未注明许可的图片。

控制工具采用 [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) 的本地插件，工具源码位于 `../../tools/blender/blender_mcp.py`，版权声明保留。此次使用 Blender 5.1.1、插件 1.8 / protocol 15，通过本机 `localhost:9877` 控制。9876 被其他程序使用，因此使用单独端口；未修改其他程序。

Godot 光照与后处理参数参照 [Godot 4.6 Environment 文档](https://docs.godotengine.org/en/4.6/classes/class_environment.html)。原项目的 Godot Forge 插件存在两处与 4.6.2 不兼容的编辑器接口；未改动插件。本场景运行与截图日志独立保存在 `../../tools/blender/godot_runtime.log`。

## 继续编辑

直接打开 `.blend` 修改集合中的对象。要重新导出，在 Blender 中运行 `../../tools/blender/export_hamlet.py`。该脚本保留可编辑对象，将临时合批的网格写到 GLB，之后移除临时导出集合。

完整重建顺序为 `build_hamlet.py` → `refine_hamlet.py` → `finish_hamlet.py` → `export_hamlet.py`。这些脚本会重建任务场景，后续手工编辑应保存在单独版本后再重建。

这是探索视觉候选样板；场景主题、建筑与制作方式不自动成为正式世界观或全项目美术定案。

