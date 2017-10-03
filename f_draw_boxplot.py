import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

#************************************
def draw_boxplot_multi(dldat, dsig, ltag, stitle, figPath, ddraw=None, dylim=None, dytick=None, hline=None):
    #-- Figure --------
    if len(ltag)==4:
        figplot = plt.figure(figsize=(0.9,2.1))
    elif len(ltag)==5:
        figplot = plt.figure(figsize=(0.9,2.6))

    for itag,tag in enumerate(ltag[::-1]):

        if len(ltag)==4:
            axplot = figplot.add_axes([0.6,0.02+0.21*itag,0.35,0.21])
        elif len(ltag)==5:
            axplot = figplot.add_axes([0.6,0.02+0.17*itag,0.35,0.17])

        #- check draw flag
        if ddraw != None:
            if ddraw[tag] == False:
                plt.tick_params(left="off",bottom="off",right="off",labelleft="off",labelbottom="off")
                continue
        #---------------

        ldat   = dldat[tag]
        nscen  = len(ldat)

        medianprops = dict(linestyle='-', linewidth=0, color='blue')
        dcolor = {1:"cyan",2:"red"}
        for iscen, dat in enumerate(ldat):
            if dsig[tag][iscen] == True:
                meanprops   = dict(linestyle='-', linewidth=2.3, color=dcolor[iscen])
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

        # yticks
        if dytick != None:
            if dytick[tag] != None:
                plt.yticks(dytick[tag],dytick[tag])
        
        # h-line
        if hline != None:
            plt.axhline(hline, color="k",linestyle="--") 
    
        #--- title ----------
        plt.suptitle(stitle, fontsize=10)
    
    plt.savefig(figPath)
    print figPath
    plt.close()


