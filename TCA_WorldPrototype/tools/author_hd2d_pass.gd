extends SceneTree
## Offline, reversible art direction pass. The shipped v1 map is never overwritten.
const BASE := "res://world/maps/lanternbrook_hd2d/"
var map: Node3D
var materials: Dictionary = {}
var texture_manifest: Dictionary = {}
var rng := RandomNumberGenerator.new()
var route_segments := PackedVector4Array()

func support_height(p: Vector3) -> float:
	var query := PhysicsRayQueryParameters3D.create(p+Vector3.UP*35,p-Vector3.UP*20,5)
	var hit := map.get_world_3d().direct_space_state.intersect_ray(query)
	return float(hit.position.y) if not hit.is_empty() else NAN

func close_terrain_seam(camera_surfaces: Node3D) -> void:
	var tool := SurfaceTool.new()
	tool.begin(Mesh.PRIMITIVE_TRIANGLES)
	var records: Array = []
	# A narrow continuous ring joins the fine terrain to the coarse distant apron.
	# The old apron omitted whole 6m cells at the edge, leaving short visible gaps.
	var inner: Array[Vector3] = [Vector3(-49.6,0,-39.6),Vector3(49.6,0,-39.6),Vector3(49.6,0,39.6),Vector3(-49.6,0,39.6)]
	var outer: Array[Vector3] = [Vector3(-56,0,-46),Vector3(56,0,-46),Vector3(56,0,46),Vector3(-56,0,46)]
	for side in range(4):
		var next := (side+1)%4
		var steps := 100 if side%2==0 else 80
		for i in range(steps):
			var a := inner[side].lerp(inner[next],float(i)/steps)
			var b := inner[side].lerp(inner[next],float(i+1)/steps)
			var c := outer[side].lerp(outer[next],float(i)/steps)
			var d := outer[side].lerp(outer[next],float(i+1)/steps)
			a.y = support_height(a)
			b.y = support_height(b)
			c.y = support_height(c)
			d.y = support_height(d)
			for strip in range(8):
				var vertices := [a.lerp(c,float(strip)/8),a.lerp(c,float(strip+1)/8),b.lerp(d,float(strip+1)/8),b.lerp(d,float(strip)/8)]
				for k in range(4):
					var current_height := support_height(vertices[k])
					if not is_nan(current_height):
						vertices[k].y = maxf(vertices[k].y,current_height)
					vertices[k].y += .018
				for ids in [[0,1,2],[0,2,3]]:
					for id in ids:
						var p: Vector3 = vertices[id]
						tool.set_normal(Vector3.UP)
						tool.set_uv(Vector2(p.x,-p.z)*.7)
						tool.add_vertex(p)
						records.append([p.x,p.y,p.z])
	var seam := own(MeshInstance3D.new(),map.get_node("Art/CompleteTransitions"),"BackdropSeam") as MeshInstance3D
	seam.mesh = tool.commit()
	seam.material_override = materials["Engine_Mossy earth"]
	var body := own(StaticBody3D.new(),camera_surfaces,"BackdropSeam") as StaticBody3D
	body.collision_layer = 4
	body.collision_mask = 0
	var shape := own(CollisionShape3D.new(),body,"Support") as CollisionShape3D
	shape.shape = seam.mesh.create_trimesh_shape()
	(shape.shape as ConcavePolygonShape3D).backface_collision = true
	var file := FileAccess.open(BASE+"terrain_seam.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(records))

func soften_perimeter(mesh: Mesh) -> Mesh:
	var result := ArrayMesh.new()
	for surface in range(mesh.get_surface_count()):
		var arrays := mesh.surface_get_arrays(surface)
		var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		for i in range(vertices.size()):
			var factor := .28 if vertices[i].z>28 or vertices[i].x>41 else .60
			vertices[i].y = .2+(vertices[i].y-.2)*factor
		arrays[Mesh.ARRAY_VERTEX] = vertices
		result.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES,arrays)
		result.surface_set_material(surface,mesh.surface_get_material(surface))
	return result

