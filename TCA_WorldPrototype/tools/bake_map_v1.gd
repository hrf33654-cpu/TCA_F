extends SceneTree
## Offline authoring: save inspectable scene nodes/resources, never rebuild the map in _ready.
const BASE := "res://world/maps/lanternbrook/"
var map: Node3D
var nav_source := NavigationMeshSourceGeometryData3D.new()
var count: int = 0

func _initialize() -> void:
	call_deferred("build")

func add(parent: Node, node: Node, label: String) -> Node:
	node.name = label
	parent.add_child(node)
	node.owner = map
	return node

func box(parent: Node, label: String, pos: Vector3, size: Vector3, layer: int = 2) -> void:
	var body := add(parent, StaticBody3D.new(), label) as StaticBody3D
	body.collision_layer = layer
	body.collision_mask = 0
	body.position = pos
	var shape := BoxShape3D.new()
	shape.size = size
	var col := add(body, CollisionShape3D.new(), "Shape") as CollisionShape3D
	col.shape = shape
	count += 1
	if layer == 2:
		var outline := PackedVector3Array([pos+Vector3(-size.x/2,0,-size.z/2),pos+Vector3(size.x/2,0,-size.z/2),pos+Vector3(size.x/2,0,size.z/2),pos+Vector3(-size.x/2,0,size.z/2)])
		nav_source.add_projected_obstruction(outline,pos.y-size.y/2,size.y,true)

func vec(data: Array) -> Vector3:
	return Vector3(float(data[0]),float(data[1]),float(data[2]))

