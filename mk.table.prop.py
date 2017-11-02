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
import myfunc.util as util

prj        = "HAPPI"
expr       = "C20"
model      = "MIROC5"
res        = "128x256"

#regiontype = "JPN"
#lregion    = ["GLB","JPN","S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]

regiontype = "IPCC"
lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion    = ["CAM"]
#lregion    = ["GLB","SAF","EAS","SEA","NAU","SAU"]

#- Switch  ------------
Fraction = True
#----------------------
#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,2+1)
#lens       = [1]

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
figDir  = baseDir + "/csv"
util.mk_dir(figDir)
#**********************************
# Proportion to all precip
#----------------------------
lkey      = [["p99.990","Freq"]]
#lkey      = [["p99.990","Ptot"]]
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
            """
            Frac0[region,tag] = ma.masked_invalid(Var0[region,tag]/Var0[region,"plain"]).filled(0.0)
            Frac1[region,tag] = ma.masked_invalid(Var1[region,tag]/Var1[region,"plain"]).filled(0.0)
            Frac2[region,tag] = ma.masked_invalid(Var2[region,tag]/Var2[region,"plain"]).filled(0.0)
            """

            plain0 = Var0[region,"tc"]+Var0[region,"cf"]+Var0[region,"ms"]+Var0[region,"ot"]
            plain1 = Var1[region,"tc"]+Var1[region,"cf"]+Var1[region,"ms"]+Var1[region,"ot"]
            plain2 = Var2[region,"tc"]+Var2[region,"cf"]+Var2[region,"ms"]+Var2[region,"ot"]

            Frac0[region,tag] = ma.masked_invalid(Var0[region,tag]/plain0).filled(0.0)
            Frac1[region,tag] = ma.masked_invalid(Var1[region,tag]/plain1).filled(0.0)
            Frac2[region,tag] = ma.masked_invalid(Var2[region,tag]/plain2).filled(0.0)




    for region,num in lregnum:
        print "*"*50
        print region, num
        stmp = Var0[region,"tc"][0] + Var0[region,"cf"][0] + Var0[region,"ms"][0] + Var0[region,"ot"][0]
        print "tc",Var0[region,"tc"][0],"cf",Var0[region,"cf"][0],"ms",Var0[region,"ms"][0],"ot",Var0[region,"ot"][0]
        print stmp
        print Var0[region,"plain"][0]
   
        print "" 
    
        stmp = Frac0[region,"tc"][0] + Frac0[region,"cf"][0] + Frac0[region,"ms"][0] + Frac0[region,"ot"][0]
        print "tc",Frac0[region,"tc"][0],"cf",Frac0[region,"cf"][0],"ms",Frac0[region,"ms"][0],"ot",Frac0[region,"ot"][0]
        print stmp


    #--- output ------
    for [region,num] in lregnum:
        sout = ",ALL"*4 + ",P15"*4 + ",P20"*4 + "\n"
        sout = sout + ",TC,ExC,MS,OT"*3+"\n"
   
        for iens,ens in enumerate(lens): 
            sout = sout + "%d"%(iens)
            s0   = ""
            s1   = ""
            s2   = ""
            for tag in ["tc","cf","ms","ot"]:
                s0  = s0 + ",%s"%(Frac0[region,tag][iens])
                s1  = s1 + ",%s"%(Frac1[region,tag][iens])
                s2  = s2 + ",%s"%(Frac2[region,tag][iens])
    
            sout = sout + s0 + s1 + s2 +"\n"
    
    
        # Path
        figPath = figDir  + "/table.proportion.%s.th.%s.%d.csv"%(vartype,thpr,num)
        f = open(figPath, "w")
        f.write(sout)
        f.close()
        print figPath
    
    
    
            