func without_old_armillary(mesh: Mesh) -> Mesh:
	var surface := SurfaceTool.new()
	surface.begin(Mesh.PRIMITIVE_TRIANGLES)
	for index in range(mesh.get_surface_count()):
		var arrays := mesh.surface_get_arrays(index)
		var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
		var normals: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
		var uvs: PackedVector2Array = arrays[Mesh.ARRAY_TEX_UV]
		var ids: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
		if ids.is_empty():
			for i in range(vertices.size()):
				ids.append(i)
		for i in range(0,ids.size(),3):
			var center := (vertices[ids[i]]+vertices[ids[i+1]]+vertices[ids[i+2]])/3
			if absf(center.x+25)<.65 and absf(center.z+28)<.65 and center.y>1.15:
				continue
			for k in range(3):
				var id: int = ids[i+k]
				surface.set_normal(normals[id])
				surface.set_uv(uvs[id])
				surface.add_vertex(vertices[id])
	var result := surface.commit()
	result.surface_set_material(0,mesh.surface_get_material(0))
	return result

func _initialize() -> void:
	if DisplayServer.get_name()=="headless":
		push_error("This authoring pass requires a rendering backend to preserve MultiMesh buffers. Run without --headless.")
		quit(2)
		return
	call_deferred("build")

func own(node: Node, parent: Node, label: String) -> Node:
	node.name = label
	parent.add_child(node)
	node.owner = map
	return node

func material_for(old: StandardMaterial3D) -> Material:
	var label: String = old.resource_name
	if materials.has(label):
		return materials[label]
	var lower := label.to_lower()
	var texture_name := ""
	var moss := 0.0
	var tint := Color.WHITE
	var scale := .7
	if "amber windows" in lower or "honey glow" in lower:
		var glass := ShaderMaterial.new()
		glass.resource_name = "TexturePass_"+label
		glass.shader = load(BASE+"window_glass_v2.gdshader")
		glass.set_shader_parameter("lantern","honey glow" in lower)
		materials[label] = glass
		return glass
	if "slate" in lower:
		texture_name = "slate"
		tint = Color(1.0,1.0,1.0).darkened(float(abs(label.hash())%5)*.025)
		scale = .55
	elif "chestnut" in lower:
		texture_name = "chestnut"
	elif "plank" in lower:
		texture_name = "oak"
	elif "bark" in lower:
		texture_name = "bark"
	elif "limestone" in lower or "dressed stone" in lower:
		texture_name = "limestone"
		moss = .30
		tint = Color.WHITE.darkened(float(abs(label.hash())%4)*.035)
	elif "plaster" in lower:
		texture_name = "plaster"
	elif "earth" in lower:
		texture_name = "earth"
		moss = .25
		scale = .8
	elif "gravel" in lower:
		texture_name = "path"
		moss = .19
	elif "woven" in lower:
		texture_name = "canvas"
	if texture_name.is_empty():
		var copy := old.duplicate() as StandardMaterial3D
		copy.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
		copy.roughness = .9
		if "iron" in lower:
			copy.roughness = .64
		if "brass" in lower:
			copy.roughness = .48
		if "flower" in lower:
			copy.albedo_color = copy.albedo_color.darkened(.28)
		materials[label] = copy
		return copy
	var mat := ShaderMaterial.new()
	mat.shader = load(BASE+"pixel_surface.gdshader")
	mat.resource_name = "Pixel_"+label.trim_prefix("Engine_")
	mat.set_shader_parameter("pixel_texture",load(BASE+"textures/"+texture_name+".png"))
	mat.set_shader_parameter("tint",tint)
	mat.set_shader_parameter("texture_scale",scale)
	mat.set_shader_parameter("moss_amount",moss)
	mat.set_shader_parameter("ground_surface",texture_name in ["earth","path"])
	mat.set_shader_parameter("path_surface",texture_name == "path")
	if texture_name == "path":
		mat.set_shader_parameter("path_segments",route_segments)
		mat.set_shader_parameter("segment_count",route_segments.size())
	configure_surface(mat,texture_name)
	materials[label] = mat
	texture_manifest[label] = texture_name
	return mat

