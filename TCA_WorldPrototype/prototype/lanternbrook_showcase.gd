extends Node3D
## Environment-only showcase. No player, characters, combat or persistent state.

const TARGET := Vector3(0.5, 1.5, -3.0)
const HERO_POSITION := Vector3(21.0, 23.0, 30.0)
var camera: Camera3D
var overlay: CanvasLayer
var orbit_yaw := 0.0
var orbit_pitch := 0.0
var capture_path := ""
@export var river_material: ShaderMaterial = preload("res://world/environments/lanternbrook/river_material.tres")

func _ready() -> void:
	_setup_lighting()
	camera = Camera3D.new()
	camera.name = "HD2DCamera"
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 15.8625
	camera.near = 0.1
	camera.far = 180.0
	add_child(camera)
	_reset_camera()
	camera.make_current()
	var optics := CameraAttributesPractical.new()
	optics.dof_blur_far_enabled = true
	optics.dof_blur_far_distance = 49.0
	optics.dof_blur_far_transition = 12.0
	optics.dof_blur_near_enabled = true
	optics.dof_blur_near_distance = 34.0
	optics.dof_blur_near_transition = 10.0
	optics.dof_blur_amount = 0.06
	camera.attributes = optics
	for item in find_children("*", "MeshInstance3D", true, false):
		var mesh_name := String(item.name).to_lower()
		if "jade" in mesh_name:
			item.material_override = river_material
		elif "silver glints" in mesh_name or "silver_glints" in mesh_name:
			# Baked white streaks are replaced by downstream-moving shader highlights.
			item.visible = false
	_setup_overlay()
	for argument in OS.get_cmdline_user_args():
		if argument.begins_with("--capture="):
			capture_path = argument.trim_prefix("--capture=")
	if not capture_path.is_empty():
		overlay.hide()
		for frame in range(24):
			await get_tree().process_frame
		await RenderingServer.frame_post_draw
		var image := get_viewport().get_texture().get_image()
		var result := image.save_png(capture_path)
		print("LANTERNBROOK_CAPTURE=", result, " path=", capture_path)
		print("LANTERNBROOK_MESHES=", find_children("*", "MeshInstance3D", true, false).size())
		get_tree().quit(0 if result == OK else 1)

func _setup_lighting() -> void:
	var world := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.19, 0.27, 0.32)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_sky_contribution = 0.0
	env.ambient_light_color = Color(0.46, 0.59, 0.69)
	env.ambient_light_energy = 0.48
	env.tonemap_mode = Environment.TONE_MAPPER_AGX
	env.tonemap_exposure = 1.1
	env.tonemap_agx_contrast = 1.38
	env.ssao_enabled = true
	env.ssao_radius = 1.1
	env.ssao_intensity = 1.4
	env.ssil_enabled = true
	env.ssil_intensity = 0.7
	env.glow_enabled = true
	env.glow_intensity = 0.24
	env.glow_hdr_threshold = 1.6
	env.fog_enabled = true
	env.fog_light_color = Color(0.40, 0.53, 0.57)
	env.fog_density = 0.001
	world.environment = env
	add_child(world)
	var sun := DirectionalLight3D.new()
	sun.name = "AmberEveningSun"
	sun.light_color = Color(1.0, 0.78, 0.52)
	sun.light_energy = 1.8
	sun.shadow_enabled = true
	sun.directional_shadow_max_distance = 85.0
	add_child(sun)
	sun.position = Vector3(-12.0, 16.0, 8.0)
	sun.look_at(to_global(Vector3(0.0, 0.0, -3.0)))
	var fill := DirectionalLight3D.new()
	fill.light_color = Color(1.0, 0.81, 0.57)
	fill.light_energy = 0.38
	add_child(fill)
	fill.rotation_degrees = Vector3(-48.0, -25.0, 0.0)
	for point: Vector3 in [Vector3(2.2, 2.44, -0.22), Vector3(5.6, 2.40, 0.73), Vector3(-6.03, 2.3, 0.9), Vector3(-0.68, 2.3, 0.9), Vector3(7.92, 2.1, 4.3), Vector3(-8.08, 1.9, 5.0), Vector3(3.2, 2.8, 0.3)]:
		var lamp := OmniLight3D.new()
		lamp.light_color = Color(1.0, 0.55, 0.20)
		lamp.light_energy = 2.0
		lamp.omni_range = 4.2
		lamp.omni_attenuation = 1.6
		lamp.shadow_enabled = false
		add_child(lamp)
		lamp.position = point
	get_viewport().msaa_3d = Viewport.MSAA_4X
	get_viewport().screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA

func _setup_overlay() -> void:
	overlay = CanvasLayer.new()
	add_child(overlay)
	var font := SystemFont.new()
	font.font_names = PackedStringArray(["Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC"])
	var title := Label.new()
	title.position = Vector2(34, 26)
	title.text = "溪灯驿站"
	title.add_theme_font_override("font", font)
	title.add_theme_font_size_override("font_size", 28)
	title.add_theme_color_override("font_color", Color(0.96, 0.91, 0.76))
	title.add_theme_color_override("font_shadow_color", Color(0.03, 0.06, 0.05, 0.9))
	title.add_theme_constant_override("shadow_offset_x", 2)
	title.add_theme_constant_override("shadow_offset_y", 2)
	overlay.add_child(title)
	var caption := Label.new()
	caption.position = Vector2(36, 65)
	caption.text = "L A N T E R N B R O O K"
	caption.add_theme_font_size_override("font_size", 12)
	caption.modulate = Color(0.83, 0.87, 0.76, 0.85)
	overlay.add_child(caption)
	var controls := Label.new()
	controls.position = Vector2(36, 94)
	controls.text = "右键环视  ·  滚轮缩放  ·  R 复位  ·  Tab 隐藏界面"
	controls.add_theme_font_override("font", font)
	controls.add_theme_font_size_override("font_size", 12)
	controls.modulate = Color(0.82, 0.87, 0.83, 0.8)
	overlay.add_child(controls)

func _reset_camera() -> void:
	var offset := HERO_POSITION - TARGET
	orbit_yaw = atan2(offset.x, offset.z)
	orbit_pitch = asin(offset.y / offset.length())
	camera.size = 15.8625
	_update_orbit_camera()

func _update_orbit_camera() -> void:
	var distance := (HERO_POSITION - TARGET).length()
	var offset := Vector3(
		sin(orbit_yaw) * cos(orbit_pitch),
		sin(orbit_pitch),
		cos(orbit_yaw) * cos(orbit_pitch)
	) * distance
	# Both position and aim are in the scene's local coordinate system.
	# Moving or rotating the complete environment must not shift the orbit centre.
	camera.transform = Transform3D(Basis.IDENTITY, TARGET + offset).looking_at(TARGET, Vector3.UP)

func _orbit_camera(mouse_delta: Vector2) -> void:
	orbit_yaw = wrapf(orbit_yaw - mouse_delta.x * 0.004, -PI, PI)
	orbit_pitch = clampf(orbit_pitch + mouse_delta.y * 0.003, 0.28, 1.2)
	_update_orbit_camera()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and (event.button_mask & MOUSE_BUTTON_MASK_RIGHT) != 0:
		_orbit_camera(event.relative)
	elif event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			camera.size = clampf(camera.size - 0.8, 10.0, 29.0)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			camera.size = clampf(camera.size + 0.8, 10.0, 29.0)
	elif event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_R:
			_reset_camera()
		elif event.keycode == KEY_TAB:
			overlay.visible = not overlay.visible
