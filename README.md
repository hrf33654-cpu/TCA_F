# TCA

TCA 当前设计与原型开发工作区。

## 项目入口

- [TCA_ID](TCA_ID/README.md)：设计总纲、角色、配方、视觉参考与美术资产。
- [TCA_BattlePrototype](TCA_BattlePrototype/README.md)：独立战斗原型的目标与实施边界。
- [TCA_WorldPrototype](TCA_WorldPrototype/README.md)：Godot 世界探索原型。

规则与设计效力以各子项目文档及当前统一总纲为准。

## 获取与开发

此仓库使用 Git LFS 保存图片、视频、模型与美术源文件。克隆前请安装 Git LFS：

```sh
git lfs install
git clone https://github.com/hrf33654-cpu/TCA_F.git
cd TCA_F
git lfs pull
```

使用 Godot 打开 `TCA_WorldPrototype/project.godot`；引擎版本和运行方式参见该子项目说明。

`tca_past/` 是本地历史参考工作区，保留独立仓库，不纳入本仓库。引擎缓存、本地生成工具、临时日志、自动备份及凭据文件同样不提交。
