import matplotlib
matplotlib.use("Agg")
from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
from myfunc.regrid  import Regrid
from myfunc.fig     import Fig
from bisect         import bisect_left
import HAPPI_detect_func as hd_func
import os, sys
import calendar
import myfunc.util as util
import f_draw_mapglobal
# Config ------------------------------------------------
configPath= os.path.dirname(os.path.abspath(__file__)) + "/config"
cfg         = SafeConfigParser(os.environ)
cfg.read(configPath)
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Cyclone     = import_module("%s.Cyclone"%(detectName))
IO_Master   = import_module("%s.IO_Master"%(detectName))

#--------------------------------------------------------

#prj     = "JRA55"
prj     = "HAPPI"
season  = "ALL"

#lkey   = [[1,"frac.ptot"],["p99.990","frac.ptot"],["p99.990","frac.freq"]]
#lkey   = [[1,"frac.ptot"],["p99.990","frac.ptot"]]
lkey   = [["p99.990","frac.freq"]]


modelRef   = "__"
runRef     = "__"
scenRef    = "__"
resRef     = "145x288"
ioRef      = IO_Master.IO_Master("JRA55", modelRef, runRef, resRef)
nyRef      = ioRef.ny
nxRef      = ioRef.nx
LatRef     = ioRef.Lat
LonRef     = ioRef.Lon

modelHap   = "MIROC5"
scenHap    = "ALL"
#scenHap    = "P15"
#scenHap    = "P20"
lens    = range(1,50+1)
expr       = "C20"
runTmp     = "C20-ALL-001"
resHap     = "128x256"
ioHap  = IO_Master.IO_Master("HAPPI", modelHap, runTmp, resHap)
nyHap  = ioHap.ny
nxHap  = ioHap.nx
LatHap = ioHap.Lat
LonHap = ioHap.Lon

Lat  = LatHap  # Used for fig
Lon  = LonHap

if prj == "JRA55":
    model=modelRef
    run  = runRef
    res  = resRef
    scen = scenRef
    io   = ioRef
    ny   = nyRef
    nx   = nxRef

elif prj == "HAPPI":
    model=modelHap
    res  = resHap
    scen = scenHap
    io   = ioHap
    ny   = nyHap
    nx   = nxHap


us     = Regrid.UpScale()
us(LatRef, LonRef, LatHap, LonHap, globflag=True)



#dtag = {"tc":"tc", "c":"c", "fbc":"f","ms":"ms"}
ltag = ["tc","cf","ms","ot"]

dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

miss = -9999.

def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr


def load_var_single(scen, ens, tag, var, thpr):
    dattype = {"sum":float32, "num":int32, "ptot":float32}
    run = "%s-%s-%03d"%(expr, scen, ens)
    iYear, eYear = dieYear[scen]
    nYear = eYear - iYear +1

    sthpr = ret_sthpr(thpr)
    if var in ["sum","num"]:
        baseDir, sDir, sPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum=var)
        return fromfile(sPath, dattype[var]).reshape(ny,nx)

    elif var == "ptot":
        a2sum = load_var_single(scen, ens, tag, "sum", thpr)
        a2out = a2sum *60*60*6 / nYear  # mm/season
        return a2out


    elif var == "freq":
        totalnum = calc_totaltimes(iYear,eYear,season)
        a2num = load_var_single(scen,ens,tag, "num", thpr)
        a2out = a2num / float(nYear)   # times per season
        return a2out

    elif var == "pint":
        totalnum = calc_totaltimes(iYear,eYear,season)
        a2sum = load_var_single(scen,ens,tag, "sum", thpr)
        a2num = load_var_single(scen,ens,tag, "num", thpr)
        a2out = a2sum / a2num * 60*60*24.  #[mm/day]
        return a2out

    elif var == "frac.ptot":
        a2all = load_var_single(scen,ens,"plain","ptot",thpr)
        a2tag = load_var_single(scen,ens,tag    ,"ptot",thpr)
        a2out = a2tag / a2all
        return a2out

    elif var == "frac.freq":
        a2all = load_var_single(scen,ens,"plain","freq",thpr)
        a2tag = load_var_single(scen,ens,tag    ,"freq",thpr)
        a2out = a2tag / a2all
        return a2out



def calc_totaltimes(iYear,eYear,season):
    n = 0
    for Year in range(iYear,eYear+1):
        for Mon in util.ret_lmon(season):
            iDay = 1
            eDay = calendar.monthrange(Year,Mon)[1]

            iDTime = datetime(Year,Mon,iDay,0)
            eDTime = datetime(Year,Mon,eDay,18)
            dDTime = timedelta(hours=6)
            lDTime = util.ret_lDTime_noleap(iDTime, eDTime, dDTime)
            n      = n + len(lDTime)
    return n



def load_var_3D(scen, lens, tag, var, thpr):
    nens  = len(lens)
    a3var = empty([nens, ny, nx])
    for iens, ens in enumerate(lens):
        a3var[iens] = load_var_single(scen, ens, tag, var, thpr)
    return a3var



for key in lkey:
    thpr, var = key
    for tag in ltag:
        a3var  = load_var_3D(scen,lens, tag, var, thpr)

        a2out  = ma.masked_invalid(a3var).mean(axis=0)
        print a2out 
        
        # Draw Map
        baseDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
        oDir     = os.path.join(baseDir, "fig")
        util.mk_dir(oDir)
        figname = oDir + "/map.%s.%s.%s.%s.%s.th.%s.%s.png"%(var,prj,model,scen,tag, thpr, season)
        cbarname= oDir + "/cbar.%s.png"%(var)
    
        cmap    = "gist_stern_r"
        stitle  = "%s %s %s %s %s"%(var, prj, scen, tag, season)
        vmin,vmax= 0, 1.0 
        a2hatch = ones([nyHap,nxHap],float32)*miss
        f_draw_mapglobal.draw_map_robin(a2out, a2hatch, Lat, Lon, cmap="gist_stern_r", vmin=vmin, vmax=vmax, figPath=figname, cbarPath=cbarname, cbarOrientation="horizontal", stitle=stitle, seaMask=True)
