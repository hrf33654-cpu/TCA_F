shader_type canvas_item;
render_mode unshaded;

// A gentle tilt-shift shoulder supplements optical DOF where tall canopies
// project into the top of the image while remaining on the optical focus plane.
uniform sampler2D scene_color : hint_screen_texture, repeat_disable, filter_linear_mipmap;
uniform float clear_boundary : hint_range(0.0, 1.0) = 0.34;
uniform float full_boundary : hint_range(0.0, 1.0) = 0.035;
uniform float blur_lod : hint_range(0.0, 5.0) = 2.25;
uniform float blend_amount : hint_range(0.0, 1.0) = 0.85;

void fragment() {
	float shoulder = 1.0 - smoothstep(full_boundary, clear_boundary, SCREEN_UV.y);
	vec3 sharp = textureLod(scene_color, SCREEN_UV, 0.0).rgb;
	// Let both blur radius and coverage taper; no hard horizontal blur boundary.
	vec3 soft = textureLod(scene_color, SCREEN_UV, blur_lod * shoulder).rgb;
	COLOR = vec4(mix(sharp, soft, shoulder * blend_amount), 1.0);
}
