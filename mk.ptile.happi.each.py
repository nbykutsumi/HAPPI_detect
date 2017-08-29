from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.IO.HAPPI as HAPPI
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
#Cyclone     = import_module("%s.Cyclone"%(detectName))
#--------------------------------------------------------
#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"
#noleap   = False

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
#lscen   = ["ALL","P15","P20"]
lscen   = ["P20"]
#lscen   = ["P15","P20"]

#lens    = [1,1,1]
#lens    = [1,11,21,31,41]
lens    = range(1,50+1)
res     = "128x256"
noleap  = True
ny      = 128
nx      = 256
nz      = 1460

dieYear = {"ALL":[2006,2015], "P15":[2106,2115], "P20":[2106,2115]}

lp      = [99.9, 99.99]

#cfg_det  = config_func.config_func(prj=prj, model=model, run="%s-%s-001"%(expr,scen))
#rootDir  = cfg_det["rootDir"]
#baseDir  = cfg_det["baseDir"]

#------------------------
def ret_lly(iYear,eYear):
    lYear = range(iYear,eYear+1)
    mem      = 8.0e+9  # 1e+9 = 1GB
    y  = int(mem / float(4*nx*6*365.*len(lYear)))
    y  = min(y, ny)
    
    ly = range(0,ny+1,y)
    if y == ny:
        lly = [[0,ny]]
    else:
        lly= zip(ly, ly[1:]+[ny])
    return lly
#------------------------
for scen in lscen:
    iYear,eYear = dieYear[scen]
    lYear = range(iYear,eYear+1)
    for ens in lens:
        lly      = ret_lly(iYear,eYear)
        da2ptile = {p:empty([ny,nx],float32) for p in lp}
        for iy,ey in lly: 
            a3seg    = empty([nz*len(lYear), ey-iy, nx],float32)
        
            ibatch  = -1
            print scen, ens, iy,ey
            run = "%s-%s-%s"%(expr, scen, ens)
            hp  = HAPPI.Happi()
            hp(model, expr, scen, ens)
            
            for kYear, Year in enumerate(lYear):
                ibatch = ibatch+1
                a3dat = hp.load_batch_6hr("prcp",Year)
                a3seg[ nz*ibatch : nz*(ibatch+1)] = a3dat[:,iy:ey,:]
        
            for p in lp:
                da2ptile[p][iy:ey,:] = percentile(a3seg, p, axis=0)
        
        
        for p in lp: 
            sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile/%s"%(scen)
            sPath = sDir + "/%s.%s.%s.%s.%03d.p%6.3f.%dx%d"%(prj,model,expr, scen, ens, p, ny, nx) 
            util.mk_dir(sDir) 
            da2ptile[p].tofile(sPath)
            print sPath
            
