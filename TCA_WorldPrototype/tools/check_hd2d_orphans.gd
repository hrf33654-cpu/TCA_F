extends SceneTree
func _initialize() -> void:
	call_deferred("check")
func check() -> void:
	var map: Node = load("res://world/maps/lanternbrook_hd2d/lanternbrook_hd2d.tscn").instantiate()
	root.add_child(map)
	await process_frame
	await process_frame
	map.free()
	await process_frame
	Node.print_orphan_nodes()
	print("ORPHAN_CHECK_FINISHED")
	quit()
