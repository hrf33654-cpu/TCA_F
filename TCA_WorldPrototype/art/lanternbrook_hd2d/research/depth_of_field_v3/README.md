# 溪灯驿站：分区景深 v3

2026-10-27。根据用户“那你做吧”的授权，完成参考《歧路旅人》的景深调整。默认预览启用新版，D 循环切换新版 / 原版 / 关闭；1～6 切换区域，R 返回驿站，Tab 隐藏审查面板。

## 画面与实现

- 前景保留明确的虚焦，清晰主体集中在中景，远景渐进柔化。初版固定 84m / 110m 的清晰范围改成围绕观察焦点的范围；不同区域分别设定近、远边界及过渡长度。
- 驿站保护门口和庭院，石桥扩大两端通路的清晰范围，遗迹放宽远端清晰距离以保留拱门和石柱。采用高质量圆形散景，关闭采样抖动。
- 平移时，六区参数按空间距离连续混合；缩小时扩大清晰范围，避免把整图压成狭窄的清晰带。距离使用实际相机空间深度，保留地图实例变换、原镜头俯角、长焦距离和转向限制。
- 相机持有独立属性副本，切换对比不修改共享的 v2 资源。对比模式复用原版散景形状和质量，镜头位置完全一致。
- 本轮只修改观察景深、审查面板和记录。地图摆放、树冠大小、碰撞、导航、雾和材质保持现状。河岸和归途仍有树冠与建筑遮挡画面的构图限制，景深不替代后续人物遮挡与构图验证。

参数文件：`world/maps/lanternbrook_hd2d/depth_profiles.json`。距离单位为米；`near_clear` 和 `far_clear` 是相对观察焦点的清晰余量，`near_transition` 和 `far_transition` 是虚化过渡长度。参数按区域中心排列，与 `complete_data.json` 的区域顺序对应。

## 截图与验证

- `before/`：实际修改前六区截图；`after/`：第一轮调试截图。
- `tuned/`：最终新版六区 720p / 1080p；`legacy/`：同镜头原版；`off/`：同镜头关闭景深。
- `limits/`：六区 × 两档缩放极限 × 左右转向极限，共 24 张 1080p 截图；`limits_contact.jpg` 为检查用缩略总览。
- `review_controls.png`：最终审查面板。最终三模式、极限与面板共 61 张实机截图。
- `validation.json`：验证通过、失败列表为空；焦点在清晰范围内，模式切换不移动镜头，原版数值准确恢复，D 三态切换与按键重复保护通过，平移连续性通过。
- 已人工查看新版六区、1080p 驿站和全部 24 个极限视角缩略图。主入口、桥面和遗迹地标保持可辨识，前后景层次可见；美术接受仍由用户审查决定。

设备为 RTX 4060 Laptop、Godot 4.6.2 Forward+。每区预热 30 帧后记录 90 帧，平均帧间隔约 5.85～8.95ms，P95 最高 9.91ms。720p 初始采样期间关闭了上一版预览窗口，因此记录包含本机并行负载变化；这些数据仅证明此次短时运行情况，不用于精确比较版本性能，也不代表人物和正式玩法验收。

复现：以有渲染后端的 Godot 启动项目并执行 `--script res://tools/validate_depth_of_field.gd`。该脚本只拍摄与检查，不重建或覆盖地图资产。

## 参考依据

- [ACQUIRE / Epic Games Japan：Unreal Fest East 2018 制作讲稿](https://docswell.com/s/EpicGamesJapan/KXPWY5-UE4_UFE2018_ACQUIRE_OCTOPATHTRAVELER)：第 19～24 页的早期清晰度探索、第 45 页后处理设置、第 48 页 Bokeh 景深、第 73 页战斗景深变化。
- [Epic 对《歧路旅人Ⅱ》开发团队的采访](https://www.unrealengine.com/developer-interviews/octopath-traveler-ii-builds-a-bigger-bolder-world-in-its-stunning-hd-2d-style?lang=en-US)：固定探索镜头与地图构图的关系。
- [Godot CameraAttributesPractical](https://docs.godotengine.org/en/stable/classes/class_cameraattributespractical.html)：近远景距离及过渡；[Godot RenderingServer](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html)：散景形状、质量与抖动。

本项目采用 Godot 原生景深，不声称还原了《歧路旅人》的未公开参数或全部渲染流程。`hd2d_observer_before.gd.txt` 与 `hd2d_observer_before.tscn.txt` 保留修改前源码；共享 `observer_optics_v2.tres` 仍是原版基准。
