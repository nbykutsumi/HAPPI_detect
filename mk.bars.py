from numpy import *
import ret_PN
import matplotlib.pyplot as plt

regiontype = "JPN"
#lregion    = ["S.ISLES","KYUSHU","SHIKOKU","CHUGOKU","KINKI","SE.JPN","NW.JPN","NE.JPN","HOKKAIDO"]
lregion    = ["KYUSHU"]
lens       = [1,1]
thpr       = "p99.900"
lvartype   = ["Freq"]
lscen      = ["JRA","ALL","P15","P20"]
ltag       = ["plain","tc","cf","ms","ot"]

wbar       = 0.6
yfontsize  = 17

#**********************************
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



lkey  = [[scen,tag] for scen in lscen for tag in ltag]

Prcp = {}
Freq = {}
Pint = {}
for [scen,tag] in lkey:
    da1prcp, da1freq, da1pint = ret_PN.main( thpr=thpr, scen=scen, tag=tag, regiontype=regiontype, lregion=lregion, lens=lens)
    print scen,tag,da1prcp

    for region in lregion:
        Prcp[region,tag,scen] = da1prcp[region]
        Freq[region,tag,scen] = da1freq[region]
        Pint[region,tag,scen] = da1pint[region]


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
            x   = iscen + wbar*0.5
            vtc = mean(Var[region,"tc",scen])
            vcf = mean(Var[region,"cf",scen])
            vms = mean(Var[region,"ms",scen])
            vot = mean(Var[region,"ot",scen])
        
            ltmp= [vtc, vcf, vms, vot]
            btc = ret_bottom(ltmp, 0)
            bcf = ret_bottom(ltmp, 1)
            bms = ret_bottom(ltmp, 2)
            bot = ret_bottom(ltmp, 3)
        
            axplot.bar(x, vtc, width=wbar, color="r") 
            axplot.bar(x, vcf, width=wbar, bottom=bcf, color="deepskyblue") 
            axplot.bar(x, vms, width=wbar, bottom=bms, color="pink") 
            axplot.bar(x, vot, width=wbar, bottom=bot, color="gold") 

            #--- no bottom ticks, y-ticklabel ----
            axplot.tick_params(bottom="off",labelbottom="off", labelsize=yfontsize)

            #--- title ----------
            stitle = "%s %s %s"%(vartype, thpr, region)
            plt.title(stitle, fontsize=8)

        
        plt.show()

