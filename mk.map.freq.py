import matplotlib
matplotlib.use("Agg")
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

prj     = "JRA55"
#prj     = "HAPPI"
season  = "ALL"

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
lens    = range(1,50+1)
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


us     = Regrid.UpScale()
us(LatRef, LonRef, LatHap, LonHap, globflag=True)



dtag = {"tc":"tc", "c":"c", "fbc":"f","ms":"ms"}
dvmax= {"tc":0.003, "c":0.005, "fbc":0.1, "ms":0.6}
ltag = ["tc","c","fbc","ms"]

miss = -9999.

def load_clim(prj, model, run, tag, season, ny, nx):
    a2freq= zeros([ny,nx],float32)

    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
    oDir    = os.path.join(baseDir, "clim.loc.%s"%(tag),prj,model,run)
    filePath= os.path.join(oDir, "freq.%s.%dx%d"%(season, ny, nx))
    a2freq  = fromfile(filePath, float32).reshape(ny,nx)

    if prj=="JRA55":
        a2freq = us.upscale(a2freq, pergrid=True)


    return a2freq


for tag in ltag:
    if   prj == "JRA55":
        # Ref
        a2freq  = load_clim(prj, model, run, tag, season, ny, nx)
    
    elif prj == "HAPPI":    
        # Happi
        a2freq = zeros([ny,nx],float32)
        for ens in lens:
            run = "C20-%s-%03d"%(scen, ens)
            a2in  = load_clim(prj, model, run, tag, season, ny, nx)
            a2freq= a2freq + a2in
    
        a2freq = a2freq/float(len(lens))

    print a2freq.shape    
    
    # Draw Map
    baseDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
    oDir     = os.path.join(baseDir, "fig")
    util.mk_dir(oDir)
    figname = oDir + "/freq.%s.%s.%s.%s.%s.png"%(prj,model,scen,dtag[tag], season)
    cbarname= oDir + "/cbar.freq.%s.png"%(dtag[tag])

    cmap    = "gist_stern_r"
    stitle  = "frequency %s %s %s %s"%(prj, scen, dtag[tag],season)
    vmax    = dvmax[tag]
    #Fig.DrawMapSimple(a2in=a2freq, a1lat=Lat, a1lon=Lon, vmax=vmax, cmap=cmap, figname=figname, cbarname= cbarname, stitle=stitle)

    a2hatch = ones([nyHap,nxHap],float32)*miss
    f_draw_mapglobal.draw_map_robin(a2freq, a2hatch, Lat, Lon, cmap="gist_stern_r", vmax=vmax, figPath=figname, cbarPath=cbarname, cbarOrientation="vertical", stitle=stitle)
