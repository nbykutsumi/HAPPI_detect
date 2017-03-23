from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
from myfunc.regrid  import Regrid
from myfunc.fig     import Fig
from bisect         import bisect_left
import os, sys
import calendar
import myfunc.util as util
# Config ------------------------------------------------
configPath= os.path.dirname(os.path.abspath(__file__)) + "/config"
cfg         = SafeConfigParser(os.environ)
cfg.read(configPath)
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Cyclone     = import_module("%s.Cyclone"%(detectName))
IO_Master   = import_module("%s.IO_Master"%(detectName))

#--------------------------------------------------------
figflag    = True
#figflag    = False

prjRef     = "JRA55"
modelRef   = "__"
runRef     = "__"
resRef     = "145x288"
ioRef      = IO_Master.IO_Master(prjRef, modelRef, runRef, resRef)
nyRef      = ioRef.ny
nxRef      = ioRef.nx
LatRef     = ioRef.Lat
LonRef     = ioRef.Lon

prj     = "HAPPI"
model   = "MIROC5"
runTmp     = "C20-ALL-001-100"
res     = "128x256"
ioHap  = IO_Master.IO_Master(prj, model, runTmp, res)
nyHap  = ioHap.ny
nxHap  = ioHap.nx
LatHap = ioHap.Lat
LonHap = ioHap.Lon


us     = Regrid.UpScale()
us(LatRef, LonRef, LatHap, LonHap, globflag=True)

iYM = [2006,1]
eYM = [2014,12]
lYM = util.ret_lYM(iYM, eYM)

def load_clim(prj, model, run, ny, nx, regrid=False):
    a2freq= zeros([ny,nx],float32)
    for [Year,Mon] in lYM:
        baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
        oDir    = os.path.join(baseDir, "clim.loc.c",prj,model,run)
        util.mk_dir(oDir)
        filePath= os.path.join(oDir, "freq.%04d.%02d.%dx%d"%(Year, Mon, ny, nx))
        a2in    = fromfile(filePath, float32).reshape(ny,nx)
        a2freq  = a2freq + a2in
    
    a2freq = a2freq / len(lYM)
    if regrid == True:
        a2freq = us.upscale(a2freq, pergrid=True)
    return a2freq

def regional_freq(a2freq, BBox):
    lllat, lllon = BBox[0]
    urlat, urlon = BBox[1]
    iy  = bisect_left(ioHap.Lat, lllat)
    ey  = bisect_left(ioHap.Lat, urlat)
    ix  = bisect_left(ioHap.Lon, lllon)
    ex  = bisect_left(ioHap.Lon, urlon)

    return a2freq[iy:ey+1,ix:ex+1].mean()


lBBox  = [
          [[30,120],[60,240]]
          ,[[30,270],[60,359]]
          ,[[30,0.5],[60,120]]
          ,[[-60,0.5],[-30,359.5]]
         ]
dlfreq = {}
da2dat = {}
# Ref
a2ref  = load_clim(prjRef, modelRef, runRef, nyRef, nxRef, regrid=True)
da2dat["ref"]  = a2ref
dlfreq["ref"]  = []
for bbox in lBBox:
    dlfreq["ref"].append(regional_freq(a2ref, bbox))

# Happi
lrate = ["org"]
#lrate = []
for rate in lrate:
    if rate == "org":
      run = "C20-ALL-001"
    else:
      run = "C20-ALL-001-%s"%(rate)
    print run
    a2hap  = load_clim(prj, model, run, nyHap, nxHap, regrid=False)
    da2dat[rate]   = a2hap
    dlfreq[rate]   = []
    for bbox in lBBox:
        dlfreq[rate].append(regional_freq(a2hap, bbox))

# sout
sout = "," + ",".join(["[[%f.1 %f.1][%f.1 %f.1]]"%(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]) for bbox in lBBox]) +"\n"
sout = sout + "Ref," + ",".join(map(str,dlfreq["ref"])) + "\n"
for rate in lrate:
    lfreq= dlfreq[rate]
    sout = sout + "%s,"%(rate) + ",".join(map(str, dlfreq[rate])) +"\n"

# Write
baseDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
oDir     = os.path.join(baseDir, "tune")
util.mk_dir(oDir)
filePath = os.path.join(oDir, "tune.c.csv")

f=open(filePath,"w"); f.write(sout); f.close()
print filePath


# Draw Map
if figflag != True: sys.exit()
for rate in ["ref"]+lrate:
    figname = oDir + "/freq.c.%s.png"%(rate)
    cmap    = "gist_stern_r"
    stitle  = "%s"%(rate)
    Fig.DrawMapSimple(da2dat[rate], LatHap, LonHap, vmax=0.005, cmap=cmap, figname=figname, stitle=stitle)
