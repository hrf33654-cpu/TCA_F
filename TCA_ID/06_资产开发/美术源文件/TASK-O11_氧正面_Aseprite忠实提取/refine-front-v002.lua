-- Authored palette cleanup in Aseprite; silhouette and alpha stay unchanged.
local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O11_氧正面_Aseprite忠实提取/'
local source=Image{fromFile=root..'exports/oxygen-front-h192.png'}
local pc=app.pixelColor
local hex={
 '14151B','20222A','2D303A','3E424E','565E70', -- hair / cool outlines
 '19191B','252527','333335','444447','59595D', -- black fabric ramp
 'FFFFFF','F1F2F6','DDE0E9','C2C6D2','A1A8BA','7D879B', -- white fabric
 'D4EDE4','B4D9CD','8FB9AD','6B968D','496E6B', -- mint fabric
 'AEDCF1','7CB6DD','4C8AC1','355D95','283C66', -- blue accents
 'F8DED0','EBC6B8','D6A59C','BC8886','965E6C', -- skin and lips
 '52404A','726078','4C6479' -- facial accents
}
local colors={}
for _,s in ipairs(hex) do colors[#colors+1]={tonumber(s:sub(1,2),16),tonumber(s:sub(3,4),16),tonumber(s:sub(5,6),16)} end
local cache={}
local function quant(c)
 if pc.rgbaA(c)==0 then return 0 end
 if cache[c] then return cache[c] end
 local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
 local best,dist
 for _,v in ipairs(colors) do
  local mean=(r+v[1])/2
  local d=(2+mean/256)*(r-v[1])^2+4*(g-v[2])^2+(2+(255-mean)/256)*(b-v[3])^2
  if not dist or d<dist then best=v;dist=d end
 end
 local result=pc.rgba(best[1],best[2],best[3],255)
 cache[c]=result;return result
end
local flat=Image(source.width,source.height,ColorMode.RGB)
for y=0,source.height-1 do for x=0,source.width-1 do flat:drawPixel(x,y,quant(source:getPixel(x,y))) end end
local cleaned=Image(flat)
local merges=0
-- Merge only low-contrast single-pixel islands inside cloth, keeping contours and head untouched.
for y=52,source.height-2 do for x=1,source.width-2 do
 local c=flat:getPixel(x,y)
 if pc.rgbaA(c)>0 then
  local votes,opaque={},true
  for dy=-1,1 do for dx=-1,1 do if dx~=0 or dy~=0 then
   local p=flat:getPixel(x+dx,y+dy)
   if pc.rgbaA(p)==0 then opaque=false end
   votes[p]=(votes[p] or 0)+1
  end end end
  if opaque and (votes[c] or 0)<=1 then
   for v,n in pairs(votes) do
    local d=(pc.rgbaR(c)-pc.rgbaR(v))^2+(pc.rgbaG(c)-pc.rgbaG(v))^2+(pc.rgbaB(c)-pc.rgbaB(v))^2
    if n>=5 and d<2400 then cleaned:drawPixel(x,y,v);merges=merges+1;break end
   end
  end
 end
end end
local s=Sprite(source.width,source.height,ColorMode.RGB)
local base=s.layers[1];base.name='01_整理色阶_34色'
s:newCel(base,1,cleaned,Point(0,0))
local ref=s:newLayer();ref.name='参考_v001_隐藏';s:newCel(ref,1,source,Point(0,0));ref.isVisible=false;ref.isEditable=false
local pal=Palette(#colors+1);pal:setColor(0,Color{r=0,g=0,b=0,a=0})
for i,v in ipairs(colors) do pal:setColor(i,Color{r=v[1],g=v[2],b=v[3],a=255}) end
s:setPalette(pal)
app.layer=base
s.data='v002: 34 authored colors; native 192px; facial pixel accents on separate layer. Original silhouette and asymmetry preserved.'
s:saveAs(root..'oxygen-front-h192-refined-v002.aseprite')
local f=assert(io.open(root..'verification/refine-v002.json','w'))
f:write('{"paletteColors":'..#colors..',"lowContrastClothPixelsMerged":'..merges..',"source":"exports/oxygen-front-h192.png","alphaChanged":false}')
f:close()
print('REFINE_BASE_PASS colors='..#colors..' merged='..merges)
