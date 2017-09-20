from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
from detect.front_fsub import *
import detect.IO_Master as IO_Master
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Front       = import_module("%s.Front"%(detectName))
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
#run     = "C20-ALL-001"  # for config
#res     = "128x256"
#ny,nx   = 128, 256
#noleap  = True

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]


iom    = IO_Master.IO_Master(prj, model, run, res)

cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
cfg_det["res"] = res
F        = Front.Front(cfg_det, miss=0.0)
miss  = -9999.
iYear = 2006
eYear = 2006
#eYear = 2006
lYear = range(iYear,eYear+1)
#lMon  = range(1,12+1)
lMon = [1]

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

                a2thermo  = iom.Load_6hrPlev("ta", DTime, 850)
                srcDir, srcPath1, srcPath2  = F.path_potloc(DTime, "t")
                a2potloc1 = fromfile(srcPath1, float32).reshape(ny,nx)
                a2potloc2 = fromfile(srcPath2, float32).reshape(ny,nx)

                #x = sin(arange(nx)/float(nx)*(2*pi))
                #y = sin(arange(ny)/float(ny)*(2*pi))
                #X,Y = meshgrid(x,y)

                #a2gradx,a2grady    = front_fsub.mk_a2grad(X.T, F.Lon, F.Lat, miss, nx, ny)
                #a2gradx = a2gradx.T
                #a2grady = a2grady.T
                print "*"*50
                print a2potloc1.shape
                print a2potloc1[:,:4]

                print "*"*50
                print a2potloc2.shape
                print a2potloc2[:,-4:]


                sys.exit()
 
    
