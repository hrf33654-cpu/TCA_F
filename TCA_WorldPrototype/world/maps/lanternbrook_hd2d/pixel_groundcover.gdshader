shader_type spatial;
render_mode cull_disabled,depth_prepass_alpha;
uniform sampler2D grass_texture : source_color,filter_nearest_mipmap,repeat_disable;
void vertex() {
	VERTEX.x+=sin(TIME*.85+MODEL_MATRIX[3].x*.7)*.014*(1.-UV.y);
}
void fragment() {
	vec2 scale=vec2(256.,112.);
	vec2 uv=(floor(UV*scale)+.5)/scale;
	vec4 color=textureGrad(grass_texture,uv,dFdx(UV),dFdy(UV));
	ALBEDO=color.rgb*vec3(.87,.94,.85);
	ALPHA=color.a;
	ALPHA_SCISSOR_THRESHOLD=.48;
	ROUGHNESS=1.;
	SPECULAR=0.;
	EMISSION=color.rgb*.055;
}
