from numpy import *
from datetime import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys
import calendar
import myfunc.util as util
import myfunc.IO.HAPPI as HAPPI
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
#Cyclone     = import_module("%s.Cyclone"%(detectName))
#--------------------------------------------------------
y,x      = 84, 93

#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"
#noleap   = False

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
scen    = "ALL"

#lens    = [1,1,1]
lens    = [1,11,21,31,41]
res     = "128x256"
noleap  = True
ny      = 128
nx      = 256
nz      = 1460

iYear   = 2006
eYear   = 2015
lYear   = range(iYear,eYear+1)

p      = 99.9

cfg_det  = config_func.config_func(prj=prj, model=model, run="%s-%s-001"%(expr,scen))
rootDir  = cfg_det["rootDir"]
baseDir  = cfg_det["baseDir"]

#------------------------
mem      = 2.0e+9  # 1e+9 = 1GB
y  = int(mem / float(4*nx*4*365.*len(lYear)*len(lens)))
y  = min(y, ny)

ly = range(0,ny+1,y)
if y == ny:
    lly = [[0,ny]]
else:
    lly= zip(ly, ly[1:]+[ny])
print lly
#------------------------
print 
print "p=",p, "*"*50
print "CALC"
a1in = empty(nz*len(lYear)*len(lens))
ibatch = -1
for iens,ens in enumerate(lens):
    run = "C20-ALL-%s"%(ens)
    hp  = HAPPI.Happi()
    hp(model, expr, scen, ens)

    for kYear,Year in enumerate(lYear):
        ibatch = ibatch+1
        print ens,Year
        a3dat = hp.load_batch_6hr("prcp",Year)
        print "pmean=",a3dat[:,y,x].mean()
        print "iz=",ibatch*nz,"-", (ibatch+1)*nz
        a1in[ibatch*nz: (ibatch+1)*nz]= a3dat[:,y,x]

print p,"tile=", percentile(a1in, p)

sout = "\n".join(map(str, a1in))
sname = "./temp.ptile.csv"
f=open(sname, "w"); f.write(sout); f.close()

print "*"*50
print "program"
sDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
sPath = sDir + "/%s.%s.%s.%s.%04dY.p%6.3f.%dx%d"%(prj,model,expr,scen,len(lYear)*len(lens), p, ny, nx)

a2in  = fromfile(sPath, float32).reshape(ny,nx)
print "ptile-program=",a2in[y,x]
print "*"*50
print sname
