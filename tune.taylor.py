from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
from myfunc.regrid import Regrid
import os, sys
import calendar
import myfunc.util as util
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Cyclone     = import_module("%s.Cyclone"%(detectName))
IO_Master   = import_module("%s.IO_Master"%(detectName))
#--------------------------------------------------------
#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"


prj     = "HAPPI"
model   = "MIROC5"
#run     = "C20-ALL-001-100"
#run     = "C20-ALL-001-070"
run     = "C20-ALL-001-130"
res     = "128x256"




iYM = [2006,1]
eYM = [2014,12]
lYM = util.ret_lYM(iYM, eYM)

a2freq= zeros([ny,nx],float32)
for [Year,Mon] in lYM:
    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
    oDir    = os.path.join(baseDir, "clim.loc.c",prj,model,run)
    util.mk_dir(oDir)
    filePath= os.path.join(oDir, "freq.%04d.%02d.%s"%(Year, Mon, res))
    a2in    = fromfile(filePath, float32).reshape(ny,nx)
    a2freq  = a2freq + a2in

a2freq = a2freq / len(lYM)

