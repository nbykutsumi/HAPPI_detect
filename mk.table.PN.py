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
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------
regiontype = "JPN"
lregion = ["S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]

#regiontype = "IPCC"
#lregion = ["EAS","SEA"]

#lthpr = [0.0]
lthpr = ["p99.900"]


prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
#lscen   = ["ALL"]
lscen   = ["JRA","ALL","P15","P20"]
lens    = [1,1,1,1,1]
nens    = len(lens)
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

ltag  = ["tc","cf","ms","ot"]
#ltag   = []
ltag_ws  = [tag for tag in ltag if tag !="ot"]
ltag_2nd = ["ms"]

dieYear = {"JRA":(2006, 2014)
         ,"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

season = "ALL"
#season = 1

ddtype = {"sum":"float32", "num":"int32"}
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


def mk_csv(var, da1var, region):
    sPath = oDir + "/%s.%s.csv"%(var,region)

    lout  = util.join_list_cols(
        [da1var[tag, scen, region]
            for tag  in ["plain"]+ltag
            for scen in lscen 
        ])
             
    label1 = ["%s"%(scen) for tag in ["plain"]+ltag for scen in lscen]
    label1 = ",".join(label1) + "\n"

    label2 = ["%s"%(tag) for tag in ["plain"]+ltag for scen in lscen]
    label2 = ",".join(label2) + "\n"

    sout   = label1 + label2 + util.list2csv(lout)

    f=open(sPath,"w"); f.write(sout); f.close()
    print sPath


def ret_regionmask(regiontype, region):
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
    return a2region
#----------------------
lKey = [[scen, thpr] for scen in lscen for thpr in lthpr]

for thpr in lthpr:
    sthpr= ret_sthpr(thpr)
    da1prcp = {}
    da1freq = {}
    da1pint = {}

    for scen in lscen:
        if scen !="JRA":
            iYear, eYear = dieYear[scen]
            nYear = eYear - iYear +1
            totaltimes = calc_totaltimes(iYear,eYear,season)
        
            for tag in ltag + ["plain"]:
                a3sum = empty([len(lens),ny,nx],float32)
                a3num = empty([len(lens),ny,nx],int32)
                for iens, ens in enumerate(lens):
                    run = "%s-%s-%03d"%(expr, scen, ens)
        
                    #- Load ---
        
                    baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
        
                    baseDir, sDir, numPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
        
                    a3sum[iens] = fromfile(sumPath, float32).reshape(ny,nx)
                    a3num[iens] = fromfile(numPath, int32).reshape(ny,nx)


                    if (tag == "plain")&(scen=="ALL"):
                        tempsum = a3sum[iens]
                        tempnum = a3num[iens]
                        print tempnum.mean(), tempsum.mean()
       
                # Regional values
                a3prcp = a3sum / nYear * 60*60*6   # mm/season
                a3freq = a3num / float(totaltimes)
                a3pint = ma.masked_invalid(a3sum / a3num)*60*60 # mm/h
        
                for region in lregion:
                    #a2region = hd_func.ret_a2region_ipcc(region, ny, nx)
                    a2region = ret_regionmask(regiontype,region)
                    a1prcp = [ma.masked_where(a2region==0., a3prcp[i]).mean()
                            for i in range(len(lens))]
    
                    a1freq = [ma.masked_where(a2region==0., a3freq[i]).mean()
                            for i in range(len(lens))]
    
                    
                    a1pint = [ma.masked_where(a2region==0., a3pint[i]).mean()
                            for i in range(len(lens))]
    
    
                    da1prcp[tag, scen, region] = a1prcp
                    da1freq[tag, scen, region] = a1freq
                    da1pint[tag, scen, region] = a1pint

        elif scen =="JRA":
            iYear, eYear = dieYear[scen]
            nYear = eYear - iYear +1
            totaltimes = calc_totaltimes(iYear,eYear,season)

            # JRA55
            jrasum ={}
            jranum ={}

            for tag in ltag + ["plain"]:
                baseDir, sDir, sumPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="sum")
                
                baseDir, sDir, numPath = hd_func.path_sumnum_clim(model="__", run="__", res="145x288", sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum="num")
                
                a2sum = fromfile(sumPath, float32).reshape(145,288)
                a2num = fromfile(numPath, int32  ).reshape(145,288)

                jrasum[tag] = a2sum
                jranum[tag] = a2num
                if tag == "plain":
                    print "** JRA **"
                    print jranum[tag].mean(),jrasum[tag].mean()
         
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



                    prcp = ma.masked_where(a2region==0., a2prcp).mean()
                    freq = ma.masked_where(a2region==0., a2freq).mean()
                    pint = ma.masked_where(a2region==0., a2pint).mean()
        
                    da1prcp[tag, scen, region] = [prcp]*len(lens)
                    da1freq[tag, scen, region] = [freq]*len(lens)
                    da1pint[tag, scen, region] = [pint]*len(lens)

    #-- Write by Region ---------
    oDir= baseDir + "/csv"
    util.mk_dir(oDir)

    var   = "prcp"
    da1var= da1prcp

    for region in lregion:
        mk_csv("prcp", da1prcp, region)        
        mk_csv("freq", da1freq, region)        
        mk_csv("pint", da1pint, region)        

