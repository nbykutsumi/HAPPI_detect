from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
model   = "MIROC5"
expr    = "C20"
res     = "128x256"

lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion = ["EAS"]


dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }

ltag  = ["tc","cf","ms","ot"]
season = "ALL"
iy   = 16   # top
ey   = -1  # bottom
ix   = 0
ex   = -1

# Directory
thpr = 0
iYear_fut, eYear_fut = dieYear["P20"]
run  = "C20-P15-001"
baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=0, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]
figDir  = baseDir + "/fig"


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
"""
thpr = 0
lvartype = ["Ptot","Freq","Pint"]
for vartype in lvartype:
    for region in lregion:
        da2dat  = {}
        for itag,tag in enumerate(ltag):
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            if itag==0:
                da2dat[itag] = a2array
            else:
                da2dat[itag] = a2array[iy:]

        a2oarray  = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3]])             
        oimg      = Image.fromarray(a2oarray)
        oPath     = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        oimg.save(oPath)
        print oPath

"""

#**********************
# Freq for Extreme precipitation
#----------------------
"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    for region in lregion:
        da2dat  = {}
        for itag,tag in enumerate(ltag):
            figPath = figDir  + "/hist.%s.th.%s.%s.%s.png"%(vartype, thpr, tag, region)
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            if itag==0:
                da2dat[itag] = a2array
            else:
                da2dat[itag] = a2array[iy:]


        a2oarray  = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3]])             
        oimg      = Image.fromarray(a2oarray)
        oPath     = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        oimg.save(oPath)
        print oPath

"""

#**********************
# Proportion for Extreme precipitation
#----------------------
#"""
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


#"""

