from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
lregion    = ["GLB","JPN","S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]
#lregion    = ["GLB"]

expr    = "C20"
res     = "128x256"

lthpr  = [0,"p99.900","p99.990"]
#lthpr  = [0]
#region = "GLB"
region = "JPN"

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
for ithpr, thpr in enumerate(lthpr):
    sthpr   = ret_sthpr(thpr)
    da2dat  = {}
    for iregion, region in enumerate(lregion):
        if thpr == 0:
            vartype="Ptot"
        else:
            vartype="Freq"

        # path
        model= "MIROC5"
        iYear_fut, eYear_fut = dieYear["P20"]
        run  = "C20-P15-001"
        baseDir, sDir, sumPath = hd_func.path_dpr(model=model, run=run, res=res, sthpr=sthpr, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")
        
        # Figure
        figDir  = baseDir + "/fig"

        figname = figDir  + "/bar.%s.th.%s.%s.png"%(vartype, thpr, region)
    
        iimg    = Image.open(figname)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array[iy:ey, ix:ex]
        
    da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
    a2oarray0 = hstack( [da2dat[0], da2dat[1], da2dat[-9999] ] )
    a2oarray1 = hstack( [da2dat[2], da2dat[3], da2dat[4] ] )
    a2oarray2 = hstack( [da2dat[5], da2dat[6], da2dat[7] ] )
    a2oarray3 = hstack( [da2dat[8], da2dat[9], da2dat[10] ] )

    a2oarray  = vstack( [a2oarray0, a2oarray1, a2oarray2, a2oarray3] )


    oimg     = Image.fromarray(a2oarray)
    oPath    = figDir + "/join.bar.th.%s.png"%(sthpr)
    
    oimg.save(oPath)
    print oPath
        
            
