from numpy import *
from bisect import bisect, bisect_right, bisect_left
import os, sys, inspect

def path_sumnum(**kwargs):
    #"""model, expr, scen, ens, sthpr, tag, sumnum, Year, Mon"""
    """model, run, sthpr, tag, sumnum, Year, Mon, res"""

    model = kwargs["model"]
    run   = kwargs["run"]
    res   = kwargs["res"]
    sthpr = kwargs["sthpr"]
    tag   = kwargs["tag"]
    sumnum= kwargs["sumnum"]
    Year  = kwargs["Year"]
    Mon   = kwargs["Mon"]
    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/tagpr/%s/%s/th.%s"%(model, run, sthpr)
    sDir  = baseDir + "/%04d%02d"%(Year,Mon)
    sPath = sDir + "/%s.%s.%s"%(sumnum, tag, res)
    return baseDir, sDir, sPath


def path_sumnum_clim(**kwargs):
    """
    model, run, res, sthpr, tag, iYear, eYear, season, sumnum 

    """

    model = kwargs["model"]
    run   = kwargs["run"]
    res   = kwargs["res"]
    sthpr = kwargs["sthpr"]
    tag   = kwargs["tag"]
    iYear = kwargs["iYear"]
    eYear = kwargs["eYear"]
    season= kwargs["season"]
    sumnum= kwargs["sumnum"] 

    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/tagpr.%04d-%04d.%s/%s"%(iYear, eYear, season, model)
    #sDir = baseDir + "/%s-%s-%03d/th.%s"%(expr, scen, ens, sthpr)
    sDir = baseDir + "/%s/th.%s"%(run, sthpr)
    sPath = sDir + "/%s.%s.%s"%(sumnum, tag, res)
    return baseDir, sDir, sPath


def path_dpr(**kwargs):
    """
    model, run, res, sthpr, tag, iYear, eYear, season, var
    var = dNI, NdI, dNdI, dP

    """

    model = kwargs["model"]
    run   = kwargs["run"]
    res   = kwargs["res"]
    sthpr = kwargs["sthpr"]
    tag   = kwargs["tag"]
    iYear = kwargs["iYear"]
    eYear = kwargs["eYear"]
    season= kwargs["season"]
    var   = kwargs["var"] 

    baseDir = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.%04d-%04d.%s/%s"%(iYear, eYear, season, model)
    sDir = baseDir + "/%s/th.%s"%(run, sthpr)
    sPath = sDir + "/%s.%s.%s"%(tag, var, res)
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


def ret_regioncode2name(region):
  if   region == "ALA": name ="Alaska"  #Alaska / Northwest Canada
  elif region == "AMZ": name ="Amazon"   #Amazon
  elif region == "CAM": name ="C.Amr"   #Central America and Mexico
  elif region == "CAS": name ="C.Asia"  #Central Asia
  elif region == "CEU": name ="C.Euro"  #Central Europe
  elif region == "CGI": name ="E.Can"   #East Canada, Greenland, Iceland
  elif region == "CNA": name ="CN.Amr"   #Central North America
  elif region == "EAF": name ="E.Afr"  #East Africa
  elif region == "EAS": name ="E.Asia"  #East Asia
  elif region == "ENA": name ="EN.Amr"  #East North America
  elif region == "MED": name ="Medit"  #Southern Europe and Mediterranean
  elif region == "NAS": name ="N.Asia"  #North Asia
  elif region == "NAU": name ="N.Aust"  #North Australia
  elif region == "NEB": name ="NE.Bras"   #Northeastern Brazil
  elif region == "NEU": name ="N.Euro"  #Northern Europe
  elif region == "SAF": name ="S.Afr"  #Southern Africa
  elif region == "SAH": name ="Sahara"  #Sahara
  elif region == "SAS": name ="S.Asia"  #South Asia
  elif region == "SAU": name ="S.Aust"  #South Australia / New Zealand
  elif region == "SSA": name ="SES.Amr"  #Southeastern South America
  elif region == "SEA": name ="SE.Asia"  #Southeast Asia
  elif region == "TIB": name ="Tibet"  #Tibetan Plateau
  elif region == "WAF": name ="W.Afr"  #West Africa
  elif region == "WAS": name ="W.Asia"  #West Asia
  elif region == "WSA": name ="WS.Amr"   #West Coast South America
  elif region == "WNA": name ="WN.Amr"   #West North America

  elif region == "JPN": name ="Japan"   #West North America
  elif region == "NWSTP": name ="NW.STPac"   #Northwestern Subtropical Pacific
  return name

