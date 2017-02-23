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
run     = "C20-ALL-001"
res     = "128x256"
noleap  = True
#tctype  = "notc"
tctype  = "obj"

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
