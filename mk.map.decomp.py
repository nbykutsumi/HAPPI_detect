import matplotlib as mpl
mpl.use("Agg")
from numpy import *
from datetime       import datetime, timedelta
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
import f_draw_mapglobal

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
lens    = range(1,50)
#lens    = range(1,3)
res     = "128x256"
ny, nx  = 128, 256
miss    = -9999.

llscen = [["ALL","P15"],["ALL","P20"],["P15","P20"]]
#llscen = [["ALL","P15"],["P15","P20"]]
#llscen = [["ALL","P20"]]



lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion     = ["SAU"]

dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="P15", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon

"""
[['Alaska/N.W. Canada [ALA:1]', 'ALA', 'land'],
 ['Amazon [AMZ:7]', 'AMZ', 'land'],
 ['Central America/Mexico [CAM:6]', 'CAM', 'land'],
 ['small islands regions Caribbean', 'CAR*', 'all'],
 ['Central Asia [CAS:20]', 'CAS', 'land'],
 ['Central Europe [CEU:12]', 'CEU', 'land'],
 ['Canada/Greenland/Iceland [CGI:2]', 'CGI', 'land'],
 ['Central North America [CNA:4]', 'CNA', 'land'],
 ['East Africa [EAF:16]', 'EAF', 'land'],
 ['East Asia [EAS:22]', 'EAS', 'land'],
 ['East North America [ENA:5]', 'ENA', 'land'],
 ['South Europe/Mediterranean [MED:13]', 'MED', 'land'],
 ['North Asia [NAS:18]', 'NAS', 'land'],
 ['North Australia [NAU:25]', 'NAU', 'land'],
 ['North-East Brazil [NEB:8]', 'NEB', 'land'],
 ['North Europe [NEU:11]', 'NEU', 'land'],
 ['Southern Africa [SAF:17]', 'SAF', 'land'],
 ['Sahara [SAH:14]', 'SAH', 'land'],
 ['South Asia [SAS:23]', 'SAS', 'land; sea'],
 ['South Australia/New Zealand [SAU:26]', 'SAU', 'land'],
 ['Southeast Asia [SEA:24]', 'SEA', 'land; sea'],
 ['Southeastern South America [SSA:10]', 'SSA', 'land'],
 ['Tibetan Plateau [TIB:21]', 'TIB', 'land'],
 ['West Africa [WAF:15]', 'WAF', 'land'],
 ['West Asia [WAS:19]', 'WAS', 'land'],
 ['West North America [WNA:3]', 'WNA', 'land'],
 ['West Coast South America [WSA:9]', 'WSA', 'land'],
 ['Antarctica', 'ANT*', 'land; sea'],
 ['Arctic', 'ARC*', 'land; sea'],
 ['Pacific Islands region[2]', 'NTP*', 'all'],
 ['Southern Topical Pacific', 'STP*', 'all'],
 ['Pacific Islands region[3]', 'ETP*', 'all'],
 ['West Indian Ocean', 'WIO*', 'all']]
"""


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


#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr


def load_var_single(scen, ens, tag, var, thpr):
    dattype = {"sum":float32, "num":int32, "ptot":float32}
    run = "%s-%s-%03d"%(expr, scen, ens)
    iYear, eYear = dieYear[scen]
    nYear = eYear - iYear +1

    sthpr = ret_sthpr(thpr)
    if var in ["sum","num"]:
        baseDir, sDir, sPath = hd_func.path_sumnum_clim(model=model, run=run, res=res, sthpr=sthpr, tag=tag, iYear=iYear, eYear=eYear, season=season, sumnum=var)
        return fromfile(sPath, dattype[var]).reshape(ny,nx)

    elif var == "ptot":
        a2sum = load_var_single(scen, ens, tag, "sum", thpr)
        a2out = a2sum *60*60*6 / nYear  # mm/season
        return a2out


    elif var == "freq":
        totalnum = calc_totaltimes(iYear,eYear,season)
        a2num = load_var_single(scen,ens,tag, "num", thpr)
        a2out = a2num / float(nYear)   # times per season
        return a2out

    elif var == "pint":
        totalnum = calc_totaltimes(iYear,eYear,season)
        a2sum = load_var_single(scen,ens,tag, "sum", thpr)
        a2num = load_var_single(scen,ens,tag, "num", thpr)
        a2out = a2sum / a2num * 60*60*24.  #[mm/day]
        return a2out

    elif var == "frac.ptot":
        a2all = load_var_single(scen,ens,"plain","ptot",thpr)
        a2tag = load_var_single(scen,ens,tag    ,"ptot",thpr)
        a2out = a2tag / a2all
        return a2out

    elif var == "frac.freq":
        a2all = load_var_single(scen,ens,"plain","freq",thpr)
        a2tag = load_var_single(scen,ens,tag    ,"freq",thpr)
        a2out = a2tag / a2all
        return a2out


