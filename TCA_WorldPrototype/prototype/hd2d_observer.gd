extends Node3D
## Inspection camera. A future player camera may reuse focus_target and the same bounds.
@export var focus: Vector3 = Vector3(2.0, 1.3, 0.0)
@export var focus_target: NodePath
@export var min_zoom: float = 14.0
@export var max_zoom: float = 27.0
@export var orbit_distance: float = 96.0
@export var view_pitch_degrees: float = 20.0
@onready var camera: Camera3D = $Camera3D
@onready var caption: Label = $Overlay/Panel/Rows/Region
@onready var optics_caption: Label = $Overlay/Panel/Rows/Optics
@onready var upper_field: CanvasLayer = $UpperField
@onready var upper_material: ShaderMaterial = $UpperField/Softness.material
const PROFILE_PATH := "res://world/maps/lanternbrook_hd2d/depth_profiles.json"
const OPTICS_NAMES := ["分区景深", "原版景深", "关闭景深"]
const PROFILE_KEYS := ["near_clear", "far_clear", "near_transition", "far_transition", "amount"]
var optics_mode: int = 0
var depth_profiles: Array = []
var optics: CameraAttributesPractical
var legacy_optics: CameraAttributesPractical
var yaw: float = 0.56
var pitch: float = deg_to_rad(20.0)
@export var base_yaw: float = 0.56
@export var yaw_limit: float = 0.20944
var zoom: float = 18.0
var regions: Array[Vector3] = [Vector3(28,1.2,30),Vector3(3,1.3,1),Vector3(-3.4,1.3,1.8),Vector3(-12,1.2,-12),Vector3(-25,1.5,-28)]
var region_names: Array[String] = ["林间入口", "驿站庭院", "溪上石桥", "河岸小径", "林中遗迹"]

func _ready() -> void:
	# Own the attributes: review modes never mutate the shared v2 resource.
	legacy_optics = camera.attributes.duplicate() as CameraAttributesPractical
	optics = legacy_optics.duplicate() as CameraAttributesPractical
	camera.attributes = optics
	upper_material = upper_material.duplicate() as ShaderMaterial
	$UpperField/Softness.material = upper_material
	var profile_data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(PROFILE_PATH))
	depth_profiles = profile_data.profiles
	RenderingServer.camera_attributes_set_dof_blur_bokeh_shape(RenderingServer.DOF_BOKEH_CIRCLE)
	RenderingServer.camera_attributes_set_dof_blur_quality(RenderingServer.DOF_BLUR_QUALITY_HIGH, false)
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://world/maps/lanternbrook_hd2d/complete_data.json"))
	regions.clear()
	region_names.clear()
	for region in data.regions:
		regions.append(Vector3(region.position[0],maxf(1.1,region.position[1]),region.position[2]))
		region_names.append(region.label)
	jump_to_region(1)

func jump_to_region(index: int) -> void:
	index = clampi(index, 0, regions.size()-1)
	focus = regions[clampi(index, 0, regions.size()-1)]
	yaw = 0.56
	pitch = deg_to_rad(view_pitch_degrees)
	zoom = 14.5 if index in [3,5] else 16.0
	caption.text = "%s  ·  HD2D 完整地图" % region_names[index]
	_update_camera()

func _process(delta: float) -> void:
	var target := get_node_or_null(focus_target) as Node3D if not focus_target.is_empty() else null
	if target != null:
		focus = focus.lerp(to_local(target.global_position) + Vector3.UP, 1.0-exp(-delta*8.0))
	_update_camera()

func _update_camera() -> void:
	yaw = clampf(yaw,base_yaw-yaw_limit,base_yaw+yaw_limit)
	pitch = deg_to_rad(view_pitch_degrees)
	zoom = clampf(zoom,min_zoom,max_zoom)
	focus.x = clampf(focus.x, -43.0, 43.0)
	focus.z = clampf(focus.z, -33.0, 33.0)
	focus.y = clampf(focus.y, 1.1, 6.0)
	var offset := Vector3(sin(yaw)*cos(pitch), sin(pitch), cos(yaw)*cos(pitch)) * orbit_distance
	var position_local := focus + offset
	# Keep the lens above terrain, including when the complete map has been transformed.
	var space := get_world_3d().direct_space_state
	var query := PhysicsRayQueryParameters3D.create(to_global(position_local+Vector3.UP*35.0),to_global(position_local-Vector3.UP*90.0),5)
	var hit := space.intersect_ray(query)
	if not hit.is_empty():
		position_local.y = maxf(position_local.y, to_local(hit.position).y + 2.0)
	camera.transform = Transform3D(Basis.IDENTITY, position_local).looking_at(focus, Vector3.UP)
	camera.projection = Camera3D.PROJECTION_PERSPECTIVE
	camera.far = 400.0
	camera.fov = rad_to_deg(2.0*atan(zoom/(2.0*orbit_distance)))
	_update_optics()