def ret_a2region_ipcc(region, ny, nx):
  if   region == "ALA": regnum =1   #Alaska / Northwest Canada
  elif region == "AMZ": regnum =7   #Amazon
  elif region == "CAM": regnum =6   #Central America and Mexico
  elif region == "CAS": regnum =20  #Central Asia
  elif region == "CEU": regnum =12  #Central Europe
  elif region == "CGI": regnum =2   #East Canada, Greenland, Iceland
  elif region == "CNA": regnum =4   #Central North America
  elif region == "EAF": regnum =16  #East Africa
  elif region == "EAS": regnum =22  #East Asia
  elif region == "ENA": regnum =5   #East North America
  elif region == "MED": regnum =13  #Southern Europe and Mediterranean
  elif region == "NAS": regnum =18  #North Asia
  elif region == "NAU": regnum =25  #North Australia
  elif region == "NEB": regnum =8   #Northeastern Brazil
  elif region == "NEU": regnum =11  #Northern Europe
  elif region == "SAF": regnum =17  #Southern Africa
  elif region == "SAH": regnum =14  #Sahara
  elif region == "SAS": regnum =23  #South Asia
  elif region == "SAU": regnum =26  #South Australia / New Zealand
  elif region == "SSA": regnum =10  #Southeastern South America
  elif region == "SEA": regnum =24  #Southeast Asia
  elif region == "TIB": regnum =21  #Tibetan Plateau
  elif region == "WAF": regnum =15  #West Africa
  elif region == "WAS": regnum =19  #West Asia
  elif region == "WSA": regnum =9   #West Coast South America
  elif region == "WNA": regnum =3   #West North America
  else:
    print "by", __file__
    print "check!! region=",region
    print inspect.currentframe().f_code.co_name

    sys.exit()
  #---------------
  sdir  = "/home/utsumi/mnt/wellshare/data/MapMask/IPCC2012/NYxNX"
  sname = sdir + "/IPCC2012_map.%dx%d"%(ny,nx)
  a2map = fromfile(sname, float32).reshape(ny,nx)
  a2map = ma.masked_not_equal(a2map, regnum).filled(0.0)
  a2map = ma.masked_equal(a2map, regnum).filled(1.0)
  return a2map

def ret_regionBBox(region):
  if region == "JPN":
    lllon = 120.0
    lllat = 22.0
    urlon = 155
    urlat = 50.0
  elif region == "GLB":
    lllon = 0.0
    lllat = -80.0
    urlon = 359.9
    urlat = 80.0


  elif region == "S.ISLES":
    lllon = 122.0
    lllat = 22.0
    urlon = 132
    urlat = 31.0
  elif region == "KYUSHU":
    lllon = 129.0
    lllat = 31.0
    urlon = 132
    urlat = 34.0
  elif region == "SHIKOKU":
    lllon = 132.0
    lllat = 32.0
    urlon = 135.0
    urlat = 34.0
  elif region == "CHUGOKU":
    lllon = 131.0
    lllat = 34.0
    urlon = 135.0
    urlat = 36.0
  elif region == "KINKI":
    lllon = 135.0
    lllat = 33.0
    urlon = 137.0
    urlat = 36.0
  elif region == "SE.JPN":
    lllon = 137.0
    lllat = 34.0
    urlon = 141.0
    urlat = 36.0
  elif region == "NW.JPN":
    lllon = 136.0
    lllat = 36.0
    urlon = 140.0
    urlat = 41.0
  elif region == "NE.JPN":
    lllon = 140.0
    lllat = 36.0
    urlon = 142.0
    urlat = 41.0
  elif region == "N.JPN":
    lllon = 136.0
    lllat = 36.0
    urlon = 142.0
    urlat = 41.0
  elif region == "HOKKAIDO":
    lllon = 139.0
    lllat = 41.0
    urlon = 149.0
    urlat = 46.0
  else:
    print "check region",region
    print "by",__file__
    print inspect.currentframe().f_code.co_name
    sys.exit()
  return [[lllat,lllon],[urlat,urlon]] 