func build() -> void:
	var meta: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(BASE+"map_data.json"))
	map = Node3D.new()
	map.name = "LanternbrookMap"
	root.add_child(map)
	map.set_script(load(BASE+"environment_motion.gd"))
	var art := add(map, Node3D.new(), "Art") as Node3D
	var wheel := add(map, Node3D.new(), "Waterwheel") as Node3D
	wheel.position = Vector3(.12,1.35,-4.1)
	var collisions := add(map, Node3D.new(), "Collision") as Node3D
	var ground := add(collisions, Node3D.new(), "GroundAndDecks")
	var obstacles := add(collisions, Node3D.new(), "Obstacles")
	var river_boundary := add(collisions, Node3D.new(), "RiverBoundary")
	var edge := add(collisions, Node3D.new(), "MapBoundary")
	var imported: Node3D = (load(BASE+"map_art.glb") as PackedScene).instantiate()
	root.add_child(imported)
	var river_material := load("res://world/environments/lanternbrook/river_material.tres")
	var foliage_shader := load(BASE+"foliage.gdshader")
	var foliage_materials: Dictionary = {}
	var meshes: int = 0
	for original in imported.find_children("*","MeshInstance3D",true,false):
		var mesh := MeshInstance3D.new()
		mesh.mesh = original.mesh
		mesh.transform = original.global_transform
		var label: String = original.name
		var is_wheel := label.begins_with("Wheel")
		add(wheel if is_wheel else art, mesh, label)
		if is_wheel:
			mesh.position -= wheel.position
		if label.begins_with("River"):
			mesh.material_override = river_material
		if label.begins_with("Canopy") or label.begins_with("Foliage"):
			for surface in range(mesh.mesh.get_surface_count()):
				var old := mesh.mesh.surface_get_material(surface) as StandardMaterial3D
				if old == null:
					continue
				var key := old.resource_path+str(label.begins_with("Canopy"))
				if not foliage_materials.has(key):
					var mat := ShaderMaterial.new()
					mat.shader = foliage_shader
					mat.set_shader_parameter("base_color",old.albedo_color)
					mat.set_shader_parameter("has_texture",old.albedo_texture != null)
					if old.albedo_texture != null:
						mat.set_shader_parameter("albedo_texture",old.albedo_texture)
					mat.set_shader_parameter("wind_strength",0.035 if label.begins_with("Canopy") else 0.018)
					foliage_materials[key] = mat
				mesh.set_surface_override_material(surface,foliage_materials[key])
		if label.begins_with("Ground") or label.begins_with("WalkSurface"):
			var body := add(ground, StaticBody3D.new(),label) as StaticBody3D
			body.collision_layer = 1
			body.collision_mask = 0
			body.transform = mesh.transform
			var col := add(body,CollisionShape3D.new(),"Surface") as CollisionShape3D
			col.shape = mesh.mesh.create_trimesh_shape()
			nav_source.add_mesh(mesh.mesh,mesh.transform)
			count += 1
		meshes += 1
	imported.free()
	for info in meta.colliders:
		var pos := vec(info.position)
		var size := vec(info.size)
		if info.kind == "trunk":
			var body := add(obstacles,StaticBody3D.new(),info.name) as StaticBody3D
			body.collision_layer = 2
			body.collision_mask = 0
			body.position = pos
			var col := add(body,CollisionShape3D.new(),"Trunk") as CollisionShape3D
			var shape := CylinderShape3D.new()
			shape.radius = maxf(size.x,size.z)*.5
			shape.height = size.y
			col.shape = shape
			var points := PackedVector3Array()
			for i in range(8):
				points.append(pos+Vector3(cos(i*TAU/8)*shape.radius,0,sin(i*TAU/8)*shape.radius))
			nav_source.add_projected_obstruction(points,pos.y-size.y/2,size.y,true)
			count += 1
		else:
			box(obstacles,info.name,pos,size)
	# River exclusion follows the bend, with deliberate openings at both bridge decks.
	for i in range(168):
		var y := -42.0+(i+.5)*.5
		if absf(y+1.8)<1.65 or absf(y-18.0)<1.72:
			continue
		var x := -3.0+.11*y+.55*sin(y*.26)
		box(river_boundary,"River_%03d"%i,Vector3(x,1.1,-y),Vector3(2.90,3.0,.54))
	# Upper bridge rails provide complete blocking spans, including between posts.
	var bx := -3.0+.11*18+.55*sin(18*.26)
	for side in [-1,1]:
		box(obstacles,"UpperBridgeRail",Vector3(bx,1.13,-18+side*1.62),Vector3(6.7,1.2,.19))
	box(edge,"West",Vector3(-50,3,0),Vector3(1,12,81))
	box(edge,"East",Vector3(50,3,0),Vector3(1,12,81))
	box(edge,"North",Vector3(0,3,-40),Vector3(101,12,1))
	box(edge,"South",Vector3(0,3,40),Vector3(101,12,1))
	var markers := add(map,Node3D.new(),"Markers")
	for label in meta.markers:
		var mark := add(markers,Marker3D.new(),label) as Marker3D
		mark.position = vec(meta.markers[label])
	var regions := add(map,Node3D.new(),"Regions")
	for region in meta.regions:
		var mark := add(regions,Marker3D.new(),region.id) as Marker3D
		mark.position = vec(region.position)
		mark.set_meta("display_name",region.label)
	var routes := add(map,Node3D.new(),"Routes")
	for i in range(meta.routes.size()):
		var path := add(routes,Path3D.new(),["MainRoute","ReturnRoute","InnApproach"][i]) as Path3D
		path.curve = Curve3D.new()
		for p in meta.routes[i]:
			path.curve.add_point(vec(p))
	# Recast receives only genuine walking surfaces and explicit blocking footprints.
	var nav := NavigationMesh.new()
	nav.cell_size = .25
	nav.cell_height = .1
	nav.agent_height = 1.6
	nav.agent_radius = .5
	nav.agent_max_climb = .3
	nav.agent_max_slope = 42
	nav.filter_baking_aabb = AABB(Vector3(-49,-2,-39),Vector3(98,12,78))
	nav.region_min_size = 1.0
	NavigationServer3D.bake_from_source_geometry_data(nav,nav_source)
	ResourceSaver.save(nav,BASE+"walkable.tres")
	var region := add(map,NavigationRegion3D.new(),"WalkableRegion") as NavigationRegion3D
	region.navigation_mesh = nav
	setup_lights(meta)
	# Partition art into editable region scenes; compressed binary scenes hold geometry.
	# The main map remains a readable hierarchy of instances, lighting and collision nodes.
	var partitions: Dictionary = {}
	for info in meta.regions:
		partitions[info.id] = add(art,Node3D.new(),String(info.id).capitalize())
	partitions["distant"] = add(art,Node3D.new(),"DistantLandscape")
	for mesh in art.get_children():
		if not mesh is MeshInstance3D:
			continue
		var center: Vector3 = mesh.transform * mesh.get_aabb().get_center()
		var nearest: String = "distant"
		if absf(center.x)<52 and absf(center.z)<43 and not String(mesh.name).begins_with("Backdrop"):
			var distance: float = INF
			for info in meta.regions:
				var d := center.distance_squared_to(vec(info.position))
				if d<distance:
					distance=d
					nearest=info.id
		mesh.reparent(partitions[nearest])
	for key in partitions:
		save_branch(partitions[key],BASE+"art_"+key+".scn")
	save_branch(wheel,BASE+"waterwheel.scn")
	save_branch(ground,BASE+"ground_collision.scn")
	var packed := PackedScene.new()
	packed.pack(map)
	var result := ResourceSaver.save(packed,BASE+"lanternbrook_map.tscn")
	print("MAP_BAKED result=",result," meshes=",meshes," colliders=",count," nav_polygons=",nav.get_polygon_count())
	map.free()
	create_preview()
	quit()

func save_branch(branch: Node, path: String) -> void:
	var parent := branch.get_parent()
	for node in branch.find_children("*","",true,false):
		node.owner = branch
	branch.owner = null
	var packed := PackedScene.new()
	packed.pack(branch)
	ResourceSaver.save(packed,path,ResourceSaver.FLAG_COMPRESS)
	parent.remove_child(branch)
	branch.free()
	var instance := (ResourceLoader.load(path,"PackedScene",ResourceLoader.CACHE_MODE_IGNORE) as PackedScene).instantiate()
	parent.add_child(instance)
	instance.owner = map

