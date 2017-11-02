import matplotlib as mpl
mpl.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import HAPPI_detect_func as hd_func
from matplotlib.ticker import MultipleLocator
#************************************
def draw_boxplot_multi(dldat, dsig, ltag, stitle, figPath, ddraw=None, dylim=None, dytick=None, hline=None):
    #-- Figure --------
    if len(ltag)==4:
        figplot = plt.figure(figsize=(1.0,2.1))
    elif len(ltag)==5:
        figplot = plt.figure(figsize=(1.0,2.6))

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

            lx = [1.0, 1.7, 2.2]
            x  = lx[iscen]
            bp = axplot.boxplot(dat,positions=[x], widths=0.4, whis=[5,95], sym="", medianprops=medianprops, showmeans=True, meanline=True, meanprops=meanprops)
    
            #plt.setp(bp['medians'], color='blue', linewidth=2)


        # x-axis
        axplot.set_xlim((lx[0]-0.2,lx[-1]+0.2))
   
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
    plt.title(stitle, fontsize=10,loc="right")
    
    plt.savefig(figPath)
    print figPath
    plt.close()

    


def draw_boxplot_AllRegions_2dat(dldat1, dldat2, drawFlag=None, dsig=None, stitle=None, figPath="./temp.png", ymin=None, ymax=None, ymajor=None,yminor=None):
    fig  = plt.figure(figsize =(9, 2.8))
    ax   = fig.add_axes([0.1,0.33,0.85,0.57])
    wbox = 0.3
    yfontsize = 10

    dregion = hd_func.dict_IPCC_codeKey()
    lregion = dldat1.keys()
    lregnum = []
    for region in lregion:
        num = dregion[region][0]
        lregnum.append([region,num])

    lregnum = sorted(lregnum, key= lambda x: x[1])



    for iregion,[region,num] in enumerate(lregnum):

        medianprops = dict(linestyle="-", linewidth=0)
        if dsig[region]==True:
            meanprops   = dict(linestyle="-", linewidth=2.6, color="red")
        else:
            meanprops   = dict(linestyle="-", linewidth=2.6, color="k")



        if drawFlag[region] == False:
            continue
        for idat,dat in enumerate([dldat1[region], dldat2[region]]):
            if idat==0:
                x  = iregion - wbox*0.55
            else:
                x  = iregion + wbox*0.55
            print x            
            ax.boxplot(dat, positions=[iregion+wbox*idat], widths=wbox, whis=[5,95], sym="", medianprops=medianprops, showmeans=True, meanline=True, meanprops=meanprops)

    # x-axis
    ax.set_xlim((-0.5,len(lregion)+1))

    # x-labels 
    lx      = []
    lxlabel = []
    for iregion,(region,num) in enumerate(lregnum):
        lx.append(iregion)
        if dsig[region]==True:
            slabel = "*%d %s"%(num,region)
        else:
            slabel = " %d %s"%(num,region)
        lxlabel.append(slabel)


    ax.set_xticks(lx)
    ax.set_xticklabels(lxlabel, rotation=-90, fontsize=12)

    for (ilabel,label) in enumerate(plt.gca().get_xticklabels()):
        region = lregnum[ilabel][0]
        if drawFlag[region] ==False:
            label.set_color('gray') 

    # y-ticks --
    if yminor !=None:
        minorLocator  = MultipleLocator(yminor)
        ax.yaxis.set_minor_locator(minorLocator)
    if ymajor !=None:    
        majorLocator  = MultipleLocator(ymajor)
        ax.yaxis.set_major_locator(majorLocator)


    # grid
    ax.xaxis.grid(linestyle="--")
    ax.yaxis.grid(linestyle="--",which="both")

    # y limit --
    ax.set_ylim(ymin,ymax)

    # h-line ---
    plt.axhline(0, color="k")
    
    # title ----      
    plt.title(stitle, fontsize=12)

    plt.savefig(figPath)
    print figPath
    plt.close()



