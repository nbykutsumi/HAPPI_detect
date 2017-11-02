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
#lregion    = ["GLB","EAS"]

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

lthpr  = [1]
lkey = [[1,"Ptot"],[1,"Freq"],[1,"Pint"],["p99.990","Ptot"],["p99.990","Freq"]]
#lkey = [[1,"Pint"]]





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
    for tasType in ["Tglb","Treg"]:
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
                print region
                print da1prcpAll0[region].mean()
                print da1prcpAll1[region].mean()
                print da1prcpAll1[region].mean()
    
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
                    a1var0 = da1freq0[region]
                    a1var1 = da1freq1[region]
                    a1var2 = da1freq2[region]

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
                dldat1[region] = array(a1var1-mean(a1var0))/mean(a1var0)*100./array(a1tas1 - mean(a1tas0))
                dldat2[region] = array(a1var2-mean(a1var1))/mean(a1var1)*100./array(a1tas2 - mean(a1tas1))
    
    
    
                #--- statistical test --
                t, p  = scipy.stats.ttest_ind(dldat1[region],dldat2[region], equal_var=False)
                if p <0.05: dsig[region] = True
                else:       dsig[region] = False
    
            #--- vmin, vmax -----
            #ymin, ymax = -30,30
            if (vartype=="Ptot")&(thpr==1):
                ymajor = 10
                yminor = 5
                if tag == "plain":
                    ymin, ymax = -20,20
                else:
                    ymin, ymax = -40,40

            elif (vartype=="Ptot")&(thpr in ["p99.990","p99.900"]):
                ymajor = 20
                yminor = 10
                ymin, ymax = -40,120
            elif (vartype=="Pint"):
                ymajor = 10
                yminor = 5
                ymin, ymax = -10,30



            else:
                ymajor = None
                yminor = None
                ymin, ymax = None,None
        
            #--- ylabel
            ylabel = "Change of Proportion"
        
        
            #--- title ----------
            if tasType=="Treg":
                stasType="Regional T"
            elif tasType=="Tglb":
                stasType="Global T"
            stitle = " [%%/K] %s %s th=%s %s"%(vartype,tag, thpr,stasType)
            
            # Path
            figPath = figDir  + "/boxplot.perK.%s.%s.th.%s.%s.png"%(vartype, tasType, thpr, tag)
            
            f_draw_boxplot.draw_boxplot_AllRegions_2dat(dldat1=dldat1, dldat2=dldat2, drawFlag=drawFlag, dsig=dsig, stitle=stitle, figPath=figPath, ymin=ymin, ymax=ymax,ymajor=ymajor, yminor=yminor)
