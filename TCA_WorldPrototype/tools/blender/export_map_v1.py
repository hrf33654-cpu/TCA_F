"""Reuse proven PBR baking, but retain spatial cells and semantic geometry groups."""
from pathlib import Path
ROOT=Path(r'E:\TCA_F\TCA_WorldPrototype')
source=(ROOT/'tools/blender/export_hamlet.py').read_text(encoding='utf8')
source=source.replace("OUT=ROOT/'art'/'alchemist_hamlet'", "OUT=ROOT/'art'/'lanternbrook_map_v1'")
source=source.replace("DEST=ROOT/'world'/'environments'/'lanternbrook'", "DEST=ROOT/'world'/'maps'/'lanternbrook'")
start=source.index('# Group the editable source file')
end=source.index('# Static triangles are merged')
source=source[:start]+'''def category(o):
    n=o.name
    if 'Waterwheel' in n and 'axle' not in n: return 'Wheel'
    if n.startswith(('V1_Ground',)): return 'Ground'
    if n.startswith(('V1_Backdrop',)): return 'Backdrop'
    if n.startswith(('V1_PerimeterRock',)): return 'ForegroundRock'
    if n.startswith(('Bridge_deck','V1_BridgeDeck','V1_DoorStep','V1_RuinStep','V1_RuinTerrace','V1_RuinInset')): return 'WalkSurface'
    if n.startswith(('V1_River',)):return 'River'
    if 'Roof' in n or 'roof' in n or n.startswith(('INN_Slate','Gable')):return 'Roof'
    if any(t in n for t in ['Foliage','Individual_leaf','Layered_fir','Canopy']):return 'Canopy'
    if any(t in n for t in ['Meadow','Wildflower','Reed','Fern','Ivy','Planter_flower']):return 'Foliage'
    if n.startswith('V1_Ruin'):return 'Ruins'
    return 'Details'

''' + source[end:]
source=source.replace("bucket=o.users_collection[0].name", "bucket=category(o)")
source=source.replace("key=(bucket,ma.name)", """center=sum((positions[i] for i in tri.vertices),Vector())/3
        cell='' if bucket in ['Wheel','Roof','River'] else '_%d_%d'%(math.floor(center.x/16),math.floor(center.y/16))
        key=(bucket+cell,ma.name)""")
source=source.replace("DEST/'lanternbrook.glb'", "DEST/'map_art.glb'")
source=source.replace("OUT/'Lanternbrook_HD2D.blend'", "OUT/'Lanternbrook_Map_v1.blend'")
source=source.replace("OUT/'renders'/'Lanternbrook_final.png'", "OUT/'renders'/'Map_v1.png'")
exec(compile(source,'export_map_v1_generated','exec'),globals())
