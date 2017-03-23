from numpy import *
import HAPPI_detect_func as hd_func
import myfunc.fig.Fig as Fig
import myfunc.grids as grids

regiontype = "JPN"
lregion = ["S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]


a1lat = arange(-89.5,89.5+0.1, 1.0)
a1lon = arange(0.5,359.5+0.1, 1.0)


for i,region in enumerate(lregion):
    BBox = hd_func.ret_regionBBox(region)
    a2tmp = grids.mk_mask_BBox(a1lat, a1lon, BBox)
    if i==0:
        a2region = a2tmp
    else:
        a2region = a2region + a2tmp*(i+1)

sPath = "./temp.png"
a2in  = a2region
Fig.DrawMapSimple(a2in=a2in, a1lat=a1lat, a1lon=a1lon, figname=sPath, BBox=[[10,110],[50,160]])
