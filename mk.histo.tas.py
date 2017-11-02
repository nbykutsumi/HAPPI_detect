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
import myfunc.IO.HAPPI as HAPPI
import ret_ClimRegion

prj        = "HAPPI"
expr       = "C20"
model      = "MIROC5"
res        = "128x256"

regiontype = "IPCC"
#lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
lregion    = ["GLB"]



lens       = range(1,50+1)
#lens       = range(1,2+1)
wbar       = 0.8
ny,nx      = 128, 256
miss       = -9999.
dieYear = {"JRA":[2006,2014]
          ,"NAT": [2006,2015]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }
#---------------------------------    
# Dirs
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"

dregNum = hd_func.dict_IPCC_codeKey()
hp      = HAPPI.Happi()


var  = "tas"
da1dat0  = ret_ClimRegion.load_da1dat(var=var, scen="NAT", regiontype=regiontype, lregion=lregion, lens=lens, lndsea=None)

da1dat1  = ret_ClimRegion.load_da1dat(var=var, scen="ALL", regiontype=regiontype, lregion=lregion, lens=lens, lndsea=None)

da1dat2  = ret_ClimRegion.load_da1dat(var=var, scen="P15", regiontype=regiontype, lregion=lregion, lens=lens, lndsea=None)

da1dat3  = ret_ClimRegion.load_da1dat(var=var, scen="P20", regiontype=regiontype, lregion=lregion, lens=lens, lndsea=None)

#**********************************
for region in lregion:
    #--- title ----------
    stitle1 = "%d %s"%(dregNum[region][0],region)
    stitle2 = ""
    # Path
    figPath = figDir  + "/hist.%s.%s.png"%(var, region)
    # Data
    ldat = []
    vm0  = mean(da1dat0[region])
    ldat.append(da1dat1[region]-vm0)
    ldat.append(da1dat2[region]-vm0)
    ldat.append(da1dat3[region]-vm0)
    ldat = array(ldat)
    # Statistical test
    lsig = [False]
    dat1 = da1dat1[region]
    dat2 = da1dat2[region]
    dat3 = da1dat3[region]

    print "Global mean"
    print mean(da1dat0[region])
    print mean(da1dat1[region])
    print mean(da1dat2[region])
    print mean(da1dat3[region])
    print "ensemble std"
    print std(da1dat0[region])
    print std(da1dat1[region])
    print std(da1dat2[region])
    print std(da1dat3[region])

    t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
    if p < 0.05: lsig.append(True)
    else:        lsig.append(False) 

    t, p  = scipy.stats.ttest_ind(dat1,dat2,equal_var=False)
    if p < 0.05: lsig.append(True)
    else:        lsig.append(False) 


    # DrawFlag
    drawFlag =True

    xmin=None
    xmax=None


    # Draw
    f_draw_hist.draw_hist(ldat,lsig,drawFlag,stitle1,stitle2,figPath, xmin=xmin, xmax=xmax)

