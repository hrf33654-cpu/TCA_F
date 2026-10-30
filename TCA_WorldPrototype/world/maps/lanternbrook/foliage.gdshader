shader_type spatial;
render_mode cull_disabled;
uniform vec4 base_color : source_color = vec4(0.3,0.4,0.2,1.0);
uniform sampler2D albedo_texture : source_color, filter_linear_mipmap, repeat_enable;
uniform bool has_texture = false;
uniform float wind_strength = 0.045;
void vertex() {
    vec3 world = (MODEL_MATRIX * vec4(VERTEX,1.0)).xyz;
    float sway = sin(world.x * 0.7 + world.z * 0.37 + TIME * 1.15);
    VERTEX.x += sway * wind_strength;
    VERTEX.z += cos(world.z * 0.6 + TIME * 0.93) * wind_strength * 0.4;
}
void fragment() {
    ALBEDO = base_color.rgb * (has_texture ? texture(albedo_texture, UV).rgb : vec3(1.0));
    ROUGHNESS = 0.86;
}
