# 溪灯驿站：材质与光影 v2

2026-10-27。用户授权“你改吧”。保留布局、出生点、碰撞、原地图实例变换，以及20度/距离96/小幅旋转的长焦镜头。

## 完成内容

- 木梁与木平台：原创精细木纹，横向纤维、木结、开裂和磨损；材质种类分别控制粗糙度与细小法线起伏。
- 石桥、石阶、遗迹与岩石：原创石灰岩纹理，矿物层、孔洞与细裂纹；地势低处增加湿色，表面苔藓按朝向及位置分布。
- 屋瓦、灰泥、土路与林地：代码原生绘制的辅助纹理，明确瓦缝和磨损边缘，墙脚潮痕及檐下旧色；土路边缘与同坐标林地纹理混合。
- 地被：新的成簇草叶精灵替换原来的细碎草纹，2264组合批；另有322片贴地树下落叶。全部无行走阻挡。
- 光影：冷色环境光、主光与局部门廊暖光分层，窗灯材质有明暗差异，接触阴影加深；加入轻景深，主体路线仍清晰。
- 六区域地图与完整可编辑 Blender 源文件均已保存；Godot 为实时材质、碰撞、水流和光照最终依据。

## 实机证据

前图：before/region_1.png 至 region_6.png，使用本轮修改前的新镜头。
最终图：../renders/region_1_1280.png 至 region_6_1280.png，以及1920版本和各区域左右旋转图。
after/ 是中途迭代截图，最终以 renders/ 为准。

validation.json：1593次临时碰撞探针，0通路失败；34段导航请求全部返回；54组区域镜头、216次边角地形射线、输入与镜头上下限通过。
RTX 4060 Laptop GPU，Godot4.6.2 Forward+；720p与1080p各六区域，预热30帧后记录90帧；平均约6.05—6.07ms，P95最高6.74ms。这是短时场景实测，不包含人物或正式游玩验收。

本轮发现并修复制作流程中 MultiMesh 在无渲染后端下保存变换为零的问题。正式场景已在渲染后端生成并重新加载检查：217树干、2264草丛及331林下细节的变换均实际存在。贴图导入必须开启mipmap，以避免远处细纹闪烁。分区只在完成修改后打包一次，避免替换仍被引用的资源缓冲。

## 回退与重建

before_texture_pass.zip 为修改前的地图目录与关键制作脚本备份，不包括Blender。认可过的 Lanternbrook_HD2D_ArtPass.blend 保留不变。

重建：make_texture_pass_assets.py → Godot重新导入 → 有渲染后端运行 tools/author_hd2d_pass.gd（不要 --headless）→ validate_hd2d.gd → write_hd2d_complete_delivery.py。Blender从 ArtPass 源文件运行 complete_hd2d_source.py。

## 原创生成素材与完整提示词

使用内置 imagegen；没有使用API或第三方游戏贴图。三张原图复制到 world/maps/lanternbrook_hd2d/textures/ 后直接使用，未用Python裁切或重绘生成图；草丛保留原始Alpha。逻辑像素采样与微凹凸在实时着色器中计算。其他辅助纹理是代码原生绘制。

### chestnut_handpainted_v2.png

Use case: stylized-concept. Asset type: one seamless repeating diffuse/albedo game texture, flat square full-bleed, for weathered chestnut timber in a finely detailed HD2D fantasy woodland inn. Primary request: create an original artisan pixel-art timber surface with convincing wood substance. Entire image is the same single wooden surface, straight-on orthographic, absolutely no perspective or surrounding objects. Four wide horizontal chestnut planks, irregular hairline dark gaps, long fibrous wood grain flowing horizontally, two subtle elliptical knots across whole sheet, worn amber ridges and dark brown growth rings, a few fine splits and nail heads in plausible places. Broad relatively quiet warm brown grain masses with meticulously grouped small pixel clusters, not random noise. Palette earthy dark umber, muted walnut, chestnut, warm desaturated honey rubbed edges. Painterly pixel art intended to be quantized to a 256px sampling grid in a 3D game. Flat neutral diffuse lighting; no cast shadows, no glossy specular, no baked light gradient, no border, no text, no symbols, no watermark. Keep all four edges seamlessly tileable and wood grain continuous. Material should feel old and tactile, never plastic, never clean uniform stripes.

### limestone_handpainted_v2.png

Use case: stylized-concept. Asset type: single seamless tileable ALBEDO texture for weathered limestone stone in an original detailed HD2D woodland game. One flat full-bleed square representing a continuous single stone surface, NOT a wall of bricks, NO mortar, NO paving grid. A warm gray buff limestone surface with large quiet soft grey-beige mineral masses, tactile pits and faint thin fractured veins, a few eroded cream chips, subtly darker stone pores, delicate mineral layering and localized sparse olive lichen freckles. Think lovingly hand-painted 256px pixel texture made of purposeful clustered pixels, finely detailed but restrained, no photographic grit. Neutral diffuse color only, no lighting direction, no specular, no perspective, no shadows, no border, no text, no watermark. Consistent brightness across edges for seamless repeat. Colors predominantly desaturated warm gray (roughly RGB125,124,108), with darker gray brown pores and pale warm grey mineral edge highlights. Do not make it green overall; lichen extremely sparse. This texture is sampled on individual beveled bridge blocks, river rocks and ancient ruins; geometry already supplies block boundaries so absolutely no drawn bricks.

### groundcover_handpainted_v2.png

Use case: stylized-concept. Asset type: ONE isolated groundcover sprite for an original finely detailed pixel-art HD2D woodland game, genuine transparent background. A small natural grouping of soft low wild grass with a few broad leaves and tiny clover, wide and low silhouette roughly 2.3:1 width to height, seen from a low oblique game camera, full clump centered with clear transparent padding. Hand-painted pixel art with purposeful coherent pixel clusters like classic late 16-bit forest scenery enriched with modern depth, muted sage and olive-green midtones, darker deep green internal leaves and a few pale desaturated straw-green blade tips. Several connected tufts growing together, blades overlap to make substantial readable forms. No black outline, no black dots, no detached scatter, no soil rectangle, no terrain tile, no rocks, no flowers, no trees, no lighting glow, no text, no watermark. Soft neutral diffuse light; intrinsic shading only. This sprite will be sampled at about 128 logical pixels and viewed at small size, so prioritize readable groups over fine thin noisy isolated grass hairs. NOT photorealistic, NOT glossy 3D render. Actual alpha transparency around every leaf.
