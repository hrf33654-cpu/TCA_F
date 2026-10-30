extends RefCounted
## Design-time regional dressing. Every prop, collider, lamp and marker is saved.
const BASE := "res://world/maps/lanternbrook_hd2d/"
var map: Node3D
var tree: SceneTree
var zones: Dictionary = {}
var mats: Dictionary = {}
var blueprint: Array = []
var routes: Array = []
var extra_collision: Node3D
var serial := 0

func add(node: Node, parent: Node, label: String) -> Node:
	var unique_label := label
	var suffix := 2
	while parent.has_node(NodePath(unique_label)):
		unique_label = label+"_%d"%suffix
		suffix += 1
	node.name = unique_label
	parent.add_child(node)
	node.owner = map
	return node

func simple_mat(label: String, color: Color, emission: float = 0.0) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.resource_name = label
	mat.albedo_color = color
	mat.roughness = .9
	if emission>0:
		mat.emission_enabled = true
		mat.emission = color
		mat.emission_energy_multiplier = emission
	return mat

func pixel_mat(label: String, texture_name: String, tint := Color.WHITE) -> ShaderMaterial:
	var mat := ShaderMaterial.new()
	mat.resource_name = label
	mat.shader = load(BASE+"pixel_surface.gdshader")
	mat.set_shader_parameter("pixel_texture",load(BASE+"textures/"+texture_name+".png"))
	mat.set_shader_parameter("tint",tint)
	mat.set_shader_parameter("moss_amount",.22 if texture_name == "limestone" else 0.0)
	# Same material palette as the main map, including material-specific relief.
	var files := {"chestnut":"chestnut_handpainted_v2","oak":"chestnut_handpainted_v2","limestone":"limestone_handpainted_v2","slate":"slate_mineral_v2"}
	if files.has(texture_name):
		mat.set_shader_parameter("pixel_texture",load(BASE+"textures/"+files[texture_name]+".png"))
	mat.set_shader_parameter("material_kind",2 if texture_name=="slate" else (0 if texture_name=="limestone" else 1))
	mat.set_shader_parameter("base_roughness",.72 if texture_name=="slate" else .86)
	mat.set_shader_parameter("source_pixels",256. if files.has(texture_name) else 64.)
	mat.set_shader_parameter("relief_strength",.12)
	return mat

func height_at(x: float, z: float) -> float:
	var ray := PhysicsRayQueryParameters3D.create(Vector3(x,12,z),Vector3(x,-8,z),1)
	var hit := map.get_world_3d().direct_space_state.intersect_ray(ray)
	return float(hit.position.y) if not hit.is_empty() else .4

func route_distance(p: Vector3) -> float:
	var distance := 1000.0
	for route in routes:
		for i in range(route.size()-1):
			var a := Vector2(route[i][0],route[i][2])
			var b := Vector2(route[i+1][0],route[i+1][2])
			var v := b-a
			var t := clampf((Vector2(p.x,p.z)-a).dot(v)/maxf(v.length_squared(),.001),0,1)
			distance = minf(distance,Vector2(p.x,p.z).distance_to(a+v*t))
	return distance

func blocking(label: String, position: Vector3, size: Vector3, layer := 2, rotation := Vector3.ZERO) -> void:
	var body := add(StaticBody3D.new(),extra_collision,label) as StaticBody3D
	body.collision_layer = layer
	body.collision_mask = 0
	body.position = position
	body.rotation = rotation
	var shape := BoxShape3D.new()
	shape.size = size
	var col := add(CollisionShape3D.new(),body,"Shape") as CollisionShape3D
	col.shape = shape

