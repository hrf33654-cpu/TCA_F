extends SceneTree
## Rendered review evidence for the inspection camera; does not rebuild map assets.
const OUT := "res://art/lanternbrook_hd2d/research/depth_of_field_v4/"
var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("review")

func check(condition: bool, message: String) -> void:
	if not condition:
		failures.append(message)
		push_error(message)

func settle(frames: int = 12) -> void:
	for i in range(frames):
		await process_frame
	await RenderingServer.frame_post_draw

func save_frame(path: String, expected_size: Vector2i) -> void:
	var frame := root.get_texture().get_image()
	check(frame.get_size() == expected_size, "Screenshot resolution " + path)
	check(frame.save_png(path) == OK, "Save screenshot " + path)

func review() -> void:
	for folder in ["tuned", "legacy", "off", "limits"]:
		DirAccess.make_dir_recursive_absolute(OUT + folder)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.content_scale_size = Vector2i.ZERO
	var scene: Node = load("res://scenes/lanternbrook_hd2d_preview.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	await settle()
	var observer := scene.get_node("Lanternbrook/MapObserver")
	observer.get_node("Overlay").hide()
	check(observer.depth_profiles.size() == observer.regions.size(), "Six region profiles")
	check(observer.upper_field.layer < observer.get_node("Overlay").layer, "Review UI must remain above upper blur")
	check(observer.get_node("UpperField/Softness").mouse_filter == Control.MOUSE_FILTER_IGNORE, "Upper blur must not intercept map input")
	var settings: Dictionary = {}
	for property in ProjectSettings.get_property_list():
		if "depth_of_field" in String(property.name):
			settings[property.name] = ProjectSettings.get_setting(property.name)
	var records: Array = []
	for size in [Vector2i(1280,720), Vector2i(1920,1080)]:
		root.size = size
		for region in range(observer.regions.size()):
			observer.jump_to_region(region)
			var expected_camera: Transform3D = observer.camera.global_transform
			for mode in range(3):
				observer.set_optics_mode(mode)
				await settle(30)
				check(observer.camera.global_transform.is_equal_approx(expected_camera), "Optics must not move camera")
				var optics: CameraAttributesPractical = observer.camera.attributes
				check(observer.upper_field.visible == (mode == 0), "Upper blur only enabled in tuned mode")
				check(observer.get_node("UpperField/Softness").size.is_equal_approx(Vector2(size)), "Upper blur follows viewport resize")
				var depth: float = -observer.camera.to_local(observer.to_global(observer.focus)).z
				if mode == 0:
					check(optics.dof_blur_near_distance < depth and optics.dof_blur_far_distance > depth, "Focus remains clear")
				elif mode == 1:
					check(is_equal_approx(optics.dof_blur_near_distance,84.0) and is_equal_approx(optics.dof_blur_far_distance,110.0) and is_equal_approx(optics.dof_blur_amount,0.045), "Exact legacy optics")
				else:
					check(not optics.dof_blur_far_enabled and not optics.dof_blur_near_enabled, "Disabled optics")
				var mode_name: String = ["tuned", "legacy", "off"][mode]
				save_frame(OUT+mode_name+"/region_%d_%d.png"%[region+1,size.x],size)
				if mode == 0:
					var timings: Array[float] = []
					var last := Time.get_ticks_usec()
					for i in range(90):
						await process_frame
						var now := Time.get_ticks_usec()
						timings.append((now-last)/1000.0)
						last = now
					timings.sort()
					var total := 0.0
					for value in timings:
						total += value
					records.append({"region":region+1,"resolution":str(size),"focus_depth":depth,"near":optics.dof_blur_near_distance,"far":optics.dof_blur_far_distance,"amount":optics.dof_blur_amount,"average_ms":total/90.0,"p95_ms":timings[85]})
	observer.set_optics_mode(0)
	for region in range(observer.regions.size()):
		for distance in [14.0,27.0]:
			for direction in [-1.0,1.0]:
				observer.jump_to_region(region)
				observer.zoom = distance
				observer.yaw = observer.base_yaw + observer.yaw_limit*direction
				observer._update_camera()
				await settle()
				var optics: CameraAttributesPractical = observer.camera.attributes
				var depth: float = -observer.camera.to_local(observer.to_global(observer.focus)).z
				check(optics.dof_blur_near_distance < depth and optics.dof_blur_far_distance > depth, "Zoom/rotation clear focus")
				check(optics.dof_blur_amount >= 0.1 and optics.dof_blur_amount <= 0.121, "Blended profile in range")
				save_frame(OUT+"limits/region_%d_zoom_%d_%s.png"%[region+1,int(distance),"left" if direction<0 else "right"],root.size)
	# A continuous pan must not cause sudden jumps at region boundaries.
	var maximum_step := 0.0
	for pair in [[0,1],[1,2],[2,3],[3,4],[4,5],[5,1]]:
		var previous_near := 0.0
		for step in range(101):
			observer.focus = observer.regions[pair[0]].lerp(observer.regions[pair[1]],step/100.0)
			observer._update_camera()
			var current_near: float = observer.optics.dof_blur_near_distance
			if step > 0:
				maximum_step = maxf(maximum_step,absf(current_near-previous_near))
			previous_near = current_near
	check(maximum_step < 0.4, "Continuous focus profile pan")
	# Exercise the actual review shortcut, including repeat protection.
	observer.set_optics_mode(0)
	var key := InputEventKey.new()
	key.physical_keycode = KEY_D
	key.pressed = true
	for expected in [1,2,0]:
		observer._unhandled_input(key)
		check(observer.optics_mode == expected, "D shortcut cycles modes")
	key.echo = true
	observer._unhandled_input(key)
	check(observer.optics_mode == 0, "D repeat ignored")
	observer.jump_to_region(1)
	observer.get_node("Overlay").show()
	await settle()
	save_frame(OUT+"review_controls.png",root.size)
	var report := {"passed":failures.is_empty(),"failures":failures,"adapter":RenderingServer.get_video_adapter_name(),"godot":Engine.get_version_info().string,"settings":settings,"performance":records,"maximum_pan_step_m":maximum_step,"screenshots":61,"method":"Rendered Forward+; 30 warmup then 90 local wall-clock frame intervals per tuned view, not an isolated GPU benchmark. Native DOF plus upper screen-space blur. Map geometry, collision and navigation unchanged. No character gameplay acceptance."}
	var file := FileAccess.open(OUT+"validation.json",FileAccess.WRITE)
	file.store_string(JSON.stringify(report,"\t"))
	print("DEPTH_REVIEW ",JSON.stringify(report))
	current_scene = null
	scene.queue_free()
	await process_frame
	quit(0 if failures.is_empty() else 1)