def load_var_3D(scen, lens, tag, var, thpr):
    nens  = len(lens)
    a3var = empty([nens, ny, nx])
    for iens, ens in enumerate(lens):
        a3var[iens] = load_var_single(scen, ens, tag, var, thpr)
    return a3var



#--------------------------------------
ltag  = ["plain","tc","cf","ms","ot"]
#ltag  = ["tc"]
thpr  = 1
for tag in ltag:
    for lscen in llscen:
        season = "ALL"
        scen0  = lscen[0]
        scen1  = lscen[1]

        # Decomposition
        a3N0 = load_var_3D(scen0,lens, tag, "freq", thpr)    #[# of 6hr]
        a3N1 = load_var_3D(scen1,lens, tag, "freq", thpr)    #[# of 6hr]
        a3I0 = load_var_3D(scen0,lens, tag, "pint", thpr)/4. #[mm/6hr]
        a3I1 = load_var_3D(scen1,lens, tag, "pint", thpr)/4. #[mm/6hr]

        a3I0 = ma.masked_invalid(a3I0)
        a3I1 = ma.masked_invalid(a3I1)

        a2N0 = a3N0.mean(axis=0)
        a2I0 = a3I0.mean(axis=0)
        a2dN = a3N1.mean(axis=0)-a3N0.mean(axis=0)
        a2dI = a3I1.mean(axis=0)-a3I0.mean(axis=0)

        a2dNI = a2dN * a2I0
        a2NdI = a2N0 * a2dI
        a2dNdI= a2dN * a2dI

        # Mask --------
        a2dNI = ma.masked_invalid(a2dNI).filled(0.0)
        a2NdI = ma.masked_invalid(a2NdI).filled(0.0)
        a2dNdI= ma.masked_invalid(a2dNdI).filled(0.0)

        #-------------- 
        for var in ["dNI","NdI","dNdI"]:
            if   var == "dNI":
                a2var = a2dNI
                a3key0= a3N0
                a3key1= a3N1

            elif var == "NdI":
                a2var = a2NdI
                a3key0= a3I0
                a3key1= a3I1

            elif var == "dNdI":
                a2var = a2dNdI


            # Check statistical Difference (Welch's t-test)
            #if var in ["dNI","NdI"]:
            #    a2t, a2p = scipy.stats.ttest_ind(a3key1, a3key0, axis=0, equal_var= False)
            #    a2hatch  = ma.masked_greater(a2p,0.05).filled(miss)
            #else:
            #    a2hatch  = None

            a2hatch  = None
    
            # Figure ********************
            figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
            figPath = os.path.join(figDir,"map.decomp.%s.%s.%s-%s.th.%s.%s.png"%(tag,var,scen1,scen0,thpr,season))
            cbarPath= os.path.join(figDir,"cbar.map.decomp.th.%s.png"%(thpr))
            
            util.mk_dir(figDir)
        
            stitle  = "decomp %s %s %s-%s th=%s"%(tag,var,scen1,scen0,thpr)
            
            #bnd = arange(-120,120+0.001,10)
            bnd = None
            vmin, vmax= -120, 120
    
    
            cmap   = "RdBu_r"
            f_draw_mapglobal.draw_map_robin(a2dat=a2var, a2hatch=a2hatch, Lat=Lat, Lon=Lon, miss=-9999, bnd=bnd, cmap=cmap, vmin=vmin, vmax=vmax, figPath=figPath, cbarPath=cbarPath, cbarOrientation="vertical",lregion=lregion,stitle=stitle) 
