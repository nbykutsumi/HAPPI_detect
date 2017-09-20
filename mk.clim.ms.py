from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Monsoon     = import_module("%s.Monsoon"%(detectName))
#--------------------------------------------------------
prj     = "JRA55"
model   = "__"
run     = "__"
lens    = [1]
res     = "145x288"
ny,nx   = 145,288
noleap   = False

#prj     = "HAPPI"
#model   = "MIROC5"
#expr    = "C20"
#scen    = "ALL"
#lens    = range(1,50+1)
#run     = "C20-ALL-001"    # for config
#res     = "128x256"
#ny,nx   = 128, 256
#noleap  = True


ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

miss    = -9999.
cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
cfg_det["res"] = res
#F        = Front.Front(cfg_det, miss=0.0)
ms       = Monsoon.MonsoonMoist(cfg_det, miss=0.0)

iYear = 2006
eYear = 2014
#eYear = 2006
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
#lMon = [1]

season = "ALL"
for ens in lens:
    if prj == "HAPPI":
        run = "%s-%s-%03d"%(expr,scen,ens)
    a2sum  = zeros([ny,nx],int32)
    ntimes = 0
    for Year in lYear:
        for Mon in lMon:
            print Year, Mon
            dDTime = timedelta(hours=6)
            eDay   = calendar.monthrange(Year,Mon)[1]
            iDTime = datetime(Year,Mon,1,6)
            eDTime = datetime(Year,Mon,eDay,18)
            lDTime = ret_lDTime(iDTime, eDTime, dDTime)
            ntimes = ntimes + len(lDTime) 
            for DTime in lDTime:
                a2ms  = ms.loadMonsoonMoist(var="spfh_3lev",DTime=DTime).astype(int32)
                a2ms  = ma.masked_equal(a2ms, miss).filled(0)
                a2sum = a2sum + a2ms
    
    a2freq  = (a2sum / float(ntimes)).astype(float32)
    # Save monthly data
    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
    oDir    = os.path.join(baseDir, "clim.loc.ms",prj,model,run)
    util.mk_dir(oDir)
    filePath= os.path.join(oDir, "freq.%s.%s"%(season, res))
    a2freq.tofile(filePath)
    print filePath
    