def draw_boxplot_Comb(dldat0, dldat1, dldat2, drawFlag, dsig1, dsig2, lregion, ltag, stitle=None, figPath="./temp.png", lylim=None, yminor=None, ymajor=None, hline=None,dlGlbMean=None):
    #fig  = plt.figure(figsize =(10, 6))
    fig  = plt.figure(figsize =(10, 3.9))
    hax  = 0.78/5.
    wax  = 0.9/len(lregion)
    #wax  = 0.9/(len(lregion)/2.)
    wbox = 0.3

    # lregnum ---------
    dregion = hd_func.dict_IPCC_codeKey()
    lregnum = []
    for region in lregion:
        num = dregion[region][0]
        lregnum.append([region,num])

    lregnum = sorted(lregnum, key= lambda x: x[1])
    #------------------
    for itag,tag in enumerate(ltag[::-1]):
        #for iregion,[region,num] in enumerate(lregnum):
        for iregion,[region,num] in enumerate(lregnum[:14]):

            ax = fig.add_axes([0.05+wax*iregion, 0.05+hax*itag,wax,hax])

            if drawFlag[region,tag] == True:
                # set meanprops ---------
                medianprops = dict(linestyle="-", linewidth=0)
                lmeanprops  = []
                lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
                if dsig1[region,tag]==True:
                    lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="cyan"))
                else:
                    lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
    
                if dsig2[region,tag]==True:
                    lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="red"))
                else:
                    lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
                #------------------------
        
                lx = [0, 0.7, 1.2]
                for idat,dat in enumerate([dldat0[region,tag],dldat1[region,tag], dldat2[region,tag]]):
                    x = lx[idat]
                    meanprops = lmeanprops[idat]
                    ax.boxplot(dat, positions=[x], widths=wbox, whis=[5,95], sym="", medianprops=medianprops, showmeans=True, meanline=True, meanprops=meanprops)

                # draw GLB line
                if dlGlbMean !=None:
                    ax.plot(lx,dlGlbMean[tag],"-",color="gray")

        
            # x-axis
            ax.set_xlim((-0.3,1.5))
        
            # x-labels 
            #ax.set_xticks(lx)
            ax.tick_params(bottom="off",labelbottom="off")
       
            # y-ticks --
            if yminor !=None:
                minorLocator  = MultipleLocator(yminor)
                ax.yaxis.set_minor_locator(minorLocator)
            if ymajor !=None:    
                majorLocator  = MultipleLocator(ymajor)
                ax.yaxis.set_major_locator(majorLocator)

            if iregion == 0:
                labelleft="on"
            else:
                labelleft="off"
            ax.tick_params(labelleft=labelleft, labelsize=11)
       
            # region name --
            if itag ==4:
                sregion = "%d %s"%(num,region)
                plt.title(sregion)

            # grid
            #ax.xaxis.grid(linestyle="--")
            #ax.yaxis.grid(linestyle="--",which="both")
        
            # y limit --
            if lylim !=None:
                ax.set_ylim(lylim)
        
            # h-line ---
            plt.axhline(hline, color="k",linestyle="--")
    
    # title ----      
    plt.suptitle(stitle, fontsize=10)

    plt.savefig(figPath)
    print figPath
    plt.close()




 
def draw_boxplot_Comb_Single(dldat0, dldat1, dldat2, drawFlag, dsig1, dsig2, ltag, stitle=None, figPath="./temp.png", lylim=None, yminor=None, ymajor=None, hline=None,dlGlbMean=None):
    #fig  = plt.figure(figsize =(10, 6))
    #fig  = plt.figure(figsize =(10, 3.5))
    fig  = plt.figure(figsize =(1.4, 4.8))
    hax  = 0.78/5.
    wbox = 0.3
    #------------------
    for itag,tag in enumerate(ltag[::-1]):
        ax = fig.add_axes([0.3, 0.05+hax*itag, 0.6, hax])

        if drawFlag[tag] == True:
            # set meanprops ---------
            medianprops = dict(linestyle="-", linewidth=0)
            lmeanprops  = []
            lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
            if dsig1[tag]==True:
                lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="cyan"))
            else:
                lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
    
            if dsig2[tag]==True:
                lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="red"))
            else:
                lmeanprops.append(dict(linestyle="-", linewidth=2.6, color="k"))
            #------------------------
        
            lx = [0, 0.7, 1.2]
            for idat,dat in enumerate([dldat0[tag],dldat1[tag], dldat2[tag]]):
                x = lx[idat]
                meanprops = lmeanprops[idat]
                ax.boxplot(dat, positions=[x], widths=wbox, whis=[5,95], sym="", medianprops=medianprops, showmeans=True, meanline=True, meanprops=meanprops)

            # draw GLB line
            if dlGlbMean !=None:
                ax.plot(lx,dlGlbMean[tag],"-",color="gray")

        
        # x-axis
        ax.set_xlim((-0.3,1.5))
        
        # y-ticks --
        if yminor !=None:
            minorLocator  = MultipleLocator(yminor)
            ax.yaxis.set_minor_locator(minorLocator)
        if ymajor !=None:    
            majorLocator  = MultipleLocator(ymajor)
            ax.yaxis.set_major_locator(majorLocator)

        ax.tick_params(labelleft="on", labelsize=13)
       
        # x-ticks --
        ax.tick_params(bottom="off",labelbottom="off")

        # title ----
        if itag == 4:
            plt.title(stitle,fontsize=14)

        # y limit --
        if lylim !=None:
            ax.set_ylim(lylim)
        
        # h-line ---
        plt.axhline(hline, color="k",linestyle="--")
    
    # title ----      
    #plt.suptitle(stitle, fontsize=10)

    plt.savefig(figPath)
    print figPath
    plt.close()

    


