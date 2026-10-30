extends Node3D
## Environment behaviour only. Authored geometry, lights and colliders live in the scene.
@export var wheel_speed: float = 0.35
@export var fade_amount: float = 0.78
@export var fade_speed: float = 6.0
@export var focus_target: NodePath
@onready var wheel: Node3D = $Waterwheel
var occluders: Array[MeshInstance3D] = []

func _ready() -> void:
	for node in $Art.find_children("*", "MeshInstance3D", true, false):
		if String(node.name).begins_with("Canopy") or String(node.name).begins_with("Roof") or String(node.name).begins_with("ForegroundRock"):
			occluders.append(node)

func _process(delta: float) -> void:
	wheel.rotate_x(wheel_speed * delta)
	var camera := get_viewport().get_camera_3d()
	if camera == null:
		return
	var target := get_node_or_null(focus_target) as Node3D if not focus_target.is_empty() else null
	var observer := camera.get_parent()
	var aim: Vector3 = target.global_position + Vector3.UP if target != null else observer.to_global(observer.focus) if "focus" in observer else global_position
	for mesh in occluders:
		var a := mesh.to_local(camera.global_position)
		var b := mesh.to_local(aim)
		var blocked: bool = mesh.get_aabb().intersects_segment(a, b) != null
		mesh.transparency = move_toward(mesh.transparency, fade_amount if blocked else 0.0, fade_speed * delta)
