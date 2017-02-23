from numpy import *
from myfunc.fig import Fig
import myfunc.IO.HAPPI as HAPPI

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
lscen   = ["ALL"]
scen    = "ALL"
ens     = 1
res     = "128x256"
noleap  = True
ny, nx  = 128, 256

hp = HAPPI.Happi()
hp(model=model, expr=expr, scen=scen, ens=ens)
Lat = hp.Lat
Lon = hp.Lon
ny  = 128
nx  = 256

lthpr = [0,0.1, 0.5, 1.0]

srcPath00 = "./temp.0.128x256"
srcPath01 = "./temp.0.1.128x256"
srcPath05 = "./temp.0.5.128x256"
srcPath10 = "./temp.1.0.128x256"

d={}
d[0] = fromfile(srcPath00, int32).reshape(ny,nx)
d[0.1] = fromfile(srcPath01, int32).reshape(ny,nx)
d[0.5] = fromfile(srcPath05, int32).reshape(ny,nx)
d[1.0] = fromfile(srcPath10, int32).reshape(ny,nx)

print d[0].max()
for thpr in [0,0.1, 0.5, 1.0]:
    a = d[thpr]/(4*365.) *100.
    figPath = "./temp.%3.1f.png"%(thpr)
    stitle  = "pecip events [%%] : thpr = %3.1f [mm/day]"%(thpr)
    Fig.DrawMapSimple( a, Lat, Lon, stitle=stitle, figname=figPath, vmin=0.0, vmax=100.)
    print figPath


