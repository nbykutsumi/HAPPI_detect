from numpy import *
import os, sys
import Image
import HAPPI_detect_func as hd_func

#
model= "MIROC5"
lkey = [[1,"Ptot"],[1,"Freq"],[1,"Pint"],["p99.990","Ptot"],["p99.990","Freq"]]


ltag  = ["plain","tc","cf","ms","ot"]
season = "ALL"
iy   = 0   # top
ey   = -1  # bottom
ix   = 0
ex   = -1
#----------------------
for (thpr,vartype) in lkey:
    for tasType in ["Tglb","Treg"]:

        da2dat = {}
        for itag,tag in enumerate(ltag):
        
            # Figure
            baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS"
            figDir  = baseDir + "/fig"
            figPath = figDir  + "/boxplot.perK.%s.%s.th.%s.%s.png"%(vartype, tasType, thpr, tag)
    
    
    
            iimg    = Image.open(figPath)
            a2array = asarray(iimg)
            da2dat[itag] = a2array[iy:ey, ix:ex]
        
        da2dat[-9999] = ones(da2dat[0].shape, dtype=uint8)*255
        a2oarray = vstack( [da2dat[0], da2dat[1], da2dat[2], da2dat[3], da2dat[4] ] )
        oimg     = Image.fromarray(a2oarray)
        oPath    = figDir + "/join.boxplot.perK.%s.%s.th.%s.png"%(vartype,tasType,thpr)
    
        oimg.save(oPath)
        print oPath
        
                
