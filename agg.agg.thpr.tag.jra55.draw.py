from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.fig  as fig
#import myfunc.IO.HAPPI as HAPPI
import myfunc.IO.JRA55 as JRA55
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#---------------------------------------------------
#lvartype = ["Ptot","Num"]
lvartype = ["Num"]

prj     = "JRA55"
model   = "__"
run     = "__"
res     = "145x288"
noleap  = True
ny, nx  = 145, 288
iYear   = 2006
eYear   = 2014

#prj     = "HAPPI"
#model   = "MIROC5"
#expr    = "C20"
#lscen   = ["ALL","P15","P20"]
##lscen   = ["P15","P20"]
#lens    = [1]
#nens    = len(lens)
#res     = "128x256"
#noleap  = True
#ny, nx  = 128, 256

ltag  = ["tc","cf","ms","ot"]
#ltag   = []
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

#season = "ALL"
season = "ALL"
#season = 1

#lthpr = [0.5]
#lthpr = [0.0]
lthpr = ["p99.900","p99.990"]
ddtype = {"sum":"float32", "num":"int32"}
BBox  = [[-80,0.0],[80,360]]
miss  = -9999.

jra   = JRA55.Jra55()
#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr

def ret_bnd(vartype, thpr):
    if vartype=="Ptot":
        bnd  = [100,400,700,1000,1300,1600,1900,2200,2500,2800]
                 
    elif (vartype=="Num")&(thpr=="p99.900"):
        bnd  = arange(2,18+1, 2)
    elif (vartype=="Num")&(thpr=="p99.990"):
        bnd  = arange(0.2, 1.8+0.01, 0.2)

    return bnd.tolist()

#----------------------
for thpr in lthpr:
    nYear = eYear - iYear +1

    Lat   = jra.Lat
    Lon   = jra.Lon

    sthpr= ret_sthpr(thpr)
    for tag in ltag + ["plain"]:
        a2sum = zeros([ny,nx],float32)
        #a2num = zeros([ny,nx],float32)
        #- Load ---
        """model, run, res, sthpr, tag, Year, Mon"""
   

        baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
    
        baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
 
        a2sum = fromfile(sumPath, float32).reshape(ny,nx)
        a2num = fromfile(numPath, int32).reshape(ny,nx)


        # Figure
        figDir= baseDir + "/fig"
        util.mk_dir(figDir)

        for vartype in lvartype:

            if vartype=="Ptot":
                # Total precipitation 
                a2var = a2sum / nYear * 60*60*6   # mm/season
                sunit = "mm/season"

            elif vartype=="Num":
                a2var = a2num
                sunit = "times/10-year"


            a2sig = ones([ny,nx], float32)*miss

            bnd    = ret_bnd(vartype, thpr)
            #cmap   = "Spectral"
            cmap   = "jet_r"
            extend = "both"   # "neither","both","min","max"
            white_minmax= "min"
    
            # Title
            stitle = "%s %s [%s] %s"%("JRA55",vartype, sunit, tag)
    
            figname= figDir + "/%s.th.%s.%s.%s.png"%("JRA55",sthpr,tag,vartype)
            if tag == "plain":
                cbarname=figDir + "/cbar.%s.%s.png"%(vartype, sthpr)
            else:
                cbarname=False

            if tag=="plain":
                sys.exit()

            hd_fig.DrawMap_dotshade(a2in=a2var, a2dot=a2sig, a1lat=Lat, a1lon=Lon, BBox=BBox, bnd=bnd, cmap=cmap, extend=extend, white_minmax=white_minmax, figname=figname, cbarname=cbarname, stitle=stitle, dotstep=5, dotcolor="0.8")
    




