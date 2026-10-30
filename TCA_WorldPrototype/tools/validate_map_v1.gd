extends SceneTree
## Standalone rendered validation avoids the editor's fixed embedded viewport resolution.
func _initialize() -> void:
	call_deferred("run_checks")

func run_checks() -> void:
	var instance := (load("res://scenes/lanternbrook_map_preview.tscn") as PackedScene).instantiate()
	root.add_child(instance)
	current_scene = instance
	for i in range(10):
		await process_frame
	var checker := preload("res://prototype/map_v1_validation.gd").new()
	var physics := await checker.run(self,instance)
	print("MAP_PHYSICS samples=",physics.samples," failures=",physics.failures.size()," max_rise=",physics.maximum_adjacent_height_change)
	var performance := await checker.capture_and_measure(self,instance)
	print("MAP_PERFORMANCE ",JSON.stringify(performance))
	quit(0 if physics.failures.is_empty() else 1)
