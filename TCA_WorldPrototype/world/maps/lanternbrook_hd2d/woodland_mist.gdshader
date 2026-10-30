shader_type spatial;
render_mode unshaded, cull_disabled, depth_draw_never;
uniform vec4 mist_color : source_color = vec4(.28,.47,.51,.12);
float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
void fragment() {
    vec2 p=UV*2.-1.;
    float edge=pow(max(0.,1.-dot(p,p)),2.0);
    float wave=.65+.15*sin(UV.x*18.+TIME*.09)+.15*sin(UV.y*23.-TIME*.07);
    float grain=.85+.15*hash(floor(UV*180.));
    ALBEDO=mist_color.rgb;
    ALPHA=edge*wave*grain*mist_color.a;
}
