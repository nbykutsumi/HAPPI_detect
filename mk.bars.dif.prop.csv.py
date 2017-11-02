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
#lens       = range(1,2+1)


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
#lkey      = [["p99.990","Freq"]]
lkey      = [[1,"Ptot"],["p99.990","Freq"],["p99.990","Ptot"]]

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


            ddat1 [region,tag] = Frac1[region,tag].mean() - Frac0[region,tag].mean()
            ddat2 [region,tag] = Frac2[region,tag].mean() - Frac0[region,tag].mean()
            ddat12 [region,tag] = Frac2[region,tag].mean() - Frac1[region,tag].mean()
    
    #--- statistical test --
    for region in lregion:
        dsig1[region] = False
        dsig2[region] = False
        dsig12[region] = False
        for tag in ltag:
            if abs(ddat1[region,tag]) >=0.01:
   
                t, p  = scipy.stats.ttest_ind(Frac0[region,tag],Frac1[region,tag], equal_var=False)
                if p <0.05: dsig1[region] = True
   
            if abs(ddat2[region,tag]) >=0.01:
                t, p  = scipy.stats.ttest_ind(Frac0[region,tag],Frac2[region,tag], equal_var=False)
                if p <0.05: dsig2[region] = True

            if abs(ddat12[region,tag]) >=0.01:
                t, p  = scipy.stats.ttest_ind(Frac1[region,tag],Frac2[region,tag], equal_var=False)
                if p <0.05: dsig12[region] = True



    #--- output ------
    sout = sout + ",,,,,,"+",TC"*6+",ExC"*6+",Monsoon"*6+",Others"*6 +"\n"
    sout = sout + "thpr,vartype,num,region,sig1,sig2,sig12" + ",ALL,P16,P20,dif1,dif2,dif12"*4 + "\n"

    for  region,num in lregnum:
        sout = sout + "%s,%s,%s,%s,%s,%s,%s"%(thpr,vartype,num,region,dsig1[region],dsig2[region],dsig12[region])
        for tag in ltag:
            v0   = mean(Frac0[region,tag])
            v1   = mean(Frac1[region,tag])
            v2   = mean(Frac2[region,tag])
            d1   = ddat1[region,tag]
            d2   = ddat2[region,tag]
            d12  = ddat12[region,tag]

            sout = sout + ",%s,%s,%s,%s,%s,%s"%(v0,v1,v2,d1,d2,d12)
        sout = sout + "\n"



# Path
figPath = figDir  + "/table.proportion.csv"
f = open(figPath, "w")
f.write(sout)
f.close()
print figPath
    
    
    
            
     
