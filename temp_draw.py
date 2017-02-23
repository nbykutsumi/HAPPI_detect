from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.fig  as fig
import myfunc.IO.HAPPI as HAPPI
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------
prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
lscen   = ["P20"]
#lscen   = ["P15","P20"]
lens    = [1,1,1]
nens    = len(lens)
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

#ltag  = ["tc","cf","ms","ot"]
ltag   = []
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

iYear_his, eYear_his = 2006, 2015
iYear_fut, eYear_fut = 2106, 2115
#iYear_his, eYear_his = 2006, 2006
#iYear_fut, eYear_fut = 2106, 2106
#season = "ALL"
season = "ALL"
#season = 1

lthpr = [0.5]
ddtype = {"sum":"float32", "num":"int32"}
hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="P15", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon
BBox  = [[-80,0.0],[80,360]]
miss  = -9999.
#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr

#----------------------

a0    = fromfile("./temp.ALL.128x256",float32).reshape(ny,nx)
a1    = fromfile("./temp.P20.128x256",float32).reshape(ny,nx)

a2var = (a1 - a0)*60*60*24*365
a2sig = ones([ny,nx],float32)

bnd  = [-200,-150,-100,-50,-20,20,50,100,150,200]
cmap = "RdBu"

figname= "./temp.d.P20.png"
hd_fig.DrawMap_dotshade(a2in=a2var, a2dot=a2sig, a1lat=Lat, a1lon=Lon, BBox=BBox, bnd=bnd, cmap=cmap, figname=figname, dotstep=5, dotcolor="0.8")





