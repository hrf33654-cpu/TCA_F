extends RefCounted
## Disposable physics probes; no player nodes or permanent test geometry are added.
func run(tree: SceneTree, scene: Node) -> Dictionary:
	var map := scene.get_node("Lanternbrook") as Node3D
	var observer := map.get_node("MapObserver")
	var space := map.get_world_3d().direct_space_state
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://world/maps/lanternbrook/map_data.json"))
	var capsule := CapsuleShape3D.new()
	capsule.radius = .30
	capsule.height = 1.6
	var failures: Array = []
	var samples: int = 0
	var max_rise: float = 0
	var nav_results: Array = []
	await tree.physics_frame
	await tree.physics_frame
	for route_index in range(data.routes.size()):
		var points: Array = data.routes[route_index]
		var previous_height: float = NAN
		for i in range(points.size()-1):
			var a := Vector3(points[i][0],points[i][1],points[i][2])
			var b := Vector3(points[i+1][0],points[i+1][1],points[i+1][2])
			var tangent := (b-a).normalized()
			var lateral := Vector3(-tangent.z,0,tangent.x).normalized()
			var steps := ceili(a.distance_to(b)/.35)
			for k in range(steps+1):
				for lane in [0.0,-.70,.70]:
					var point: Vector3 = a.lerp(b,float(k)/steps)+lateral*float(lane)
					var ray := PhysicsRayQueryParameters3D.create(map.to_global(point+Vector3.UP*7),map.to_global(point-Vector3.UP*7),1)
					var support := space.intersect_ray(ray)
					if support.is_empty():
						failures.append({"route":route_index,"point":point,"reason":"no_ground"})
						continue
					var local_ground := map.to_local(support.position)
					if lane == 0.0:
						if not is_nan(previous_height):
							max_rise = maxf(max_rise,absf(local_ground.y-previous_height))
						previous_height = local_ground.y
					var query := PhysicsShapeQueryParameters3D.new()
					query.shape = capsule
					query.transform = Transform3D(map.global_basis,map.to_global(local_ground+Vector3.UP*.84))
					query.collision_mask = 2
					var hits := space.intersect_shape(query,4)
					for hit in hits:
						if failures.size()<150:
							failures.append({"route":route_index,"point":local_ground,"lane":lane,"obstacle":String(hit.collider.name)})
					samples += 1
			var nav_map := map.get_world_3d().navigation_map
			var start := NavigationServer3D.map_get_closest_point(nav_map,map.to_global(a))
			var end := NavigationServer3D.map_get_closest_point(nav_map,map.to_global(b))
			var path := NavigationServer3D.map_get_path(nav_map,start,end,true)
			nav_results.append({"route":route_index,"segment":i,"points":path.size(),"start_offset":start.distance_to(map.to_global(a)),"end_offset":end.distance_to(map.to_global(b))})
	var camera_checks: Array = []
	for region_index in range(5):
		observer.jump_to_region(region_index)
		for turn in range(12):
			for size in [10.0,24.0,48.0]:
				observer.yaw = turn*TAU/12
				observer.pitch = .32 if turn%2 == 0 else 1.2
				observer.zoom = size
				observer._update_camera()
				var camera := observer.camera as Camera3D
				var projected := camera.unproject_position(observer.to_global(observer.focus))
				camera_checks.append({"region":region_index,"turn":turn,"zoom":size,"center_error":projected.distance_to(camera.get_viewport().get_visible_rect().size*.5),"above_ground":observer.to_local(camera.global_position).y>2})
	observer.jump_to_region(1)
	var result := {"capsule_radius":.30,"capsule_height":1.6,"tested_clear_width":2.0,"samples":samples,"failures":failures,"maximum_adjacent_height_change":max_rise,"navigation":nav_results,"camera_checks":camera_checks,"root_transform":str(map.transform)}
	var boundaries: Array = []
	for point in [Vector3(-49.8,1,0),Vector3(49.8,1,0),Vector3(0,1,-39.8),Vector3(0,1,39.8),Vector3(-3,1,0),Vector3(-2.1,1,-8)]:
		var query := PhysicsShapeQueryParameters3D.new()
		query.shape = capsule
		query.transform = Transform3D(map.global_basis,map.to_global(point))
		query.collision_mask = 2
		boundaries.append({"point":str(point),"blocked":not space.intersect_shape(query).is_empty()})
	result["boundary_checks"] = boundaries
	var controls: Dictionary = {}
	var action := InputEventAction.new()
	action.action = "world_map_region_5"
	action.pressed = true
	observer._unhandled_input(action)
	controls["region_shortcut"] = observer.focus.distance_to(observer.regions[4])<.001
	var mouse := InputEventMouseMotion.new()
	mouse.relative = Vector2(160,120)
	var before: float = observer.yaw
	Input.action_press("world_map_orbit")
	observer._unhandled_input(mouse)
	Input.action_release("world_map_orbit")
	controls["orbit_drag"] = absf(observer.yaw-before)>.1
	var before_pan: Vector3 = observer.focus
	Input.action_press("world_map_pan")
	observer._unhandled_input(mouse)
	Input.action_release("world_map_pan")
	controls["pan_drag"] = before_pan.distance_to(observer.focus)>.1
	var zoom_event := InputEventAction.new()
	zoom_event.action = "world_map_zoom_out"
	zoom_event.pressed = true
	for i in range(100):
		observer._unhandled_input(zoom_event)
	controls["zoom_limit"] = is_equal_approx(observer.zoom,observer.max_zoom)
	action.action = "world_reset"
	observer._unhandled_input(action)
	controls["reset"] = observer.focus.distance_to(observer.regions[1])<.001
	var ui: CanvasLayer = observer.get_node("Overlay")
	var was_visible := ui.visible
	action.action = "world_map_ui"
	observer._unhandled_input(action)
	controls["ui_toggle"] = ui.visible != was_visible
	observer._unhandled_input(action)
	result["input_checks"] = controls
	var output := FileAccess.open("res://art/lanternbrook_map_v1/physics_validation.json",FileAccess.WRITE)
	output.store_string(JSON.stringify(result,"\t"))
	return result