func set_optics_mode(mode: int) -> void:
	optics_mode = posmod(mode, OPTICS_NAMES.size())
	# The comparison includes the original renderer defaults, not just v2 distances.
	RenderingServer.camera_attributes_set_dof_blur_bokeh_shape(RenderingServer.DOF_BOKEH_CIRCLE if optics_mode == 0 else int(ProjectSettings.get_setting("rendering/camera/depth_of_field/depth_of_field_bokeh_shape", 1)))
	RenderingServer.camera_attributes_set_dof_blur_quality(RenderingServer.DOF_BLUR_QUALITY_HIGH if optics_mode == 0 else int(ProjectSettings.get_setting("rendering/camera/depth_of_field/depth_of_field_bokeh_quality", 1)), false if optics_mode == 0 else bool(ProjectSettings.get_setting("rendering/camera/depth_of_field/depth_of_field_use_jitter", false)))
	_update_optics()

func _update_optics() -> void:
	if optics == null:
		return
	optics_caption.text = "D 切换对比：%s" % OPTICS_NAMES[optics_mode]
	upper_field.visible = optics_mode == 0
	optics.dof_blur_near_enabled = optics_mode != 2
	optics.dof_blur_far_enabled = optics_mode != 2
	if optics_mode == 1:
		for property in ["dof_blur_near_distance", "dof_blur_far_distance", "dof_blur_near_transition", "dof_blur_far_transition", "dof_blur_amount"]:
			optics.set(property, legacy_optics.get(property))
		return
	if optics_mode == 2:
		return
	# Smooth spatial weights avoid a focus pop when panning between adjacent regions.
	var blended := {"near_clear":0.0, "far_clear":0.0, "near_transition":0.0, "far_transition":0.0, "amount":0.0}
	var weight_sum := 0.0
	for i in range(mini(regions.size(), depth_profiles.size())):
		var distance_squared := Vector2(focus.x-regions[i].x, focus.z-regions[i].z).length_squared()
		var weight := 1.0 / pow(distance_squared + 4.0, 2.0)
		weight_sum += weight
		for key in PROFILE_KEYS:
			blended[key] += float(depth_profiles[i][key]) * weight
	for key in PROFILE_KEYS:
		blended[key] /= maxf(weight_sum, 1.0e-20)
	# Use camera-space depth, including terrain clearance and the map instance transform.
	var focus_depth := -camera.to_local(to_global(focus)).z
	var framing_scale := clampf(zoom / 16.0, 0.875, 1.6875)
	# Keep the screen-space shoulder independent of render resolution. Widen the
	# clear center slightly in the overview, and keep all review UI above it.
	upper_material.set_shader_parameter("clear_boundary", lerpf(0.34, 0.28, clampf((zoom-16.0)/11.0, 0.0, 1.0)))
	var resolution_scale := maxf(get_viewport().get_texture().get_height() / 720.0, 0.5)
	upper_material.set_shader_parameter("blur_lod", 2.25 + log(resolution_scale)/log(2.0))
	optics.dof_blur_near_distance = maxf(camera.near + 1.0, focus_depth - blended.near_clear * framing_scale)
	optics.dof_blur_far_distance = focus_depth + blended.far_clear * framing_scale
	optics.dof_blur_near_transition = blended.near_transition * framing_scale
	optics.dof_blur_far_transition = blended.far_transition * framing_scale
	optics.dof_blur_amount = blended.amount

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_D:
		set_optics_mode(optics_mode + 1)
		get_viewport().set_input_as_handled()
		return
	if event is InputEventMouseMotion:
		if Input.is_action_pressed("world_map_orbit"):
			yaw = clampf(yaw-event.relative.x*0.003,base_yaw-yaw_limit,base_yaw+yaw_limit)
			pitch = deg_to_rad(view_pitch_degrees)
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
	for index in range(regions.size()):
		if event.is_action_pressed("world_map_region_%d" % (index+1)):
			jump_to_region(index)
