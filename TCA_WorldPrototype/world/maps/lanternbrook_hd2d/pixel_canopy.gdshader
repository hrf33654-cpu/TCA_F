shader_type spatial;
render_mode cull_disabled, depth_prepass_alpha;
uniform sampler2D crown_texture : source_color, filter_nearest, repeat_disable;
uniform vec4 leaf_tint : source_color = vec4(1.0);
uniform float source_pixels = 192.0;
uniform float wind_strength = .022;
varying vec3 object_pos;
void vertex() {
    object_pos=VERTEX;
    VERTEX.x+=sin(TIME*.85+MODEL_MATRIX[3].x*.7)*wind_strength*(UV.y*.3+.7);
}
void fragment() {
    vec2 pixel_uv=(floor(UV*source_pixels)+.5)/source_pixels;
    vec4 tex=texture(crown_texture,pixel_uv);
    ALBEDO=tex.rgb*leaf_tint.rgb;
    ALPHA=tex.a;
    ALPHA_SCISSOR_THRESHOLD=.45;
    // Illustrated leaves already contain their small shadows. Keep broad light soft.
    NORMAL=normalize(vec3((UV.x-.5)*.35,(.5-UV.y)*.35,1.0));
    ROUGHNESS=1.0;
    SPECULAR=0.0;
    EMISSION=tex.rgb*leaf_tint.rgb*.16;
}