func capture_and_measure(tree: SceneTree, scene: Node) -> Dictionary:
	var observer := scene.get_node("Lanternbrook/MapObserver")
	var output_path := "res://art/lanternbrook_map_v1/renders"
	DirAccess.make_dir_recursive_absolute(output_path)
	var records: Array = []
	tree.root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	for dimensions in [Vector2i(1280,720),Vector2i(1920,1080)]:
		tree.root.size = dimensions
		tree.root.content_scale_size = Vector2i.ZERO
		for region in range(5):
			observer.jump_to_region(region)
			for frame in range(35):
				await tree.process_frame
			var durations: Array[float] = []
			var last := Time.get_ticks_usec()
			for frame in range(90):
				await tree.process_frame
				var now := Time.get_ticks_usec()
				durations.append((now-last)/1000.0)
				last = now
			durations.sort()
			var sum_ms: float = 0
			for value in durations:
				sum_ms += value
			observer.get_node("Overlay").hide()
			await RenderingServer.frame_post_draw
			var image := tree.root.get_texture().get_image()
			image.save_png(output_path+"/region_%d_%d.png"%[region+1,dimensions.x])
			records.append({"region":region+1,"requested_size":str(dimensions),"actual_size":str(image.get_size()),"average_ms":sum_ms/durations.size(),"p95_ms":durations[int(durations.size()*.95)],"draw_calls":Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME),"video_adapter":RenderingServer.get_video_adapter_name()})
			observer.get_node("Overlay").show()
	# Orthographic layout captured from the real scene, not an illustrative substitute.
	for index in [0,1,3,4]:
		observer.jump_to_region(index)
		observer.yaw += PI
		observer._update_camera()
		observer.get_node("Overlay").hide()
		for frame in range(12):
			await tree.process_frame
		await RenderingServer.frame_post_draw
		tree.root.get_texture().get_image().save_png(output_path+"/region_%d_reverse.png"%(index+1))
	observer.set_process(false)
	observer.focus = Vector3(0,1,0)
	observer.pitch = PI/2-.001
	observer.yaw = 0
	observer.zoom = 85
	observer._update_camera()
	observer.get_node("Overlay").hide()
	await RenderingServer.frame_post_draw
	tree.root.get_texture().get_image().save_png(output_path+"/map_top.png")
	observer.set_process(true)
	observer.get_node("Overlay").show()
	observer.jump_to_region(1)
	tree.root.size = Vector2i(1280,720)
	tree.root.content_scale_size = Vector2i.ZERO
	var result := {"adapter":RenderingServer.get_video_adapter_name(),"measurements":records,"method":"90 consecutive process-frame intervals per region after 35 warmup frames; editor/game concurrent; average and p95 wall-clock frame times"}
	var output := FileAccess.open("res://art/lanternbrook_map_v1/performance.json",FileAccess.WRITE)
	output.store_string(JSON.stringify(result,"\t"))
	return result
