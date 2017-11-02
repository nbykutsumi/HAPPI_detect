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
#lscen   = ["ALL","P15","P20"]
lscen   = ["P15","P20"]
res     = "128x256"

dieYear = {"JRA55":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["plain","tc","cf","ms","ot"]
#ltag  = ["tc","cf","ms","ot"]
season = "ALL"

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
thpr    = 1
llscen  = [["ALL","P15"],["ALL","P20"],["P15","P20"]]
for lscen in llscen:
    scen0,scen1 = lscen
    da2dat  = {}
    i  = -1
    for var in ["ptot","dNI","NdI"]:
        for tag in ltag:
            i = i+1
        
            # Figure
            figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"

            if var == "ptot":
                figPath = os.path.join(figDir,"map.dif.%s.%s.%s-%s.th.%s.%s.png"%(tag,var,scen1,scen0,thpr,season))

            elif var in ["dNI","NdI"]:
                figPath = os.path.join(figDir,"map.decomp.%s.%s.%s-%s.th.%s.%s.png"%(tag,var,scen1,scen0,thpr,season))
                #cbarPath= os.path.join(figDir,"cbar.map.dif.%s.%s.th.%s.png"%(tag,var,thpr))
        
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            #da2dat[i] = a2array
            da2dat[i] = a2array[:,ix:ex]
        
    da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255

    line0 = concatenate([da2dat[0], da2dat[1],da2dat[2],da2dat[3],da2dat[4]] ,axis=0)
    line1 = concatenate([da2dat[5],da2dat[6],da2dat[7],da2dat[8],da2dat[9]] ,axis=0)
    line2 = concatenate([da2dat[10],da2dat[11],da2dat[12],da2dat[13],da2dat[14]] ,axis=0)


    a2oarray = concatenate([line0, line1, line2],axis=1)
    oimg     = Image.fromarray(a2oarray)
    oPath    = figDir + "/join.decomp.map.%s-%s.th.%s.png"%(scen1, scen0, thpr)
    oimg.save(oPath)
    print oPath
    
    
