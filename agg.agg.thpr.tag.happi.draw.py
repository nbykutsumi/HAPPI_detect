import matplotlib
matplotlib.use("Agg")
from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.fig  as fig
import myfunc.IO.HAPPI as HAPPI
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
import f_draw_mapglobal
# Config --------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#----------------------------------------------------
lvartype = ["Ptot"]
#lvartype = ["Num"]
lthpr = [1]
#lthpr = [0.0]
#lthpr = ["p99.990"]
#lthpr = ["p99.900","p99.990"]


prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
#lscen   = ["ALL","P15","P20"]
#lscen   = ["P15","P20"]
#lscen   = ["P20"]
lscen   = ["ALL"]
lens    = range(1,50+1)
nens    = len(lens)
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

ltag  = ["tc","cf","ms","ot"]
#ltag   = []
ltag_ws  = [tag for tag in ltag if tag !="ot"]
dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

#season = "ALL"
season = "ALL"
#season = 1

ddtype = {"sum":"float32", "num":"int32"}
hp    = HAPPI.Happi()
BBox  = [[-80,0.0],[80,360]]
#BBox  = [[-80,0.0],[80,179]]
#BBox  = [[20,120],[48,150]]
miss  = -9999.
#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr

def ret_bnd(vartype, thpr):
    if vartype=="Ptot":
        bnd  = array([100,400,700,1000,1300,1600,1900,2200,2500,2800])
        #bnd  = array([100,600,1100,1600,2100,2600,2])

    elif (vartype=="Num")&(thpr=="p99.900"):
        bnd  = arange(2,18+1, 2)
    elif (vartype=="Num")&(thpr=="p99.990"):
        bnd  = arange(0.2, 1.8+0.01, 0.2)

    return bnd.tolist()
#----------------------
lKey = [[scen, thpr, vartype] for scen in lscen for thpr in lthpr for vartype in lvartype]

for (scen, thpr, vartype) in lKey:
    iYear, eYear = dieYear[scen]
    nYear = eYear - iYear +1

    hp(model=model, expr=expr, scen="P15", ens=1)
    Lat   = hp.Lat
    Lon   = hp.Lon

    sthpr= ret_sthpr(thpr)
    for tag in ltag + ["plain"]:
        a3sum = zeros([len(lens),ny,nx],float32)
        a3num = zeros([len(lens),ny,nx],float32)
        for iens, ens in enumerate(lens):
            run = "%s-%s-%03d"%(expr, scen, ens)

            #- Load ---
            """model, expr, scen, ens, sthpr, tag, Year, Mon"""
   

            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
    
            baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")

            if vartype == "Ptot": 
                a3sum[iens] = fromfile(sumPath, float32).reshape(ny,nx)
            elif vartype == "Num":
                a3num[iens] = fromfile(numPath, int32).reshape(ny,nx)


        if vartype=="Ptot":
            # Total precipitation 
            a3var = a3sum / nYear * 60*60*6   # mm/season 
            a2var = a3var.mean(axis=0)
            sunit = "mm/season"

        elif vartype=="Num":
            a2var = a3num.mean(axis=0)
            sunit = "times/10-year"


        a2sig = ones([ny,nx],float32)*miss

        # Figure

        #bnd  = [0,100,400,700,1000,1300,1600,1900,2200,2500,2800]
        #bnd  = arange(0,2800+1,700)
        #bnd = ret_bnd(vartype, thpr)
        bnd  = None
        #bnd  = range(0,300+1,20)

        #cmap = "jet_r"
        #vmax = None
        #vmin = None

        cmap = "gnuplot2_r"
        #vmax = 2800
        vmax = 2500
        vmin = 0

        #extend = "both"   # "neither","both","min","max"
        #extend = "neither"   # "neither","both","min","max"

        #white_minmax= "min"

        # Title
        stitle = "%s %s %s [%s] %s"%(model,scen,vartype, sunit, tag)

        # Figure name
        #figDir= baseDir + "/fig"
        figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
        util.mk_dir(figDir)
        figname= figDir + "/%s.th.%s.%s.%s.png"%(model ,sthpr, tag,"Ptot")
        # Cbar
        if tag == "plain":
            cbarname=figDir + "/cbar.%s.%s.png"%(vartype, sthpr)
        else:
            cbarname=False


        figname= figDir + "/map.%s.th.%s.%s.%s.png"%(scen,sthpr,tag,vartype)

        #hd_fig.DrawMap_dotshade(a2in=a2var, a2dot=a2sig, a1lat=Lat, a1lon=Lon, BBox=BBox, bnd=bnd, cmap=cmap, extend=extend, white_minmax=white_minmax, figname=figname, cbarname=cbarname, stitle=stitle, dotstep=5, dotcolor="0.8")

        a2hatch = ones([ny,nx],float32)*miss

        #f_draw_mapglobal.draw_map_robin(a2dat=a2var, a2hatch=a2hatch, Lat=Lat, Lon=Lon, miss=-9999, bnd=bnd, cmap=cmap, vmin=vmin, vmax=vmax, figPath=figname, cbarPath=cbarname, stitle=stitle, cbarOrientation="vertical")
        f_draw_mapglobal.draw_map_robin(a2dat=a2var, a2hatch=a2hatch, Lat=Lat, Lon=Lon, miss=-9999, bnd=bnd, cmap=cmap, vmin=vmin, vmax=vmax, figPath=figname, cbarPath=cbarname, stitle=stitle, cbarOrientation="horizontal")




