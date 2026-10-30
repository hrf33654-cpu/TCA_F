shader_type spatial;
render_mode cull_disabled;

// Godot +Z points downstream; coordinates follow the curved river centre.
uniform float flow_speed : hint_range(0.0, 3.0, 0.05) = 1.15;
uniform float highlight_strength : hint_range(0.0, 1.0, 0.05) = 0.42;
uniform vec4 deep_color : source_color = vec4(0.10, 0.38, 0.35, 1.0);
uniform vec4 shallow_color : source_color = vec4(0.22, 0.52, 0.44, 1.0);
varying vec3 river_local;

float hash21(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float streak_layer(vec2 uv) {
    vec2 cell = floor(uv);
    vec2 local = fract(uv);
    float seed = hash21(cell);
    float offset = 0.25 + hash21(cell + 19.2) * 0.50;
    float width = mix(0.025, 0.075, seed);
    float length_half = mix(0.10, 0.26, hash21(cell + 7.8));
    float x = abs(local.x - offset);
    float y = abs(local.y - 0.5);
    float ends = 1.0 - smoothstep(length_half * 0.55, length_half, y);
    float line = 1.0 - smoothstep(width * 0.3, width, x);
    return line * ends * smoothstep(0.23, 0.60, seed);
}

void vertex() {
    river_local = VERTEX;
    VERTEX.y += sin(river_local.z * 7.0 - TIME * flow_speed * 7.0 + river_local.x * 2.0) * 0.012;
}

void fragment() {
    float along = floor(river_local.z*28.0)/28.0;
    float centre = -3.0 - 0.11 * along - 0.55 * sin(0.26 * along);
    float across = river_local.x - centre;
    float travel = floor((along-TIME*flow_speed)*24.0)/24.0;
    float meander = sin(travel * 2.0 + across * 5.0) * 0.045;
    float streaks = streak_layer(vec2((across + meander) * 3.4, travel * 1.45));
    streaks += streak_layer(vec2((across - meander) * 5.2 + 13.2, travel * 2.0 + 9.1)) * 0.38;
    float bank = smoothstep(0.94, 1.31, abs(across));
    float edge_foam = bank * (0.5 + 0.5 * sin(travel * 11.0 + across * 17.0));
    float waviness = sin(travel * 10.0 + sin(across * 9.0) * 1.5);
    float colour_mix = clamp(abs(across) * 0.50 + waviness * 0.06, 0.0, 1.0);
    vec3 base = mix(deep_color.rgb, shallow_color.rgb, colour_mix);
    float foam = clamp(streaks * highlight_strength + edge_foam * 0.12, 0.0, 0.72);
    ALBEDO = mix(base, vec3(0.62, 0.80, 0.69), foam);
    EMISSION = vec3(0.16, 0.25, 0.20) * foam * 0.12;
    METALLIC = 0.0;
    ROUGHNESS = 0.72;
    // World-space normal does not require UV tangents on the imported river mesh.
    vec3 ripple_normal = normalize(vec3(
        cos(across * 9.0 + travel * 4.0) * 0.012,
        1.0,
        cos(travel * 10.0 + across * 2.0) * 0.018
    ));
    NORMAL = normalize((VIEW_MATRIX * MODEL_MATRIX * vec4(ripple_normal, 0.0)).xyz);
}
