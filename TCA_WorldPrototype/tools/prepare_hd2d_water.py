from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'world/maps/lanternbrook_hd2d'
s=(ROOT/'world/environments/lanternbrook/river.gdshader').read_text(encoding='utf8')
s=s.replace('float along = river_local.z;','float along = floor(river_local.z*28.0)/28.0;')
s=s.replace('float travel = along - TIME * flow_speed;','float travel = floor((along-TIME*flow_speed)*24.0)/24.0;')
s=s.replace('METALLIC = 0.18;','METALLIC = 0.0;').replace('ROUGHNESS = 0.24 + foam * 0.18;','ROUGHNESS = 0.72;').replace('* 0.055','* 0.012').replace('* 0.085','* 0.018')
(base/'pixel_river.gdshader').write_text(s,encoding='utf8')
s=(ROOT/'world/environments/lanternbrook/river_material.tres').read_text(encoding='utf8')
s=s.replace('res://world/environments/lanternbrook/river.gdshader','res://world/maps/lanternbrook_hd2d/pixel_river.gdshader')
s=s.replace('Color(0.10, 0.38, 0.35, 1)','Color(0.07, 0.29, 0.30, 1)').replace('Color(0.22, 0.52, 0.44, 1)','Color(0.18, 0.43, 0.37, 1)')
(base/'river_material.tres').write_text(s,encoding='utf8')
