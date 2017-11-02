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
model   = "MIROC5"
expr    = "C20"
res     = "128x256"
noleap  = True
ny, nx  = 128, 256
lscen   = ["P15","P20"]
#lthpr   = ["p99.990"]
#lthpr   = ["p99.900"]
#lthpr   = [0]
#lthpr   = [0,"p99.900","p99.990"]
lthpr   = [0,"p99.990"]

region = "GLB"
#region = "JPN"

dieYear = {"JRA":(2006, 2014)
         ,"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

lens   = [1,11,21,31,41]

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

if region == "GLB":
    BBox  = [[-80,0.0],[80,360]]
    parallels=arange(-90,90+0.1,30)
    meridians=arange(-180,360+0.1,30)
elif region=="JPN":
    BBox  = [[20,120],[50,150]]
    parallels=arange(-90,90+0.1,10)
    meridians=arange(-180,360+0.1,10)

#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

#----------------------
lkey = [[thpr, scen] for thpr in lthpr for scen in lscen]
for thpr in lthpr:
    sthpr = ret_sthpr(thpr)

    a3Sum = {}
    a3Num = {}
    a3FracSum = {}
    a3FracNum = {}

    for scen in ["ALL"] + lscen:
        for tag in ["plain"]+ltag:
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
            
            #Sum[scen, tag] = a3sum.mean(axis=0)
            #Num[scen, tag] = a3num.mean(axis=0)
        
            a3Sum[scen, tag] = a3sum
            a3Num[scen, tag] = a3num
   
    #-- Frac  ---------------
    for scen in ["ALL"] + lscen:
        for tag in ltag:
            a3FracSum[scen,tag] = ma.masked_invalid(a3Sum[scen,tag]/a3Sum[scen,"plain"]).filled(miss)
            a3FracNum[scen,tag] = ma.masked_invalid(a3Num[scen,tag]
                            /a3Num[scen,"plain"].astype(float32)).filled(miss)

    #-- dFrac ---------------
    a3dFracSum = {}
    a3dFracNum = {}
    for scen in lscen:
        for tag in ltag:        
            a3dFracSum[scen,tag] = a3FracSum[scen,tag] - a3FracSum["ALL",tag] 
            a3dFracNum[scen,tag] = a3FracNum[scen,tag] - a3FracNum["ALL",tag]

    #-- Figure --------------
    for dattype in ["Num","Sum"]:
        if   dattype=="Num":
            Dat = a3dFracNum
        elif dattype=="Sum":
            Dat = a3dFracSum

        for scen in lscen: 
            for itag, tag in enumerate(ltag):
                run = "%s-%s-%03d"%(expr, scen, 1)
    
                a2in = Dat[scen,tag].mean(axis=0)

                # significance test
                a2t  = (a2in-0.0)/sqrt(Dat[scen,tag].var(axis=0)/(len(lens)-1))
                a2pv = scipy.stats.t.sf( abs(a2t), len(lens)-1)*2

                # mask
                a2in = ma.masked_where(a2pv >0.05, a2in)
                #atemp = ma.masked_where(a2pv >0.05, a2in)
                #atempstd=sqrt(Dat[scen,tag].var(axis=0))



                cmap = "RdBu"
                bnd  = [-0.2, -0.15, -0.05, 0.05, 0.15, 0.2]
    
                # Name
                #baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")

                iYear_fut, eYear_fut = dieYear[scen]
                baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear_fut, eYear=eYear_fut, season=season, var=var)[0:2]

 
                figDir  = baseDir + "/fig"
                print "*"*50
                print figDir
                figname = figDir + "/%s.%s.inc.frac.th.%s.%s.%s.png"%(region, scen, sthpr, dattype, tag)
    
                if itag==0:
                    cbarname= figDir + "/cbar.inc.frac.png"
                else:
                    cbarname= False
    
                stitle = "%s %s %s %s"%(scen, sthpr, dattype, tag)
    
                Fig.DrawMapSimple(a2in=a2in, a1lat=a1lat, a1lon=a1lon, BBox=BBox, bnd=bnd, parallels=parallels, meridians=meridians,  extend="both", white_minmax="center", cmap=cmap, stitle=stitle, figname=figname, cbarname=cbarname, maskcolor="gray", figsize=(6,3))
    

