from numpy          import *
from ConfigParser   import SafeConfigParser
from importlib      import import_module
import  os,sys
import  myfunc.util as util
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
config_func = import_module("%s.config_func"%(detectName))
#--------------------------------------------------------
prj  = "HAPPI"
model= "MIROC5"
#run  = "C20-ALL-001"
expr = "C20"
scen = "ALL"
lens  = [1]
#ltune = ["100-100","130-100","100-130","130-130"]
ltune = ["090-100","080-100"]
res  = "128x256"

def my_symlink(srcPath, dstPath):
    if os.path.exists(dstPath):
        print "file exists"
        print dstPath
        print "SKIP"
        pass
    else:
        os.symlink(srcPath, dstPath)


# Make tuning directories and link dupplications
for ens in lens:
    for tune in ltune:
        run = "%s-%s-%03d"%(expr, scen, ens)
        cfgDet      = config_func.config_func(prj, model, run)
        baseDirSrc  = cfgDet["baseDir"]
    
        run = "%s-%s-%03d-%s"%(expr, scen, ens, tune)
        cfgDet      = config_func.config_func(prj, model, run)
        baseDirDst  = cfgDet["baseDir"]

        # Link
        print "-"*50
        print "Link"
        print baseDirDst
        my_symlink(baseDirSrc, baseDirDst)





