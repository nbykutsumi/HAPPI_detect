from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys, inspect
import calendar
import myfunc.util as util
import myfunc.fig.Fig  as Fig
import myfunc.IO.HAPPI as HAPPI
import myfunc.IO.JRA55 as JRA55
import myfunc.grids as grids
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
# Config ------------------------------------------------
configPath= os.path.dirname(os.path.abspath(__file__)) + "/config"

cfg         = SafeConfigParser(os.environ)
cfg.read(configPath)
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------

prj     = "HAPPI"
#model   = "MIROC5"
expr    = "C20"
res     = "128x256"
noleap  = True
ny, nx  = 128, 256
lscen   = ["JRA","ALL","P15","P20"]
#lscen   = ["JRA"]
#lscen   = ["ALL","P15","P20"]
#lthpr   = ["p99.900"]
#lthpr   = [0]
lthpr   = [0,"p99.900"]

dieYear = {"JRA":(2006, 2014)
         ,"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

lens   = [1]

season = "ALL"
#season = 1
ltag   = ["tc","cf","ms","ot"]
ddtype = {"sum":"float32", "num":"int32"}
BBox  = [[-80,0.0],[80,360]]
miss  = -9999.
hp    = HAPPI.Happi()
hp(model="MIROC5", expr=expr, scen="ALL", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon


jra   = JRA55.Jra55()
LatJRA= jra.Lat
LonJRA= jra.Lon
#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

def ret_model(scen):
    if scen == "JRA":
        model = "__"
    else:
        model = "MIROC5"
    return model
#----------------------
lkey = [[thpr, scen] for thpr in lthpr for scen in lscen]
for thpr, scen in lkey:
    sthpr = ret_sthpr(thpr)
    model = ret_model(scen)

    Sum = {}
    Num = {}
    FracSum = {}
    FracNum = {}

    for tag in ["plain"]+ltag:
        if scen !="JRA":
            a1lat = Lat
            a1lon = Lon      
            iYear, eYear = dieYear[scen]
            nYear = eYear - iYear +1
            a3sum = empty([len(lens),ny,nx],float32)
            a3num = empty([len(lens),ny,nx],int32)
            for iens, ens in enumerate(lens):
                run = "%s-%s-%03d"%(expr, scen, ens)
        
                #- Load ---
        
                baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
        
                baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
        
                a3sum[iens] = fromfile(sumPath, float32).reshape(ny,nx)
                a3num[iens] = fromfile(numPath, int32).reshape(ny,nx)
        
            Sum[tag] = a3sum.mean(axis=0)
            Num[tag] = a3num.mean(axis=0)
        
        elif scen =="JRA":
            a1lat = LatJRA
            a1lon = LonJRA
            iYear, eYear = dieYear[scen]
            nYear = eYear - iYear +1 

            # JRA55
            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
            
            baseDir, sDir, numPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
            
            a2sum = fromfile(sumPath, float32).reshape(145,288)
            a2num = fromfile(numPath, int32  ).reshape(145,288)

            Sum[tag] = a2sum
            Num[tag] = a2num        
   
    #-- Frac  ---------------
    for tag in ltag:
        FracSum[tag] = ma.masked_invalid(Sum[tag]/Sum["plain"]).filled(miss)
        FracNum[tag] = ma.masked_invalid(Num[tag]
                        /Num["plain"].astype(float32)).filled(miss)

    #-- Figure --------------
    for dattype in ["Num","Sum"]:
        if   dattype=="Num":
            Dat = FracNum
        elif dattype=="Sum":
            Dat = FracSum
 
        for itag, tag in enumerate(ltag):
            if scen == "JRA":
                run = "__"
            else:
                run = "%s-%s-%03d"%(expr, scen, 1)

            a2in = Dat[tag]
            cmap = "jet_r"
            bnd  = arange(0.1,0.9+0.01, 0.1)

            # Name
            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")

            figDir  = baseDir + "/fig"
            print "*"*50
            print figDir
            figname = figDir + "/%s.frac.th.%s.%s.%s.png"%(scen, sthpr, dattype, tag)

            if itag==0:
                cbarname= figDir + "/frac.cbar.png"
            else:
                cbarname= False

            stitle = "%s %s %s %s"%(scen, sthpr, dattype, tag)

            Fig.DrawMapSimple(a2in=a2in, a1lat=a1lat, a1lon=a1lon, BBox=BBox, bnd=bnd, extend="both", white_minmax="min", cmap=cmap, stitle=stitle, figname=figname, cbarname=cbarname, figsize=(6,3))

           
            
