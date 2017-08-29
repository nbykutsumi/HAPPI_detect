from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
expr    = "C20"
lscen   = ["P15","P20"]
#lscen   = ["P20"]
res     = "128x256"

#lthpr  = [0,"p99.900","p99.990"]
lthpr  = [0]
region = "GLB"
#region = "JPN"

dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["tc","cf","ms","ot"]
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
    for scen in lscen:
        iYear, eYear = dieYear[scen]
        da2dat  = {}
        for tag in ["plain"]+ltag:
            for ivar, var in enumerate(["dP","dNI","NdI"]):
                model= "MIROC5"
                run  = "%s-%s-001"%(expr,scen)  # only for baseDir
        
                baseDir, sDir, sumPath = hd_func.path_dpr(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, var=var)
            
                # Figure
                figDir  = baseDir + "/fig"
                figname= figDir + "/%s.%s.th.%s.%s.%s.png"%(region, scen,sthpr,tag,var)
    
    
                iimg    = Image.open(figname)
                a2array = asarray(iimg)
                da2dat[ivar] = a2array[iy:ey, ix:ex]
            
            da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
            a2oarray = vstack( [da2dat[0], da2dat[1], da2dat[2] ] )
            oimg     = Image.fromarray(a2oarray)
            oPath    = figDir + "/join.%s.%s.th.%s.%s.png"%(region, scen,sthpr,tag)
    
            oimg.save(oPath)
            print oPath
        
            
