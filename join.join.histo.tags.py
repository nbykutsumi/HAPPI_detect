from numpy import *
import os, sys
import Image
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

ltag  = ["tc","cf","ms","ot"]
season = "ALL"
iy   = 16   # top
ey   = -1  # bottom
ix   = 0
ex   = -1

# Directory
thpr = 0
iYear_fut, eYear_fut = dieYear["P20"]
run  = "C20-P15-001"
baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=0, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]
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
    for i in range(28):
        da2dat[i] = concatenate([da2dat[i],a2margin],axis=0)

    line1 = concatenate([da2dat[i] for i in range(0,7)],axis=1)
    line2 = concatenate([da2dat[i] for i in range(7,14)],axis=1)
    line3 = concatenate([da2dat[i] for i in range(14,21)],axis=1)
    line4 = concatenate([da2dat[i] for i in range(21,28)],axis=1)
    return concatenate([line1,line2,line3,line4]).astype(uint8)
#**********************
# Ptot, Freq, Pint for Total precipitation
#----------------------
"""
thpr = 0
lvartype = ["Ptot","Freq","Pint"]
for vartype in lvartype:
    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath

"""

#**********************
# Freq for Extreme precipitation
#----------------------
"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array
    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath

"""

#**********************
# Proportion for Extreme precipitation
#----------------------
#"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/hist.Fraction.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.Fraction.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath


#"""

