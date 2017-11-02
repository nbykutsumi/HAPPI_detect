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

#- Switch  ------------
Fraction = True
#----------------------
#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,10+1)


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
#- output ---------
lregnum = []
for region in lregion:
    num = dregInfo[region][0]
    lregnum.append([region,num])

lregnum = sorted(lregnum, key= lambda x: x[1])


#---------------------------------    
# Dirs
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"

#**********************************
# Proportion to all precip
#----------------------------
lkey      = [["p99.990","Freq"]]
#lkey      = [[1,"Ptot"],["p99.990","Freq"],["p99.990","Ptot"]]

sout = ""
for [thpr,vartype] in lkey:
    Var0  = {}
    Frac0 = {}

    Var1  = {}
    Frac1 = {}

    Var2  = {}
    Frac2 = {}

    ddat1  = {}
    dsig1  = {}

    ddat2  = {}
    dsig2  = {}

    ddat12 = {}
    dsig12 = {}
 

    for tag in ltag+["plain"]:

        if vartype =="Ptot":
            da1prcp0, da1freq0, da1pint0 = ret_PN.main( thpr=thpr, scen="ALL", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1prcp1, da1freq1, da1pint1 = ret_PN.main( thpr=thpr, scen="P15", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1prcp2, da1freq2, da1pint2 = ret_PN.main( thpr=thpr, scen="P20", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    
        elif vartype =="Freq":
            da1freq0 = ret_PN.load_Freq( thpr=thpr, scen="ALL", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1freq1 = ret_PN.load_Freq( thpr=thpr, scen="P15", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1freq2 = ret_PN.load_Freq( thpr=thpr, scen="P20", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    
         
        for region in lregion:
            if   vartype=="Ptot":
                Var0[region,tag] = da1prcp0[region]
                Var1[region,tag] = da1prcp1[region]
                Var2[region,tag] = da1prcp2[region]


            elif vartype=="Freq":
                Var0[region,tag] = da1freq0[region]
                Var1[region,tag] = da1freq1[region]
                Var2[region,tag] = da1freq2[region]
            else:
                print "check vartype",vartype
                sys.exit()

    for tag in ltag:
        for region in lregion:
            Frac0[region,tag] = ma.masked_invalid(Var0[region,tag]/Var0[region,"plain"]).filled(0.0)
            Frac1[region,tag] = ma.masked_invalid(Var1[region,tag]/Var1[region,"plain"]).filled(0.0)
            Frac2[region,tag] = ma.masked_invalid(Var2[region,tag]/Var2[region,"plain"]).filled(0.0)



            ddat1 [region,tag] = (Frac1[region,tag] - Frac0[region,tag].mean())/0.7
            ddat2 [region,tag] = (Frac2[region,tag] - Frac1[region,tag].mean())/0.5

            #ddat1 [region,tag] = (Frac1[region,tag] - Frac0[region,tag].mean())
            #ddat2 [region,tag] = (Frac2[region,tag] - Frac1[region,tag].mean())


    """
    region = "CAM"
    sout = "tc,cf,ms,ot,tc,cf,ms,ot\n"
    for ens in lens:
        for tag in ["tc","cf","ms","ot"]:
            sout = sout + "%s,"%ddat1[region,tag][ens-1]
        for tag in ["tc","cf","ms","ot"]:
            sout = sout + "%s,"%ddat2[region,tag][ens-1]
        sout = sout.strip() + "\n"

    oPath = figDir + "/temp.csv"
    f=open(oPath,"w"); f.write(sout); f.close()
    print oPath
    """

    tmp1 = 0
    tmp2 = 0
    for tag in ["tc","cf","ms","ot"]:
        print "-"*10
        print tag
        print ddat1["CAM",tag].mean()
        print ddat2["CAM",tag].mean()
        tmp1 = tmp1 + abs(ddat1["CAM",tag]).mean()
        tmp2 = tmp2 + abs(ddat2["CAM",tag]).mean()
    print tmp1*0.5
    print tmp2*0.5
    didx1 = {}
    didx2 = {}
    for region in lregion:

        didx1[region] = 0.5*array([abs(ddat1[region,tag]) for tag in ["tc","cf","ms","ot"]]).sum(axis=0)
        didx2[region] = 0.5*array([abs(ddat2[region,tag]) for tag in ["tc","cf","ms","ot"]]).sum(axis=0)

     
    print "x"*10 
    print didx1["CAM"].mean()
    print didx2["CAM"].mean()
    #--- statistical test --
    dsig  = {}
    for region in lregion:
        dsig[region] = False
        t, p  = scipy.stats.ttest_ind(didx1[region],didx2[region], equal_var=False)
        if p <0.05: dsig1[region] = True

    #--- Figure ------
    fig = plt.figure(figsize=(7.5,2.8))
    ax1  = fig.add_axes([0.1,0.33,0.85,0.57])
    ax2  = ax1.twinx()

    wbar= 0.35
    yfontsize = 10


    lx  = []
    for iregion, [region,num] in enumerate(lregnum):    

        x    = iregion
        x1   = iregion-0.5*wbar
        x2   = iregion+0.5*wbar
        lx.append(x)
        v1  = didx1[region].mean()
        v2  = didx2[region].mean()
        rat = v2/v1
        sig = dsig [region]

        ax1.bar(x1, v1, width=wbar, color="gray")
        ax1.bar(x2, v2, width=wbar, color="black")

        ax2.plot(x, rat, "o", markerfacecolor="w", markeredgecolor="k")


    #--- ylim  ----------
    ax1.set_ylim([0,0.5])
    ax2.set_ylim([0,2.0])
    #--- hline ----------
    ax1.axhline(y=0)
    ax2.axhline(y=1, linestyle="--", color="gray")

    #--- vertical grids
    ax1.xaxis.grid(linestyle="--")
    ax1.yaxis.grid(linestyle="--")

    #--- x-ticklabel ----
    ax1.set_xticks(lx)

    lxlabel = []
    for (region,num) in lregnum:
        if dsig[region]==True:
            slabel = "*%d %s"%(num,region)
        else:
            slabel = " %d %s"%(num,region)
        lxlabel.append(slabel)

    ax1.set_xticklabels(lxlabel, rotation=-90, fontsize=12)
    #ax.tick_params(bottom="off",labelbottom="off", labelsize=yfontsize)


        

    # Path
    figPath = figDir  + "/bar.SSI.%s.th.%s.png"%(vartype,thpr)
    plt.savefig(figPath)
    print figPath
        
    
    
            
     
