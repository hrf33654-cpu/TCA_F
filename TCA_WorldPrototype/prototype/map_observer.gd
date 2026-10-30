extends Node3D
## Inspection camera. A future player camera may reuse focus_target and the same bounds.
@export var focus: Vector3 = Vector3(2.0, 1.3, 0.0)
@export var focus_target: NodePath
@export var min_zoom: float = 10.0
@export var max_zoom: float = 48.0
@export var orbit_distance: float = 68.0
@onready var camera: Camera3D = $Camera3D
@onready var caption: Label = $Overlay/Panel/Rows/Region
var yaw: float = 0.56
var pitch: float = 0.62
var zoom: float = 18.0
var regions: Array[Vector3] = [Vector3(28,1.2,30),Vector3(3,1.3,1),Vector3(-3.4,1.3,1.8),Vector3(-12,1.2,-12),Vector3(-25,1.5,-28)]
var region_names: Array[String] = ["林间入口", "驿站庭院", "溪上石桥", "河岸小径", "林中遗迹"]

func _ready() -> void:
	jump_to_region(1)

func jump_to_region(index: int) -> void:
	focus = regions[clampi(index, 0, 4)]
	yaw = 0.56
	pitch = 0.62
	zoom = 18.0 if index != 4 else 21.0
	caption.text = "%s  ·  地图场景 v1" % region_names[index]
	_update_camera()

func _process(delta: float) -> void:
	var target := get_node_or_null(focus_target) as Node3D if not focus_target.is_empty() else null
	if target != null:
		focus = focus.lerp(to_local(target.global_position) + Vector3.UP, 1.0-exp(-delta*8.0))
	_update_camera()

func _update_camera() -> void:
	focus.x = clampf(focus.x, -43.0, 43.0)
	focus.z = clampf(focus.z, -33.0, 33.0)
	focus.y = clampf(focus.y, 1.1, 6.0)
	var offset := Vector3(sin(yaw)*cos(pitch), sin(pitch), cos(yaw)*cos(pitch)) * orbit_distance
	var position_local := focus + offset
	# Keep the lens above terrain, including when the complete map has been transformed.
	var space := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(to_global(position_local+Vector3.UP*35.0),to_global(position_local-Vector3.UP*90.0),1)
	var hit := space.intersect_ray(query)
	if not hit.is_empty():
		position_local.y = maxf(position_local.y, to_local(hit.position).y + 2.0)
	camera.transform = Transform3D(Basis.IDENTITY, position_local).looking_at(focus, Vector3.UP)
	camera.size = zoom

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		if Input.is_action_pressed("world_map_orbit"):
			yaw = wrapf(yaw-event.relative.x*0.004,-PI,PI)
			pitch = clampf(pitch+event.relative.y*0.003,0.32,1.20)
		elif Input.is_action_pressed("world_map_pan"):
			var right := Vector3(cos(yaw),0,-sin(yaw))
			var forward := Vector3(sin(yaw),0,cos(yaw))
			focus += (-right*event.relative.x-forward*event.relative.y)*zoom/720.0
	elif event.is_action_pressed("world_map_zoom_in"):
		zoom = clampf(zoom-1.2,min_zoom,max_zoom)
	elif event.is_action_pressed("world_map_zoom_out"):
		zoom = clampf(zoom+1.2,min_zoom,max_zoom)
	elif event.is_action_pressed("world_reset"):
		jump_to_region(1)
	elif event.is_action_pressed("world_map_ui"):
		$Overlay.visible = not $Overlay.visible
	for index in range(5):
		if event.is_action_pressed("world_map_region_%d" % (index+1)):
			jump_to_region(index)
