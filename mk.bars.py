from numpy import *
import ret_PN
import matplotlib.pyplot as plt
import HAPPI_detect_func as hd_func

model      = "MIROC5"
res        = "128x256"

#regiontype = "JPN"
#lregion    = ["GLB","JPN","S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]

regiontype = "IPCC"
lregion     = ["ALA","AMZ","CAM","CAS","CEU","CGI","CNA","EAF","EAS","ENA","MED","NAS","NAU","NEB","NEU","SAF","SAH","SAS","SAU","SSA","SEA","TIB","WAF","WAS","WSA","WNA"]



#lregion    = ["HOKKAIDO"]
#lens       = [1,11,21,31,41]
lens       = range(1,50+1)
#lthpr      = [0,"p99.900","p99.990"]
#lthpr      = ["p99.900","p99.990"]
lthpr      = [0]
#lvartype   = ["Ptot"]
lvartype   = ["Freq","Ptot"]
lscen      = ["JRA","ALL","P15","P20"]
ltag       = ["plain","tc","cf","ms","ot"]

wbar       = 0.8
yfontsize  = 17

dieYear = {"JRA":[2006,2014]
          ,"ALL": [2006,2015]
          ,"P15": [2106,2115]
          ,"P20": [2106,2115]
          }


season     = "ALL"
#**********************************
def ret_xlabel(scen):
    if scen=="JRA":
        return "JRA"
    elif scen=="ALL":
        return "NOW"
    elif scen=="P15":
        return "+1.5"
    elif scen=="P20":
        return "+2.0"




for thpr in lthpr:
    lkey  = [[scen,tag] for scen in lscen for tag in ltag+["plain"]]
    
    Prcp = {}
    Freq = {}
    Pint = {}
    for [scen,tag] in lkey:
        da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens)
        #print scen,tag,da1prcp
 
        for region in lregion:
            Prcp[region,tag,scen] = da1prcp[region]
            Freq[region,tag,scen] = da1freq[region]*4*365
            Pint[region,tag,scen] = da1pint[region]

    
    #---------------------------------    
    for vartype in lvartype:
        if   vartype == "Ptot":
            Var = Prcp
        elif vartype == "Freq":
            Var = Freq
        elif vartype == "Pint":
            Var = Pint
            
        for region in lregion:
            #-- Figure --------
            figplot = plt.figure(figsize=(4,4))
            axplot  = figplot.add_axes([0.2,0.2,0.7,0.6])
        
        
            for iscen,scen in enumerate(lscen):
                offset = wbar*6
                xpl = wbar*1.2*iscen
                xtc = wbar*1.2*iscen + offset
                xcf = wbar*1.2*iscen + offset*2
                xms = wbar*1.2*iscen + offset*3
                xot = wbar*1.2*iscen + offset*4
                
                vpl = mean(Var[region,"plain",scen])
                vtc = mean(Var[region,"tc",scen])
                vcf = mean(Var[region,"cf",scen])
                vms = mean(Var[region,"ms",scen])
                vot = mean(Var[region,"ot",scen])
            
                epl = Var[region,"plain",scen].std()
                etc = Var[region,"tc",scen].std()
                ecf = Var[region,"cf",scen].std()
                ems = Var[region,"ms",scen].std()
                eot = Var[region,"ot",scen].std()

           
                axplot.bar(xpl, vpl, width=wbar, color="gray") 
                axplot.bar(xtc, vtc, width=wbar, color="r") 
                axplot.bar(xcf, vcf, width=wbar, color="deepskyblue") 
                axplot.bar(xms, vms, width=wbar, color="pink") 
                axplot.bar(xot, vot, width=wbar, color="gold")

                axplot.errorbar(xpl, vpl, epl, color="k", linewidth=1) 
                axplot.errorbar(xtc, vtc, etc, color="k", linewidth=1) 
                axplot.errorbar(xcf, vcf, ecf, color="k", linewidth=1) 
                axplot.errorbar(xms, vms, ems, color="k", linewidth=1) 
                axplot.errorbar(xot, vot, eot, color="k", linewidth=1) 

            #--- bottom line --------------------
            plt.axhline(0, color="black")

    
            #--- no bottom ticks, y-ticklabel ----
            axplot.tick_params(bottom="off",labelbottom="off", labelsize=yfontsize)
    
            #--- title ----------
            stitle = "%s %s %s"%(vartype, thpr, region)
            plt.title(stitle, fontsize=8)
            plt.suptitle(region, fontsize=25)
    
            iYear_fut, eYear_fut = dieYear["P20"]
            run  = "C20-P15-001"
            baseDir, sDir = hd_func.path_dpr(model=model, run=run, res=res, sthpr=thpr, tag="plain", iYear=iYear_fut, eYear=eYear_fut, season=season, var="dP")[0:2]
    
            figDir  = baseDir + "/fig"
            figname = figDir  + "/bar.%s.th.%s.%s.png"%(vartype, thpr, region)
            plt.savefig(figname)
            print figname
            plt.close()
