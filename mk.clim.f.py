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
Front       = import_module("%s.Front"%(detectName))
#--------------------------------------------------------
#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"
#noleap   = False

prj     = "HAPPI"
model   = "MIROC5"
#run     = "C20-ALL-001"
#run     = "C20-ALL-001-100-070"
#run     = "C20-ALL-001-070-100"
#run     = "C20-ALL-001-080-100"
run     = "C20-ALL-001-090-100"
res     = "128x256"
noleap  = True

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
cfg_det["res"] = res
F        = Front.Front(cfg_det, miss=0.0)

iYear = 2006
eYear = 2014
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
#lMon = [1]

for Year in lYear:
    for Mon in lMon:
        
        dDTime = timedelta(hours=6)
        eDay   = calendar.monthrange(Year,Mon)[1]
        iDTime = datetime(Year,Mon,1,6)
        eDTime = datetime(Year,Mon,eDay,18)
        lDTime = ret_lDTime(iDTime, eDTime, dDTime)

        ny     = F.ny
        nx     = F.nx
        a2sum  = zeros([ny,nx],float32)        
        for DTime in lDTime:
            #print DTime
            a2f   = F.mk_tfront(DTime)
            a2sum = a2sum + a2f

        a2freq  = a2sum / len(lDTime)
        # Save monthly data
        baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
        oDir    = os.path.join(baseDir, "clim.loc.fbc",prj,model,run)
        util.mk_dir(oDir)
        filePath= os.path.join(oDir, "freq.%04d.%02d.%s"%(Year, Mon, res))
        a2freq.tofile(filePath)
        print filePath

