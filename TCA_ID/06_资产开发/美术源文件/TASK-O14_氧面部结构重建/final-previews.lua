local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O14_氧面部结构重建/'
local function nearest(src,n)
 local o=Image(src.width*n,src.height*n,ColorMode.RGB)
 for y=0,o.height-1 do for x=0,o.width-1 do o:drawPixel(x,y,src:getPixel(math.floor(x/n),math.floor(y/n))) end end
 return o
end
local function crop(src,x,y,w,h)
 local o=Image(w,h,ColorMode.RGB);o:drawImage(src,Point(-x,-y));return o
end
local function sheet(w,h)
 local o=Image(w,h,ColorMode.RGB)
 for y=0,h-1 do for x=0,w-1 do o:drawPixel(x,y,app.pixelColor.rgba(226,228,229,255)) end end
 return o
end
local s=app.open(root..'character_face_refined.aseprite')
local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,1)
im:saveAs(root..'reopened_final.png')
local before=Image{fromFile=root..'backup/before.png'}
local head=crop(im,38,8,44,46)
head:saveAs(root..'head_1x.png')
for _,n in ipairs({4,8,12}) do nearest(head,n):saveAs(root..'head_'..n..'x.png') end
nearest(crop(im,48,29,24,17),16):saveAs(root..'face_16x.png')
nearest(im,4):saveAs(root..'character_face_refined_4x.png')
local pair=sheet(92,46);pair:drawImage(crop(before,38,8,44,46),Point(0,0));pair:drawImage(head,Point(48,0))
pair:saveAs(root..'before_after_heads_1x.png');nearest(pair,8):saveAs(root..'before_after_heads_8x.png')
local body=sheet(216,208);body:drawImage(before,Point(0,0));body:drawImage(im,Point(112,0))
body:saveAs(root..'before_after_full_1x.png');nearest(body,4):saveAs(root..'before_after_full_4x.png')
print('FINAL_PREVIEWS_OK')
