import matplotlib
matplotlib.use("Agg")
from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
from myfunc.regrid  import Regrid
from myfunc.fig     import Fig
from bisect         import bisect_left
import HAPPI_detect_func as hd_func
import os, sys
import calendar
import myfunc.util as util
import f_draw_mapglobal
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

#prj     = "JRA55"
prj     = "HAPPI"
season  = "ALL"

lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion    = ["CEU","NEU"]

modelRef   = "__"
runRef     = "__"
scenRef    = "__"
resRef     = "145x288"
ioRef      = IO_Master.IO_Master("JRA55", modelRef, runRef, resRef)
nyRef      = ioRef.ny
nxRef      = ioRef.nx
LatRef     = ioRef.Lat
LonRef     = ioRef.Lon

modelHap   = "MIROC5"
scenHap    = "ALL"
#scenHap    = "P15"
#scenHap    = "P20"
lens    = range(1,50+1)
expr       = "C20"
runTmp     = "C20-ALL-001"
resHap     = "128x256"
ioHap  = IO_Master.IO_Master("HAPPI", modelHap, runTmp, resHap)
nyHap  = ioHap.ny
nxHap  = ioHap.nx
LatHap = ioHap.Lat
LonHap = ioHap.Lon

Lat  = LatHap  # Used for fig
Lon  = LonHap

if prj == "JRA55":
    model=modelRef
    run  = runRef
    res  = resRef
    scen = scenRef
    io   = ioRef
    ny   = nyRef
    nx   = nxRef

elif prj == "HAPPI":
    model=modelHap
    res  = resHap
    scen = scenHap
    io   = ioHap
    ny   = nyHap
    nx   = nxHap


miss = -9999.

# Draw Map
baseDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
oDir     = os.path.join(baseDir, "fig")
util.mk_dir(oDir)
figname = oDir + "/map.IPCC.Region.png"
cbarname= oDir + "/cbar.IPCC.Region.png"

vmin    = 0
vmax    = 10
a2out   = ones([nyHap,nxHap],float32)*miss
a2hatch = ones([nyHap,nxHap],float32)*miss
stitle  =""
f_draw_mapglobal.draw_map_robin(a2out, a2hatch, Lat, Lon, cmap="gist_stern_r", vmin=vmin, vmax=vmax, figPath=figname, cbarPath=cbarname, cbarOrientation="horizontal", lregion=lregion, stitle=stitle, seaMask=True)
