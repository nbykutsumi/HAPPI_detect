from numpy import *
import f_draw_mapglobal

import myfunc.IO.HAPPI as HAPPI

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"

hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="P15", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon

bnd = range(0,200,1)
dotstep = 3
miss  = -9999.
midpoint = None

lregion=['ALA','AMZ','CAM','CAR*','CAS','CEU','CGI','CNA','EAF','EAS','ENA','MED','NAS','NAU','NEB','NEU','SAF','SAH','SAS','SAU','SEA','SSA','TIB','WAF','WAS','WNA','WSA','ANT*','ARC*','NTP*','STP*','ETP*','WIO*']


#lregion=['ALA','AMZ','CAM','CAR*','CAS','CEU','CGI','CNA']

# Load Sample data
figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
figPath = figDir + "/HAPPI.MIROC5.C20.ALL.0500Y.p99.900.128x256"
a2dat   = fromfile(figPath, float32).reshape(128,256)*60*60*24

a2hatch = ma.masked_less(a2dat, 50).filled(miss)


figPath = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.2106-2115.ALL/MIROC5/fig/temp.map.png"
cbarPath = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.2106-2115.ALL/MIROC5/fig/cbar.temp.png"

shapePath= '/home/utsumi/mnt/wellshare/data/MapMask/IPCC2012_shapefile/referenceRegions.shp'


f_draw_mapglobal.draw_map_robin(a2dat, a2hatch, Lat, Lon, miss=-9999, bnd=None, cmap="Spectral", midpoint=None, figPath=figPath, cbarPath=cbarPath, lregion=lregion)