func prop(zone: String, label: String, kind: String, p: Vector3, size: Vector3, material: String, rotation := Vector3.ZERO) -> MeshInstance3D:
	serial += 1
	var node := add(MeshInstance3D.new(),zones[zone],label+"_%03d"%serial) as MeshInstance3D
	var mesh: PrimitiveMesh
	if kind == "box":
		var box := BoxMesh.new()
		box.size = size
		mesh = box
	elif kind == "cylinder":
		var cylinder := CylinderMesh.new()
		cylinder.top_radius = size.x*.42
		cylinder.bottom_radius = size.x*.5
		cylinder.height = size.y
		cylinder.radial_segments = 10
		mesh = cylinder
	elif kind == "ring":
		var ring := TorusMesh.new()
		ring.inner_radius = size.x-size.y
		ring.outer_radius = size.x+size.y
		ring.rings = 48
		ring.ring_segments = 6
		mesh = ring
	else:
		var sphere := SphereMesh.new()
		sphere.radius = size.x*.5
		sphere.height = size.y
		sphere.radial_segments = 8
		sphere.rings = 4
		mesh = sphere
	node.mesh = mesh
	node.position = p
	node.rotation = rotation
	node.material_override = mats[material]
	blueprint.append({"zone":zone,"name":String(node.name),"kind":kind,"position":[p.x,p.y,p.z],"size":[size.x,size.y,size.z],"rotation":[rotation.x,rotation.y,rotation.z],"material":material})
	return node

func lamp(zone: String, label: String, p: Vector3, cool := false) -> void:
	var color := Color(.37,.73,.76) if cool else Color(1,.66,.31)
	var mat := "crystal" if cool else "honey"
	prop(zone,label+"Foot","box",p+Vector3(0,.12,0),Vector3(.6,.24,.6),"stone")
	prop(zone,label+"Post","box",p+Vector3(0,.8,0),Vector3(.13,1.36,.13),"timber")
	prop(zone,label+"Frame","box",p+Vector3(0,1.58,0),Vector3(.4,.46,.4),"iron")
	prop(zone,label+"Glow","box",p+Vector3(0,1.58,.215),Vector3(.26,.31,.025),mat)
	prop(zone,label+"Cap","box",p+Vector3(0,1.85,0),Vector3(.58,.12,.55),"slate")
	var light := add(OmniLight3D.new(),map.get_node("Lighting"),label) as OmniLight3D
	light.position = p+Vector3(0,1.6,0)
	light.light_color = color
	light.light_energy = 2.2 if cool else 2.5
	light.omni_range = 4.8
	blocking(label,p+Vector3(0,.8,0),Vector3(.55,1.7,.55))

func bench(zone: String, p: Vector3, angle: float) -> void:
	var basis := Basis(Vector3.UP,angle)
	for dx in [-.7,.7]:
		prop(zone,"BenchLeg","box",p+basis*Vector3(dx,.28,0),Vector3(.13,.56,.5),"timber",Vector3(0,angle,0))
	prop(zone,"BenchSeat","box",p+Vector3(0,.59,0),Vector3(1.9,.13,.6),"oak",Vector3(0,angle,0))
	prop(zone,"BenchBack","box",p+basis*Vector3(0,.98,-.25),Vector3(1.9,.52,.12),"oak",Vector3(0,angle,0))
	blocking("Bench",p+Vector3(0,.57,0),Vector3(1.9,1.14,.65),2,Vector3(0,angle,0))

func sign_board(zone: String, p: Vector3, angle: float) -> void:
	prop(zone,"WaymarkPost","box",p+Vector3(0,.85,0),Vector3(.14,1.7,.14),"timber")
	prop(zone,"WaymarkBoard","box",p+Vector3(0,1.5,0),Vector3(1.4,.36,.12),"oak",Vector3(0,angle,0))
	var basis := Basis(Vector3.UP,angle)
	prop(zone,"WaymarkInlay","box",p+basis*Vector3(.02,1.5,.075),Vector3(.62,.035,.018),"brass",Vector3(0,angle,0))
	blocking("Waymark",p+Vector3(0,.8,0),Vector3(.2,1.6,.2))

