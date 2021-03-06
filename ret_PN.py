from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys, inspect
import calendar
import myfunc.util as util
import myfunc.fig  as fig
import myfunc.IO.HAPPI as HAPPI
import myfunc.IO.JRA55 as JRA55
import myfunc.grids as grids
import HAPPI_detect_func as hd_func
import HAPPI_detect_fig  as hd_fig
import scipy.stats
# Config ------------------------------------------------
configPath= os.path.dirname(os.path.abspath(__file__)) + "/config"
#f = open(configPath, "r")
#lines = f.readlines()
#for line in lines:
#    if line.split(":")[0].strip()=="detectName":
#        detectName = line.split(":")[1].strip()

cfg         = SafeConfigParser(os.environ)
cfg.read(configPath)
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
res     = "128x256"
noleap  = True
ny, nx  = 128, 256


dieYear = {"JRA":(2006, 2014)
         ,"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

season = "ALL"
#season = 1

ddtype = {"sum":"float32", "num":"float32"}
#BBox  = [[-80,0.0],[80,360]]
miss  = -9999.
hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="ALL", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon


jra   = JRA55.Jra55()
LatJRA= jra.Lat
LonJRA= jra.Lon
#----------------------
def ret_gridarea(model):
    if model=="MIROC5":
        srcPath = "/data4/common/HAPPI/MIROC5/MIROC5.area.float32.128x256"
    else:
        print "check model",model
        sys.exit()
    aOut = fromfile(srcPath, float32).reshape(ny,nx)
    return aOut



def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

def calc_totaltimes(iYear,eYear,season):
    n = 0
    for Year in range(iYear,eYear+1):
        for Mon in util.ret_lmon(season):
            iDay = 1
            eDay = calendar.monthrange(Year,Mon)[1]

            iDTime = datetime(Year,Mon,iDay,0)
            eDTime = datetime(Year,Mon,eDay,18)
            dDTime = timedelta(hours=6)
            lDTime = util.ret_lDTime_noleap(iDTime, eDTime, dDTime)
            n      = n + len(lDTime)
    return n



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
        #a2region = ma.masked_where(a2lndfrc ==0.0, a2region).filled(0.)
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
def main(**kwargs):

    tag        = kwargs["tag"]
    scen       = kwargs["scen"]
    thpr       = kwargs["thpr"]
    regiontype = kwargs["regiontype"]
    lregion    = kwargs["lregion"]
    lens       = kwargs["lens"]
    lndsea     = kwargs["lndsea"]
    nens       = len(lens)

    a2gridarea   = ret_gridarea(model)/1.e+9

    sthpr= ret_sthpr(thpr)
    da1prcp = {}
    da1freq = {}
    da1pint = {}
    
    if scen !="JRA":
        iYear, eYear = dieYear[scen]
        nYear = eYear - iYear +1
        totaltimes = calc_totaltimes(iYear,eYear,season)
        a3sum = empty([len(lens),ny,nx],float32)
        a3num = empty([len(lens),ny,nx],float32)
        for iens, ens in enumerate(lens):
            run = "%s-%s-%03d"%(expr, scen, ens)
    
            #- Load ---
    
            baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
    
            baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
    
            a3sum[iens] = fromfile(sumPath, float32).reshape(ny,nx)
            a3num[iens] = fromfile(numPath, float32).reshape(ny,nx)
    
    
        # Regional values
        a3prcp = a3sum / nYear * 60*60*6   # mm/season
        a3freq = a3num / float(totaltimes)
        a3pint = ma.masked_invalid(a3sum / a3num)*60*60 # mm/h
    
        for region in lregion:
            #a2region = hd_func.ret_a2region_ipcc(region, ny, nx)
            a2region = ret_regionmask(regiontype,region,lndsea)
            # GRID AREA WEIGHTING ---
            a2gridarea_tmp = ma.masked_where(a2region==0, a2gridarea)
            a2wgt = a2gridarea_tmp / a2gridarea_tmp.sum()
            #------------------------
            #a1prcp = [ma.masked_where(a2region==0., a3prcp[i]).mean()
            a1prcp = [ma.masked_where(a2region==0., a3prcp[i]*a2wgt).sum()
                    for i in range(len(lens))]
    
            #a1freq = [ma.masked_where(a2region==0., a3freq[i]).mean()
            a1freq = [ma.masked_where(a2region==0., a3freq[i]*a2wgt).sum()
                    for i in range(len(lens))]
    
            
            #a1pint = [ma.masked_where(a2region==0., a3pint[i]).mean()
            a1pint = [ma.masked_where(a2region==0., a3pint[i]*a2wgt).sum()
                    for i in range(len(lens))]
    
    
            da1prcp[region] = ma.masked_invalid(array(a1prcp)).filled(0.0)
            da1freq[region] = ma.masked_invalid(array(a1freq)).filled(0.0)
            da1pint[region] = ma.masked_invalid(array(a1pint)).filled(0.0)
    
    elif scen =="JRA":
        iYear, eYear = dieYear[scen]
        nYear = eYear - iYear +1
        totaltimes = calc_totaltimes(iYear,eYear,season)
    
        # JRA55
        jrasum ={}
        jranum ={}
    
        baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
        
        baseDir, sDir, numPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
        
        a2sum = fromfile(sumPath, float32).reshape(145,288)
        a2num = fromfile(numPath, float32  ).reshape(145,288)
    
        jrasum[tag] = a2sum
        jranum[tag] = a2num
     
        # Regional values
        a2prcp = a2sum / nYear * 60*60*6   # mm/season
        a2freq = a2num / float(totaltimes)
        a2pint = ma.masked_invalid(a2sum / a2num) *60*60 # mm/h
        
        for region in lregion:
            if regiontype=="IPCC":
                a2region = hd_func.ret_a2region_ipcc(region, 145, 288)
            elif regiontype=="JPN":
                BBox    = hd_func.ret_regionBBox(region)
                a2region= grids.mk_mask_BBox(LatJRA, LonJRA, BBox)
    
            # GRID AREA WEIGHTING ---
            a2gridarea_tmp = ma.masked_where(a2region==0, a2gridarea)
            a2wgt = a2gridarea_tmp / a2gridarea_tmp.sum()
            #------------------------
    
            #prcp = ma.masked_where(a2region==0., a2prcp).mean()
            #freq = ma.masked_where(a2region==0., a2freq).mean()
            #pint = ma.masked_where(a2region==0., a2pint).mean()

            prcp = ma.masked_where(a2region==0., a2prcp*a2wgt).sum()
            freq = ma.masked_where(a2region==0., a2freq*a2wgt).sum()
            pint = ma.masked_where(a2region==0., a2pint*a2wgt).sum()
 
    
            da1prcp[region] = array([prcp]*len(lens))
            da1freq[region] = array([freq]*len(lens))
            da1pint[region] = array([pint]*len(lens))
    

    #-- return --------------
    return da1prcp, da1freq, da1pint





def load_Freq(**kwargs):

    tag        = kwargs["tag"]
    scen       = kwargs["scen"]
    thpr       = kwargs["thpr"]
    regiontype = kwargs["regiontype"]
    lregion    = kwargs["lregion"]
    lens       = kwargs["lens"]
    lndsea     = kwargs["lndsea"]
    nens       = len(lens)

    a2gridarea   = ret_gridarea(model)/1.e+9
    a2wgt        = a2gridarea / a2gridarea.sum()

    sumnum = "num"
    dtype  = {"sum":float32, "num":float32}[sumnum]
    sthpr= ret_sthpr(thpr)
    da1freq = {}

    if scen !="JRA":
        iYear, eYear = dieYear[scen]
        nYear = eYear - iYear +1
        totaltimes = calc_totaltimes(iYear,eYear,season)
        a3var = empty([len(lens),ny,nx],float32)
        for iens, ens in enumerate(lens):
            run = "%s-%s-%03d"%(expr, scen, ens)
    
            #- Load ---
            baseDir, sDir, varPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum=sumnum)
    
            a3var[iens] = fromfile(varPath, dtype=dtype).reshape(ny,nx)
    
        # Regional values
        a3freq = a3var / float(totaltimes)
    
        for region in lregion:
            #a2region = hd_func.ret_a2region_ipcc(region, ny, nx)
            a2region = ret_regionmask(regiontype,region,lndsea)

            # GRID AREA WEIGHTING ---
            a2gridarea_tmp = ma.masked_where(a2region==0, a2gridarea)
            a2wgt = a2gridarea_tmp / a2gridarea_tmp.sum()
            #------------------------
    
            #a1freq = [ma.masked_where(a2region==0., a3freq[i]).mean()
            a1freq = [ma.masked_where(a2region==0., a3freq[i]*a2wgt).sum()
                    for i in range(len(lens))]
    
            da1freq[region] = ma.masked_invalid(array(a1freq)).filled(0.0)

    
    elif scen =="JRA":
        iYear, eYear = dieYear[scen]
        nYear = eYear - iYear +1
        totaltimes = calc_totaltimes(iYear,eYear,season)
    
        # JRA55
        jravar ={}
    
        baseDir, sDir, varPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum=sumnum)
        
        a2var = fromfile(sumPath, dtype=dtype).reshape(145,288)
    
        jravar[tag] = a2var
     
        # Regional values
        a2freq = a2var / float(totaltimes)
        
        for region in lregion:
            if regiontype=="IPCC":
                a2region = hd_func.ret_a2region_ipcc(region, 145, 288)
            elif regiontype=="JPN":
                BBox    = hd_func.ret_regionBBox(region)
                a2region= grids.mk_mask_BBox(LatJRA, LonJRA, BBox)
    
            # GRID AREA WEIGHTING ---
            a2gridarea_tmp = ma.masked_where(a2region==0, a2gridarea)
            a2wgt = a2gridarea_tmp / a2gridarea_tmp.sum()
            #------------------------
    
            #freq = ma.masked_where(a2region==0., a2freq).mean()
            freq = ma.masked_where(a2region==0., a2freq*a2wgt).sum()
    
            da1freq[region] = array([freq]*len(lens))
    

    #-- return --------------
    return da1freq
