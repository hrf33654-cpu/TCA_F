extends SceneTree
func _initialize() -> void:
	call_deferred("capture")
func capture() -> void:
	var scene: Node = load("res://scenes/lanternbrook_hd2d_preview.tscn").instantiate()
	root.add_child(scene)
	current_scene = scene
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.content_scale_size = Vector2i.ZERO
	root.size = Vector2i(1920,1080)
	var observer := scene.get_node("Lanternbrook/MapObserver")
	observer.set_process(false)
	observer.focus = Vector3(0,1.5,0)
	observer.get_node("Overlay").hide()
	var camera := observer.get_node("Camera3D") as Camera3D
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	var direction := Vector3(sin(.56)*cos(.55),sin(.55),cos(.56)*cos(.55))
	camera.transform = Transform3D(Basis.IDENTITY,Vector3(0,1.5,0)+direction*140).looking_at(Vector3(0,1.5,0),Vector3.UP)
	camera.size = 84
	for i in range(25):
		await process_frame
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	image.save_png("res://art/lanternbrook_hd2d/renders/map_overview_1920.png")
	print("OVERVIEW_SAVED ",image.get_size())
	current_scene = null
	scene.queue_free()
	for i in range(3):
		await process_frame
	quit()
