local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O12_氧192正面系统精修/'
local s=app.open(root..'backup/character_original.aseprite')
local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,1)
local regions={{'head',40,8,40,46},{'chest',32,48,55,49},{'white-skirt',8,91,54,109},{'black-cloth',49,89,47,111}}
for _,r in ipairs(regions) do
 local out=Image(r[4],r[5],ColorMode.RGB);out:drawImage(im,Point(-r[2],-r[3]))
 out:resize(r[4]*8,r[5]*8);out:saveAs(root..'verification/before-'..r[1]..'-8x.png')
end
local f=io.open(root..'verification/original-palette.json','w')
local cs={};for i=0,#s.palettes[1]-1 do local c=s.palettes[1]:getColor(i);cs[#cs+1]=string.format('"%02X%02X%02X%02X"',c.red,c.green,c.blue,c.alpha) end
f:write('['..table.concat(cs,',')..']');f:close()
