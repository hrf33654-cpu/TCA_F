extends SceneTree
const OUT := "res://art/lanternbrook_hd2d/"
func _initialize() -> void:
	call_deferred("run_checks")

func run_checks() -> void:
	DirAccess.make_dir_recursive_absolute(OUT+"renders")
	var scene: Node = load("res://scenes/lanternbrook_hd2d_preview.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	for i in range(12):
		await process_frame
	# Reuse the independently authored v1 route/collision probes, with the new camera limits.
	var source := FileAccess.get_file_as_string("res://prototype/map_v1_validation.gd")
	source = source.replace("res://art/lanternbrook_map_v1/",OUT)
	source = source.replace("res://world/maps/lanternbrook/map_data.json","res://world/maps/lanternbrook_hd2d/complete_data.json")
	source = source.replace("for region_index in range(5):","for region_index in range(6):")
	source = source.replace("for turn in range(12):","for turn in range(3):")
	source = source.replace("[10.0,24.0,48.0]","[14.0,20.0,27.0]")
	source = source.replace("observer.yaw = turn*TAU/12","observer.yaw = observer.base_yaw+(turn-1)*observer.yaw_limit")
	var script := GDScript.new()
	script.source_code = source
	var error := script.reload()
	if error != OK:
		push_error("Validation script did not compile")
		quit(1)
		return
	var checker: RefCounted = script.new()
	var physics: Dictionary = await checker.run(self,scene)
	var observer := scene.get_node("Lanternbrook/MapObserver")
	var checks: Dictionary = {"route_samples":physics.samples,"route_failures":physics.failures.size(),"physics":physics,"camera_limits":[]}
	for offset in [-1000.0,1000.0]:
		observer.yaw = offset
		observer.pitch = offset
		observer.zoom = offset
		observer._update_camera()
		checks.camera_limits.append({"yaw":observer.yaw,"pitch":observer.pitch,"zoom":observer.zoom,"pass":absf(observer.yaw-observer.base_yaw)<=observer.yaw_limit+.0001 and is_equal_approx(observer.pitch,deg_to_rad(observer.view_pitch_degrees)) and observer.zoom>=14 and observer.zoom<=27})
	observer.jump_to_region(1)
	var action := InputEventAction.new()
	action.action = "world_map_region_6"
	action.pressed = true
	observer._unhandled_input(action)
	checks["return_shortcut"] = observer.focus.distance_to(observer.regions[5])<.001
	var framing: Array = []
	for x in [-43.,0.,43.]:
		for z in [-33.,0.,33.]:
			for angle in [-observer.yaw_limit,0.0,observer.yaw_limit]:
				for zoom in [14.,27.]:
					observer.focus = Vector3(x,1.3,z)
					observer.yaw = observer.base_yaw+angle
					observer.zoom = zoom
					observer._update_camera()
					var size := root.get_visible_rect().size
					for pixel in [Vector2(1,1),Vector2(size.x-1,1),Vector2(1,size.y-1),size-Vector2.ONE]:
						var from: Vector3 = observer.camera.project_ray_origin(pixel)
						var ray := PhysicsRayQueryParameters3D.create(from,from+observer.camera.project_ray_normal(pixel)*240,5)
						framing.append({"focus":str(observer.focus),"yaw":observer.yaw,"zoom":zoom,"has_ground":not scene.get_node("Lanternbrook").get_world_3d().direct_space_state.intersect_ray(ray).is_empty()})
	checks["edge_framing"] = framing
	observer.jump_to_region(1)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.content_scale_size = Vector2i.ZERO
	var records: Array = []
	for size in [Vector2i(1280,720),Vector2i(1920,1080)]:
		root.size = size
		for region in range(6):
			observer.jump_to_region(region)
			observer.get_node("Overlay").hide()
			for i in range(30):
				await process_frame
			var samples: Array[float] = []
			var last := Time.get_ticks_usec()
			for i in range(90):
				await process_frame
				var now := Time.get_ticks_usec()
				samples.append((now-last)/1000.0)
				last = now
			samples.sort()
			var total := 0.0
			for value in samples:
				total += value
			await RenderingServer.frame_post_draw
			var image := root.get_texture().get_image()
			image.save_png(OUT+"renders/region_%d_%d.png"%[region+1,size.x])
			records.append({"region":region+1,"actual_size":str(image.get_size()),"average_ms":total/samples.size(),"p95_ms":samples[85],"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)})
	for region in range(6):
		observer.jump_to_region(region)
		for sign_value in [-1.0,1.0]:
			observer.yaw = observer.base_yaw+sign_value*observer.yaw_limit
			observer._update_camera()
			for i in range(8):
				await process_frame
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(OUT+"renders/region_%d_%s.png"%[region+1,"left" if sign_value<0 else "right"])
	checks["performance"] = records
	checks["adapter"] = RenderingServer.get_video_adapter_name()
	checks["method"] = "90 frame wall-clock intervals after 30 warmup frames per region; standalone Forward+ window; render benchmark, no character gameplay acceptance"
	var passed: bool = physics.failures.is_empty() and checks.return_shortcut
	for result in framing:
		passed = passed and result.has_ground
	for result in physics.navigation:
		passed = passed and result.points>0
	for result in physics.camera_checks:
		passed = passed and result.above_ground and result.center_error<1.0
	for result in checks.camera_limits:
		passed = passed and result.pass
	for result in physics.input_checks.values():
		passed = passed and result
	checks["passed"] = passed
	var f := FileAccess.open(OUT+"validation.json",FileAccess.WRITE)
	f.store_string(JSON.stringify(checks,"\t"))
	print("HD2D_VALIDATED ",JSON.stringify({"passed":passed,"samples":physics.samples,"failures":physics.failures.size(),"camera_limits":checks.camera_limits,"performance":records}))
	current_scene = null
	scene.queue_free()
	for i in range(3):
		await process_frame
	quit(0 if passed else 1)
