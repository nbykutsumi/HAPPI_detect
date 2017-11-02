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

#----------------------
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,2+1)
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
lregnum = []
for region in lregion:
    num = dregInfo[region][0]
    lregnum.append([region,num])

lregnum = sorted(lregnum, key= lambda x: x[1])


#---------------------------------    
# Dirs
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"



Vtot = {}
for tag in ltag:
    # load total precip
    da1prcp0, da1freq0, da1pint0 = ret_PN.main( thpr=1, scen="ALL", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    da1prcp1, da1freq1, da1pint1 = ret_PN.main( thpr=1, scen="P15", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    da1prcp2, da1freq2, da1pint2 = ret_PN.main( thpr=1, scen="P20", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")

    for region in lregion:
        Vtot[region,tag,"ALL"] = da1prcp0[region]
        Vtot[region,tag,"P15"] = da1prcp1[region]
        Vtot[region,tag,"P20"] = da1prcp2[region]


#**********************************
lkey1      = [["p99.990","Freq"]]
#lkey1      = [[1,"Ptot"],[1,"Freq"],[1,"Pint"],["p99.990","Freq"],["p99.990","Ptot"]]

sout = ",,,"+",ALL"*7+",TC"*7+",ExC"*7+",Monsoon"*7+",Others"*7 +"\n"
sout = sout + "thpr,vartype,num,region" + ",ALL,P15,P20,pv,dif%%P15,pv,dif%%P20"*5 + "\n"
for thpr, vartype in lkey1:
    Var = {}
    PV  = {}

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
                Var[region,tag,scen] = da1freq[region] *4 * 365.  # [#/season]
            elif vartype=="Pint":
                Var[region,tag,scen] = da1pint[region]

    for region,num in lregnum:
        dldat = {}
        for tag in ltag:
            dldat[tag] = []
            for scen in ["ALL","P15","P20"]:
                lvfut  = Var[region,tag,scen]
                vpre   = Var[region,tag,"ALL"].mean()
                lvout  = lvfut/vpre
                dldat[tag].append(lvout)

        #--- statistical test --
        dsig  = {}
        for tag in ltag:
            dat0  = dldat[tag][0]
            dat1  = dldat[tag][1]
            dat2  = dldat[tag][2]

            t, p  = scipy.stats.ttest_ind(dat0,dat1,equal_var=False)
            dsig[tag] = [False]
            PV[tag,"P15"]   = p
            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)

            t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
            PV[tag,"P20"]   = p
            if p <0.05: dsig[tag].append(True)
            else:  dsig[tag].append(False)


        sout = sout + "%s,%s,%s,%s"%(thpr,vartype,num,region)
        for tag in ltag:
            if max(mean(Vtot[region,tag,"ALL"])
                  ,mean(Vtot[region,tag,"P15"])
                  ,mean(Vtot[region,tag,"P20"])
                  )  < 10.:  # mm/year
                v0   = ""
                v1   = ""
                v2   = ""
                p1   = ""
                p2   = ""
                rat1 = ""
                rat2 = ""
            else:
                v0   = mean(Var[region,tag,"ALL"])
                v1   = mean(Var[region,tag,"P15"])
                v2   = mean(Var[region,tag,"P20"])
                p1   = PV[tag,"P15"]
                p2   = PV[tag,"P20"]
                rat1 = (v1-v0)/v0*100.
                rat2 = (v2-v0)/v0*100.

            stmp = ",%s,%s,%s,%s,%s,%s,%s"%(
                    v0,v1,v2,p1,rat1,p2,rat2)
            sout = sout + stmp
        sout = sout.strip() + "\n"



# Path
figPath = figDir  + "/table.boxplot.rat.csv"
f = open(figPath,"w")
f.write(sout)
f.close()
print figPath

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
   
