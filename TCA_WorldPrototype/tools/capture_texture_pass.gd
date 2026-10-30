extends SceneTree

func _initialize() -> void:
	call_deferred("capture")

func capture() -> void:
	var args := OS.get_cmdline_user_args()
	var label: String = args[0] if not args.is_empty() else "after"
	var target := "res://art/lanternbrook_hd2d/research/"+label+"/"
	DirAccess.make_dir_recursive_absolute(target)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.size = Vector2i(1280,720)
	var scene: Node = load("res://scenes/lanternbrook_hd2d_preview.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	var observer := scene.get_node("Lanternbrook/MapObserver")
	observer.get_node("Overlay").hide()
	for region in range(6):
		observer.jump_to_region(region)
		for i in range(18):
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(target+"region_%d.png"%(region+1))
	var info: Array = []
	for n in scene.get_node("Lanternbrook/Art/Courtyard").get_children():
		if n is MeshInstance3D:
			var arrays: Array = n.mesh.surface_get_arrays(0)
			var mat: Material = n.get_active_material(0)
			var tex: Texture2D = mat.get_shader_parameter("pixel_texture") if mat is ShaderMaterial else null
			info.append({"name":String(n.name),"material":str(mat),"shader":mat.shader.resource_path if mat is ShaderMaterial else "", "texture":tex.resource_path if tex!=null else "", "roughness":mat.get_shader_parameter("base_roughness") if mat is ShaderMaterial else 0,"aabb":str(n.get_aabb()),"uv":str((arrays[Mesh.ARRAY_TEX_UV] as PackedVector2Array).slice(0,8))})
	var f := FileAccess.open(target+"geometry.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(info,"\t"))
	for n in scene.get_node("Lanternbrook/Art").find_children("*","MultiMeshInstance3D",true,false):
		print("MULTI ",n.name," ",n.multimesh.instance_count," ",n.multimesh.get_instance_transform(0))
	print("TEXTURE_CAPTURED ",label)
	current_scene = null
	scene.queue_free()
	await process_frame
	await process_frame
	quit()
