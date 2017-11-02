import matplotlib as mpl
mpl.use("Agg")
import ret_PN
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func
import f_draw_bars
from numpy import *
import sys

prj        = "HAPPI"
expr       = "C20"
model      = "MIROC5"
res        = "128x256"

#regiontype = "JPN"
#lregion    = ["GLB","JPN","S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]

regiontype = "IPCC"
lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion    = ["CAM"]

llscen   = [["ALL","P15"],["ALL","P20"],["P15","P20"]]
#- Switch  ------------
Fraction = True
#----------------------
#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,2+1)

#lthpr  = [1,"p99.900","p99.990"]
#lthpr  = [1,"p99.990"]
#lthpr  = ["p99.990"]
#vartype="Ptot"
#lthpr  = ["p99.900","p99.990"]
lthpr  = ["p99.990"]
vartype="Freq"




#ltag       = ["plain","tc","cf","ms","ot"]
ltag       = ["tc","cf","ms","ot"]
ny,nx      = 128, 256
miss       = -9999.
dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

dTagName   = {"plain":"All","tc":"TC","cf":"ExC","ms":"MS","ot":"OT"}
season     = "ALL"

dregInfo   = hd_func.dict_IPCC_codeKey()
#---------------------------------    
# Dirs
iYear_fut, eYear_fut = dieYear["P20"]
run  = "C20-P15-001"
#baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=0, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"




#**********************************
# Proportion to all precip
#----------------------------

for thpr in lthpr:
    if Fraction == False: continue

    for lscen in llscen:
        scen0, scen1 = lscen

        Var0  = {}
        Frac0 = {}

        Var1  = {}
        Frac1 = {}

        dldat = {}
        ddat  = {}
        dsig  = {}

        for tag in ltag+["plain"]:

            if vartype =="Ptot":
                da1prcp0, da1freq0, da1pint0 = ret_PN.main( thpr=thpr, scen=scen0, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
                da1prcp1, da1freq1, da1pint1 = ret_PN.main( thpr=thpr, scen=scen1, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    
            elif vartype =="Freq":
                da1freq0 = ret_PN.load_Freq( thpr=thpr, scen=scen0, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
                da1freq1 = ret_PN.load_Freq( thpr=thpr, scen=scen1, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    
             
            for region in lregion:
                if   vartype=="Ptot":
                    Var0[region,tag] = da1prcp0[region]
                    Var1[region,tag] = da1prcp1[region]


                elif vartype=="Freq":
                    Var0[region,tag] = da1freq0[region]
                    Var1[region,tag] = da1freq1[region]
                else:
                    print "check vartype",vartype
                    sys.exit()

        for tag in ltag:
            for region in lregion:
                Frac0[region,tag] = ma.masked_invalid(Var0[region,tag]/Var0[region,"plain"]).filled(0.0)
                Frac1[region,tag] = ma.masked_invalid(Var1[region,tag]/Var1[region,"plain"]).filled(0.0)


                ddat [region,tag] = Frac1[region,tag].mean() - Frac0[region,tag].mean()
                #print scen0,"->",scen1,"%.2f"%(Frac0[region,tag]),"->","%.2f"%(Frac1[region,tag])
        
        #--- statistical test --
        for region in lregion:
            dsig[region] = False
            for tag in ltag:
                if abs(ddat[region,tag]) <0.01:
                    continue
   
                t, p  = scipy.stats.ttest_ind(Frac0[region,tag],Frac1[region,tag], equal_var=False)
                if p <0.05: dsig[region] = True
   

        #--- vmin, vmax -----
        vmin, vmax = -0.15, 0.15

        #--- ylabel
        ylabel = "Change of Proportion"


        #--- title ----------
        stitle = "Change of Proportion @(%s-%s) %s th=%s"%(scen1,scen0,vartype,thpr)
    
        # Path
        figPath = figDir  + "/bars.dFraction.%s.%s-%s.th.%s.png"%(vartype, scen1, scen0, thpr)
    
    
        # Draw
        ltag_tmp = ["tc","cf","ms","ot"]
    
        f_draw_bars.draw_barstack(ddat=ddat, dsig=dsig, lregion=lregion, vmin=vmin, vmax=vmax, stitle=stitle, ylabel=ylabel, figPath=figPath)
            
     
