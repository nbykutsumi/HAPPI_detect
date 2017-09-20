import matplotlib as mpl
mpl.use("Agg")
import ret_PN
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func
import f_draw_boxplot
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
#lregion    = ["ALA"]

PtotMin = 10   # mm/year
#- Switch  ------------
Total   = False
ExFreq  = False
Fraction= False
TotalRat= True
#----------------------
#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lthpr      = [0,"p99.900","p99.990"]
#lthpr      = ["p99.900","p99.990"]
lscen      = ["ALL","P15","P20"]
ltag       = ["plain","tc","cf","ms","ot"]
wbar       = 0.8
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
# Ptot, Freq, Pint for Total precipitation
#----------------------------------

thpr = 1
lkey  = [[scen,tag] for scen in lscen for tag in ltag]

Prcp = {}
Freq = {}
Pint = {}
for [scen,tag] in lkey:
    #if Total == False: continue

    da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    #print scen,tag,da1prcp

    for region in lregion:
        Prcp[region,tag,scen] = da1prcp[region]
        Freq[region,tag,scen] = da1freq[region]*4*365
        Pint[region,tag,scen] = da1pint[region]



lvartype   = ["Ptot","Freq","Pint"]
#lvartype   = ["Ptot"]
for vartype in lvartype:

    if Total == False: continue

    if   vartype == "Ptot":
        Var = Prcp
    elif vartype == "Freq":
        Var = Freq
    elif vartype == "Pint":
        Var = Pint
        
    for region in lregion:
        dldat = {}
        for tag in ltag:
            dldat[tag] = []
            for scen in lscen:
                dldat[tag].append(Var[region,tag,scen])

        #--- ddraw -----------
        ddraw = {}
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                ddraw[tag] = True
            elif max(lmeanPrcp) < PtotMin:
                ddraw[tag] = False
            else:
                ddraw[tag] = True

        #--- ylim -----------
        #dylim = None
        #dytick= {tag:None for tag in ltag}

        #--- statistical test --
        dp    = {}
        dsig  = {}
        for tag in ltag:
            dat0  = Var[region,tag,"P15"]
            dat1  = Var[region,tag,"P20"]
            t, dp[tag]  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if dp[tag]<0.05: dsig[tag]=True
            else:  dsig[tag] = False

        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        stitle2 = "%s (%s thres=%s)"%(region, vartype, thpr)
        if dp["plain"] < 0.05: stitle1 = "*" + stitle1

        # Path
        figPath = figDir  + "/boxplot.%s.th.%s.%s.png"%(vartype, thpr, region)

        #f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, dylim)
        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, ddraw)


#**********************************
# Freq for extreme precipitation
#----------------------------------
lthpr     = ["p99.900","p99.990"]
vartype   = "Freq"
for thpr in lthpr:

    if ExFreq == False: continue

    lkey  = [[scen,tag] for scen in lscen for tag in ltag]
    
    Freq   = {}
    for [scen,tag] in lkey:
        da1freq = ret_PN.load_Freq( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

 
        print "loading",thpr,scen,tag
        for region in lregion:
            Freq[region,tag,scen] = da1freq[region]*4*365


    Var = Freq
    for region in lregion:
        dldat = {}
        for tag in ltag:
            dldat[tag] = []
            for scen in lscen:
                dldat[tag].append(Var[region,tag,scen])

        #--- ddraw -----------
        ddraw = {}
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                ddraw[tag] = True
            elif max(lmeanPrcp) < PtotMin:
                ddraw[tag] = False
            else:
                ddraw[tag] = True

    
        #--- ylim -----------
        #dylim = None

        #--- statistical test --
        dp    = {}
        dsig  = {}
        for tag in ltag:
            dat0  = Var[region,tag,"P15"]
            dat1  = Var[region,tag,"P20"]
            t, dp[tag]  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if dp[tag]<0.05: dsig[tag]=True
            else:  dsig[tag] = False

        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        if dp["plain"] < 0.05: stitle1 = "*" + stitle1
    
        # Path
        figPath = figDir  + "/boxplot.%s.th.%s.%s.png"%(vartype, thpr, region)
    
        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, ddraw)


#**********************************
# Proportion to all precip
#----------------------------
#lthpr  = ["p99.900","p99.990"]
#vartype="Freq"

