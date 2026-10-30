-- Aseprite-native extraction. RGB values of retained source pixels are never changed.
local root = 'E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O11_氧正面_Aseprite忠实提取/'
local source = root .. 'references/oxygen-user-reference.png'
local rgba = app.pixelColor.rgba
local pc = app.pixelColor
local src = Image{fromFile=source}
assert(src.width == 2752 and src.height == 1536, 'Unexpected reference dimensions')
local ox,oy,w,h = 150,80,680,1360
local crop = Image(w,h,ColorMode.RGB)
crop:drawImage(src,Point(-ox,-oy))
local bg,removed,queue = {},{},{}
local function id(x,y) return y*w+x+1 end
local function isbg(c)
  local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  return r>=140 and r<=210 and math.max(r,g,b)-math.min(r,g,b)<=5
end
for y=0,h-1 do for x=0,w-1 do
  if isbg(crop:getPixel(x,y)) then bg[id(x,y)]=true end
end end
local function seed(x,y)
  local i=id(x,y)
  if bg[i] and not removed[i] then removed[i]=true;queue[#queue+1]=i end
end
for x=0,w-1 do seed(x,0);seed(x,h-1) end
for y=0,h-1 do seed(0,y);seed(w-1,y) end
-- Background pockets between the arms and dress, reviewed against the reference.
seed(234,509)
seed(534,753)
local qi=1
while qi<=#queue do
  local p=queue[qi]-1;qi=qi+1
  local x,y=p%w,math.floor(p/w)
  if x>0 then seed(x-1,y) end
  if x<w-1 then seed(x+1,y) end
  if y>0 then seed(x,y-1) end
  if y<h-1 then seed(x,y+1) end
end
queue={};bg=nil
-- Retain the main connected figure only; detached heading/label fragments are excluded.
local seen,best={},{}
for y=0,h-1 do for x=0,w-1 do
  local i=id(x,y)
  if not removed[i] and not seen[i] then
    local component={i};seen[i]=true;local k=1
    while k<=#component do
      local p=component[k]-1;k=k+1
      local xx,yy=p%w,math.floor(p/w)
      for dy=-1,1 do for dx=-1,1 do
        local nx,ny=xx+dx,yy+dy
        if nx>=0 and nx<w and ny>=0 and ny<h then
          local ni=id(nx,ny)
          if not removed[ni] and not seen[ni] then seen[ni]=true;component[#component+1]=ni end
        end
      end end
    end
    if #component>#best then best=component end
  end
end end
local xmin,ymin,xmax,ymax=w,h,0,0
local keep={}
for _,i in ipairs(best) do
  keep[i]=true;local p=i-1;local x,y=p%w,math.floor(p/w)
  xmin=math.min(xmin,x);ymin=math.min(ymin,y);xmax=math.max(xmax,x);ymax=math.max(ymax,y)
end
local margin=24
local fw,fh=xmax-xmin+1+margin*2,ymax-ymin+1+margin*2
local clean=Image(fw,fh,ColorMode.RGB)
local ref=Image(fw,fh,ColorMode.RGB)
local sourceX,sourceY=ox+xmin-margin,oy+ymin-margin
ref:drawImage(src,Point(-sourceX,-sourceY))
local count=0
for y=ymin,ymax do for x=xmin,xmax do
  if keep[id(x,y)] then
    local pixel=crop:getPixel(x,y)
    clean:drawPixel(x-xmin+margin,y-ymin+margin,pixel)
    assert(pixel==src:getPixel(ox+x,oy+y))
    count=count+1
  end
end end
clean:saveAs(root .. 'exports/oxygen-front-original-resolution.png')
ref:saveAs(root .. 'verification/reference-aligned-crop.png')
local sprite=Sprite(fw,fh,ColorMode.RGB)
local foreground=sprite.layers[1];foreground.name='正面人物_保留原图RGB'
sprite:newCel(foreground,1,clean,Point(0,0))
local original=sprite:newLayer()
original.name='参考原图_同坐标_隐藏'
sprite:newCel(original,1,ref,Point(0,0))
original.isVisible=false;original.isEditable=false
app.layer=foreground
sprite.data='Source-faithful front extraction; original RGB retained. Background alpha mask only. Not a redesigned or regenerated character.'
sprite:saveAs(root .. 'oxygen-front-faithful-v001.aseprite')
local scaled=Image(clean)
local bh=ymax-ymin+1
local factor=192/bh
-- Pixel coordinates sampled explicitly with nearest-neighbour; native file stays unchanged.
local sw=math.floor((xmax-xmin+1)*factor+0.5)
local small=Image(sw+16,208,ColorMode.RGB)
for y=0,191 do for x=0,sw-1 do
  local sx=margin+math.min(xmax-xmin,math.floor((x+0.5)/factor))
  local sy=margin+math.min(bh-1,math.floor((y+0.5)/factor))
  small:drawPixel(x+8,y+8,clean:getPixel(sx,sy))
end end
small:saveAs(root .. 'exports/oxygen-front-h192.png')
local preview=Image(small);preview:resize(small.width*4,small.height*4)
preview:saveAs(root .. 'exports/oxygen-front-h192-preview4x.png')
local checker=Image(small.width,small.height,ColorMode.RGB)
for y=0,checker.height-1 do for x=0,checker.width-1 do
  local even=(math.floor(x/8)+math.floor(y/8))%2==0
  checker:drawPixel(x,y,even and rgba(226,230,233,255) or rgba(245,247,248,255))
end end
checker:drawImage(small,Point(0,0))
checker:resize(small.width*4,small.height*4)
checker:saveAs(root .. 'exports/oxygen-front-h192-preview4x-checker.png')
local s2=Sprite(small.width,small.height,ColorMode.RGB)
s2.layers[1].name='正面_原图最近邻192像素'
s2:newCel(s2.layers[1],1,small,Point(0,0))
s2:saveAs(root .. 'oxygen-front-h192-v001.aseprite')
local f=assert(io.open(root .. 'verification/extraction.json','w'))
f:write(string.format('{"sourceWidth":2752,"sourceHeight":1536,"cropOrigin":[%d,%d],"canvas":[%d,%d],"subjectBounds":[24,24,%d,%d],"retainedPixels":%d,"rgbChangedPixels":0,"sampling":"none for native; nearest for h192","nativeMargin":24}',sourceX,sourceY,fw,fh,xmax-xmin+1,bh,count))
f:close()
print('FRONT_EXTRACTION_PASS '..fw..'x'..fh..' retained '..count..' pixels')
