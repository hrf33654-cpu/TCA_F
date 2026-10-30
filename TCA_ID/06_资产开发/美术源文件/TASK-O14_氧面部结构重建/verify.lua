local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O14_氧面部结构重建/'
local a=app.open(root..'backup/before.aseprite')
local original=Image(a.width,a.height,ColorMode.RGB);original:drawSprite(a,1)
assert(a.width==104 and a.height==208 and #a.layers==9)
local paths={'variants/face_A.aseprite','variants/face_B.aseprite','variants/face_C.aseprite','character_face_refined.aseprite'}
local checks={}
for j,path in ipairs(paths) do
 local b=app.open(root..path)
 assert(b.width==a.width and b.height==a.height and b.colorMode==a.colorMode)
 assert(#b.frames==#a.frames and b.frames[1].duration==a.frames[1].duration)
 assert(#b.layers==(j==4 and 11 or 10))
 for i=1,#a.layers do
  local la,lb=a.layers[i],b.layers[i]
  assert(la.name==lb.name and la.isVisible==lb.isVisible and la.isEditable==lb.isEditable and la.opacity==lb.opacity and la.blendMode==lb.blendMode)
  local ca,cb=la:cel(1),lb:cel(1)
  assert(ca.position==cb.position and ca.image.width==cb.image.width and ca.image.height==cb.image.height)
  for y=0,ca.image.height-1 do for x=0,ca.image.width-1 do assert(ca.image:getPixel(x,y)==cb.image:getPixel(x,y)) end end
 end
 assert(#a.palettes[1]==#b.palettes[1])
 for i=0,#a.palettes[1]-1 do assert(a.palettes[1]:getColor(i).rgbaPixel==b.palettes[1]:getColor(i).rgbaPixel) end
 local out=Image(b.width,b.height,ColorMode.RGB);out:drawSprite(b,1)
 local delta=0
 for y=0,b.height-1 do for x=0,b.width-1 do
  local old,new=original:getPixel(x,y),out:getPixel(x,y)
  assert(app.pixelColor.rgbaA(old)==app.pixelColor.rgbaA(new),'Alpha changed')
  if old~=new then assert(x>=51 and x<=66 and y>=28 and y<=44,'Outside face');delta=delta+1 end
 end end
 assert(delta>0)
 local png=Image{fromFile=root..(j==4 and 'character_face_refined.png' or 'variants/face_'..({'A','B','C'})[j]..'.png')}
 for y=0,b.height-1 do for x=0,b.width-1 do assert(out:getPixel(x,y)==png:getPixel(x,y),'Export mismatch') end end
 checks[#checks+1]=string.format('{"file":"%s","layers":%d,"changedCompositePixels":%d,"originalNineLayersAndPaletteUnchanged":true,"alphaUnchanged":true,"changesRestrictedToFace":true,"nativePNGMatchesSavedProject":true}',path,#b.layers,delta)
end
local f=assert(io.open(root..'verification.json','w'))
f:write('{"passed":true,"width":104,"height":208,"frames":1,"results":['..table.concat(checks,',')..']}');f:close()
print('ALL_VARIANTS_AND_FINAL_VERIFIED')
