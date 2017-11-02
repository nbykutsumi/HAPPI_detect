from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
model   = "MIROC5"
expr    = "C20"
res     = "128x256"

lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion = ["GLB"]

#- Switch  ------------
Total    = False
ExFreq   = True
Fraction = False

ChangeRat= True
#----------------------
dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["plain","tc","cf","ms","ot"]
season = "ALL"
iy   = 17   # top
ey   = -1  # bottom
ix   = 0
ex   = -1

# Directory
baseDir ="/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"


# lregnum ---------
dregion = hd_func.dict_IPCC_codeKey()
lregnum = []
for region in lregion:
    num = dregion[region][0]
    lregnum.append([region,num])

lregnum = sorted(lregnum, key= lambda x: x[1])
#------------------


#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr

#**********************
# Ptot, Freq, Pint for Total precipitation
#----------------------
#"""
thpr = 1
#lvartype = ["Ptot","Freq","Pint"]
lvartype = ["Ptot"]
for vartype in lvartype:
    if Total != True: continue

    if ChangeRat == True:
        vartype_tmp="rat."+vartype
    else:
        vartype_tmp=vartype

    for region,num in lregnum:
        da2dat  = {}
        for itag,tag in enumerate(ltag):
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype_tmp, thpr, tag, region)
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            if itag==0:
                da2dat[itag] = a2array
            else:
                da2dat[itag] = a2array[iy:]

        a2oarray  = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3], da2dat[4]]) 
        oimg      = Image.fromarray(a2oarray)
        oPath     = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype_tmp, thpr, region)
        oimg.save(oPath)
        print oPath

#"""

#**********************
# Freq for Extreme precipitation
#----------------------
vartype = "Freq"
#lthpr  = ["p99.900","p99.990"]
lthpr  = ["p99.990"]
for thpr in lthpr:
    if ExFreq != True: continue

    if ChangeRat == True:
        vartype_tmp="rat."+vartype


    for region in lregion:
        da2dat  = {}
        for itag,tag in enumerate(ltag):
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype_tmp, thpr, tag, region)
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            if itag==0:
                da2dat[itag] = a2array
            else:
                da2dat[itag] = a2array[iy:]


        a2oarray  = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3], da2dat[4]]) 
        oimg      = Image.fromarray(a2oarray)
        oPath     = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype_tmp, thpr, region)
        oimg.save(oPath)
        print oPath


#**********************
# Proportion for Extreme precipitation
#----------------------
"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    for region in lregion:
        da2dat  = {}
        for itag,tag in enumerate(ltag):
            figPath = figDir  + "/hist.Fraction.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            if itag==0:
                da2dat[itag] = a2array
            else:
                da2dat[itag] = a2array[iy:]

        a2oarray  = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3]])             
        oimg      = Image.fromarray(a2oarray)
        oPath     = figDir + "/hist.Fraction.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        oimg.save(oPath)
        print oPath


"""

