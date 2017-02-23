from numpy import *

def path_sumnum(**kwargs):
    """model, expr, scen, ens, sthpr, tag, sumnum, Year, Mon"""

    model = kwargs["model"]
    expr  = kwargs["expr"]
    scen  = kwargs["scen"]
    ens   = kwargs["ens"]
    sthpr = kwargs["sthpr"]
    tag   = kwargs["tag"]
    sumnum= kwargs["sumnum"]
    Year  = kwargs["Year"]
    Mon   = kwargs["Mon"]

    ny, nx  = 128, 256
    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/tagpr/%s/%s-%s-%03d/th.%s"%(model, expr, scen, ens, sthpr)
    sDir  = baseDir + "/%04d%02d"%(Year,Mon)
    sPath = sDir + "/%s.%s.%sx%s"%(sumnum, tag,ny,nx)
    return baseDir, sDir, sPath

def path_dpr(**kwargs):
    """
    model, expr, scen, ens, sthpr, tag, iYear, eYear, season, var
    var = dNI, NdI, dNdI, dP

    """

    model = kwargs["model"]
    expr  = kwargs["expr"]
    scen  = kwargs["scen"]
    ens   = kwargs["ens"]
    sthpr = kwargs["sthpr"]
    tag   = kwargs["tag"]
    iYear = kwargs["iYear"]
    eYear = kwargs["eYear"]
    season= kwargs["season"]
    var   = kwargs["var"] 

    ny, nx  = 128, 256
    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.%04d-%04d.%s/%s"%(iYear, eYear, season, model)
    sDir = baseDir + "/%s-%s-%03d/th.%s"%(expr, scen, ens, sthpr)
    sPath = sDir + "/%s.%s.%sx%s"%(tag, var, ny,nx)
    return baseDir, sDir, sPath


def ret_lMon(season):
  if season == "DJF":
    lmon  = [1,2, 12]
  elif season == "MAM":
    lmon  = [3,4,5]
  elif season == "JJA":
    lmon  = [6,7,8]
  elif season == "SON":
    lmon  = [9,10,11]
  elif season == "ALL":
    lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  elif type(season) == int:
    lmon  = [season]
  return lmon

