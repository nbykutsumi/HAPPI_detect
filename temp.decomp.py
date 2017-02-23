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
#lscen   = ["P15","P20"]
lscen   = ["P20"]
lens    = [1]
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

ltag  = ["tc","cf","ms","ot"]
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

#iYear_his, eYear_his = 2006, 2015
#iYear_fut, eYear_fut = 2106, 2115
iYear_his, eYear_his = 2006, 2006
iYear_fut, eYear_fut = 2106, 2106
season = "ALL"
#season = 1

lthpr = [0.5]
#lthpr = ["p99.990"]
ddtype = {"sum":"float32", "num":"int32"}
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
    
def update_dict(d1, d2):
    d1.update(d2)
    return d1
#----------------------
lKey = [[scen, thpr] for scen in lscen for thpr in lthpr]

for (scen, thpr) in lKey:
    sthpr= ret_sthpr(thpr)
    for ens in lens:
        for tag in ltag + ["plain"]:
            dkw = {}
            dkw["model"] = model
            dkw["expr"]  = expr
            dkw["scen"]  = scen
            dkw["ens"]   = ens
            dkw["sthpr"] = sthpr
            dkw["season"]= season
            dkw["tag"]   = tag

            sum_his=mk_clim(model=model, expr=expr, scen="ALL", ens=ens, sthpr=sthpr, tag=tag, sumnum="sum", iYear=iYear_his, eYear=eYear_his, season=season)
            sum_fut=mk_clim(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, sumnum="sum", iYear=iYear_fut, eYear=eYear_fut, season=season)
        
            num_his=mk_clim(model=model, expr=expr, scen="ALL", ens=ens, sthpr=sthpr, tag=tag, sumnum="num", iYear=iYear_his, eYear=eYear_his, season=season)
        
            num_fut=mk_clim(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, sumnum="num", iYear=iYear_fut, eYear=eYear_fut, season=season)

       
            int_his = ma.masked_invalid(sum_his / num_his).filled(0.0)   # mm/sec
            int_fut = ma.masked_invalid(sum_fut / num_fut).filled(0.0)   # mm/sec

            # test
            print "*"*50
        
            #- Change [mm/season] -----
            dNI    = (num_fut-num_his)*int_his * 60*60*6
            NdI    = num_his * (int_fut - int_his) * 60*60*6
            dNdI   = (num_fut-num_his)*(int_fut - int_his) * 60*60*6
            dP     = (sum_fut - sum_his)*60*60*6
        
            #- Save ---
            """model, expr, scen, ens, sthpr, tag, Year, Mon"""
    
            sDir = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var="dNI")[1]

            dNIpath = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var="dNI")[-1]
            NdIpath = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var="NdI")[-1]
            dNdIpath = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var="dNdI")[-1]
            dPpath = hd_func.path_dpr(model=model, expr=expr, scen=scen, ens=ens, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[-1]

            util.mk_dir(sDir)
            dNI .astype(float32).tofile(dNIpath)
            NdI .astype(float32).tofile(NdIpath)
            dNdI.astype(float32).tofile(dNdIpath)
            dP  .astype(float32).tofile(dPpath)

            print dNIpath