func configure_surface(mat: ShaderMaterial, texture_name: String) -> void:
	var files := {"chestnut":"chestnut_handpainted_v2","oak":"chestnut_handpainted_v2","limestone":"limestone_handpainted_v2","plaster":"plaster_v2","slate":"slate_mineral_v2","earth":"forest_floor_v2","path":"path_soil_v2"}
	if files.has(texture_name):
		mat.set_shader_parameter("pixel_texture",load(BASE+"textures/"+files[texture_name]+".png"))
	var kinds := {"limestone":0,"chestnut":1,"oak":1,"bark":1,"slate":2,"plaster":3,"earth":4,"path":5}
	var roughness := {"limestone":.88,"chestnut":.82,"oak":.79,"slate":.72,"plaster":.97,"earth":1.,"path":.98}
	mat.set_shader_parameter("material_kind",kinds.get(texture_name,0))
	mat.set_shader_parameter("base_roughness",roughness.get(texture_name,.93))
	mat.set_shader_parameter("source_pixels",256. if files.has(texture_name) else 64.)
	mat.set_shader_parameter("relief_strength",.12 if texture_name in ["limestone","chestnut","oak"] else .06)
	if texture_name == "oak":
		mat.set_shader_parameter("tint",Color(1.08,1.10,1.03))
	if texture_name == "chestnut":
		mat.set_shader_parameter("tint",Color(.82,.91,.97))
	if texture_name in ["earth","path"]:
		mat.set_shader_parameter("texture_scale",.42)
		mat.set_shader_parameter("moss_amount",0.)
		mat.set_shader_parameter("ground_texture",load(BASE+"textures/forest_floor_v2.png"))
	if texture_name == "limestone":
		mat.set_shader_parameter("texture_scale",.26)
	if texture_name in ["chestnut","oak"]:
		mat.set_shader_parameter("texture_scale",.33)

func pack_branch(node: Node, path: String) -> void:
	for child in node.find_children("*","",true,false):
		child.owner = node
	node.owner = null
	var packed := PackedScene.new()
	packed.pack(node)
	ResourceSaver.save(packed,path,ResourceSaver.FLAG_COMPRESS)
	var parent := node.get_parent()
	parent.remove_child(node)
	node.free()
	var instance: Node = ResourceLoader.load(path,"PackedScene",ResourceLoader.CACHE_MODE_IGNORE).instantiate()
	parent.add_child(instance)
	instance.owner = map

