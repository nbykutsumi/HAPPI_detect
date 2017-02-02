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
ltune = ["100-t02","130-t02","160-t02","190-t02"]
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
        run = "%s-%s-%03d-100"%(expr, scen, ens)
        cfgDet      = config_func.config_func(prj, model, run)
        baseDirSrc  = cfgDet["baseDir"]
    
        run = "%s-%s-%03d-%s"%(expr, scen, ens, tune)
        cfgDet      = config_func.config_func(prj, model, run)
        baseDirDst  = cfgDet["baseDir"]

        # Make directories
        print "-"*50
        print "Make directory"
        print baseDirDst
        util.mk_dir(baseDirDst)

        Dir6hr = os.path.join(baseDirDst, "6hr") 
        print Dir6hr
        util.mk_dir(Dir6hr)

        # Link
        latSrc = os.path.join(baseDirSrc,"lat.txt")
        lonSrc = os.path.join(baseDirSrc,"lon.txt")
        constSrc= os.path.join(baseDirSrc,"const") 
        runmeanSrc= os.path.join(baseDirSrc,"run.mean")
        pgradSrc= os.path.join(baseDirSrc,"6hr","pgrad") 
        vortlwSrc= os.path.join(baseDirSrc,"6hr","vortlw") 
        clistSrc= os.path.join(baseDirSrc,"6hr","clist") 

        latDst = os.path.join(baseDirDst,"lat.txt")
        lonDst = os.path.join(baseDirDst,"lon.txt")
        constDst= os.path.join(baseDirDst,"const") 
        runmeanDst= os.path.join(baseDirDst,"run.mean") 
        pgradDst= os.path.join(baseDirDst,"6hr","pgrad") 
        vortlwDst= os.path.join(baseDirDst,"6hr","vortlw") 
        clistDst= os.path.join(baseDirDst,"6hr","clist") 

        print "-"*50
        print "Link"
        print latDst
        my_symlink(latSrc, latDst)
        print lonDst
        my_symlink(lonSrc, lonDst)
        print constDst
        my_symlink(constSrc, constDst)
        print runmeanDst
        my_symlink(runmeanSrc, runmeanDst)
        print pgradDst
        my_symlink(pgradSrc, pgradDst)
        print vortlwDst
        my_symlink(vortlwSrc, vortlwDst)
        print clistDst
        my_symlink(clistSrc, clistDst)






