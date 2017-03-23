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
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------
prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
lscen   = ["P20"]
#lscen   = ["P15","P20"]
lens    = [1]
nens    = len(lens)
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

ltag  = ["tc","cf","ms","ot"]
#ltag   = []
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

iYear_his, eYear_his = 2006, 2015
iYear_fut, eYear_fut = 2106, 2115

#iYear_his, eYear_his = 2006, 2006
#iYear_fut, eYear_fut = 2106, 2106
#season = "ALL"
season = "ALL"
#season = 1

#lthpr = [0.5]
lthpr = [0.0]
ddtype = {"sum":"float32", "num":"int32"}
hp    = HAPPI.Happi()
BBox  = [[-80,0.0],[80,360]]
miss  = -9999.
#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr


def load_var(**kwargs):
    """model, expr, scen, ens, sthpr, tag, sumnum, Year, Mon"""

    sumnum = kwargs["sumnum"]
    sPath = hd_func.path_sumnum(**kwargs)[-1]

    return fromfile(sPath, dtype=ddtype[sumnum]).reshape(ny,nx)

def mk_clim(**kwargs):
    """model, expr, scen, ens, sthpr, tag, sumnum, iYear, eYear, season"""
    iYear = kwargs["iYear"]
    eYear = kwargs["eYear"]
    season= kwargs["season"]
    sumnum= kwargs["sumnum"]
    lYear = range(iYear, eYear+1)
    lMon  = hd_func.ret_lMon(season)
    a2out = zeros([ny,nx], ddtype[sumnum])
    for Year in lYear:
        for Mon in lMon:
            kwargs["Year"] = Year
            kwargs["Mon"]  = Mon
            a2out = a2out + load_var(**kwargs)

    a2out = a2out / float(len(lYear))   # per season
    return a2out

#----------------------
lKey = [[scen, thpr] for scen in lscen for thpr in lthpr]

for (scen, thpr) in lKey:
    hp(model=model, expr=expr, scen="P15", ens=1)
    Lat   = hp.Lat
    Lon   = hp.Lon

    sthpr= ret_sthpr(thpr)
    for tag in ltag + ["plain"]:
        for var in ["dNI","NdI","dNdI","dP"]:
            a3var = zeros([len(lens),ny,nx],float32)
            for iens, ens in enumerate(lens):
                dkw = {}
                dkw["model"] = model
                dkw["expr"]  = expr
                dkw["scen"]  = scen
                dkw["ens"]   = ens
                dkw["sthpr"] = sthpr
                dkw["season"]= season
                dkw["tag"]   = tag

                #- Load ---
                """model, expr, scen, ens, sthpr, tag, Year, Mon"""
                baseDir, sDir = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var=var)[0:2]
                sPath = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var=var)[-1]
    
                a3var[iens] = fromfile(sPath, float32).reshape(ny,nx)

            # Change
            a2var = a3var.mean(axis=0)
            a2t   = (a2var-0.0)/( a3var.var(axis=0)/sqrt(nens))
            a2pv  = scipy.stats.t.sf( a2t, abs(a2t), nens-1)
            a2sig = ma.masked_greater(a2pv, 0.05).filled(miss)

            figDir= baseDir + "/fig"
            util.mk_dir(figDir)

            bnd  = [-200,-150,-100,-50,-20,20,50,100,150,200]
            cmap = "RdBu"

            figname= figDir + "/%s.th.%s.%s.%s.png"%(scen,sthpr,tag,var)
            hd_fig.DrawMap_dotshade(a2in=a2var, a2dot=a2sig, a1lat=Lat, a1lon=Lon, BBox=BBox, bnd=bnd, cmap=cmap, figname=figname, dotstep=5, dotcolor="0.8")

            # Relative change [%]