func build() -> void:
	rng.seed = 271027
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://world/maps/lanternbrook/map_data.json"))
	for route in data.routes:
		for i in range(route.size()-1):
			route_segments.append(Vector4(route[i][0],route[i][2],route[i+1][0],route[i+1][2]))
	map = load("res://world/maps/lanternbrook/lanternbrook_map.tscn").instantiate()
	root.add_child(map)
	# Normalize legacy automatic names before adding lamps. Serialized @ names can
	# collide with the engine's new automatic-name counter when a scene is reloaded.
	var lamp_index := 0
	for lamp in map.get_node("Lighting").get_children():
		if lamp is OmniLight3D:
			lamp.name = "Lantern_%02d"%lamp_index
			lamp_index += 1
	var art := map.get_node("Art")
	var replaced := 0
	for partition in art.get_children():
		var replacement := Node3D.new()
		replacement.name = partition.name
		for original in partition.get_children():
			if not original is MeshInstance3D:
				continue
			var label := String(original.name)
			if label.begins_with("Canopy"):
				continue
			# Replace the evenly scattered triangular grass with authored pixel clumps.
			if "Meadow" in label:
				continue
			# Full-height low-poly trunks protrude through illustrated leaf-card holes.
			if label.ends_with("Bark") or label.ends_with("Silver birch bark"):
				continue
			var mesh := MeshInstance3D.new()
			mesh.name = label
			mesh.mesh = without_old_armillary(original.mesh) if label.begins_with("Ruins") and "Aged brass" in label else original.mesh
			if label.begins_with("ForegroundRock"):
				mesh.mesh = soften_perimeter(mesh.mesh)
			mesh.transform = original.transform
			replacement.add_child(mesh)
			mesh.owner = replacement
			if label.begins_with("River"):
				mesh.material_override = load(BASE+"river_material.tres")
			else:
				for surface in range(mesh.mesh.get_surface_count()):
					var old := mesh.mesh.surface_get_material(surface) as StandardMaterial3D
					if old != null:
						if label.begins_with("ForegroundRock"):
							var cliff := material_for(old).duplicate() as ShaderMaterial
							cliff.set_shader_parameter("tint",Color(.47,.63,.56))
							cliff.set_shader_parameter("moss_amount",.65)
							mesh.set_surface_override_material(surface,cliff)
						else:
							mesh.set_surface_override_material(surface,material_for(old))
			replaced += 1
		var label: String = partition.name
		art.remove_child(partition)
		partition.free()
		art.add_child(replacement)
		replacement.owner = map
		# Pack once after finishing; repeated in-place MultiMesh serialization can
		# replace its transform buffer while the old scene still references it.
	await physics_frame
	await physics_frame
	var completion: RefCounted = load("res://tools/complete_hd2d_regions.gd").new()
	var completed: Dictionary = await completion.build(self,map,data)
	# Camera support follows the visible distant apron and river, without extending
	# the player's walkable region beyond the boundary or adding blocking foliage.
	var camera_surfaces := own(Node3D.new(),map.get_node("Collision"),"CameraSurfaces") as Node3D
	for visual in art.find_children("*","MeshInstance3D",true,false):
		if not String(visual.name).begins_with("Backdrop") and not String(visual.name).begins_with("River"):
			continue
		var body := own(StaticBody3D.new(),camera_surfaces,String(visual.name)) as StaticBody3D
		body.collision_layer = 4
		body.collision_mask = 0
		body.transform = visual.global_transform
		var shape := own(CollisionShape3D.new(),body,"Support") as CollisionShape3D
		shape.shape = visual.mesh.create_trimesh_shape()
		(shape.shape as ConcavePolygonShape3D).backface_collision = true
	await physics_frame
	await physics_frame
	close_terrain_seam(camera_surfaces)
	pack_branch(camera_surfaces,BASE+"camera_surfaces.scn")
	# The main and optional lookout paths share the same natural edge treatment.
	route_segments.clear()
	for route in data.routes:
		for i in range(route.size()-1):
			route_segments.append(Vector4(route[i][0],route[i][2],route[i+1][0],route[i+1][2]))
	var forest := own(Node3D.new(),art,"PixelWoodland") as Node3D
	var crown_materials: Array[ShaderMaterial] = []
	for color in [Color(1,1,1),Color(.84,.98,.95),Color(1.08,1.02,.83),Color(.9,.94,1.0)]:
		var mat := ShaderMaterial.new()
		mat.shader = load(BASE+"pixel_canopy.gdshader")
		mat.set_shader_parameter("crown_texture",load(BASE+"textures/woodland_crown.png"))
		mat.set_shader_parameter("leaf_tint",color)
		crown_materials.append(mat)
	var tree_count := 0
	var trunk_transforms: Array[Transform3D] = []
	var forest_placement: Array = []
	for collider in data.colliders:
		if collider.kind != "trunk":
			continue
		var p := Vector3(collider.position[0],collider.position[1],collider.position[2])
		var h: float = collider.size[1]
		var bottom := p.y-h*.5
		var ruin_distance := Vector2(p.x+25,p.z+28).length()
		if ruin_distance<15 and p.x>-31 and p.z>-33:
			h *= .58
		if Vector2(p.x-28,p.z-30).length()<11 and p.z>26 and p.x>23:
			h *= .5
		p.y = bottom+h*.5
		var crown := own(MeshInstance3D.new(),forest,"CanopyPixel_%03d"%tree_count) as MeshInstance3D
		var quad := QuadMesh.new()
		var width := clampf(h*.95+1.7,3.5,9.0)
		quad.size = Vector2(width,width*.91)
		crown.mesh = quad
		crown.position = p+Vector3(0,h*.42,0)
		crown.rotation = Vector3(-.55,.56,0)
		var river_center := -3.0-.11*p.z-.55*sin(.26*p.z)
		var is_willow := p.z>-27 and p.z<0 and absf(p.x-river_center)<10
		var material := crown_materials[tree_count%4]
		if is_willow:
			material = material.duplicate() as ShaderMaterial
			material.set_shader_parameter("crown_texture",load(BASE+"textures/river_willow.png"))
		crown.material_override = material
		crown.extra_cull_margin = .15
		var diameter: float = maxf(float(collider.size[0]),float(collider.size[2]))
		trunk_transforms.append(Transform3D(Basis.IDENTITY.scaled(Vector3(diameter,h*.72,diameter)),p-Vector3.UP*h*.14))
		forest_placement.append({"name":String(crown.name),"position":[crown.position.x,crown.position.y,crown.position.z],"width":width,"height":width*.91,"trunk_position":[p.x,p.y-h*.14,p.z],"trunk_size":[diameter,h*.72,diameter],"texture":"river_willow.png" if is_willow else "woodland_crown.png","tint":tree_count%4})
		tree_count += 1
	var trunks := own(MultiMeshInstance3D.new(),forest,"PixelTreeTrunks") as MultiMeshInstance3D
	var cylinder := CylinderMesh.new()
	cylinder.top_radius = .36
	cylinder.bottom_radius = .5
	cylinder.height = 1.0
	cylinder.radial_segments = 8
	cylinder.material = materials.get("Engine_Bark")
	if cylinder.material == null:
		var bark := ShaderMaterial.new()
		bark.shader = load(BASE+"pixel_surface.gdshader")
		bark.set_shader_parameter("pixel_texture",load(BASE+"textures/bark.png"))
		configure_surface(bark,"bark")
		cylinder.material = bark
	var trunk_multi := MultiMesh.new()
	trunk_multi.transform_format = MultiMesh.TRANSFORM_3D
	trunk_multi.mesh = cylinder
	trunk_multi.instance_count = trunk_transforms.size()
	for i in range(trunk_transforms.size()):
		trunk_multi.set_instance_transform(i,trunk_transforms[i])
	trunks.multimesh = trunk_multi
	await physics_frame
	await physics_frame
	var clumps: Array[Transform3D] = []
	var grass := ShaderMaterial.new()
	grass.shader = load(BASE+"pixel_groundcover.gdshader")
	grass.set_shader_parameter("grass_texture",load(BASE+"textures/groundcover_handpainted_v2.png"))
	for i in range(6500):
		var p := Vector3(rng.randf_range(-49,49),0,rng.randf_range(-39,39))
		var distance := 1000.0
		for s in route_segments:
			var a := Vector2(s.x,s.y)
			var v := Vector2(s.z,s.w)-a
			var t := clampf((Vector2(p.x,p.z)-a).dot(v)/maxf(v.length_squared(),.001),0,1)
			distance = minf(distance,Vector2(p.x,p.z).distance_to(a+v*t))
		if distance<1.1 or Vector2(p.x+25,p.z+28).length()<5.4 or (distance>5 and rng.randf()<.68):
			continue
		var query := PhysicsRayQueryParameters3D.create(p+Vector3.UP*10,p-Vector3.UP*10,3)
		var hit := map.get_world_3d().direct_space_state.intersect_ray(query)
		if hit.is_empty() or hit.position.y>1.1:
			continue
		p.y = hit.position.y+.30
		var scale := rng.randf_range(.7,1.35)
		clumps.append(Transform3D(Basis.from_euler(Vector3(-.18,.56,0)).scaled(Vector3.ONE*scale),p))
	var foliage := own(MultiMeshInstance3D.new(),forest,"RoadsidePixelGrass") as MultiMeshInstance3D
	foliage.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var grass_quad := QuadMesh.new()
	grass_quad.size = Vector2(1.35,.56)
	grass_quad.material = grass
	var multi := MultiMesh.new()
	multi.transform_format = MultiMesh.TRANSFORM_3D
	multi.mesh = grass_quad
	multi.instance_count = clumps.size()
	for i in range(clumps.size()):
		multi.set_instance_transform(i,clumps[i])
	foliage.multimesh = multi
	var placements := FileAccess.open(BASE+"forest_placement.json",FileAccess.WRITE)
	placements.store_string(JSON.stringify(forest_placement,"\t"))
	var groundcover: Array = []
	for placement in clumps:
		groundcover.append({"position":[placement.origin.x,placement.origin.y,placement.origin.z],"scale":placement.basis.get_scale().x})
	placements = FileAccess.open(BASE+"understory_placement.json",FileAccess.WRITE)
	placements.store_string(JSON.stringify(groundcover,"\t"))
	# Preserve all original collision, navigation, marker and map transforms.
	var environment := map.get_node("Lighting/WorldEnvironment").environment as Environment
	environment = environment.duplicate() as Environment
	map.get_node("Lighting/WorldEnvironment").environment = environment
	environment.ambient_light_color = Color(.39,.49,.60)
	environment.ambient_light_energy = .50
	environment.tonemap_exposure = 1.13
	environment.tonemap_agx_contrast = 1.45
	environment.ssao_radius = .90
	environment.ssao_intensity = 1.65
	environment.glow_intensity = .30
	environment.glow_hdr_threshold = 1.45
	environment.fog_light_color = Color(.21,.33,.37)
	environment.fog_density = .0018
	var sun := map.get_node("Lighting/EveningSun") as DirectionalLight3D
	sun.light_color = Color(1,.86,.70)
	sun.light_energy = 1.45
	sun.rotation_degrees = Vector3(-38,-55,0)
	var fill := map.get_node("Lighting/WarmFill") as DirectionalLight3D
	fill.light_color = Color(.47,.63,.76)
	fill.light_energy = .08
	for lamp in map.get_node("Lighting").get_children():
		if lamp is OmniLight3D:
			if String(lamp.name).begins_with("Lantern"):
				var near_inn: bool = Vector2(lamp.position.x-3.2,lamp.position.z+2).length()<6
				lamp.light_energy = 1.65 if near_inn else .85+float(abs(String(lamp.name).hash())%4)*.16
				lamp.omni_range = 4.1 if near_inn else 3.6
				lamp.shadow_enabled = near_inn and lamp.position.z>-.7
	# Weathering remains in map coordinates when the complete map instance is moved.
	var finish: RefCounted = load("res://tools/texture_finish.gd").new()
	await finish.apply(self,map,data)
	for branch in art.get_children():
		var prefix := "" if String(branch.name).begins_with("Complete") or String(branch.name) in ["PixelWoodland","TextureFinish"] else "art_"
		pack_branch(branch,BASE+prefix+String(branch.name).to_snake_case()+".scn")
	var packed := PackedScene.new()
	packed.pack(map)
	ResourceSaver.save(packed,BASE+"lanternbrook_hd2d.tscn")
	var report := {"materials":texture_manifest,"pixel_crowns":tree_count,"grass_clumps":clumps.size(),"retained_meshes":replaced,"completion":completed,"base_map":"res://world/maps/lanternbrook/lanternbrook_map.tscn","scope":"Complete HD2D outdoor map; original map remains available"}
	var f := FileAccess.open(BASE+"art_pass.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(report,"\t"))
	print("HD2D_AUTHORED ",JSON.stringify(report))
	var key := InputEventKey.new()
	key.physical_keycode = KEY_6
	ProjectSettings.set_setting("input/world_map_region_6",{"deadzone":.2,"events":[key]})
	ProjectSettings.set_setting("layer_names/3d_physics/layer_3","CameraSupport")
	ProjectSettings.save()
	map.free()
	completion = null
	await process_frame
	await process_frame
	quit()
