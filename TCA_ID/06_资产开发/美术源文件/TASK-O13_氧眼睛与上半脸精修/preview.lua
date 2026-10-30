local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O13_氧眼睛与上半脸精修/'
local s=app.open(root..'character_eyes_refined.aseprite')
local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,1)
im:saveAs(root..'character_eyes_refined.png')
local before=Image{fromFile=root..'backup/character_before.png'}
local function crop(src,x,y,w,h)
 local o=Image(w,h,ColorMode.RGB);o:drawImage(src,Point(-x,-y));return o
end
local function nearest(src,n)
 local o=Image(src.width*n,src.height*n,ColorMode.RGB)
 for y=0,o.height-1 do for x=0,o.width-1 do o:drawPixel(x,y,src:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return o
end
for _,n in ipairs({4,8,12}) do nearest(crop(im,40,8,40,46),n):saveAs(root..'head_'..n..'x.png') end
nearest(im,4):saveAs(root..'character_eyes_refined_4x.png')
local comp=Image(84,46,ColorMode.RGB)
comp:drawImage(crop(before,40,8,40,46),Point(0,0));comp:drawImage(crop(im,40,8,40,46),Point(44,0))
nearest(comp,8):saveAs(root..'eyes_before_after_8x.png')
print('PREVIEW_OK')
