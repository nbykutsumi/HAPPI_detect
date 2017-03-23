from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
#model   = "__"
#run     = "__"
#res     = "145x288"
#lscen   = ["JRA55"]

model   = "MIROC5"
expr    = "C20"
run     = "C20-ALL-001"   # only for baseDir, no need to change
lscen   = ["ALL","P15","P20"]
res     = "128x256"

dieYear = {"JRA55":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["plain"] + ["tc","cf","ms","ot"]
thpr  = 0
season = "ALL"
#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr
#----------------------
sthpr   = ret_sthpr(thpr)
da2dat  = {}
for scen in lscen:
    iYear, eYear = dieYear[scen]
    for i, tag in enumerate(ltag):
        baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
    
        # Figure
        figDir  = baseDir + "/fig"
        figname = figDir + "/%s.th.%s.%s.%s.png"%(scen,sthpr,tag,"Ptot")
    
        iimg    = Image.open(figname)
        a2array = asarray(iimg)
        da2dat[i] = a2array
    
    da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
    line0 = hstack( [da2dat[0], da2dat[-9999]] )
    line1 = hstack( [da2dat[1], da2dat[2]] )
    line2 = hstack( [da2dat[3], da2dat[4]] )

    a2oarray = vstack([line0, line1, line2])
    oimg     = Image.fromarray(a2oarray)
    oPath    = figDir + "/join.%s.%s.%s.png"%(scen, sthpr, "Ptot")
    oimg.save(oPath)
    print oPath

    
