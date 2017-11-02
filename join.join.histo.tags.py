from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
model   = "MIROC5"
expr    = "C20"
res     = "128x256"

#lregion     = ["GLB","ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]

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

ltag  = ["tc","cf","ms","ot"]
season = "ALL"
iy   = 16   # top
ey   = -1  # bottom
ix   = 0
ex   = -1

# Directory
baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
figDir  = baseDir + "/fig"

# lregnum ---------
dregion = hd_func.dict_IPCC_codeKey()
lregnum = []
for region in lregion:
    num = dregion[region][0]
    lregnum.append([region,num])

lregnum = sorted(lregnum, key= lambda x: x[1])

#----------------------
def ret_sthpr(thpr):
    if type(thpr) == str:
      sthpr = thpr
    else:
      sthpr = "%05.1f"%(thpr)
    return sthpr


def join_block(da2dat):
    a2margin = da2dat[0][:28]*0+255
    a2blank  = ones(da2dat[0].shape)*0 +255
    da2dat[26]= a2blank
    da2dat[27]= a2blank
    da2dat[28]= a2blank
    print "*"*50
    print da2dat.keys()
    print "*"*50
    for i in range(29):
        da2dat[i] = concatenate([da2dat[i],a2margin],axis=0)

    #line1 = concatenate([da2dat[26],da2dat[26]]+[da2dat[i] for i in range(0,5)],axis=1)
    #line2 = concatenate([da2dat[i] for i in range(5,12)],axis=1)
    #line3 = concatenate([da2dat[i] for i in range(12,19)],axis=1)
    #line4 = concatenate([da2dat[i] for i in range(19,26)],axis=1)

    line1 = concatenate([da2dat[26],da2dat[26]]+[da2dat[i] for i in range(0,4)],axis=1)
    line2 = concatenate([da2dat[26],da2dat[26]]+[da2dat[i] for i in range(4,8)],axis=1)
    line3 = concatenate([da2dat[i] for i in range(8,14)],axis=1)
    line4 = concatenate([da2dat[i] for i in range(14,20)],axis=1)
    line5 = concatenate([da2dat[i] for i in range(20,26)],axis=1)


    #return concatenate([line1,line2,line3,line4]).astype(uint8)
    return concatenate([line1,line2,line3,line4,line5]).astype(uint8)



#**********************
# Ptot, Freq, Pint for Total precipitation
#----------------------
#thpr = 1
thpr = "p99.990"
#lvartype = ["Ptot","Freq","Pint"]
#lvartype = ["Ptot"]
lvartype = ["rat.Freq"]
for vartype in lvartype:
    if Total != True: continue

    if ChangeRat == True:
        vartype_tmp="rat."+vartype
    else:
        vartype_tmp=vartype


    da2dat  = {}
    for iregion,[region,num] in enumerate(lregnum):
        print iregion
        figPath = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype_tmp, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.%s.th.%s.png"%(vartype_tmp, thpr)
    oimg.save(oPath)
    print oPath


#**********************
# Freq for Extreme precipitation
#----------------------
vartype = "Freq"
lthpr  = ["p99.990"]
for thpr in lthpr:
    if ExFreq != True: continue

    if ChangeRat == True:
        vartype_tmp = "rat."+vartype

    da2dat  = {}
    #for iregion,region in enumerate(lregion):
    for iregion,[region,num] in enumerate(lregnum):
        figPath = figDir + "/hist.%s.th.%s.join.%s.png"%(vartype_tmp, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array
    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.%s.th.%s.png"%(vartype_tmp, thpr)
    oimg.save(oPath)
    print oPath


#**********************
# Proportion for Extreme precipitation
#----------------------
"""
vartype = "Freq"
lthpr  = ["p99.900","p99.990"]
for thpr in lthpr:
    da2dat  = {}
    for iregion,region in enumerate(lregion):
        figPath = figDir + "/hist.Fraction.%s.th.%s.join.%s.png"%(vartype, thpr, region)
        iimg    = Image.open(figPath)
        a2array = asarray(iimg)
        da2dat[iregion] = a2array

    a2oarray  = join_block(da2dat)
    oimg      = Image.fromarray(a2oarray)
    oPath     = figDir + "/join.hist.Fraction.%s.th.%s.png"%(vartype, thpr)
    oimg.save(oPath)
    print oPath


"""

