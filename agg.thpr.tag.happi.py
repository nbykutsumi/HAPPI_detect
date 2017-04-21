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
#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"
#noleap   = False

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
lscen   = ["ALL","P20","P15"]
#lscen   = ["P15","P20"]
#lscen   = ["ALL"]
lens    = [1,11,21,31,41]
res     = "128x256"
noleap  = True
ny, nx  = 128, 256


#lthpr = [0.0,"p99.900","p99.990"]
#lthpr = ["p99.900","p99.990"]
#lthpr = ["p99.990"]
lthpr = ["p99.900"]

print "lscen=",lscen
print "lthpr=",lthpr


ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

ltag  = ["tc","cf","ms","ot"]
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

dlYear = {"ALL": range(2006, 2015+1)
         ,"P15": range(2106, 2115+1)
         ,"P20": range(2106, 2115+1)
         }

lMon  = range(1,12+1)
#lMon = [8]

lkey = [[scen, ens] for scen in lscen for ens in lens]

#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

def ret_a2thpr(thpr):
    #nYear  = 30
    nYear  = 50
    if type(thpr) == str:
        sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
        sPath = sDir + "/%s.%s.%s.%s.%04dY.%s.%dx%d"%(prj,model,expr, "ALL", nYear, thpr, ny, nx)     
        a2thpr = fromfile(sPath, float32).reshape(ny,nx)

    else:
        a2thpr = ones([ny,nx],float32)/(60.*60.*24)*thpr 

    return a2thpr 

#----------------------
for scen, ens in lkey:
    lYear    = dlYear[scen]
    run      = "%s-%s-%03d"%(expr, scen, ens)
    cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
    cfg_det["res"] = res
    T        = Tag.Tag(cfg_det, miss=0.0)
    hp       = HAPPI.Happi()
    hp(model, expr, scen, ens)

    dthpr = {thpr: ret_a2thpr(thpr) for thpr in lthpr}
   
    for Year in lYear:
        for Mon in lMon:
            print Year,Mon
            dDTime = timedelta(hours=6)
            eDay   = calendar.monthrange(Year,Mon)[1]
            iDTime = datetime(Year,Mon,1,6)
            eDTime = datetime(Year,Mon,eDay,18)
            lDTime = ret_lDTime(iDTime, eDTime, dDTime)

            # init array
            dsum  = {(tag, thpr):zeros([ny,nx],float32) for tag in ltag+["plain"] for thpr in lthpr}
            
            dnum  = {(tag, thpr):zeros([ny,nx],int32) for tag in ltag+["plain"] for thpr in lthpr}
            
            # init Cyclone
            T.init_cyclone([Year,Mon],[Year,Mon], cfg_det, tctype="obj")
    
            for DTime in lDTime: 
            #for DTime in lDTime[8:8+1]: 
                dtag = T.mkMaskFrac(ltag_ws, DTime, ltag_2nd)
                a2pr = hp.load_6hr("prcp",DTime)

                for thpr in lthpr:
                    p = ma.masked_less(a2pr, dthpr[thpr]).filled(0.0)
                    n= ma.masked_greater_equal(a2pr, dthpr[thpr]).mask
                    dsum["plain",thpr] += p
                    dnum["plain",thpr] += n

                    for tag in ltag:
                        dsum[tag,thpr] += p * dtag[tag]
                        dnum[tag,thpr] += (n * dtag[tag]).astype(int32)


            for thpr in lthpr:
                sthpr = ret_sthpr(thpr)

                for tag in ltag+["plain"]:

                    sDir    = hd_func.path_sumnum(model=model, run=run, res=res, sthpr=sthpr, tag=tag, sumnum="sum", Year=Year, Mon=Mon)[1]
                    sumPath = hd_func.path_sumnum(model=model, run=run, res=res, sthpr=sthpr, tag=tag, sumnum="sum", Year=Year, Mon=Mon)[-1]
                    numPath = hd_func.path_sumnum(model=model, run=run, res=res, sthpr=sthpr, tag=tag, sumnum="num", Year=Year, Mon=Mon)[-1]


                    util.mk_dir(sDir)
                    dsum[tag,thpr].tofile(sumPath)
                    dnum[tag,thpr].tofile(numPath)
                    print sumPath
