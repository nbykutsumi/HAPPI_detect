import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def draw_hist(ldat, lsig, drawFlag, stitle1, stitle2, figPath, xmin=None, xmax=None):
    #-- Figure --------
    figplot = plt.figure(figsize=(1.8,0.6))
    axplot1  = figplot.add_axes([0.16,0.33,0.77,0.26])
    axplot2  = axplot1.twinx()

 
    #lcolor = ["orangered","blue","mediamseagreen"]
    lcolor = ["g","blue","orangered"]
    n_bins = 10

    if drawFlag == True: 
        for iscen, dat in enumerate(ldat):
            if np.allclose(dat, np.zeros(len(dat))): continue
            color = lcolor[iscen]
            kde   = scipy.stats.gaussian_kde(dat, bw_method="scott")
            N,Bins,Patches = axplot1.hist(dat, bins=n_bins, alpha=0.3, histtype="bar", color=color)
     
            x     = np.linspace(dat.min(),dat.max(),100)
            axplot2.plot(x, kde(x), color=color)

            #-- mean -----------
            vm = dat.mean()
            meanPlot=axplot1.plot(vm, 0, ".",markersize=10,color=color)[0]
            meanPlot.set_clip_on(False)
            
        #--- statistical test--
        if lsig[1]==True:
            axplot1.text(0.02,-0.05, "*", fontsize=16, transform=plt.gcf().transFigure, color="b")
        if lsig[2]==True:
            axplot1.text(0.07,-0.05, "*", fontsize=16, transform=plt.gcf().transFigure, color="r")
        #--- ylimit -------------------------
        axplot1.set_ylim(bottom=0)
        axplot2.set_ylim(bottom=0)
    
        #--- xlimit -------------------------
        print "ininin",xmin
        if xmin != None:
            axplot1.set_xlim((xmin,xmax))
            axplot2.set_xlim((xmin,xmax))
        #--- axis tick labels ---------------
        axplot1.tick_params(axis="x", pad=0)
        axplot1.tick_params(axis="y", pad=0)
        #axplot2.tick_params(axis="y", pad=0)

        # Suppress 2nd y-axis
        axplot2.tick_params(right="off",labelright="off")
     
        #--- bottom line --------------------
        plt.axhline(0, color="black")

    else:
        axplot1.tick_params(left="off",bottom="off",labelleft="off",labelbottom="off")
        axplot2.tick_params(right="off",bottom="off",labelright="off")
 
    #--- frame off ------
    axplot1.spines["top"].set_visible(False)
    axplot2.spines["top"].set_visible(False)
    #--- title1 ---------
    plt.title(stitle1, fontsize=11)

    #--- title2 -----------
    axplot1.text(0.01,0.60, stitle2, fontsize=11, transform=axplot1.transAxes)

       
    plt.savefig(figPath)
    print figPath
    plt.close()
 