lthpr  = [1,"p99.900","p99.990"]
vartype="Ptot"

for thpr in lthpr:

    if Fraction == False: continue

    lkey  = [[scen,tag] for scen in lscen for tag in ltag]

    Var  = {}
    Frac = {}
    for [scen,tag] in lkey:
        print "loading",thpr,scen,tag
        if vartype =="Ptot":
            da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

        elif vartype =="Freq":
            da1freq = ret_PN.load_Freq( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

         
        for region in lregion:
            if vartype=="Freq":
                Var[region,tag,scen] = da1freq[region]
            elif vartype=="Ptot":
                Var[region,tag,scen] = da1prcp[region]


    for [scen,tag] in lkey:
        for region in lregion:
            Frac[region,tag,scen] = ma.masked_invalid(Var[region,tag,scen]/Var[region,"plain",scen]).filled(0.0)


    Var = Frac
    for region in lregion:
        dldat = {}
        for tag in ltag:
            if tag == "plain":continue

            dldat[tag] = []
            for scen in lscen:
                dldat[tag].append(Var[region,tag,scen])

        #--- ddraw -----------
        ddraw = {}
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                ddraw[tag] = True
            elif max(lmeanPrcp) < PtotMin:
                ddraw[tag] = False
            else:
                ddraw[tag] = True

        #--- statistical test --
        dp    = {}
        dsig  = {"tc":False, "cf":False, "ms":False,"ot":False}
        for tag in ["tc","cf","ms","ot"]:
            if array(dldat[tag]).max() < 0.05: continue

            dat0  = Var[region,tag,"P15"]
            dat1  = Var[region,tag,"P20"]
            t, dp[tag]  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if dp[tag]<0.05: dsig[tag]=True
            else:  dsig[tag] = False

        p = dp.values()

        #print region,tag,"p=",p,"--",p_tc,p_cf,p_ms,p_ot
        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        if p < 0.05: stitle1 = "*" + stitle1


        # Path
        figPath = figDir  + "/boxplot.Fraction.%s.th.%s.%s.png"%(vartype, thpr, region)

        #--- ylim -----------
        #dylim = None


        # Draw
        ltag_tmp = ["tc","cf","ms","ot"]

        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag_tmp,stitle1,figPath, ddraw=ddraw)


#**********************************
# fractional change Ptot, Freq, Pint for Total precipitation
#----------------------------------
#lkey1      = [[1,"Ptot"],[1,"Freq"],[1,"Pint"],["99.900","Freq"],["p99.990","Freq"]]
lkey1      = [["p99.900","Freq"],["p99.990","Freq"]]
#lkey1      = [[1,"Ptot"]]
for thpr, vartype in lkey1:

    if TotalRat == False: continue

    Var = {}
    Rat = {}
    lkey2 = [[scen,tag] for scen in ["ALL","P15","P20"] for tag in ltag]
    for [scen,tag] in lkey2:
        print "loading",thpr,scen,tag
        if vartype in ["Ptot","Pint"]:
            da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

        elif vartype =="Freq":
            da1freq = ret_PN.load_Freq( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")


        for region in lregion:
            if vartype=="Ptot":
                Var[region,tag,scen] = da1prcp[region]
            elif vartype=="Freq":
                Var[region,tag,scen] = da1freq[region]
            elif vartype=="Pint":
                Var[region,tag,scen] = da1pint[region]



    for region in lregion:
        dldat = {}
        for tag in ltag:
            dldat[tag] = []
            for scen in ["P15","P20"]:
                lvfut  = Var[region,tag,scen]
                vpre   = Var[region,tag,"ALL"].mean()
                lvout  = lvfut/vpre
                dldat[tag].append(lvout)

        #--- ddraw -----------
        ddraw = {}
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                ddraw[tag] = True
            elif max(lmeanPrcp) < PtotMin:
                ddraw[tag] = False
            else:
                ddraw[tag] = True

        #--- ylim -----------
        dylim = {}
        dytick= {}
        lmean = []
        for tag in ltag:
            for dat in dldat[tag]:
                if ddraw[tag] ==True:
                    lmean.append(abs(dat.mean()-1.0))
                else:
                    lmean.append(nan)

        if thpr == 1:
            difMax = 0.1
            lytick = [0.95, 1.0, 1.05]
        elif thpr in ["p99.900","p99.990"]:
            difMax = 1.0
            lytick = [0.5, 1.0, 1.5]

        if max(lmean) > difMax:
            ymin =1.0 - max(lmean)*1.3
            ymax =1.0 + max(lmean)*1.3
            for tag in ltag: dytick[tag] = None
        else:
            ymin = 1.0-difMax
            ymax = 1.0+difMax
            for tag in ltag: dytick[tag]= lytick

        for tag in ltag: dylim[tag] = [ymin,ymax]


        #--- statistical test --
        dp    = {}
        dsig  = {}
        for tag in ltag:
            #dat0  = Var[region,tag,"P15"]
            #dat1  = Var[region,tag,"P20"]
            #t, dp[tag]  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            #if dp[tag]<0.05: dsig[tag]=True
            #else:  dsig[tag] = False
            dsig[tag] = False

        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        stitle2 = "%s (%s thres=%s)"%(region, vartype, thpr)
        #if dp["plain"] < 0.05: stitle1 = "*" + stitle1

        # Path
        figPath = figDir  + "/boxplot.rat.%s.th.%s.%s.png"%(vartype, thpr, region)

        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, ddraw, dylim, dytick=dytick, hline=1)





