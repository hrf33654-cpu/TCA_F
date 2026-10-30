local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O12_氧192正面系统精修/'
local a=app.open(root..'backup/character_original.aseprite')
local b=app.open(root..'character_refined.aseprite')
assert(a.width==b.width and a.height==b.height and a.colorMode==b.colorMode)
assert(#a.frames==1 and #b.frames==1 and a.frames[1].duration==b.frames[1].duration)
assert(#a.layers==3 and #b.layers==8)
for i=1,#a.layers do
 local la,lb=a.layers[i],b.layers[i]
 assert(la.name==lb.name and la.isVisible==lb.isVisible and la.isEditable==lb.isEditable and la.opacity==lb.opacity and la.blendMode==lb.blendMode)
 local ca,cb=la:cel(1),lb:cel(1)
 assert(ca.position==cb.position and ca.image.width==cb.image.width and ca.image.height==cb.image.height)
 for y=0,ca.image.height-1 do for x=0,ca.image.width-1 do assert(ca.image:getPixel(x,y)==cb.image:getPixel(x,y)) end end
end
for i=0,#a.palettes[1]-1 do
 local ca,cb=a.palettes[1]:getColor(i),b.palettes[1]:getColor(i)
 assert(ca.rgbaPixel==cb.rgbaPixel)
end
local f=assert(io.open(root..'verification/layer-preservation.json','w'))
f:write('{"originalLayerCount":3,"finalLayerCount":8,"originalLayerNamesVisibilityLocksOpacityBlendAndPixelsUnchanged":true,"originalPalettePrefixUnchanged":true,"frameCountAndDurationUnchanged":true,"nativeDimensionsAndColorModeUnchanged":true}')
f:close()
print('ORIGINAL_LAYERS_PRESERVED_PASS')
