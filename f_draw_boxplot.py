import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats


#************************************
def draw_boxplot_multi(dldat, stitle, figPath, dylim=None):
    #-- Figure --------
    figplot = plt.figure(figsize=(0.82,2.0))
    #figplot = plt.figure(figsize=(2.0,0.8))
    ltag   = ["tc","cf","ms","ot"]
    #lcolor = ["g","blue","orangered"]

    for itag,tag in enumerate(ltag[::-1]):

        axplot = figplot.add_axes([0.55,0.05+0.22*itag,0.4,0.18])

        ldat   = dldat[tag]
        nscen  = len(ldat)
        for iscen, dat in enumerate(ldat):
            if np.allclose(dat, np.zeros(len(dat))): continue
            bp = axplot.boxplot(dat,positions=[iscen], widths=0.8, whis=[5,95], sym="")
    
            plt.setp(bp['medians'], color='red', linewidth=2)
    
        # x-axis
        axplot.set_xlim((-0.5,nscen-0.5))
   
        #--- no bottom ticks, y-ticklabel ----
        axplot.tick_params(bottom="off",labelbottom="off")
    
    
        # y-axis
        axplot.tick_params(axis='y', which='major', pad=0)

        # ylim
        if dylim != None:
            ymin = dylim[tag][0]
            ymax = dylim[tag][1]
            if ymin != None:
               axplot.set_ylim((ymin,ymax))
            if ymax != None:
               axplot.set_ylim((ymin,ymax))
        
    
        #    color = lcolor[iscen]
        #    kde   = scipy.stats.gaussian_kde(dat, bw_method="scott")
        #    N,Bins,Patches = axplot1.hist(dat, bins=n_bins, alpha=0.3, histtype="bar", color=color)
     
        #    x     = np.linspace(dat.min(),dat.max(),100)
        #    axplot2.plot(x, kde(x), color=color)
     
        ##--- ylimit -------------------------
        #axplot1.set_ylim(bottom=0)
        #axplot2.set_ylim(bottom=0)
    
        ##--- xlimit -------------------------
        #if xmin != None:
        #    axplot1.set_xlim((xmin,xmax))
        #    axplot2.set_xlim((xmin,xmax))
     
        ##--- bottom line --------------------
        #plt.axhline(0, color="black")
     
        ##--- frame off ------
        #axplot1.spines["top"].set_visible(False)
        #axplot2.spines["top"].set_visible(False)
        #--- title ----------
        plt.suptitle(stitle, fontsize=10)
        #axplot1.text(0.01,0.79, stitle2, fontsize=10, transform=axplot1.transAxes)
    
    plt.savefig(figPath)
    print figPath
    plt.close()
     
