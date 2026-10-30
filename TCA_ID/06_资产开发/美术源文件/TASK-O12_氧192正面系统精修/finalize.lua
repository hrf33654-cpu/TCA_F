local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O12_氧192正面系统精修/'
local s=app.open(root..'character_refined.aseprite')
assert(s.width==104 and s.height==208 and #s.frames==1 and #s.layers==8)
local extra={'B3AAA0','BCAA91','E6DCCD','2F84B9','61C2DF','DCF7F5','F1ECE3','C4B5A5','D7C8B8','B9A99C','93877E'}
local old=s.palettes[1]
if #old==35 then
 local pal=Palette(#old+#extra)
 for i=0,#old-1 do pal:setColor(i,old:getColor(i)) end
 for i,v in ipairs(extra) do pal:setColor(#old+i-1,Color{r=tonumber(v:sub(1,2),16),g=tonumber(v:sub(3,4),16),b=tonumber(v:sub(5,6),16),a=255}) end
 s:setPalette(pal)
else assert(#old==46,'Unexpected palette size') end
s.data='TASK-O12: native 104x208 front-view refinement through Aseprite MCP. Original three layers retained. Five named editable correction layers. No resampling of the working sprite, no new views. See report.md.'
app.layer=s.layers[#s.layers]
s:saveAs(root..'character_refined.aseprite')
local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,1)
im:saveAs(root..'character_refined.png')
im:saveAs(root..'verification/cli-reopened-final.png')
local function scale(image,n) local o=Image(image);o:resize(image.width*n,image.height*n);return o end
scale(im,4):saveAs(root..'character_refined_4x.png')
scale(im,2):saveAs(root..'verification/character_refined_2x.png')
local before=Image{fromFile=root..'backup/character_before.png'}
local pc=app.pixelColor
local function checker(w,h)
 local out=Image(w,h,ColorMode.RGB)
 for y=0,h-1 do for x=0,w-1 do local v=(math.floor(x/8)+math.floor(y/8))%2==0 and 226 or 240;out:drawPixel(x,y,pc.rgba(v,v+2,v+3,255)) end end
 return out
end
local single=checker(104,208);single:drawImage(im,Point(0,0))
scale(single,4):saveAs(root..'character_refined_4x_checker.png')
local comp=checker(216,208);comp:drawImage(before,Point(0,0));comp:drawImage(im,Point(112,0))
scale(comp,4):saveAs(root..'character_before_after.png')
local regions={{'head',40,8,40,46},{'chest',32,48,55,49},{'white-skirt',8,91,54,109},{'black-cloth',49,89,47,111}}
for _,r in ipairs(regions) do
 local out=Image(r[4],r[5],ColorMode.RGB);out:drawImage(im,Point(-r[2],-r[3]))
 scale(out,8):saveAs(root..'verification/after-'..r[1]..'-8x.png')
end
local f=assert(io.open(root..'verification/final-engine-state.json','w'))
f:write(string.format('{"width":%d,"height":%d,"frames":%d,"frameDuration":%f,"layers":%d,"paletteEntries":%d,"engine":"Aseprite 1.3.18.6-dev"}',s.width,s.height,#s.frames,s.frames[1].duration,#s.layers,#s.palettes[1]))
f:close()
print('FINALIZE_PASS')
