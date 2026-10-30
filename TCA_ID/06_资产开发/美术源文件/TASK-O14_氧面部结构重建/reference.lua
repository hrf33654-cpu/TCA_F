local root='E:/projects/TCA_ID/06_资产开发/美术源文件/TASK-O14_氧面部结构重建/'
local src=Image{fromFile=root..'reference/turnaround.png'}
local o=Image(120,140,ColorMode.RGB);o:drawImage(src,Point(-270,-85))
o:resize(480,560);o:saveAs(root..'reference/front-head-4x.png')
local b=Image{fromFile=root..'backup/before.png'}
local crop=Image(28,32,ColorMode.RGB);crop:drawImage(b,Point(-46,-22));crop:resize(336,384);crop:saveAs(root..'reference/before-face-12x.png')
