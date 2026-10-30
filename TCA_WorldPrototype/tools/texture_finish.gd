extends RefCounted
## Offline finishing only. Shared assets, saved nodes, no runtime map construction.
const BASE := "res://world/maps/lanternbrook_hd2d/"
var rng := RandomNumberGenerator.new()
var map: Node3D
var leaf_records: Array = []

func ground_at(p: Vector3) -> Dictionary:
	return map.get_world_3d().direct_space_state.intersect_ray(PhysicsRayQueryParameters3D.create(p+Vector3.UP*15,p-Vector3.UP*10,1))

func distance_to_route(p: Vector3, data: Dictionary) -> float:
	var distance := 999.
	for route in data.routes:
		for i in range(route.size()-1):
			var a := Vector2(route[i][0],route[i][2])
			var b := Vector2(route[i+1][0],route[i+1][2])
			var v := b-a
			var t := clampf((Vector2(p.x,p.z)-a).dot(v)/maxf(v.length_squared(),.001),0,1)
			distance = minf(distance,Vector2(p.x,p.z).distance_to(a+v*t))
	return distance

func apply(author: SceneTree, root_map: Node3D, data: Dictionary) -> void:
	map = root_map
	rng.seed = 271029
	var warm_key := SpotLight3D.new()
	warm_key.name = "InnPorchWarmSpill"
	warm_key.position = Vector3(3.2,4.7,2.8)
	warm_key.light_color = Color(1.,.66,.34)
	warm_key.light_energy = 2.2
	warm_key.spot_range = 10.
	warm_key.spot_angle = 58.
	warm_key.spot_attenuation = .8
	warm_key.shadow_enabled = true
	map.get_node("Lighting").add_child(warm_key)
	warm_key.owner = map
	warm_key.look_at_from_position(warm_key.global_position,map.to_global(Vector3(3.2,1.2,-.7)),Vector3.UP)
	for visual in map.get_node("Art").find_children("*","GeometryInstance3D",true,false):
		var local: Transform3D = map.global_transform.affine_inverse()*visual.global_transform
		visual.set_instance_shader_parameter("map_row_x",Vector4(local.basis.x.x,local.basis.y.x,local.basis.z.x,local.origin.x))
		visual.set_instance_shader_parameter("map_row_y",Vector4(local.basis.x.y,local.basis.y.y,local.basis.z.y,local.origin.y))
		visual.set_instance_shader_parameter("map_row_z",Vector4(local.basis.x.z,local.basis.y.z,local.basis.z.z,local.origin.z))
	var root := Node3D.new()
	root.name = "TextureFinish"
	map.get_node("Art").add_child(root)
	root.owner = map
	await author.physics_frame
	# Litter is concentrated beneath trees and beside paths, never uniformly spread.
	var tool := SurfaceTool.new()
	tool.begin(Mesh.PRIMITIVE_TRIANGLES)
	for collider in data.colliders:
		if collider.kind!="trunk":
			continue
		var center := Vector3(collider.position[0],0,collider.position[2])
		for k in range(3):
			var angle := rng.randf()*TAU
			var p := center+Vector3(cos(angle),0,sin(angle))*rng.randf_range(.5,1.85)
			if distance_to_route(p,data)<1.05 or absf(p.x)>48 or absf(p.z)>38:
				continue
			var hit := ground_at(p)
			if hit.is_empty() or hit.position.y>1.1:
				continue
			p.y = hit.position.y+.024
			var width := rng.randf_range(.6,1.45)
			var basis := Basis(Vector3.UP,angle)
			var corners: Array[Vector3] = []
			for v in [Vector3(-1,0,-1),Vector3(1,0,-1),Vector3(1,0,1),Vector3(-1,0,1)]:
				var point: Vector3 = p+basis*(v*width*.5)
				var support := ground_at(point)
				point.y = support.position.y+.024 if not support.is_empty() else p.y
				corners.append(point)
			for ids in [[0,2,1],[0,3,2]]:
				for id in ids:
					tool.set_normal(Vector3.UP)
					tool.set_uv([Vector2(0,0),Vector2(1,0),Vector2(1,1),Vector2(0,1)][id])
					tool.add_vertex(corners[id])
			leaf_records.append({"corners":corners.map(func(v):return [v.x,v.y,v.z])})
	var leaves := MeshInstance3D.new()
	leaves.name = "TreeRootLeafLitter"
	leaves.mesh = tool.commit()
	leaves.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	var mat := StandardMaterial3D.new()
	mat.resource_name = "Damp leaves beneath trees"
	mat.albedo_texture = load(BASE+"textures/leaf_litter_v2.png")
	mat.albedo_color = Color(.78,.82,.70)
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA_SCISSOR
	mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST_WITH_MIPMAPS
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	mat.roughness = .94
	leaves.material_override = mat
	root.add_child(leaves)
	leaves.owner = map
	# Foliage needs room for readable clusters rather than equal contrast everywhere.
	for n in map.get_node("Art/PixelWoodland").get_children():
		if n is MeshInstance3D and n.material_override is ShaderMaterial:
			var color: Color = n.material_override.get_shader_parameter("leaf_tint")
			var variation: float = .92+float(abs(String(n.name).hash())%5)*.025
			n.material_override = n.material_override.duplicate()
			n.material_override.set_shader_parameter("leaf_tint",color*Color(variation,variation,variation))
	var file := FileAccess.open(BASE+"texture_finish_data.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"leaf_patches":leaf_records,"surface_version":2,"collision_changes":0},"\t"))
	print("TEXTURE_FINISH ",leaf_records.size()," leaf patches")
