from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
expr    = "C20"
#lscen   = ["P15","P20"]
lscen   = ["P20"]
res     = "128x256"

ldattype = ["Sum","Num"]
dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["tc","cf","ms","ot"]
lthpr  = [0,"p99.900","p99.990"]
#lthpr  = [0]
region = "GLB"
#region = "JPN"

season = "ALL"
iy   = 0   # top
ey   = -1  # bottom
ix   = 0
ex   = -1
#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr
#----------------------
for thpr in lthpr:
    sthpr   = ret_sthpr(thpr)
    lkey    = [[scen,dattype] for scen in lscen for dattype in ldattype]
    for [scen,dattype] in lkey:
        iYear, eYear = dieYear[scen]
        da2dat  = {}
        for i, tag in enumerate(ltag):
            model= "MIROC5"
            run  = "%s-%s-001"%(expr,scen)  # only for baseDir
    
#            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")


            iYear_fut, eYear_fut = dieYear[scen]
            baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var=var)[0:2]

        
            # Figure
            figDir  = baseDir + "/fig"
            figname = figDir + "/%s.%s.inc.frac.th.%s.%s.%s.png"%(region, scen, sthpr, dattype, tag)


            iimg    = Image.open(figname)
            a2array = asarray(iimg)
            da2dat[i] = a2array[iy:ey, ix:ex]
        
        da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
        a2oarray = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3]] )
        oimg     = Image.fromarray(a2oarray)
        oPath    = figDir + "/join.%s.inc.frac.%s.th.%s.%s.png"%(region, scen, sthpr, dattype)
        oimg.save(oPath)
        print oPath
    
        
