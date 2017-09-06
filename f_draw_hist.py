import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def draw_hist(ldat, stitle1, stitle2, figPath, xmin=None, xmax=None):
    #-- Figure --------
    figplot = plt.figure(figsize=(3.5,0.8))
    axplot1  = figplot.add_axes([0.13,0.28,0.73,0.45])
    axplot2  = axplot1.twinx()
 
    #lcolor = ["orangered","blue","mediamseagreen"]
    lcolor = ["g","blue","orangered"]
    n_bins = 10
 
    for iscen, dat in enumerate(ldat):
        if np.allclose(dat, np.zeros(len(dat))): continue
        color = lcolor[iscen]
        kde   = scipy.stats.gaussian_kde(dat, bw_method="scott")
        N,Bins,Patches = axplot1.hist(dat, bins=n_bins, alpha=0.3, histtype="bar", color=color)
 
        x     = np.linspace(dat.min(),dat.max(),100)
        axplot2.plot(x, kde(x), color=color)
 
    #--- ylimit -------------------------
    axplot1.set_ylim(bottom=0)
    axplot2.set_ylim(bottom=0)

    #--- xlimit -------------------------
    if xmin != None:
        axplot1.set_xlim((xmin,xmax))
        axplot2.set_xlim((xmin,xmax))
 
    #--- bottom line --------------------
    plt.axhline(0, color="black")
 
    #--- frame off ------
    axplot1.spines["top"].set_visible(False)
    axplot2.spines["top"].set_visible(False)
    #--- title ----------
    #plt.suptitle(stitle1, fontsize=10)
    plt.title(stitle1, fontsize=11)
    axplot1.text(0.01,0.79, stitle2, fontsize=10, transform=axplot1.transAxes)
    plt.savefig(figPath)
    print figPath
    plt.close()
 
