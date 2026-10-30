shader_type spatial;
render_mode cull_disabled;
uniform sampler2D pixel_texture : source_color, filter_nearest_mipmap, repeat_enable;
uniform sampler2D ground_texture : source_color, filter_nearest_mipmap, repeat_enable;
uniform vec4 tint : source_color = vec4(1.0);
uniform float texture_scale = 0.75;
uniform float moss_amount = 0.0;
uniform int material_kind = 0;
uniform float base_roughness = 0.87;
uniform float relief_strength = 0.12;
uniform float source_pixels = 256.0;
instance uniform vec4 map_row_x = vec4(1.,0.,0.,0.);
instance uniform vec4 map_row_y = vec4(0.,1.,0.,0.);
instance uniform vec4 map_row_z = vec4(0.,0.,1.,0.);
uniform bool ground_surface = false;
uniform bool path_surface = false;
uniform vec4 path_segments[48];
uniform int segment_count = 0;
varying vec3 map_position;
varying vec3 map_normal;

float hash(vec2 p) { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
float field(vec2 p) {
	vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
	return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);
}
void vertex() {
	vec4 p=vec4(VERTEX,1.);
	map_position=vec3(dot(map_row_x,p),dot(map_row_y,p),dot(map_row_z,p));
	map_normal=normalize(vec3(dot(map_row_x.xyz,NORMAL),dot(map_row_y.xyz,NORMAL),dot(map_row_z.xyz,NORMAL)));
}
void fragment() {
	vec2 uv=UV*texture_scale;
	if (ground_surface) { uv=map_position.xz*.23; }
	vec2 pixel_uv=(floor(uv*source_pixels)+.5)/source_pixels;
	vec2 grad_x=dFdx(uv), grad_y=dFdy(uv);
	vec3 color=textureGrad(pixel_texture,pixel_uv,grad_x,grad_y).rgb*tint.rgb;
	float mineral=field(floor(map_position.xz*32.)/21.);
	float broad=field(map_position.xz*.19);
	float river_x=-3.-.11*map_position.z-.55*sin(.26*map_position.z);
	float wet=(1.-smoothstep(1.5,3.4,abs(map_position.x-river_x)))*(1.-smoothstep(.05,.8,map_position.y));
	float up=smoothstep(.3,.86,map_normal.y);
	float moss=smoothstep(.50,.80,mineral*.55+broad*.45)*moss_amount*(up*.7+wet*.7);
	color=mix(color,vec3(.16,.205,.095)*(0.78+mineral*.3),clamp(moss,0.,.58));
	if (material_kind==0) {
		color*=mix(.86,1.05,field(map_position.xz*.83+map_position.y*.25));
		color*=1.-wet*.32;
	} else if (material_kind==1) {
		float foot=(1.-smoothstep(.35,1.15,map_position.y))*(.4+.6*field(map_position.xz*1.6));
		color=mix(color,color*vec3(.66,.72,.63),foot*.6);
	} else if (material_kind==2) {
		color*=.91+.13*field(map_position.xz*2.2);
	} else if (material_kind==3) {
		float tide=(1.-smoothstep(.9,1.7,map_position.y))*(.30+.7*field(map_position.xz*3.1));
		color=mix(color,vec3(.29,.32,.23),tide*.52);
		float eaves=exp(-abs(map_position.y-3.08)*10.)*.13+exp(-abs(map_position.y-4.55)*7.)*.14;
		color*=1.-eaves*(.6+.4*field(map_position.xz*6.));
	}
	if (ground_surface) {
		if (path_surface) {
			float distance_to_path=999.;
			for (int i=0;i<48;i++) {
				if (i>=segment_count) { break; }
				vec2 a=path_segments[i].xy, b=path_segments[i].zw, v=b-a;
				float t=clamp(dot(map_position.xz-a,v)/max(dot(v,v),.001),0.,1.);
				distance_to_path=min(distance_to_path,length(map_position.xz-a-t*v));
			}
			float irregular=field(map_position.xz*2.3)*.14+field(map_position.xz*9.)*.05;
			float edge=smoothstep(.82+irregular,1.22+irregular,distance_to_path);
			vec3 verge=textureGrad(ground_texture,pixel_uv,grad_x,grad_y).rgb;
			color=mix(color,verge,edge);
			color*=1.+(1.-smoothstep(.15,.90,distance_to_path))*.08;
		}
		color*=mix(.80,1.13,smoothstep(.22,.78,broad));
		color=mix(color,vec3(.040,.038,.022)*(0.85+mineral*.15),wet*.75);
	}
	float h=dot(textureGrad(pixel_texture,pixel_uv,grad_x,grad_y).rgb,vec3(.299,.587,.114));
	float hx=dot(textureGrad(pixel_texture,pixel_uv+vec2(1./source_pixels,0),grad_x,grad_y).rgb,vec3(.299,.587,.114));
	float hy=dot(textureGrad(pixel_texture,pixel_uv+vec2(0,1./source_pixels),grad_x,grad_y).rgb,vec3(.299,.587,.114));
	vec3 qx=dFdx(VERTEX), qy=dFdy(VERTEX);
	vec2 tx=dFdx(uv), ty=dFdy(uv);
	vec3 s=qx*ty.y-qy*tx.y, t=-qx*ty.x+qy*tx.x;
	float inv=1./max(max(length(s),length(t)),.00001);
	NORMAL=normalize(NORMAL-(s*(hx-h)+t*(hy-h))*inv*relief_strength*6.);
	ALBEDO=color;
	ROUGHNESS=clamp(base_roughness+(mineral-.5)*.11-wet*.18,.55,1.);
	SPECULAR=material_kind==2 ? .24 : .16;
	AO=1.-moss*.14;
	AO_LIGHT_AFFECT=.22;
}
