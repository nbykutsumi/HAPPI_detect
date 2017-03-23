from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.IO.HAPPI as HAPPI
import HAPPI_detect_func as hd_func
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
#--------------------------------------------------------
prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
#lscen   = ["ALL","P15","P20"]
#lscen   = ["P15","P20"]
lscen   = ["P15"]
lens    = [1]
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

#lthpr = ["p99.990"]
lthpr = ["p99.900"]


ltag  = ["tc","cf","ms","ot"]
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

season = "ALL"
#season = 1

#lthpr = [0.5]
#lthpr = [0.0,0.5]
ddtype = {"sum":"float32", "num":"int32"}
#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr

def load_var(**kwargs):
    """model, run, sthpr, tag, sumnum, Year, Mon"""

    sumnum = kwargs["sumnum"]
    sPath = hd_func.path_sumnum(**kwargs)[-1]

    return fromfile(sPath, dtype=ddtype[sumnum]).reshape(ny,nx) 

def mk_clim(**kwargs):
    """model, run, sthpr, tag, sumnum, iYear, eYear, season"""
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

    #a2out = a2out / float(len(lYear))   # per season : if not use, simple total per period

    return a2out 
    
def update_dict(d1, d2):
    d1.update(d2)
    return d1
#----------------------
lKey = [[scen, thpr] for scen in lscen for thpr in lthpr]

for (scen, thpr) in lKey:
    [iYear, eYear] = dieYear[scen]

    sthpr= ret_sthpr(thpr)
    for ens in lens:
        run      = "%s-%s-%03d"%(expr, scen, ens)

        for tag in ltag + ["plain"]:

            a2sum =mk_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, sumnum="sum", iYear=iYear, eYear=eYear, season=season)
            a2num =mk_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, sumnum="num", iYear=iYear, eYear=eYear, season=season)
 
       
            #- Save ---
            """model, run, res, sthpr, tag, Year, Mon"""
    
            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")

            baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")


            util.mk_dir(sDir)
            a2sum.astype(float32).tofile(sumPath)
            a2num.astype(int32  ).tofile(numPath)
            print sumPath 

