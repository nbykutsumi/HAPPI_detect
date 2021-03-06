import matplotlib as mpl
mpl.use("Agg")
import ret_PN
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func
import f_draw_hist
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
#lregion    = ["GLB"]

#- Switch  ------------
Total    = False
ExFreq   = True
Fraction = False

ChangeRat= True
#----------------------

#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,3+1)
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
PtotMin    = 10. # mm/year
dTagName   = {"plain":"All","tc":"TC","cf":"ExC","ms":"MS","ot":"OT"}
season     = "ALL"
#---------------------------------    
# Dirs
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"

dregNum = hd_func.dict_IPCC_codeKey()


#***********************************
# Total precip
#***********************************
thpr = 1
lvartype   = ["Ptot","Freq","Pint"]
lkey  = [[scen,tag] for scen in lscen for tag in ltag]

PrcpTot = {}
FreqTot = {}
PintTot = {}
for [scen,tag] in lkey:
    da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    #print scen,tag,da1prcp

    for region in lregion:
        PrcpTot[region,tag,scen] = da1prcp[region]
        FreqTot[region,tag,scen] = da1freq[region]*4*365
        PintTot[region,tag,scen] = da1pint[region]


#**********************************
# Ptot, Freq, Pint for Total precipitation
#----------------------------------
thpr = 1
#lvartype   = ["Ptot","Freq","Pint"]
lvartype   = ["Ptot"]
for vartype in lvartype:
    if Total != True: continue

    if   vartype == "Ptot":
        Var = PrcpTot
    elif vartype == "Freq":
        Var = FreqTot
    elif vartype == "Pint":
        Var = PintTot


    if ChangeRat ==True:
        for [scen,tag] in lkey:
            for region in lregion:
                Var[region,tag,scen] = Var[region,tag,scen] / mean(Var[region,tag,"ALL"])

    else:
        pass

        
    for region in lregion:
        for tag in ltag:

            #--- title ----------
            if tag=="plain":
                stitle1 = "%d %s"%(dregNum[region][0],region)
            else:
                stitle1 = ""

            stitle2 = "%s"%(dTagName[tag])

            # Path
            if ChangeRat ==True:
                figPath = figDir  + "/hist.rat.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)
            else:
                figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Var[region,tag,scen])

            # Statistical test
            lsig = [False]
            dat0 = Var[region,tag,"ALL"]
            dat1 = Var[region,tag,"P15"]
            dat2 = Var[region,tag,"P20"]
            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if p < 0.05: lsig.append(True)
            else:        lsig.append(False) 

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p < 0.05: lsig.append(True)
            else:        lsig.append(False) 


            # DrawFlag
            if region =="GLB":
                drawFlag =True

            elif max([mean(PrcpTot[region,tag,scen]) for scen in lscen])< PtotMin:
                drawFlag = False
            else:
                drawFlag = True


            xmin=None
            xmax=None


            # Draw
            f_draw_hist.draw_hist(ldat,lsig,drawFlag,stitle1,stitle2,figPath)

#**********************************
# Freq for Extreme precipitation
#----------------------------------
#lthpr  = ["p99.900","p99.990"]
lthpr  = ["p99.990"]
vartype="Freq"
for thpr in lthpr:
    if ExFreq != True: continue

    lkey  = [[scen,tag] for scen in lscen for tag in ltag]
    
    Freq   = {}
    for [scen,tag] in lkey:
        da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

 
        for region in lregion:
            Freq[region,tag,scen] = da1freq[region]*4*365


    Var  = Freq

    if ChangeRat ==True:
        Var = {}
        for [scen,tag] in lkey:
            for region in lregion:
                Var[region,tag,scen] = Freq[region,tag,scen] / mean(Freq[region,tag,"ALL"])

    else:
        Var = Freq


    for region in lregion:
        for tag in ltag:

            # xmin, xmax
            if region == "GLB":
                xmin = 0.7
                xmax = 2.2
            else:
                xmin = 0.5
                xmax = 2.8

            #--- title ----------
            if tag=="plain":
                stitle1 = "%d %s"%(dregNum[region][0],region)
            else:
                stitle1 = ""

            stitle2 = "%s"%(dTagName[tag])

            # Path
            if ChangeRat==True:
                figPath = figDir  + "/hist.rat.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)
            else:
                figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Var[region,tag,scen])


            # Statistical test
            lsig = [False]
            dat0 = Var[region,tag,"ALL"]
            dat1 = Var[region,tag,"P15"]
            dat2 = Var[region,tag,"P20"]
            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if p < 0.05: lsig.append(True)
            else:        lsig.append(False) 

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p < 0.05: lsig.append(True)
            else:        lsig.append(False) 

            # DrawFlag
            if region =="GLB":
                drawFlag =True

            elif max([mean(PrcpTot[region,tag,scen]) for scen in lscen])< PtotMin:
                drawFlag = False
            else:
                drawFlag = True

            # Draw
            #f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)
            f_draw_hist.draw_hist(ldat,lsig,drawFlag,stitle1,stitle2,figPath,xmin=xmin,xmax=xmax)




#**********************************
# Proportion to all precip
#----------------------------
lthpr  = ["p99.900","p99.990"]
vartype="Freq"
for thpr in lthpr:
    if Fraction != True: continue

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
            stitle1 = "%s (Fraction %s thres=%s)"%(region,vartype, thpr)
            stitle2 = "%s"%(dTagName[tag])

            # Path
            figPath = figDir  + "/hist.Fraction.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)

            # Data
            ldat = []
            for scen in lscen:
                ldat.append(Out[region,tag,scen])


            # Draw
            f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)



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
        figPath = figDir  + "/hist.ptile.th.%s.%s.png"%(thpr, region)

        # Data
        ldat = []
        for scen in lscen:
            ldat.append(array(Out[region,scen]))


        # Draw
        f_draw_hist.draw_hist(ldat,stitle1,stitle2,figPath)

"""
   
