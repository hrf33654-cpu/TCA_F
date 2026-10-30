local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O13_氧眼睛与上半脸精修/'
local a=app.open(root..'backup/character_before.aseprite')
local b=app.open(root..'character_eyes_refined.aseprite')
assert(a.width==104 and a.height==208 and a.width==b.width and a.height==b.height and a.colorMode==b.colorMode)
assert(#a.frames==1 and #b.frames==1 and a.frames[1].duration==b.frames[1].duration)
assert(#a.layers==8 and #b.layers==9)
for i=1,#a.layers do
 local la,lb=a.layers[i],b.layers[i]
 assert(la.name==lb.name and la.isVisible==lb.isVisible and la.isEditable==lb.isEditable and la.opacity==lb.opacity and la.blendMode==lb.blendMode)
 local ca,cb=la:cel(1),lb:cel(1)
 assert(ca.position==cb.position and ca.image.width==cb.image.width and ca.image.height==cb.image.height)
 for y=0,ca.image.height-1 do for x=0,ca.image.width-1 do assert(ca.image:getPixel(x,y)==cb.image:getPixel(x,y)) end end
end
assert(#a.palettes[1]==#b.palettes[1])
for i=0,#a.palettes[1]-1 do assert(a.palettes[1]:getColor(i).rgbaPixel==b.palettes[1]:getColor(i).rgbaPixel) end
local ia=Image(a.width,a.height,ColorMode.RGB);ia:drawSprite(a,1)
local ib=Image(b.width,b.height,ColorMode.RGB);ib:drawSprite(b,1)
local changed=0
for y=0,a.height-1 do for x=0,a.width-1 do
 local pa,pb=ia:getPixel(x,y),ib:getPixel(x,y)
 assert(app.pixelColor.rgbaA(pa)==app.pixelColor.rgbaA(pb),'Alpha changed')
 if pa~=pb then assert(x>=51 and x<=66 and y>=33 and y<=37,'Outside eye region');changed=changed+1 end
end end
ib:saveAs(root..'reopened_verified.png')
local expected=Image{fromFile=root..'character_eyes_refined.png'}
for y=0,b.height-1 do for x=0,b.width-1 do assert(ib:getPixel(x,y)==expected:getPixel(x,y)) end end
assert(changed>0)
local f=assert(io.open(root..'verification.json','w'))
f:write(string.format('{"passed":true,"width":104,"height":208,"frames":1,"layers":9,"originalEightLayersUnchanged":true,"paletteUnchanged":true,"alphaUnchanged":true,"changesRestrictedToEyesAndBrows":true,"changedCompositePixels":%d,"savedProjectMatchesPNG":true}',changed));f:close()
print('VERIFY_PASS')
