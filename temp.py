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
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------
prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
#lscen   = ["ALL"]
lscen   = ["ALL","P20"]
lens    = [1]
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

dlYear = {"ALL": range(2006, 2015+1)
         ,"P15": range(2106, 2115+1)
         ,"P20": range(2106, 2115+1)
         }

#dlYear = {"ALL": range(2006, 2006+1)
#         ,"P15": range(2106, 2115+1)
#         ,"P20": range(2106, 2115+1)
#         }



lMon  = range(1,12+1)
#lMon = [8]

lkey = [[scen, ens] for scen in lscen for ens in lens]

thpr = 0.5

#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

def ret_a2thpr(thpr):
    nYear  = 30
    if type(thpr) == str:
        sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
        #sPath = sDir + "/%s.%s.%s.%s.%04dY.p%6.3f.%dx%d"%(prj,model,expr,scen,len(lYear)*len(lens), p, ny, nx)     
        sPath = sDir + "/%s.%s.%s.%s.%04dY.%s.%dx%d"%(prj,model,expr, "ALL", nYear, thpr, ny, nx)     
        a2thpr = fromfile(sPath, float32).reshape(ny,nx)

    else:
        a2thpr = ones([ny,nx],float32)/(60.*60.*24)*thpr 

    return a2thpr 

#----------------------
for scen in lscen:
    ens      = 1
    lYear    = dlYear[scen]
    run      = "%s-%s-%03d"%(expr, scen, ens)
    cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
    cfg_det["res"] = res
    T        = Tag.Tag(cfg_det, miss=0.0)
    hp       = HAPPI.Happi()
    hp(model, expr, scen, ens)

    a2thpr      = ret_a2thpr(thpr)
    a2sum       = zeros([ny,nx],float32)
    i = 0
    for Year in lYear:
        for Mon in lMon:
            print Year,Mon
            dDTime = timedelta(hours=6)
            eDay   = calendar.monthrange(Year,Mon)[1]
            iDTime = datetime(Year,Mon,1,6)
            eDTime = datetime(Year,Mon,eDay,18)
            lDTime = ret_lDTime(iDTime, eDTime, dDTime)

            for DTime in lDTime:
                i = i+1
                print DTime
                a2pr = hp.load_6hr("prcp",DTime)
                p = ma.masked_less(a2pr, a2thpr).filled(0.0)
                a2sum += p

    a2sum = a2sum / i 
    sPath = "./temp.%s.%dx%d"%(scen,ny,nx)
    a2sum.astype(float32).tofile(sPath)
    print sPath