func setup_lights(meta: Dictionary) -> void:
	var lighting := add(map,Node3D.new(),"Lighting")
	var world := add(lighting,WorldEnvironment.new(),"WorldEnvironment") as WorldEnvironment
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(.19,.27,.32)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_sky_contribution = 0
	env.ambient_light_color = Color(.46,.59,.69)
	env.ambient_light_energy = .55
	env.tonemap_mode = Environment.TONE_MAPPER_AGX
	env.tonemap_exposure = 1.1
	env.tonemap_agx_contrast = 1.25
	env.ssao_enabled = true
	env.ssao_radius = 1.0
	env.ssao_intensity = 1.1
	env.glow_enabled = true
	env.glow_intensity = .22
	env.glow_hdr_threshold = 1.6
	env.fog_enabled = true
	env.fog_light_color = Color(.40,.53,.57)
	env.fog_density = .0025
	world.environment = env
	var sun := add(lighting,DirectionalLight3D.new(),"EveningSun") as DirectionalLight3D
	sun.rotation_degrees = Vector3(-51,-56,0)
	sun.light_color = Color(1,.80,.57)
	sun.light_energy = 1.6
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 115
	var fill := add(lighting,DirectionalLight3D.new(),"WarmFill") as DirectionalLight3D
	fill.rotation_degrees = Vector3(-48,-25,0)
	fill.light_color = Color(1,.81,.57)
	fill.light_energy = .25
	var points: Array = meta.lamps.duplicate()
	points.append_array([[2.2,2.44,-.22],[5.6,2.40,.73],[-6.03,2.3,.9],[-.68,2.3,.9],[7.92,2.1,4.3],[-8.08,1.9,5],[3.2,2.8,.3]])
	for p in points:
		var lamp := add(lighting,OmniLight3D.new(),"Lantern") as OmniLight3D
		lamp.position = vec(p)
		lamp.light_color = Color(1,.55,.2)
		lamp.light_energy = 1.7
		lamp.omni_range = 4.2
		lamp.shadow_enabled = false

func create_preview() -> void:
	map = Node3D.new()
	map.name = "MapObserver"
	map.set_script(load("res://prototype/map_observer.gd"))
	var camera := add(map,Camera3D.new(),"Camera3D") as Camera3D
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 18
	camera.near = .1
	camera.far = 250
	camera.current = true
	var overlay := add(map,CanvasLayer.new(),"Overlay")
	var panel := add(overlay,PanelContainer.new(),"Panel") as PanelContainer
	panel.position = Vector2(24,22)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(.035,.065,.055,.78)
	style.content_margin_left = 18
	style.content_margin_right = 18
	style.content_margin_top = 12
	style.content_margin_bottom = 12
	style.corner_radius_top_left = 7
	style.corner_radius_top_right = 7
	style.corner_radius_bottom_left = 7
	style.corner_radius_bottom_right = 7
	panel.add_theme_stylebox_override("panel",style)
	var rows := add(panel,VBoxContainer.new(),"Rows")
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft YaHei UI","Microsoft YaHei"])
	var title := add(rows,Label.new(),"Title") as Label
	title.text = "溪灯驿站 · 河谷环线"
	title.add_theme_font_override("font",font)
	title.add_theme_font_size_override("font_size",24)
	title.modulate = Color(.96,.91,.76)
	var caption := add(rows,Label.new(),"Region") as Label
	caption.add_theme_font_override("font",font)
	var text := add(rows,Label.new(),"Controls") as Label
	text.text = "右键环视 · 中键平移 · 滚轮缩放 · R 复位 · Tab 隐藏\n1 林间入口   2 驿站   3 石桥   4 河岸   5 遗迹"
	text.add_theme_font_override("font",font)
	text.add_theme_font_size_override("font_size",13)
	var packed := PackedScene.new()
	packed.pack(map)
	ResourceSaver.save(packed,"res://prototype/map_observer.tscn")
	map.free()
	for label in ["world_map_orbit","world_map_pan","world_map_zoom_in","world_map_zoom_out","world_map_ui","world_map_region_1","world_map_region_2","world_map_region_3","world_map_region_4","world_map_region_5"]:
		var event: InputEvent
		var index: int = ["world_map_orbit","world_map_pan","world_map_zoom_in","world_map_zoom_out"].find(label)
		if index >= 0:
			var mouse := InputEventMouseButton.new()
			mouse.button_index = [MOUSE_BUTTON_RIGHT,MOUSE_BUTTON_MIDDLE,MOUSE_BUTTON_WHEEL_UP,MOUSE_BUTTON_WHEEL_DOWN][index]
			event = mouse
		else:
			var key := InputEventKey.new()
			key.physical_keycode = KEY_TAB if label == "world_map_ui" else KEY_1+int(label.right(1))-1
			event = key
		ProjectSettings.set_setting("input/"+label,{"deadzone":.2,"events":[event]})
	ProjectSettings.set_setting("layer_names/3d_physics/layer_1","WalkingSurfaces")
	ProjectSettings.set_setting("layer_names/3d_physics/layer_2","WorldObstacles")
	ProjectSettings.set_setting("rendering/anti_aliasing/quality/msaa_3d",2)
	ProjectSettings.set_setting("navigation/3d/default_cell_height",.1)
	ProjectSettings.save()