"""
#**********************************
# fractional change Ptot, Freq, Pint for Total precipitation
#----------------------------------
lvartype   = ["Ptot","Freq","Pint"]
#lvartype   = ["Ptot"]
for vartype in lvartype:

    if TotalRat == False: continue

    if   vartype == "Ptot":
        Var = Prcp
    elif vartype == "Freq":
        Var = Freq
    elif vartype == "Pint":
        Var = Pint
        
    for region in lregion:
        dldat = {}
        for tag in ltag:
            dldat[tag] = []
            for scen in ["P15","P20"]:
                lvfut  = Var[region,tag,scen]
                vpre   = Var[region,tag,"ALL"].mean()
                lvout  = lvfut/vpre
                dldat[tag].append(lvout)

        #--- ddraw -----------
        ddraw = {}
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                ddraw[tag] = True
            elif max(lmeanPrcp) < PtotMin:
                ddraw[tag] = False
            else:
                ddraw[tag] = True

        #--- ylim -----------
        dylim = {}
        dytick= {}
        lmean = []
        for tag in ltag:
            for dat in dldat[tag]:
                if ddraw[tag] ==True:
                    lmean.append(abs(dat.mean()-1.0))
                else:
                    lmean.append(nan)

        if max(lmean) > 0.1:
            ymin =1.0 - max(lmean)*1.3
            ymax =1.0 + max(lmean)*1.3
            for tag in ltag: dytick[tag] = None
        else:
            ymin = 0.9
            ymax = 1.1
            for tag in ltag: dytick[tag]= [0.95,1.0,1.05]

        for tag in ltag: dylim[tag] = [ymin,ymax]


        #--- statistical test --
        dp    = {}
        dsig  = {}
        for tag in ltag:
            #dat0  = Var[region,tag,"P15"]
            #dat1  = Var[region,tag,"P20"]
            #t, dp[tag]  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            #if dp[tag]<0.05: dsig[tag]=True
            #else:  dsig[tag] = False
            dsig[tag] = False

        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        stitle2 = "%s (%s thres=%s)"%(region, vartype, thpr)
        #if dp["plain"] < 0.05: stitle1 = "*" + stitle1

        # Path
        figPath = figDir  + "/boxplot.rat.%s.th.%s.%s.png"%(vartype, thpr, region)

        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, ddraw, dylim, dytick=dytick, hline=1)

"""


#**********************************
# extreme values (99.9 & 99.99 percentiles)
#----------------------------------
"""

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
        stitle2 = "%s"%(thpr)

        # Path
        figPath = figDir  + "/boxplot.ptile.th.%s.%s.png"%(thpr, region)

        # Data
        ldat = []
        for scen in lscen:
            ldat.append(array(Out[region,scen]))


        # Draw
        f_draw_boxplot.draw_boxplot(ldat,stitle1,stitle2,figPath)

"""
   
