import matplotlib as mpl
mpl.use("Agg")
from numpy import *
from datetime       import datetime, timedelta
from ConfigParser   import SafeConfigParser
from importlib      import import_module
from matplotlib.ticker import AutoMinorLocator
import os, sys
import calendar
import myfunc.util as util
import matplotlib.pyplot as plt
# Config ------------------------------------------------
cfg         = SafeConfigParser(os.environ)
cfg.read("/".join(__file__.split("/")[:-1]) + "/config")
cfg._sections["Defaults"]
detectName  = cfg.get("Defaults","detectName")
config_func = import_module("%s.config_func"%(detectName))
Tag         = import_module("%s.Tag"%(detectName))
#--------------------------------------------------------
prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"
lens    = range(1,50)
#lens    = range(1,3)
res     = "128x256"
ny, nx  = 128, 256
miss    = -9999.
vmin    = 100  # mm/year


#ltag   = ["plain","tc","cf","ms","ot"]


lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]
#lregion     = ["SAU"]

dieYear = {"ALL": (2006, 2015)
         ,"P15": (2106, 2115)
         ,"P20": (2106, 2115)
         }

"""
[['Alaska/N.W. Canada [ALA:1]', 'ALA', 'land'],
 ['Amazon [AMZ:7]', 'AMZ', 'land'],
 ['Central America/Mexico [CAM:6]', 'CAM', 'land'],
 ['small islands regions Caribbean', 'CAR*', 'all'],
 ['Central Asia [CAS:20]', 'CAS', 'land'],
 ['Central Europe [CEU:12]', 'CEU', 'land'],
 ['Canada/Greenland/Iceland [CGI:2]', 'CGI', 'land'],
 ['Central North America [CNA:4]', 'CNA', 'land'],
 ['East Africa [EAF:16]', 'EAF', 'land'],
 ['East Asia [EAS:22]', 'EAS', 'land'],
 ['East North America [ENA:5]', 'ENA', 'land'],
 ['South Europe/Mediterranean [MED:13]', 'MED', 'land'],
 ['North Asia [NAS:18]', 'NAS', 'land'],
 ['North Australia [NAU:25]', 'NAU', 'land'],
 ['North-East Brazil [NEB:8]', 'NEB', 'land'],
 ['North Europe [NEU:11]', 'NEU', 'land'],
 ['Southern Africa [SAF:17]', 'SAF', 'land'],
 ['Sahara [SAH:14]', 'SAH', 'land'],
 ['South Asia [SAS:23]', 'SAS', 'land; sea'],
 ['South Australia/New Zealand [SAU:26]', 'SAU', 'land'],
 ['Southeast Asia [SEA:24]', 'SEA', 'land; sea'],
 ['Southeastern South America [SSA:10]', 'SSA', 'land'],
 ['Tibetan Plateau [TIB:21]', 'TIB', 'land'],
 ['West Africa [WAF:15]', 'WAF', 'land'],
 ['West Asia [WAS:19]', 'WAS', 'land'],
 ['West North America [WNA:3]', 'WNA', 'land'],
 ['West Coast South America [WSA:9]', 'WSA', 'land'],
 ['Antarctica', 'ANT*', 'land; sea'],
 ['Arctic', 'ARC*', 'land; sea'],
 ['Pacific Islands region[2]', 'NTP*', 'all'],
 ['Southern Topical Pacific', 'STP*', 'all'],
 ['Pacific Islands region[3]', 'ETP*', 'all'],
 ['West Indian Ocean', 'WIO*', 'all']]
"""


#----------------------
def ret_sthpr(thpr):
      if type(thpr) == str:
        sthpr = thpr
      else:
        sthpr = "%05.1f"%(thpr)
      return sthpr


# Function ----------

def draw_bar(d_p, d_n, ytick, lylim, stitle, figPath):
    fig  = plt.figure(figsize=(2.4,3.4))
    ax   = fig.add_axes([0.21,0.28,0.70,0.62])
    ltag = ["All","TC","ExC","Mons","Others"]
    llndsea = ["lnd","sea"]
    wbar = 0.3

    for itag, tag in enumerate(ltag):
        x = itag
        colorp="gray"
        colorn="gray"
   
        y =  d_p[tag]
        ax.bar(x,y,width=wbar, color=colorp,hatch=None,edgecolor="k")
    
        y = -d_n[tag]
        ax.bar(x,y,width=wbar, color=colorn, hatch="////",edgecolor="k")
    
    
        # h-line
        plt.axhline(0, color="k", linestyle="-",linewidth=0.5)
    
        # x-axis
        lx = [i+0.5*wbar for i in [0,1,2,3,4]]
        lsx= ltag
        plt.xticks(lx, lsx, fontsize=14, rotation=90)
    
        # y-axis
        ml  = AutoMinorLocator(2)
        ax.yaxis.set_minor_locator(ml)

        lyp =  ytick
        lyn = -lyp[::-1]
        ly  = concatenate([lyn,[0],lyp],axis=0)
        lsy = [abs(y) for y in ly]
        plt.yticks(ly,lsy, fontsize=14)
        plt.ylim(lylim)
    
        # title
        plt.title(stitle, fontsize=8)
    
    plt.savefig(figPath)
    print figPath



#--------------------------------------

# Load (Region counts) *****
n_all = {}
n_sig_p = {}
n_sig_n = {}
r_sig_p= {}    # positive change (increase)
r_sig_n= {}    # negative change (decrease)

       
figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/fig"
util.mk_dir(figDir)
csvPath = os.path.join(figDir,"count.sig.Region.csv")
f = open(csvPath, "r"); lines=f.readlines(); f.close()

for line in lines[1:]:
    line   = line.strip().split(",")
    thpr   = line[0]
    tag    = line[1]
    var    = line[2]
    scen0  = line[3]
    scen1  = line[4]
    lndsea = line[5]
    Nall   = int(line[6])
    Nsigp  = int(line[7])
    Nsign  = int(line[8])
    Rsigp  = float(line[9])
    Rsign  = float(line[10])

    r_sig_p[thpr,tag,var,scen0,scen1,lndsea] = Rsigp
    r_sig_n[thpr,tag,var,scen0,scen1,lndsea] = Rsign


# Figure (count regions) ****
llscen = [["P15","P20"]]

#lkey1  = [["1","ptot"],["1","pint"],["1","freq"]]
#lkey2  = [["p99.990","freq"],["p99.990","ptot"]]
#lkey   =  lkey1 + lkey2 
lkey   = [["1","ptot"],["p99.990","freq"]]

d_p   = {}
d_n   = {}
lndsea= "lnd"
for [scen0,scen1] in llscen:
    for [thpr,var] in lkey:
        for tag in ["All","TC","ExC","Mons","Others"]:
            d_p[tag] =  r_sig_p[thpr,tag,var,scen0,scen1,lndsea]
            d_n[tag] =  r_sig_n[thpr,tag,var,scen0,scen1,lndsea]

        ytick = arange(0.2, 1.0+0.01, 0.2)   # Do not include zero
        lylim = [-1.0,1.0]

        figPath = figDir + "/bar.count.sig.Region.%s.%s.thp.%s.%s.png"%(scen0,scen1,thpr,var)
        stitle = "%s th=%s (%s-%s) Reg"%(var,thpr,scen1,scen0)

        draw_bar(d_p,d_n, ytick, lylim, stitle, figPath)





