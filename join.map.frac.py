from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
#model   = "__"
#run     = "__"
#res     = "145x288"
#lscen   = ["JRA55"]

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
run     = "C20-ALL-001"   # only for baseDir, no need to change
#lscen   = ["ALL","P15","P20"]
lscen   = ["ALL"]
res     = "128x256"

dieYear = {"JRA55":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["tc","cf","ms","ot"]
season = "ALL"

lkey  = [["p99.990","frac.freq"]]
#lkey  = [[1,"frac.ptot"],["p99.990","frac.ptot"],["p99.990","frac.freq"]]
ix    = 80
ex    = -80
#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr
#----------------------

for key in lkey:
    thpr, var = key    
    da2dat  = {}
    lscen  = ["ALL","P15","P20"]
    i  = -1
    for scen in lscen:
        for tag in ltag:
            i = i+1
        
            # Figure
            figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
            figPath = figDir + "/map.%s.%s.%s.%s.%s.th.%s.%s.png"%(var,prj,model,scen,tag, thpr, season)
            #cbarPath= os.path.join(figDir,"cbar.map.dif.%s.%s.th.%s.png"%(tag,var,thpr))
        
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            #da2dat[i] = a2array
            da2dat[i] = a2array[:,ix:ex]
        
    da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
    line0 = concatenate([da2dat[0], da2dat[1],da2dat[2],da2dat[3]] ,axis=0)
    line1 = concatenate([da2dat[4], da2dat[5],da2dat[6],da2dat[7]] ,axis=0)
    line2 = concatenate([da2dat[8], da2dat[9],da2dat[10],da2dat[11]] ,axis=0)

    a2oarray = concatenate([line0, line1, line2],axis=1)
    oimg     = Image.fromarray(a2oarray)
    oPath    = figDir + "/join.frac.map.%s.th.%s.png"%(var, thpr)
    oimg.save(oPath)
    print oPath
    
    
