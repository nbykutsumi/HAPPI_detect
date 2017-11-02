from numpy import *
import os, sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import HAPPI_detect_func as hd_func

#
model   = "MIROC5"
expr    = "C20"
res     = "128x256"

lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]


#lregion = ["EAS"]
dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

season = "ALL"

#- Switch  ------------
Total    = False
ExFreq   = False
Fraction = True
ChangeRat= False


# Directory
thpr = 0
iYear_fut, eYear_fut = dieYear["P20"]
run  = "C20-P15-001"
#baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=0, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]

baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"


#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr


def join_block(da2dat):
    a2margin = da2dat[0][:18]*0+255
    a2blank  = ones(da2dat[0].shape)*0 +255
    da2dat[26]= a2blank
    da2dat[27]= a2blank

    line0   = concatenate([a2blank for i in range(0,9)],axis=1)[:40]

    for i in range(27):
        da2dat[i] = concatenate([a2margin,da2dat[i]],axis=0)

    line1 = concatenate([da2dat[i] for i in range(0,9)],axis=1)
    line2 = concatenate([da2dat[i] for i in range(9,18)],axis=1)
    line3 = concatenate([da2dat[i] for i in range(18,27)],axis=1)
    return concatenate([line0,line1,line2,line3]).astype(uint8)


def add_title(oimg, stitle):
    font      = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf",size=16)
    draw      = ImageDraw.Draw(oimg)
    W, H      = oimg.size
    w, h      = draw.textsize(stitle,font=font)
    pos       = ((W-w)/2, 30)
    draw.text(pos,stitle,fill="black", font=font)
    return oimg

#**********************
# Ptot, Freq, Pint for Total precipitation
#----------------------
#"""
thpr = 0
lvartype = ["Ptot","Freq","Pint"]
for vartype in lvartype:
    if Total == False: continue
    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/boxplot.%s.th.%s.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)

    # Add text
    stitle    = "%s th=%s"%(vartype, thpr)
    oimg      = add_title(oimg, stitle)

    oPath     = figDir + "/join.boxplot.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath

#"""

#**********************
# Freq for Extreme precipitation
#----------------------
#"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    if ExFreq == False: continue

    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/boxplot.%s.th.%s.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array
    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)

    # Add text
    stitle    = "%s th=%s"%(vartype, thpr)
    oimg      = add_title(oimg, stitle)

    oPath     = figDir + "/join.boxplot.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath

#"""

#**********************
# Proportion for Extreme precipitation
#----------------------
#"""
#vartype = "Freq"
#lthpr  = ["p99.900","p99.990"]

vartype = "Ptot"
lthpr  = [1,"p99.900","p99.990"]

for thpr in lthpr:
    if Fraction == False: continue

    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/boxplot.Fraction.%s.th.%s.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)

    # Add text
    stitle    = "Proportions %s th=%s"%(vartype, thpr)
    oimg      = add_title(oimg, stitle)

    oPath     = figDir + "/join.boxplot.Fraction.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath


#"""

