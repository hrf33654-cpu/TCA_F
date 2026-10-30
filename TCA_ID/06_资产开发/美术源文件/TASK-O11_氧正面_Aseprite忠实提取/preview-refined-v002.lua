local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O11_氧正面_Aseprite忠实提取/'
local before=Image{fromFile=root..'exports/oxygen-front-h192.png'}
local after=Image{fromFile=root..'exports/oxygen-front-h192-refined-v002-final.png'}
local rgba=app.pixelColor.rgba
local bg=rgba(222,227,232,255)
local function background(w,h)
 local image=Image(w,h,ColorMode.RGB)
 image:clear(bg)
 return image
end
local full=background(after.width,after.height);full:drawImage(after,Point(0,0));full:resize(after.width*4,after.height*4)
full:saveAs(root..'exports/oxygen-front-h192-refined-v002-preview4x.png')
local compare=background(before.width*2+8,before.height)
compare:drawImage(before,Point(0,0));compare:drawImage(after,Point(before.width+8,0))
compare:resize(compare.width*4,compare.height*4)
compare:saveAs(root..'exports/oxygen-front-h192-v001-v002-comparison.png')
local heads=background(72,42)
local crop1=Image(32,40,ColorMode.RGB);crop1:drawImage(before,Point(-40,-10))
local crop2=Image(32,40,ColorMode.RGB);crop2:drawImage(after,Point(-40,-10))
heads:drawImage(crop1,Point(0,1));heads:drawImage(crop2,Point(40,1));heads:resize(720,420)
heads:saveAs(root..'verification/face-before-after-v002.png')
-- Reload the saved source and compare its composite to the MCP export independently.
local s=app.open(root..'oxygen-front-h192-refined-v002.aseprite')
local composite=Image(s.width,s.height,ColorMode.RGB);composite:drawSprite(s,1)
for y=0,s.height-1 do for x=0,s.width-1 do assert(composite:getPixel(x,y)==after:getPixel(x,y),'Saved source mismatch') end end
print('SAVED_SOURCE_COMPOSITE_PASS')
