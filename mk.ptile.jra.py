from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.IO.HAPPI as HAPPI
import myfunc.IO.JRA55 as JRA55
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
#Cyclone     = import_module("%s.Cyclone"%(detectName))
#--------------------------------------------------------
prj     = "JRA55"
model   = "__"
#run     = "__"
expr  = "__"
scen  = "__"


res     = "145x288"
noleap   = False

#prj     = "HAPPI"
#model   = "MIROC5"
#expr    = "C20"
#scen    = "ALL"

#lens    = [1,1,1]
lens    = [1]
res     = "128x256"
noleap  = True
iYear   = 2006
eYear   = 2014
lYear   = range(iYear,eYear+1)
iDTime  = datetime(iYear,1,1,0)
eDTime  = datetime(eYear,12,31,18)
dDTime  = timedelta(hours=3)
lDTime  = util.ret_lDTime(iDTime, eDTime, dDTime)
nz      = len(lDTime)

lp      = [99.9, 99.99]

cfg_det  = config_func.config_func(prj=prj, model=model, run="%s-%s-001"%(expr,scen))
rootDir  = cfg_det["rootDir"]
baseDir  = cfg_det["baseDir"]

jra     = JRA55.Jra55()
ny      = jra.ny
nx      = jra.nx

#------------------------
mem      = 2.0e+9  # 1e+9 = 1GB
y  = int(mem / float(4*nx*nz))
y  = min(y, ny)

ly = range(0,ny+1,y)
if y == ny:
    lly = [[0,ny]]
else:
    lly= zip(ly, ly[1:]+[ny])
print lly
#------------------------
da2ptile = {p:empty([ny,nx],float32) for p in lp}

for iy,ey in lly: 
    a3seg   = empty([nz, ey-iy, nx],float32)
    for kDT,DTime in enumerate(lDTime):
        a2pr1 = jra.load_3hr("APCP",DTime)
        a2pr2 = jra.load_3hr("APCP",DTime+timedelta(hours=3))
        a2pr  = (a2pr1 + a2pr2)/2.0 /(60.*60.*24.)  # mm/day --> mm/s
        a3seg[kDT] = a2pr[iy:ey,:]


    for p in lp:
        da2ptile[p][iy:ey,:] = percentile(a3seg, p, axis=0)


for p in lp: 
    sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
    sPath = sDir + "/%s.%s.%s.%s.%04dY.p%6.3f.%dx%d"%(prj,model,expr,scen,len(lYear)*len(lens), p, ny, nx) 
    
    da2ptile[p].tofile(sPath)
    print sPath
    
