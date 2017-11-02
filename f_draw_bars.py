import matplotlib
matplotlib.use("Agg")

import os, sys
from numpy import *
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func

def ret_bottom(lv, idat):
  if idat == 0:
    bottom = 0
  else:
    bottom_posi  = 0.0
    bottom_nega  = 0.0
    for i,v in enumerate(lv[:idat]):
      if v >=0:
        bottom_posi = bottom_posi + v
      elif v <0:
        bottom_nega = bottom_nega + v
    #-------
    if lv[idat] >=0:
      bottom = bottom_posi
    elif lv[idat] <0:
      bottom = bottom_nega
  return bottom



def draw_barstack(ddat, dsig, lregion, vmin, vmax, stitle, ylabel, figPath):
    fig = plt.figure(figsize=(7.5,2.8))
    ax  = fig.add_axes([0.1,0.33,0.85,0.57])
    wbar= 0.2
    yfontsize = 10


    dregion = hd_func.dict_IPCC_codeKey()
    lnum    = []
    for region in lregion:
        lnum.append(dregion[region][0])

    lregnum = zip(lregion,lnum)
    lregnum = sorted(lregnum, key= lambda x: x[1])

    lx = []
    for iregion,[region,num] in enumerate(lregnum):
        x   = iregion*wbar*1.2
        lx.append(x)
        vtc = ddat[region,"tc"]
        vcf = ddat[region,"cf"]
        vms = ddat[region,"ms"]
        vot = ddat[region,"ot"]

        ltmp= [vtc,vcf,vms,vot]
        btc = ret_bottom(ltmp, 0)    
        bcf = ret_bottom(ltmp, 1) 
        bms = ret_bottom(ltmp, 2) 
        bot = ret_bottom(ltmp, 3)

        #ax.bar(x, vtc, width=wbar, color="r", tick_label="%s"%(num))
        ax.bar(x, vtc, width=wbar, color="orangered")
        ax.bar(x, vcf, width=wbar, bottom=bcf, color="skyblue")
        ax.bar(x, vms, width=wbar, bottom=bms, color="navy")
        ax.bar(x, vot, width=wbar, bottom=bot, color="gold")

    #--- hline ----------
    ax.axhline(y=0)

    #--- vertical grids
    ax.xaxis.grid(linestyle="--")
    ax.yaxis.grid(linestyle="--")

    #--- x-ticklabel ----
    ax.set_xticks(lx)

    lxlabel = []
    for (region,num) in lregnum:
        if dsig[region]==True:
            slabel = "*%d %s"%(num,region)
        else:
            slabel = " %d %s"%(num,region)
        lxlabel.append(slabel)

    ax.set_xticklabels(lxlabel, rotation=-90, fontsize=12)
    #ax.tick_params(bottom="off",labelbottom="off", labelsize=yfontsize)

    #--- y-ticklabel ----
    ly = arange(-1.0,1.0+0.01,0.05)
    lylabel= ["%.2f"%(y) for y in ly]
    ax.set_yticks(ly)
    ax.set_yticklabels(lylabel)
    ax.set_ylim([vmin,vmax])

    #--- y-axis label
    ax.set_ylabel(ylabel)

    #--- x-axis limit
    ax.set_xlim([lx[0]-wbar*0.6, lx[-1]+wbar*0.6])

    #--- title ----------
    plt.title(stitle, fontsize=12)

    plt.savefig(figPath)
    plt.close()
    print figPath


