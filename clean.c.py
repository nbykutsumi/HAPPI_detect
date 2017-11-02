from ConfigParser   import SafeConfigParser
from importlib      import import_module
import os, sys, shutil
import calendar
import myfunc.util as util
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Cyclone     = import_module("%s.Cyclone"%(detectName))
#--------------------------------------------------------
#prj     = "JRA55"
#model   = "__"
#run     = "__"
#res     = "145x288"
#noleap   = False
#tctype  = "bst"

prj     = "HAPPI"
model   = "MIROC5"
expr    ="C20"
lscen   = ["ALL","P20","P15"]
#lscen   = ["ALL"]
#lens    = [1,11,21,31,41]
lens    = range(1,50+1)
#lens    = [1]
res     = "128x256"
noleap  = True
#tctype  = "notc"
tctype  = "obj"

lkey = [[scen, ens] for scen in lscen for ens in lens]
for scen, ens in lkey:
    run  = "%s-%s-%03d"%(expr, scen, ens)
    cfg_det  = config_func.config_func(prj=prj, model=model, run=run)
    cfg_det["res"] = res
    
    baseDir = cfg_det["baseDir"]




    lvar = ["run.mean","age","dura","ipos","pgrad","vortlw","epos","idate","nextpos","prepos"]
    
    dPath = {}
    for var in lvar:
      if var == "run.mean":
        dPath[var] = baseDir + "/%s"%(var)
      else:
        dPath[var] = baseDir + "/6hr/%s"%(var)
    
      print dPath[var]
      print os.path.exists(dPath[var])
      if os.path.exists(dPath[var]):
        shutil.rmtree(dPath[var])





