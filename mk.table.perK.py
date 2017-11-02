import matplotlib as mpl
mpl.use("Agg")
import ret_PN
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func
#import f_draw_bars
import f_draw_boxplot
import sys
import ret_ClimRegion
from numpy import *



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
Fraction = True
#----------------------
#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lens       = range(1,5+1)

#lthpr  = [1]
#lthpr  = [1,"p99.900","p99.990"]
#lthpr  = [1,"p99.990"]
#lthpr  = ["p99.990"]
#vartype="Ptot"
#vartype="Ptot"

#lthpr  = ["p99.900","p99.990"]
#lthpr  = ["p99.990"]
#vartype="Freq"

#lkey = [[1,"Ptot"],[1,"Freq"],[1,"Pint"],["p99.990","Ptot"],["p99.990","Freq"]]
lkey = [["p99.990","Freq"]]

dregion = hd_func.dict_IPCC_codeKey()



ltag       = ["plain","tc","cf","ms","ot"]
#ltag       = ["tc","cf","ms","ot"]
#ltag       = ["plain"]
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
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"




#**********************************
for [thpr,vartype] in lkey:
    #for tasType in ["Tglb","Treg"]:
    for tasType in ["Tglb"]:
        V0  = {}
        dV1 = {}
        dV2 = {}
        ddV = {}
        PVd1= {} 
        PVd2= {} 
        PVdd= {} 
        for tag in ltag:
            # load total precip
            da1prcpAll0, da1freqAll0, da1pintAll0 = ret_PN.main( thpr=1, scen="ALL", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1prcpAll1, da1freqAll1, da1pintAll1 = ret_PN.main( thpr=1, scen="P15", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
            da1prcpAll2, da1freqAll2, da1pintAll2 = ret_PN.main( thpr=1, scen="P20", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
    
            if thpr ==1:
                da1prcp0, da1freq0, da1pint0 = da1prcpAll0, da1freqAll0, da1pintAll0
                da1prcp1, da1freq1, da1pint1 = da1prcpAll1, da1freqAll1, da1pintAll1
                da1prcp2, da1freq2, da1pint2 = da1prcpAll2, da1freqAll2, da1pintAll2
    
            else:
                da1prcp0, da1freq0, da1pint0 = ret_PN.main( thpr=thpr, scen="ALL", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
                da1prcp1, da1freq1, da1pint1 = ret_PN.main( thpr=thpr, scen="P15", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
                da1prcp2, da1freq2, da1pint2 = ret_PN.main( thpr=thpr, scen="P20", tag=tag, regiontype=regiontype, lregion=lregion, lens=lens, lndsea="lnd")
        
    
            # load temperature
            if tasType == "Tglb":
                lregion_tmp=["GLB"]
                lndsea     =None
            elif tasType=="Treg":
                lregion_tmp=lregion+["GLB"]
                lndsea     ="lnd"


            da1tas0  = ret_ClimRegion.load_da1dat(var="tas", scen="ALL", regiontype=regiontype, lregion=lregion_tmp, lens=lens, lndsea=lndsea)
            
            da1tas1  = ret_ClimRegion.load_da1dat(var="tas", scen="P15", regiontype=regiontype, lregion=lregion_tmp, lens=lens, lndsea=lndsea)
            
            da1tas2  = ret_ClimRegion.load_da1dat(var="tas", scen="P20", regiontype=regiontype, lregion=lregion_tmp, lens=lens, lndsea=lndsea)
    
    
            dldat1  = {}
            dldat2  = {}
            dsig    = {}
            drawFlag= {}
            for region in lregion:
                # check draw or not draw
    
                if max([da1prcpAll0[region].mean()
                       ,da1prcpAll1[region].mean()
                       ,da1prcpAll1[region].mean()
                        ]) < 10.:  # mm/year
    
                    drawFlag[region]=False
                else:
                    drawFlag[region]=True
    
                if   vartype=="Ptot":
                    a1var0 = da1prcp0[region]
                    a1var1 = da1prcp1[region]
                    a1var2 = da1prcp2[region]
    
                elif vartype=="Freq":
                    a1var0 = da1freq0[region]*4*365*10 #[#/10-year]
                    a1var1 = da1freq1[region]*4*365*10
                    a1var2 = da1freq2[region]*4*365*10

                elif vartype=="Pint":
                    a1var0 = da1pint0[region]
                    a1var1 = da1pint1[region]
                    a1var2 = da1pint2[region]


                else:
                    print "check vartype",vartype
                    sys.exit()
    
                if tasType == "Tglb":
                    a1tas0 = da1tas0["GLB"]
                    a1tas1 = da1tas1["GLB"]
                    a1tas2 = da1tas2["GLB"]
                elif tasType=="Treg":
                    a1tas0 = da1tas0[region]
                    a1tas1 = da1tas1[region]
                    a1tas2 = da1tas2[region]


                #-- change --
                dldat1[region] = array(a1var1-mean(a1var0))/array(a1tas1 - mean(a1tas0))/mean(a1var0)*100
                dldat2[region] = array(a1var2-mean(a1var1))/array(a1tas2 - mean(a1tas1))/mean(a1var0)*100


                dldat1[region] = array(a1var1-mean(a1var0))/array(a1tas1 - mean(a1tas0))
                dldat2[region] = array(a1var2-mean(a1var1))/array(a1tas2 - mean(a1tas1))




                print "freq0----------------"
                print mean(a1var0)
                print "freq1----------------"
                print mean(a1var1)
                print "dfreq 0-->1 ---------"
                mean(a1var1) - mean(a1var0)



                #--- statistical test --

                t, p_d1  = scipy.stats.ttest_ind(a1var0,a1var1, equal_var=False)
                t, p_d2  = scipy.stats.ttest_ind(a1var1,a1var2, equal_var=False)
                t, p_dd  = scipy.stats.ttest_ind(dldat1[region],dldat2[region], equal_var=False)

                #--- for table ----
                if drawFlag[region] == True:
                    V0 [region,tag] = mean(a1var0)
                    dV1[region,tag] = mean(dldat1[region])
                    dV2[region,tag] = mean(dldat2[region])
                    ddV[region,tag] = (mean(dldat2[region])-mean(dldat1[region]))/abs(mean(dldat1[region]))*100.
                    PVd1[region,tag] = p_d1 
                    PVd2[region,tag] = p_d2 
                    PVdd[region,tag] = p_dd 
                else:
                    V0 [region,tag] = ""
                    dV1[region,tag] = ""
                    dV2[region,tag] = ""
                    ddV[region,tag] = ""
                    PVd1[region,tag] = ""
                    PVd2[region,tag] = ""
                    PVdd[region,tag] = ""

        #- output ---------
        lregnum = []
        for region in lregion:
            num = dregion[region][0]
            lregnum.append([region,num])
    
        lregnum = sorted(lregnum, key= lambda x: x[1])



        sout = ",,"+"ALL,"*7 + "TC,"*7 + "ExC,"*7 + "Monsoon,"*7 + "Others,"*7
        sout = sout.strip() + "\n"
        sout = sout + "num,region," + "ALL,P15-ALL(%%/K),pv1,P20-P15(%%/K),pv2,dif of dif,p-v,"*5
        sout = sout.strip() + "\n"
        for (region,num) in lregnum:
            num  = dregion[region][0]
            sout = sout + "%s,%s"%(num,region)
            for tag in ltag:
                sout = sout + ",%s,%s,%s,%s,%s,%s,%s"%(V0[region,tag],dV1[region,tag],PVd1[region,tag],dV2[region,tag],PVd2[region,tag],ddV[region,tag],PVdd[region,tag])

            sout = sout + "\n"


        # Path
        csvPath = figDir  + "/table.perK.%s.%s.th.%s.csv"%(vartype, tasType, thpr)
        f = open(csvPath, "w")
        f.write(sout)
        f.close()
        print csvPath
            
