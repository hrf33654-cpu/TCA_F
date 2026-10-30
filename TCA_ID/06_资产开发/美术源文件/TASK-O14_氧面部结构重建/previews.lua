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
local heads=sheet(136,46);local full=sheet(328,208);local eyes=sheet(76,14)
for i,id in ipairs({'A','B','C'}) do
 local im=Image{fromFile=root..'variants/face_'..id..'.png'}
 heads:drawImage(crop(im,38,8,44,46),Point((i-1)*46,0))
 full:drawImage(im,Point((i-1)*112,0))
 eyes:drawImage(crop(im,48,29,24,14),Point((i-1)*26,0))
 nearest(crop(im,38,8,44,46),8):saveAs(root..'variants/head_'..id..'_8x.png')
end
heads:saveAs(root..'ABC_heads_1x.png');nearest(heads,8):saveAs(root..'ABC_heads_8x.png')
full:saveAs(root..'ABC_full_1x.png');nearest(full,4):saveAs(root..'ABC_full_4x.png')
nearest(eyes,12):saveAs(root..'ABC_eyes_12x.png')
print('ABC_PREVIEWS_OK')
