from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys, inspect
import calendar
import myfunc.util as util
import myfunc.fig  as fig
import myfunc.IO.HAPPI as HAPPI
import myfunc.grids as grids
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
## Config ------------------------------------------------
#configPath= os.path.dirname(os.path.abspath(__file__)) + "/config"
##f = open(configPath, "r")
##lines = f.readlines()
##for line in lines:
##    if line.split(":")[0].strip()=="detectName":
##        detectName = line.split(":")[1].strip()
#
#cfg         = SafeConfigParser(os.environ)
#cfg.read(configPath)
#cfg._sections["Defaults"]
#detectName  = cfg.get("Defaults","detectName")
#config_func = import_module("%s.config_func"%(detectName))
#Tag         = import_module("%s.Tag"%(detectName))
##--------------------------------------------------------

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
res     = "128x256"
noleap  = True
ny, nx  = 128, 256


dieYear = {"JRA":(2006, 2014)
         ,"NAT": (2006, 2015)
         ,"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

season = "ALL"

miss  = -9999.
hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="ALL", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon


#----------------------
def ret_gridarea(model):
    if model=="MIROC5":
        srcPath = "/data4/common/HAPPI/MIROC5/MIROC5.area.float32.128x256"
    else:
        print "check model",model
        sys.exit()
    aOut = fromfile(srcPath, float32).reshape(ny,nx)
    return aOut

def ret_regionmask(regiontype, region, lndsea=None):
    if regiontype=="IPCC":
        a2region= hd_func.ret_a2region_ipcc(region, ny, nx)
    elif regiontype=="JPN":
        BBox    = hd_func.ret_regionBBox(region)
        a2region= grids.mk_mask_BBox(Lat, Lon, BBox)
    else:
        print "check regiontype",regiontype
        print "by",__file__
        print inspect.currentframe().f_code.co_name
        sys.exit()

    if   lndsea == None:
        pass
    elif lndsea == "lnd":
        a2lndfrc = hp.load_const("lndfrc") 
        a2region = ma.masked_where(a2lndfrc <0.1, a2region).filled(0.)
    elif lndsea == "sea":
        a2lndfrc = hp.load_const("lndfrc") 
        a2region = ma.masked_where(a2lndfrc >=0.1, a2region).filled(0.)
    else:
        print "check lndsea",lndsea
        print "must be None / lnd / sea"
        print "by",__file__
        print inspect.currentframe().f_code.co_name
        sys.exit()

    return a2region


#----------------------
def load_clim(model,expr,scen,ens,var,iYear,eYear):
    hp(model, expr, scen, ens)
    nYear = eYear-iYear+1
    a3dat = empty([nYear,ny,nx])
    for i,Year in enumerate(range(iYear,eYear+1)):
        a3dat[i] = hp.load_Year(var,Year)
    return a3dat.mean(axis=0)


#----------------------
def load_da1dat(**kwargs):
    var        = kwargs["var"]
    scen       = kwargs["scen"]
    regiontype = kwargs["regiontype"]
    lregion    = kwargs["lregion"]
    lens       = kwargs["lens"]
    lndsea     = kwargs["lndsea"]
    nens       = len(lens)

    a2gridarea   = ret_gridarea(model)/1.e+9

    iYear,eYear = dieYear[scen]
    #- load data ------
    Dat = empty([len(lens),ny,nx])
    for iens,ens in enumerate(lens):
        hp(model, expr, scen, ens)
        Dat[iens] = load_clim(model,expr,scen,ens,var,iYear,eYear)


    da1dat = {}
    for region in lregion:
        a2region = ret_regionmask(regiontype,region,lndsea)

        # GRID AREA WEIGHTING ---
        a2gridarea_tmp = ma.masked_where(a2region==0, a2gridarea)
        a2wgt = a2gridarea_tmp / a2gridarea_tmp.sum()
        #------------------------

        a1dat = [ma.masked_where(a2region==0., Dat[i]*a2wgt).sum()
        #a1dat = [ma.masked_where(a2region==0., Dat[i]).mean()
                for i in range(len(lens))]
        da1dat[region] = a1dat
     
    return da1dat


