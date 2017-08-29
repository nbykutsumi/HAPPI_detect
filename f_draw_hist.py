import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def draw_hist(ldat, stitle1, stitle2, figPath):
    #-- Figure --------
    figplot = plt.figure(figsize=(3.5,1.2))
    axplot1  = figplot.add_axes([0.13,0.2,0.73,0.60])
    axplot2  = axplot1.twinx()
 
    #lcolor = ["orangered","blue","mediamseagreen"]
    lcolor = ["g","blue","orangered"]
    n_bins = 10
 
    for iscen, dat in enumerate(ldat):
        color = lcolor[iscen]
        kde   = scipy.stats.gaussian_kde(dat, bw_method="scott")
        N,Bins,Patches = axplot1.hist(dat, bins=n_bins, alpha=0.3, histtype="bar", color=color)
 
        x     = np.linspace(dat.min(),dat.max(),100)
        axplot2.plot(x, kde(x), color=color)
 
    #--- ylimit -------------------------
    axplot1.set_ylim(bottom=0)
    axplot2.set_ylim(bottom=0)
 
    #--- bottom line --------------------
    plt.axhline(0, color="black")
 
    #--- frame off ------
    axplot1.spines["top"].set_visible(False)
    axplot2.spines["top"].set_visible(False)
    #--- title ----------
    plt.suptitle(stitle1, fontsize=15)
    plt.title(stitle2, fontsize=8)
 
    plt.savefig(figPath)
    print figPath
    plt.close()
 
