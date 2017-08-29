import matplotlib as mpl
mpl.use("Agg")
import ret_PN
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func
import f_draw_hist
from numpy import *

prj        = "HAPPI"
expr       = "C20"
model      = "MIROC5"
res        = "128x256"

#regiontype = "JPN"
#lregion    = ["GLB","JPN","S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]

regiontype = "IPCC"
#lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
lregion    = ["EAS"]



#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lthpr      = [0,"p99.900","p99.990"]
#lthpr      = ["p99.900","p99.990"]
lscen      = ["ALL","P15","P20"]
ltag       = ["plain","tc","cf","ms","ot"]
wbar       = 0.8
yfontsize  = 17
ny,nx      = 128, 256
miss       = -9999.
dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }


season     = "ALL"
#---------------------------------    
# Dirs
iYear_fut, eYear_fut = dieYear["P20"]
run  = "C20-P15-001"
baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=0, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]
figDir  = baseDir + "/fig"
#**********************************
#"""
thpr = 0
lvartype   = ["Ptot","Freq","Pint"]
lkey  = [[scen,tag] for scen in lscen for tag in ltag]

Prcp = {}
Freq = {}
Pint = {}
for [scen,tag] in lkey:
    da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    #print scen,tag,da1prcp

    for region in lregion:
        Prcp[region,tag,scen] = da1prcp[region]
        Freq[region,tag,scen] = da1freq[region]*4*365
        Pint[region,tag,scen] = da1pint[region]


for vartype in lvartype:
    if   vartype == "Ptot":
        Var = Prcp
    elif vartype == "Freq":
        Var = Freq
    elif vartype == "Pint":
        Var = Pint
        
    for region in lregion:
        for tag in ltag:

            #--- title ----------
            stitle1 = region
            stitle2 = "%s %s %s %s"%(vartype, thpr, region, tag)

            # Path
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Var[region,tag,scen])

            # Draw
            f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)
#"""

#**********************************
"""
lthpr  = ["p99.900","p99.990"]
vartype="Freq"
for thpr in lthpr:
    lkey  = [[scen,tag] for scen in lscen for tag in ltag]
    
    Freq   = {}
    for [scen,tag] in lkey:
        da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
        #print scen,tag,da1prcp
 
        for region in lregion:
            Freq[region,tag,scen] = da1freq[region]*4*365

    Var  = Freq
    for region in lregion:
        for tag in ltag:

            #--- title ----------
            stitle1 = region
            stitle2 = "%s %s %s %s"%(vartype, thpr, region, tag)

            # Path
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Var[region,tag,scen])

            # Draw
            f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)

"""


"""
#**********************************
# Proportion to all precip

lthpr  = ["p99.900","p99.990"]
vartype="Freq"
for thpr in lthpr:
    lkey  = [[scen,tag] for scen in lscen for tag in ltag]
    
    Var  = {}
    Frac = {}
    for [scen,tag] in lkey:
        da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
        #print scen,tag,da1prcp
 
        for region in lregion:
            if vartype=="Freq":
                Var[region,tag,scen] = da1freq[region]
            elif vartype=="Ptot":
                Var[region,tag,scen] = da1prcp[region]


    for [scen,tag] in lkey:
        for region in lregion:
            Frac[region,tag,scen] = ma.masked_invalid(Var[region,tag,scen]/Var[region,"plain",scen]).filled(0.0)


    Out = Frac
    for region in lregion:
        for tag in ltag:
            if tag == "plain":continue
            #--- title ----------
            stitle1 = region
            stitle2 = "Fraction %s %s %s %s"%(vartype, thpr, region, tag)

            # Path
            figPath = figDir  + "/hist.Fraction.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Out[region,tag,scen])

            # Draw
            f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)

"""


"""
#**********************************
# extreme values (99.9 & 99.99 percentiles)

lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    Var  = {}
    for region in lregion:
        for scen in lscen:
            Var[region,scen] = []

    for scen in lscen:        
        for ens in lens:
            sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile/%s"%(scen)
            sPath = sDir + "/%s.%s.%s.%s.%03d.%s.%dx%d"%(prj,model,expr, scen, ens, thpr, ny, nx)
            a2thpr = fromfile(sPath, float32).reshape(ny,nx)*60*60*24
    
            for region in lregion:
                a2region = ret_PN.ret_regionmask(regiontype, region, lndsea="lnd")
                ptile    = ma.masked_where(a2region==miss, a2thpr).mean()
                Var[region,scen].append(ptile)


    Out = Var
    for region in lregion:
        #--- title ----------
        stitle1 = region
        stitle2 = "%s %s"%(thpr, region)

        # Path
        figPath = figDir  + "/hist.ptile.th.%s.%s.png"%(thpr, region)

        # Data
        ldat = []
        for scen in lscen:
            ldat.append(array(Out[region,scen]))


        # Draw
        f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)

"""
   
