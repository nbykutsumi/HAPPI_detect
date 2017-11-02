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
Total    = False
ExFreq   = False
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

dTagName   = {"plain":"All","tc":"TC","cf":"ExC","ms":"MS","ot":"OT"}
season     = "ALL"

# lregnum ---------
dregion = hd_func.dict_IPCC_codeKey()
lregnum = []
for region in lregion:
    num = dregion[region][0]
    lregnum.append([region,num])

lregnum = sorted(lregnum, key= lambda x: x[1])

#---------------------------------    
# Dirs
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



#lvartype   = ["Ptot","Freq","Pint"]
lvartype   = ["Ptot"]
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
        dsig  = {}
        for tag in ltag:
            dat0  = dldat[tag][0]
            dat1  = dldat[tag][1]
            dat2  = dldat[tag][2]

            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            dsig[tag] = [False]

            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)




        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        stitle2 = "%s (%s thres=%s)"%(region, vartype, thpr)
        if dsig["plain"][1] ==True: stitle1 = "*" + stitle1

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
        dsig  = {}
        for tag in ltag:
            dat0  = dldat[tag][0]
            dat1  = dldat[tag][1]
            dat2  = dldat[tag][2]

            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            dsig[tag] = [False]

            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)


        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)
        if dsig["plain"] == True: stitle1 = "*" + stitle1
    
        # Path
        figPath = figDir  + "/boxplot.%s.th.%s.%s.png"%(vartype, thpr, region)
    
        f_draw_boxplot.draw_boxplot_multi(dldat,dsig,ltag,stitle1,figPath, ddraw)


#**********************************
# Proportion to all precip
#----------------------------

lthpr  = [1,"p99.900","p99.990"]
vartype="Ptot"
#lthpr  = ["p99.900","p99.990"]
#vartype="Freq"

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
        dsig  = {}
        for tag in ["tc","cf","ms","ot"]:
            dat0  = dldat[tag][0]
            dat1  = dldat[tag][1]
            dat2  = dldat[tag][2]

            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            dsig[tag] = [False]

            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)


        #--- title ----------
        regNum  = dregInfo[region][0]
        stitle1 = "%s (%d)"%(region, regNum)


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
#lkey1      = [[1,"Ptot"],[1,"Freq"],[1,"Pint"]]
#lkey1      = [["p99.900","Freq"],["p99.990","Freq"]]
#lkey1      = [["p99.990","Freq"]]
lkey1      = [[1,"Ptot"]]
for thpr, vartype in lkey1:

    if ChangeRat == False: continue

    Var = {}
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



    dldat0 = {}
    dldat1 = {}
    dldat2 = {}
    dsig1  = {}
    dsig2  = {}
    drawFlag = {}
    for region in lregion:
        for tag in ltag:
            dldat0[region,tag] = []
            dldat1[region,tag] = []
            dldat2[region,tag] = []

            for scen in ["ALL","P15","P20"]:
                lvfut  = Var[region,tag,scen]
                vpre   = Var[region,tag,"ALL"].mean()
                lvout  = lvfut/vpre
                if   scen =="ALL":
                    dldat0[region,tag] = lvout
                elif scen =="P15":
                    dldat1[region,tag] = lvout
                elif scen == "P20":
                    dldat2[region,tag] = lvout
        
        #--- ddraw -----------
        for tag in ltag:
            lmeanPrcp = [mean(Prcp[region,tag,scen]) for scen in lscen]
            if region=="GLB":
                drawFlag[region,tag] = True
            elif max(lmeanPrcp) < PtotMin:
                drawFlag[region,tag] = False
            else:
                drawFlag[region,tag] = True

        #for tag in ltag: dylim[tag] = [ymin,ymax]
        if   thpr in [1]:
            lylim = [0.76, 1.24]
            yminor= None
            ymajor= None

        elif thpr in ["p99.990"]:
            lylim = [0.8, 2.3]
            yminor= 0.1
            ymajor= None



        #--- statistical test --
        for tag in ltag:
            dat0  = dldat0[region,tag]
            dat1  = dldat1[region,tag]
            dat2  = dldat2[region,tag]

            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            if p <0.05: dsig1[region,tag] = True
            else:  dsig1[region,tag] = False

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            if p <0.05: dsig2[region,tag] = True
            else:  dsig2[region,tag] = False



    #--- GLB line --
    dlGlbMean = {}
    for tag in ltag:
        glbMean0 = mean(dldat0["GLB",tag])
        glbMean1 = mean(dldat1["GLB",tag])
        glbMean2 = mean(dldat2["GLB",tag])

        dlGlbMean[tag]=[glbMean0,glbMean1,glbMean2]

    #--- hline -----
    hline = 1.0
    #--- title ----------
    stitle = "%s thres=%s"%(vartype, thpr)

    #-- 1st ---
    lregion_tmp = []
    for regnum in lregnum[1:13+1]:
        lregion_tmp.append(regnum[0]) 
    figPath = figDir  + "/boxplot.rat.%s.th.%s.1.png"%(vartype, thpr)

    f_draw_boxplot.draw_boxplot_Comb(dldat0,dldat1,dldat2,drawFlag,dsig1,dsig2,lregion_tmp,ltag,stitle,figPath,lylim=lylim, ymajor=ymajor, yminor=yminor, hline=hline, dlGlbMean=dlGlbMean)


    #-- 2nd ---
    lregion_tmp = []
    for regnum in lregnum[14:]:
        lregion_tmp.append(regnum[0]) 

    figPath = figDir  + "/boxplot.rat.%s.th.%s.2.png"%(vartype, thpr)

    f_draw_boxplot.draw_boxplot_Comb(dldat0,dldat1,dldat2,drawFlag,dsig1,dsig2,lregion_tmp,ltag,stitle,figPath,lylim=lylim, ymajor=ymajor, yminor=yminor, hline=hline, dlGlbMean=dlGlbMean)


    #-- GLB ---
    stitle  = "%s %s"%(0, "GLB")
    figPath = figDir  + "/boxplot.rat.%s.th.%s.%s.png"%(vartype, thpr, "GLB" )

    DAT0 = {}
    DAT1 = {}
    DAT2 = {}
    DRAW = {}
    SIG1 = {}
    SIG2 = {}
    for tag in ltag:
        DAT0[tag] = dldat0["GLB",tag]
        DAT1[tag] = dldat1["GLB",tag]
        DAT2[tag] = dldat2["GLB",tag]

        DRAW[tag] = True

        SIG1[tag] = dsig1[region,tag]
        SIG2[tag] = dsig2[region,tag]

    f_draw_boxplot.draw_boxplot_Comb_Single(DAT0,DAT1,DAT2,DRAW,SIG1,SIG2,ltag,stitle,figPath,lylim=lylim, ymajor=ymajor, yminor=yminor, hline=hline, dlGlbMean=dlGlbMean)


    
