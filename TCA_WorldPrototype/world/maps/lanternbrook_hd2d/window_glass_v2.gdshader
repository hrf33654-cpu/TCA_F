shader_type spatial;
render_mode cull_disabled;
uniform bool lantern = false;
varying vec3 pane_position;
void vertex() { pane_position=VERTEX; }
void fragment() {
	float horizontal=abs(NORMAL.x)>.6 ? pane_position.z : pane_position.x;
	float ripple=.5+.5*sin(horizontal*39.+sin(pane_position.y*6.)*.7);
	float curtain=smoothstep(.10,.82,.5+.5*sin(horizontal*5.3+pane_position.y*.55));
	float glow=lantern ? .90 : .55+curtain*.31;
	float soot=(1.-smoothstep(0.,.42,fract(pane_position.y*.97)))*.14;
	vec3 amber=mix(vec3(.52,.18,.025),vec3(1.,.56,.17),glow);
	amber*=1.-soot+ripple*.035;
	ALBEDO=amber*.68;
	EMISSION=amber*(lantern ? 2.7 : 1.25+curtain*.9);
	ROUGHNESS=.43;
	SPECULAR=.24;
}
