import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

#************************************
def draw_boxplot_multi(dldat, dsig, ltag, stitle, figPath, dylim=None):
    #-- Figure --------
    if len(ltag)==4:
        figplot = plt.figure(figsize=(0.8,2.1))
    elif len(ltag)==5:
        figplot = plt.figure(figsize=(0.8,2.6))

    for itag,tag in enumerate(ltag[::-1]):
        if len(ltag)==4:
            axplot = figplot.add_axes([0.6,0.02+0.21*itag,0.35,0.21])
        elif len(ltag)==5:
            axplot = figplot.add_axes([0.6,0.02+0.17*itag,0.35,0.17])

        ldat   = dldat[tag]
        nscen  = len(ldat)

        medianprops = dict(linestyle='-', linewidth=0, color='blue')
        for iscen, dat in enumerate(ldat):
            if (dsig[tag] == True)&(iscen==2):
                meanprops   = dict(linestyle='-', linewidth=2.3, color='red')
            else:
                meanprops   = dict(linestyle='-', linewidth=2.3, color='blue')

            if np.allclose(dat, np.zeros(len(dat))): continue
            bp = axplot.boxplot(dat,positions=[iscen], widths=0.8, whis=[5,95], sym="", medianprops=medianprops, showmeans=True, meanline=True, meanprops=meanprops)
    
            #plt.setp(bp['medians'], color='blue', linewidth=2)


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
        
    
        #--- title ----------
        plt.suptitle(stitle, fontsize=10)
    
    plt.savefig(figPath)
    print figPath
    plt.close()
     