func build(scene_tree: SceneTree, root: Node3D, data: Dictionary) -> Dictionary:
	map = root
	tree = scene_tree
	routes = data.routes.duplicate(true)
	var branch: Array = []
	for p in [Vector2(-12,-12),Vector2(-9,-12),Vector2(-7,-12),Vector2(-5.5,-12)]:
		branch.append([p.x,height_at(p.x,p.y),p.y])
	routes.append(branch)
	data.routes = routes
	data.regions[3].position = [-6.5,1.3,-12]
	data.regions[4].position = [-25,1.5,-29]
	data.regions.append({"id":"return","label":"林间归途","position":[3,1.3,-18]})
	data.markers["RiversideLookout"] = [-5.5,.8,-12]
	data.markers["Observatory"] = [-25,1.2,-28]
	data.markers["ReturnJunction"] = [7,.6,-20]
	for label in ["RiversideLookout","Observatory","ReturnJunction"]:
		var mark := add(Marker3D.new(),map.get_node("Markers"),label) as Marker3D
		var p: Array = data.markers[label]
		mark.position = Vector3(p[0],p[1],p[2])
	var return_region := add(Marker3D.new(),map.get_node("Regions"),"return") as Marker3D
	return_region.position = Vector3(3,1.3,-18)
	return_region.set_meta("display_name","林间归途")
	map.get_node("Regions/riverside").position = Vector3(-6.5,1.3,-12)
	map.get_node("Regions/ruins").position = Vector3(-25,1.5,-29)
	var path := add(Path3D.new(),map.get_node("Routes"),"LookoutApproach") as Path3D
	path.curve = Curve3D.new()
	for p in branch:
		path.curve.add_point(Vector3(p[0],p[1],p[2]))
	extra_collision = add(Node3D.new(),map.get_node("Collision"),"RegionDetails") as Node3D
	for label in ["Entrance","Riverside","Ruins","Return","Transitions"]:
		zones[label] = add(Node3D.new(),map.get_node("Art"),"Complete"+label)
	mats = {"timber":pixel_mat("Timber","chestnut"),"oak":pixel_mat("Oak","oak"),"slate":pixel_mat("TealSlate","slate"),"stone":pixel_mat("OldStone","limestone",Color(.84,.96,.92)),"brass":simple_mat("OldBrass",Color(.53,.43,.24)),"iron":simple_mat("DarkIron",Color(.12,.19,.2)),"honey":simple_mat("WarmGlass",Color(1,.68,.30),2),"crystal":simple_mat("QuietJade",Color(.25,.74,.76),1.8),"paper":simple_mat("Parchment",Color(.64,.62,.46)),"moss":simple_mat("Moss",Color(.17,.26,.14))}
	entrance()
	riverside()
	ruins()
	return_path()
	await tree.physics_frame
	await tree.physics_frame
	var understory := dress_understory()
	var nav := bake_navigation()
	ResourceSaver.save(nav,BASE+"complete_walkable.tres")
	map.get_node("WalkableRegion").navigation_mesh = nav
	var file := FileAccess.open(BASE+"complete_data.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(data,"\t"))
	file = FileAccess.open(BASE+"region_blueprint.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"props":blueprint,"understory":understory,"materials":{"timber":"chestnut","oak":"oak","slate":"slate","stone":"limestone"}},"\t"))
	return {"props":serial,"understory_clusters":understory.size(),"navigation_polygons":nav.get_polygon_count(),"new_routes":1,"zones":zones.keys()}

func dress_understory() -> Array:
	var rng := RandomNumberGenerator.new()
	rng.seed = 7427
	var groups: Dictionary = {"fern":[],"reeds":[],"blueflowers":[]}
	var records: Array = []
	for i in range(3300):
		var p := Vector3(rng.randf_range(-46,46),0,rng.randf_range(-36,36))
		var distance := route_distance(p)
		if distance<1.7:
			continue
		var ruin_distance := Vector2(p.x+25,p.z+28).length()
		if ruin_distance<5.6:
			continue
		var river_center := -3.-.11*p.z-.55*sin(.26*p.z)
		var river_distance := absf(p.x-river_center)
		var kind := ""
		if river_distance>1.85 and river_distance<3.0 and absf(p.z+18)>2 and absf(p.z-1.8)>2:
			kind = "reeds"
		elif ruin_distance<14 and rng.randf()<.6:
			kind = "blueflowers"
		elif distance>2 and distance<4.8 and rng.randf()<.5:
			kind = "fern"
		if kind.is_empty():
			continue
		var query := PhysicsRayQueryParameters3D.create(p+Vector3.UP*12,p-Vector3.UP*8,3)
		var hit := map.get_world_3d().direct_space_state.intersect_ray(query)
		if hit.is_empty() or not String(hit.collider.name).begins_with("Ground"):
			continue
		var scale := rng.randf_range(.7,1.25)
		p.y = hit.position.y+.30*scale
		groups[kind].append(Transform3D(Basis.from_euler(Vector3(-.18,.56,0)).scaled(Vector3.ONE*scale),p))
		records.append({"kind":kind,"position":[p.x,p.y,p.z],"scale":scale})
	for kind in groups:
		var material := StandardMaterial3D.new()
		material.albedo_texture = load(BASE+"textures/"+kind+".png")
		material.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
		material.cull_mode = BaseMaterial3D.CULL_DISABLED
		material.roughness = 1.0
		var quad := QuadMesh.new()
		quad.size = Vector2(1.2,.8)
		quad.material = material
		var multi := MultiMesh.new()
		multi.transform_format = MultiMesh.TRANSFORM_3D
		multi.mesh = quad
		multi.instance_count = groups[kind].size()
		for i in range(multi.instance_count):
			multi.set_instance_transform(i,groups[kind][i])
		var node := add(MultiMeshInstance3D.new(),zones.Transitions,String(kind).capitalize()+"Beds") as MultiMeshInstance3D
		node.multimesh = multi
		node.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	return records

func entrance() -> void:
	var y := height_at(28,32)
	for side in [-1,1]:
		prop("Entrance","GatewaySlate","box",Vector3(28+side*1.43,4.04,32),Vector3(3.12,.13,1.5),"slate",Vector3(0,0,-side*.26))
	prop("Entrance","GatewayRidge","box",Vector3(28,4.48,32),Vector3(.18,.2,1.65),"timber")
	# Noticeboard and parked handcart are well outside the main entrance corridor.
	var p := Vector3(32.7,height_at(32.7,27),27)
	for side in [-1,1]:
		prop("Entrance","NoticePost","box",p+Vector3(side*.75,1,0),Vector3(.13,2,.13),"timber")
	prop("Entrance","NoticeBacking","box",p+Vector3(0,1.65,0),Vector3(1.85,1.25,.16),"oak")
	prop("Entrance","NoticePaper","box",p+Vector3(0,1.66,.095),Vector3(1.33,.84,.025),"paper")
	for i in range(4):
		prop("Entrance","NoticeMarks","box",p+Vector3(-.08,1.95-i*.16,.115),Vector3(.6 if i%2 else .9,.025,.012),"timber")
	prop("Entrance","NoticeShelter","box",p+Vector3(0,2.38,0),Vector3(2.12,.13,.8),"slate",Vector3(.13,0,0))
	blocking("Noticeboard",p+Vector3(0,1.2,0),Vector3(1.9,2.4,.4))
	p = Vector3(21.3,height_at(21.3,27.8),27.8)
	prop("Entrance","HandcartBed","box",p+Vector3(0,.57,0),Vector3(1.8,.16,1.1),"oak")
	for side in [-1,1]:
		prop("Entrance","HandcartSide","box",p+Vector3(0,.91,side*.52),Vector3(1.8,.6,.09),"oak")
		prop("Entrance","HandcartWheel","cylinder",p+Vector3(-.3,.38,side*.69),Vector3(.76,.13,.76),"timber",Vector3(PI/2,0,0))
		prop("Entrance","HandcartHandle","box",p+Vector3(1.2,.6,side*.44),Vector3(1.3,.075,.075),"timber")
	prop("Entrance","CartCrate","box",p+Vector3(-.1,1.02,0),Vector3(.78,.72,.75),"oak")
	blocking("Handcart",p+Vector3(.25,.6,0),Vector3(2.4,1.2,1.5))
	lamp("Entrance","EntranceWelcome",Vector3(31.5,height_at(31.5,31),31))
	sign_board("Entrance",Vector3(24,height_at(24,22.5),22.5),0)

func riverside() -> void:
	var center := Vector3(-5.45,height_at(-5.45,-12)+.16,-12)
	for i in range(13):
		prop("Riverside","LookoutPlank","box",center+Vector3(-1.43+i*.235,0,0),Vector3(.22,.13,3.1),"oak")
	blocking("LookoutDeck",center,Vector3(3.1,.13,3.1),1)
	for side in [-1,1]:
		prop("Riverside","LookoutFoot","cylinder",center+Vector3(1.25,-.35,side*1.27),Vector3(.19,.8,.19),"timber")
	# Low front rail faces the water; the western approach is left completely open.
	for z in [-13.42,-10.58]:
		prop("Riverside","LookoutPost","box",Vector3(-3.98,center.y+.45,z),Vector3(.12,.9,.12),"timber")
	prop("Riverside","LookoutRail","box",Vector3(-3.98,center.y+.86,-12),Vector3(.10,.10,2.9),"oak")
	blocking("LookoutRail",Vector3(-3.98,center.y+.45,-12),Vector3(.12,.9,3.05))
	bench("Riverside",Vector3(-6.1,height_at(-6.1,-14.1),-14.1),.1)
	prop("Riverside","FishingBasket","cylinder",Vector3(-4.5,center.y+.24,-13.05),Vector3(.40,.42,.4),"oak")
	prop("Riverside","FishingRod","cylinder",Vector3(-3.72,center.y+1.1,-13.03),Vector3(.035,2.25,.035),"timber",Vector3(0,0,-.5))
	lamp("Riverside","LookoutLantern",Vector3(-8.2,height_at(-8.2,-14.3),-14.3))
	sign_board("Riverside",Vector3(-10.4,height_at(-10.4,-9.6),-9.6),-.2)
	# A low, textured connector makes the optional resting place legible.
	for i in range(17):
		var x := -11.8+i*.36
		var y := height_at(x,-12)+.025
		prop("Riverside","LookoutStepping","box",Vector3(x,y,-12),Vector3(.28,.025,.5 if i%2 else .65),"stone",Vector3(0,sin(i)*.12,0))

func ruins() -> void:
	var center := Vector3(-25,1.95,-28)
	for angle in [Vector3(.3,0,PI/2),Vector3(1.05,.4,.5),Vector3(.7,-.7,-.7)]:
		prop("Ruins","ArmillaryRing","ring",center,Vector3(.72,.027,0),"brass",angle)
	prop("Ruins","ArmillaryCore","sphere",center,Vector3(.28,.5,.28),"crystal",Vector3(.2,0,.12))
	prop("Ruins","ArmillaryStem","cylinder",Vector3(-25,1.39,-28),Vector3(.12,.45,.12),"brass")
	var light := add(OmniLight3D.new(),map.get_node("Lighting"),"ObservatoryGlow") as OmniLight3D
	light.position = center+Vector3(0,.3,0)
	light.light_color = Color(.32,.70,.76)
	light.light_energy = 2.1
	light.omni_range = 5.4
	# Fallen masonry and the engraved back panel frame the open central terrace.
	prop("Ruins","FallenColumn","cylinder",Vector3(-30.3,1.0,-27.9),Vector3(.7,2.1,.7),"stone",Vector3(0,.3,1.42))
	blocking("FallenColumn",Vector3(-30.3,1,-27.9),Vector3(2.2,.8,.8))
	prop("Ruins","ObservatoryTablet","box",Vector3(-25,2.35,-32.18),Vector3(1.7,1.46,.20),"stone")
	for i in range(8):
		var a := float(i)*PI/4
		prop("Ruins","TabletStar","box",Vector3(-25+sin(a)*.29,2.35+cos(a)*.29,-32.055),Vector3(.025,.43,.018),"brass",Vector3(0,0,-a))
	for p in [Vector2(-28.6,-30.6),Vector2(-21.8,-30.1)]:
		if route_distance(Vector3(p.x,0,p.y))>2:
			lamp("Ruins","RelicLight",Vector3(p.x,height_at(p.x,p.y),p.y),true)
	var mist := add(MeshInstance3D.new(),zones.Ruins,"QuietMist") as MeshInstance3D
	var plane := PlaneMesh.new()
	plane.size = Vector2(14,10)
	mist.mesh = plane
	mist.position = Vector3(-25,.93,-29)
	mist.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var material := ShaderMaterial.new()
	material.shader = load(BASE+"woodland_mist.gdshader")
	mist.material_override = material
	for i in range(10):
		var a := float(i)*TAU/10
		var p := Vector3(-25+cos(a)*5.3,0,-28+sin(a)*5.3)
		if route_distance(p)<2.3:
			continue
		p.y = height_at(p.x,p.z)+.18
		prop("Ruins","BrokenCoping","box",p,Vector3(.8,.35,.55),"stone",Vector3(0,-a,.08*sin(i)))
		blocking("BrokenCoping",p,Vector3(.8,.35,.55),2,Vector3(0,-a,0))

func return_path() -> void:
	bench("Return",Vector3(7.8,height_at(7.8,-22.8),-22.8),.15)
	sign_board("Return",Vector3(9.8,height_at(9.8,-17),-17),.2)
	lamp("Return","UpperBridgeBeacon",Vector3(3.8,height_at(3.8,-21),-21))
	var p := Vector3(15,height_at(15,-15),-15)
	prop("Return","TrailStoneBase","box",p+Vector3(0,.18,0),Vector3(1.1,.36,.9),"stone")
	prop("Return","TrailStone","box",p+Vector3(0,1.0,0),Vector3(.55,1.5,.38),"stone",Vector3(0,.12,.08))
	prop("Return","TrailStoneInlay","box",p+Vector3(0,1.2,.22),Vector3(.04,.5,.025),"brass")
	blocking("TrailStone",p+Vector3(0,.85,0),Vector3(1.1,1.7,.9))
	# Rough wayside edging has gaps and stays clear of the traversable ribbon.
	for i in range(7):
		p = Vector3(16.0+i*.67,0,-18.4)
		if route_distance(p)<2.4:
			continue
		p.y = height_at(p.x,p.z)+.15
		prop("Return","WaysideStone","box",p,Vector3(.6,.3,.44),"stone",Vector3(0,sin(i)*.3,.05))
		blocking("WaysideStone",p,Vector3(.6,.3,.44))

func bake_navigation() -> NavigationMesh:
	var source := NavigationMeshSourceGeometryData3D.new()
	for mesh in map.get_node("Art").find_children("*","MeshInstance3D",true,false):
		if String(mesh.name).begins_with("Ground") or String(mesh.name).begins_with("WalkSurface") or String(mesh.name).begins_with("LookoutPlank"):
			source.add_mesh(mesh.mesh,mesh.global_transform)
	for col in map.get_node("Collision").find_children("*","CollisionShape3D",true,false):
		var body := col.get_parent() as StaticBody3D
		if body == null or body.collision_layer != 2:
			continue
		var points := PackedVector3Array()
		var shape: Shape3D = col.shape
		var height := 0.0
		var base_y := 0.0
		if shape is BoxShape3D:
			var half: Vector3 = shape.size*.5
			for p in [Vector3(-half.x,-half.y,-half.z),Vector3(half.x,-half.y,-half.z),Vector3(half.x,-half.y,half.z),Vector3(-half.x,-half.y,half.z)]:
				points.append(col.global_transform*p)
			height = shape.size.y
			base_y = (col.global_transform*Vector3(0,-half.y,0)).y
		elif shape is CylinderShape3D:
			for i in range(8):
				points.append(col.global_transform*Vector3(cos(i*TAU/8)*shape.radius,-shape.height*.5,sin(i*TAU/8)*shape.radius))
			height = shape.height
			base_y = (col.global_transform*Vector3(0,-height*.5,0)).y
		if not points.is_empty():
			source.add_projected_obstruction(points,base_y,height,true)
	var nav := NavigationMesh.new()
	nav.cell_size = .25
	nav.cell_height = .1
	nav.agent_height = 1.6
	nav.agent_radius = .5
	nav.agent_max_climb = .3
	nav.agent_max_slope = 42
	nav.region_min_size = 1
	nav.filter_baking_aabb = AABB(Vector3(-49,-2,-39),Vector3(98,12,78))
	NavigationServer3D.bake_from_source_geometry_data(nav,source)
	return nav
