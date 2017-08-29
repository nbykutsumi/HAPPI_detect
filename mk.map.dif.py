from numpy import *
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
lens    = range(1,50)
#lens    = range(1,3)
res     = "128x256"
ny, nx  = 128, 256
miss    = -9999.

#ltag    = ["plain","tc","cf","ms","ot"]
ltag    = ["plain"]
lvar    = ["Ptot"]


dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

thpr   = 0
hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="P15", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon


#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr


def load_var_single(scen, ens, var):
    dattype = {"sum":float32, "num":int32, "ptot":float32}
    run = "%s-%s-%03d"%(expr, scen, ens)
    iYear, eYear = dieYear[scen]
    nYear = eYear - iYear +1

    if var in ["sum","num"]:
        baseDir, sDir, sPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum=var)
        return fromfile(sPath, dattype[var]).reshape(ny,nx) /nYear

    elif var == "ptot":
        a2sum = load_var_single(scen, ens, "sum")
        a2out = a2sum *60*60*6 / nYear  # mm/season
        return a2out


def load_var_3D(scen, lens, var):
    nens  = len(lens)
    a3var = empty([nens, ny, nx])
    for iens, ens in enumerate(lens):
        a3var[iens] = load_var_single(scen, ens, var)
    return a3var

sthpr  = ret_sthpr(thpr)

llscen = [["ALL","P15"],["ALL","P20"],["P15","P20"]]
for lscen in llscen:
    tag    = "plain"
    var    = "ptot"
    season = "ALL"
    scen0  = lscen[0]
    scen1  = lscen[1]
    # Check statistical Difference (Welch's t-test)
    a3var0 = load_var_3D(scen0,lens, var)
    a3var1 = load_var_3D(scen1,lens, var)
    
    a2t, a2p = scipy.stats.ttest_ind(a3var1, a3var0, axis=0, equal_var= False)
    
    a2dot    = ma.masked_greater(a2p,0.05).filled(miss)
    a2dif    = a3var1.mean(axis=0) - a3var0.mean(axis=0)
    
    # Figure ********************
    figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
    figPath = os.path.join(figDir,"map.dif.%s.%s.%s-%s.%s.png"%(tag,var,scen1,scen0,season))
    cbarPath= os.path.join(figDir,"cbar.map.dif.%s.%s.png"%(tag,var))
    
    util.mk_dir(figDir)
    # title
    stitle  = "diff %s %s %s-%s"%(tag,var,scen1,scen0)
    
    bnd   = arange(-30,30+1, 5) 
    hd_fig.DrawMap_dotshade(a2dif, a2dot, Lat, Lon, bnd=bnd, figname=figPath, cbarname=cbarPath, dotstep=2, markersize=0.2, stitle=stitle) 
    
