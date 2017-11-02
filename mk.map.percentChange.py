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


#lkey   = [[1,"plain","ptot"]]
#lkey   = [[1,"tc","ptot"]]
#lkey1   = [[1,tag,"ptot"] for tag in ["plain","tc","cf","ms","ot"]]
#lkey2   = [[1,tag,"pint"] for tag in ["plain","tc","cf","ms","ot"]]
#lkey3   = [[1,tag,"freq"] for tag in ["plain","tc","cf","ms","ot"]]
lkey   = [["p99.990",tag,"freq"] for tag in ["plain","tc","cf","ms","ot"]]
#lkey   = [[1,tag,"freq"] for tag in ["tc","cf","ms","ot"]]
#lkey   = [[1,tag,"frac.ptot"] for tag in ["tc","cf","ms","ot"]]
#lkey   = [["p99.990",tag,"frac.ptot"] for tag in ["tc","cf","ms","ot"]]
#lkey   = [["p99.990",tag,"frac.freq"] for tag in ["tc","cf","ms","ot"]]
#lkey   = [["p99.990",tag,"freq"] for tag in ["tc","cf","ms","ot"]]
#lkey   = [[1,"plain","ptot"],[1,"plain","freq"],[1,"plain","pint"]]
#lkey   = [[1,"plain","freq"],[1,"plain","pint"]]
#lkey   = [[1,"plain","freq"],[1,"plain","pint"]]
#lkey   = [["p99.900","plain","freq"],["p99.990","plain","freq"]]

#lkey = lkey1 + lkey2 + lkey3


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
for [thpr, tag, var] in lkey:
    llscen = [["ALL","P15"],["ALL","P20"],["P15","P20"]]
    #llscen = [["ALL","P20"]]
    for lscen in llscen:
        season = "ALL"
        scen0  = lscen[0]
        scen1  = lscen[1]
        # Check statistical Difference (Welch's t-test)
        a3var0 = load_var_3D(scen0,lens, tag, var, thpr)
        a3var1 = load_var_3D(scen1,lens, tag, var, thpr)


        # Mask --------
        a3var0 = ma.masked_invalid(a3var0)
        a3var1 = ma.masked_invalid(a3var1)

        #-------------- 
        a2t, a2p = scipy.stats.ttest_ind(a3var1, a3var0, axis=0, equal_var= False)
        
        a2hatch  = ma.masked_greater(a2p,0.05).filled(miss)

        a2hatch  = ma.masked_invalid(a2hatch).filled(miss)
        a2dif    = (a3var1.mean(axis=0) - a3var0.mean(axis=0))/a3var0.mean(axis=0)*100.

        # Mask for Pint
        if var == "pint":
            a3ptot = load_var_3D(scen0,lens, tag, "ptot", thpr)
            print a3ptot[0]
            a2ptot = a3ptot.mean(axis=0)
            a2dif  = ma.masked_where(a2ptot<100., a2dif).filled(0.0)
            a2hatch= ma.masked_where(a2ptot<100., a2hatch).filled(miss)

        # Figure ********************
        figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
        figPath = os.path.join(figDir,"map.pctChng.%s.%s.%s-%s.th.%s.%s.png"%(tag,var,scen1,scen0,thpr,season))
        cbarPath= os.path.join(figDir,"cbar.map.pctChng.%s.%s.th.%s.png"%(tag,var,thpr))
        
        util.mk_dir(figDir)
        # title
        #dtag={ "plain":""
        #     ,"tc":"tropical cyclones"
        #     ,"cf":"extratropical cyclones"
        #     ,"ms":"monsoon"
        #     ,"ot":"others"
        #     }
    
        stitle  = "dif[%%] %s %s %s-%s th=%s"%(tag,var,scen1,scen0,thpr)
        
        if   (thpr==1):
            bnd = None
            vmin, vmax= -20, 20
            a2mask = None
        elif   (thpr in ["p99.900","p99.990"]):
            bnd = None
            vmin, vmax= -150, 150
            a2mask = None
        else:
            bnd = None
            vmin, vmax= -150, 150
            a2mask = None



        cmap   = "RdBu_r"
        #hd_fig.DrawMap_dotshade(a2dif, a2dot, Lat, Lon, bnd=bnd, figname=figPath, cbarname=cbarPath, dotstep=2, markersize=0.2, stitle=stitle) 
        f_draw_mapglobal.draw_map_robin(a2dat=a2dif, a2hatch=a2hatch, Lat=Lat, Lon=Lon, miss=-9999, bnd=bnd, cmap=cmap, vmin=vmin, vmax=vmax, figPath=figPath, cbarPath=cbarPath, cbarOrientation="vertical",lregion=lregion,stitle=stitle, seaMask=True) 
