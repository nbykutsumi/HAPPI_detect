from numpy import *
import sys, os
from PIL import Image
from PIL import ImageFont, ImageDraw
import HAPPI_detect_func as hp_func

lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]


#lkey   = [[1,"Ptot"]]
#lkey   = [[1,"Ptot"],[1,"Freq"],[1,"Pint"]]
lkey   = [[1,"rat.Ptot"],[1,"rat.Freq"],[1,"rat.Pint"]]
#lkey   = [["p99.900","rat.Freq"],["p99.990","rat.Freq"]]
#lkey   = [["p99.990","rat.Freq"]]
#lkey   = [["p99.900","Freq"],["p99.990","Freq"]]
#lkey   = [[1,"Fraction.Ptot"],["p99.900","Fraction.Ptot"],["p99.990","Fraction.Ptot"]]
#lkey   = [["p99.900","Fraction.Freq"],["p99.990","Fraction.Freq"]]

figDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"

def ret_posbox(num, wbox, hbox):
    xleft = 1
    ytop  = 70


    y = ytop + int(hbox*0.3)
    if num in [1,2]:
        pos = (xleft+wbox*(num-1), y)

    y = ytop + int(hbox*0.3) + hbox
    if num in [3,4]:
        pos = (xleft+wbox*(num-3), y)

    y = ytop + int(hbox*0.3) + hbox*2
    if num in [5,6]:
        pos = (xleft+wbox*(num-5), y)

    
    y     = ytop
    if num in range(7,16+1):
        x = xleft + (num-5)*wbox
        pos = (x, y)



    y = ytop + int(hbox*2.6)
    if num in range(17,26+1):
        x = xleft + (num-15)*wbox
        pos = (x, y)

    y = ytop 
    if num==0:
        #x = xleft + int(12*wbox) + 30
        x = xleft + int(12*wbox) + 5
        pos = (x, y)
        print "*"*50
        print "GLB pos=",pos
        print "*"*50

    return pos


#----------------------------------
for [thpr,var] in lkey:
    # Open sample boxplot
    region  = lregion[0]
    boxPath = figDir + "/boxplot.%s.th.%s.%s.png"%(var,thpr,region)
    imbox   = Image.open(boxPath)
    sizebox = array(imbox.size)
    wbox, hbox = sizebox
    
    
    # Background
    bg    = Image.new("RGBA",size=(int(wbox*13*1.12),int(hbox*4*0.98)))
    
    dregion = hp_func.dict_IPCC_codeKey()
    for region in lregion:
        num = dregion[region][0]
    
        posbox = ret_posbox(num, wbox, hbox)
        print num,posbox, bg.size
        # Open boxplot
        #boxPath = figDir + "/boxplot.Freq.th.p99.990.WSA.png"
        boxPath = figDir + "/boxplot.%s.th.%s.%s.png"%(var,thpr,region)
        imbox = Image.open(boxPath)
    
        # resize GLB (0)
        if num==0:
            size_org = imbox.size
            size_new = tuple((array(size_org)*1.5).astype(int32))
            imbox    = imbox.resize(size_new, resample=Image.BICUBIC)
    
        # Paste boxplot
        pos     = ret_posbox(num, wbox, hbox)
        print "region=",region,num
        if region=="GLB": print region, num,pos
        bg.paste(imbox, posbox)
    
    
    # Add title
    stitle = "%s th=%s"%(var, thpr)
    font   = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",size=16)
    draw   = ImageDraw.Draw(bg)
    W, H   = bg.size
    w, h   = draw.textsize(stitle,font=font)
    #pos    = ((W-w)/2, 30)
    pos    = ((W-w)/2, 30)
    draw.text(pos,stitle,fill="black", font=font)
    
    
    
    
    outPath = figDir + "/join.boxplot.forMap.%s.th.%s.png"%(var,thpr)
    bg.save(outPath)
    print outPath
    
    
    
