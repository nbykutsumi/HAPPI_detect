import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pylab as pylab
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patheffects as patheffects
from numpy import *
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import maskoceans
from matplotlib import cbook
import shapefile
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

class MidPointNorm(Normalize):    
    def __init__(self, midpoint=0, vmin=None, vmax=None, clip=False):
        Normalize.__init__(self,vmin, vmax, clip)
        self.midpoint = midpoint

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if not (vmin < midpoint < vmax):
            raise ValueError("midpoint must be between maxvalue and minvalue.")       
        elif vmin == vmax:
            result.fill(0) # Or should it be all masked? Or 0.5?
        elif vmin > vmax:
            raise ValueError("maxvalue must be bigger than minvalue")
        else:
            vmin = float(vmin)
            vmax = float(vmax)
            if clip:
                mask = ma.getmask(result)
                result = ma.array(np.clip(result.filled(vmax), vmin, vmax),
                                  mask=mask)

            # ma division is very slow; we can take a shortcut
            resdat = result.data

            #First scale to -1 to 1 range, than to from 0 to 1.
            resdat -= midpoint            
            resdat[resdat>0] /= abs(vmax - midpoint)            
            resdat[resdat<0] /= abs(vmin - midpoint)

            resdat /= 2.
            resdat += 0.5
            result = ma.array(resdat, mask=result.mask, copy=False)                

        if is_scalar:
            result = result[0]            
        return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if cbook.iterable(value):
            val = ma.asarray(value)
            val = 2 * (val-0.5)  
            val[val>0]  *= abs(vmax - midpoint)
            val[val<0] *= abs(vmin - midpoint)
            val += midpoint
            return val
        else:
            val = 2 * (val - 0.5)
            if val < 0: 
                return  val*abs(vmin-midpoint) + midpoint
            else:
                return  val*abs(vmax-midpoint) + midpoint


def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap



def rotate_a2dat(Dat):
    Dat_new1 = Dat[:,:128]
    Dat_new2 = Dat[:,128:]
    return np.concatenate((Dat_new2, Dat_new1), axis=1)


def rotate_a2dat_between180(Dat):
    Dat_new1 = Dat[:,:128]
    Dat_new2 = Dat[:,128:]-360.
    return np.concatenate((Dat_new2, Dat_new1), axis=1)

#***************************************************************

"""
[['Alaska/N.W. Canada [ALA:1]', 'ALA', 'land'],
 ['Amazon [AMZ:7]', 'AMZ', 'land'],
 ['Central America/Mexico [CAM:6]', 'CAM', 'land'],
 ['small islands regions Caribbean', 'CAR*', 'all'],
 ['Central Asia [CAS:20]', 'CAS', 'land'],
 ['Central Europe [CEU:12]', 'CEU', 'land'],
 ['Canada/Greenland/Iceland [CGI:2]', 'CGI', 'land'],
 ['Central North America [CNA:4]', 'CNA', 'land'],
 ['East Africa [EAF:16]', 'EAF', 'land'],
 ['East Asia [EAS:22]', 'EAS', 'land'],
 ['East North America [ENA:5]', 'ENA', 'land'],
 ['South Europe/Mediterranean [MED:13]', 'MED', 'land'],
 ['North Asia [NAS:18]', 'NAS', 'land'],
 ['North Australia [NAU:25]', 'NAU', 'land'],
 ['North-East Brazil [NEB:8]', 'NEB', 'land'],
 ['North Europe [NEU:11]', 'NEU', 'land'],
 ['Southern Africa [SAF:17]', 'SAF', 'land'],
 ['Sahara [SAH:14]', 'SAH', 'land'],
 ['South Asia [SAS:23]', 'SAS', 'land; sea'],
 ['South Australia/New Zealand [SAU:26]', 'SAU', 'land'],
 ['Southeast Asia [SEA:24]', 'SEA', 'land; sea'],
 ['Southeastern South America [SSA:10]', 'SSA', 'land'],
 ['Tibetan Plateau [TIB:21]', 'TIB', 'land'],
 ['West Africa [WAF:15]', 'WAF', 'land'],
 ['West Asia [WAS:19]', 'WAS', 'land'],
 ['West North America [WNA:3]', 'WNA', 'land'],
 ['West Coast South America [WSA:9]', 'WSA', 'land'],
 ['Antarctica', 'ANT*', 'land; sea'],
 ['Arctic', 'ARC*', 'land; sea'],
 ['Pacific Islands region[2]', 'NTP*', 'all'],
 ['Southern Topical Pacific', 'STP*', 'all'],
 ['Pacific Islands region[3]', 'ETP*', 'all'],
 ['West Indian Ocean', 'WIO*', 'all']]
"""


# Load HAPPI module
import myfunc.IO.HAPPI as HAPPI

prj     = "HAPPI"
model   = "MIROC5"
expr    = "C20"

hp    = HAPPI.Happi()
hp(model=model, expr=expr, scen="P15", ens=1)
Lat   = hp.Lat
Lon   = hp.Lon

bnd = range(0,200,1)
dotstep = 3
miss  = -9999.
midpoint = None


# Load Sample data
figDir  = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/ptile"
figPath = figDir + "/HAPPI.MIROC5.C20.ALL.0500Y.p99.900.128x256"
a2dat   = fromfile(figPath, float32).reshape(128,256)*60*60*24

a2hatch = ma.masked_less(a2dat, 50).filled(miss)


figPath = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.2106-2115.ALL/MIROC5/fig/temp.map.png"
cbarPath = "/home/utsumi/mnt/wellshare/HAPPI/anlWS/dif.tagpr.2106-2115.ALL/MIROC5/fig/cbar.temp.png"

shapePath= '/home/utsumi/mnt/wellshare/data/MapMask/IPCC2012_shapefile/referenceRegions.shp'

def draw_map_robin(a2dat, a2hatch, Lat, Lon, miss=-9999, bnd=None, cmap="RdBu_r", vmin=None, vmax=None, figPath=None, cbarPath=None, cbarOrientation="horizontal",lregion=None,stitle=None,seaMask=False):



    # Shift Lon
    a2dat_new   = rotate_a2dat(a2dat)

    
    X,Y     = meshgrid(Lon, Lat)
    X_new   = rotate_a2dat(X)
    Y_new   = Y

    X_new180= rotate_a2dat_between180(X)   
    Y_new180= Y
    
    # Hatches
    if a2hatch !=None:
        a2hatch_new = rotate_a2dat(a2hatch)
    
    # Plot
    if bnd != None:
        norm = colors.BoundaryNorm(boundaries=bnd, ncolors=256)
    
    fig = plt.figure(figsize=(8,4))
    
    ax   = fig.add_axes([0.1,0.05,0.8,0.8], axisbg="white")
    M    = Basemap( projection="robin", lon_0=0, resolution="l", ax=ax)
    
    X_prj, Y_prj = M(X_new,Y_new)


    # Mask oceans
    if seaMask==True:
        a2dat_new = maskoceans(X_new180, Y_new180, a2dat_new)
    if (seaMask==True)&(a2hatch !=None):
        a2hatch_new= maskoceans(X_new180, Y_new180, a2hatch_new)
     
    # Fill colors
    if bnd != None:
        fill = M.pcolormesh(X_prj,Y_prj,a2dat_new,  cmap=cmap, norm=norm)
    else:
        fill = M.pcolormesh(X_prj,Y_prj,a2dat_new,  cmap=cmap, vmin=vmin, vmax=vmax)


    # Hatches
    if a2hatch !=None:
        dotsize   = 1
        dotcolor  = "0.2"
        a2dot_new = a2hatch_new
        Xdot_new = ma.masked_where(a2dot_new==miss, X_new)[::dotstep,::dotstep]
        Ydot_new = ma.masked_where(a2dot_new==miss, Y_new)[::dotstep,::dotstep]
        Xdot_prj, Ydot_prj = M(Xdot_new, Ydot_new)
        M.plot(Xdot_prj, Ydot_prj, "o", markersize=dotsize, color=dotcolor)
    
    # Coastline
    M.drawcoastlines(linewidth=0.3, color="k")

   
    # Shapefile
    if lregion == None: lregion=[]
    sf    = shapefile.Reader(shapePath)
    shapes = sf.shapes()
    records= sf.records()
    for [record, shape] in zip(records, shapes):
        code=record[1]

        if code not in lregion: continue
        regionnum = int(record[0].split(":")[-1][:-1])
        # simple plotting
        xx,yy = zip(*shape.points)
    
        xx0, yy0 = xx[:-1], yy[:-1]
        xx1, yy1 = xx[1:],  yy[1:]

        #-------------
        # draw domain    
        for ii in range(len(xx0)):
            x0 = xx0[ii]
            y0 = yy0[ii]
            x1 = xx1[ii]
            y1 = yy1[ii]

            #-----------------
            # CAUSION
            # longitude of 180 and -180 --> 179.9, -179,9
            if x0 ==  180: x0 =  179.9
            if x0 == -180: x0 = -179.9
            if x1 ==  180: x1 =  179.9
            if x1 == -180: x1 = -179.9

            x_prj0, y_prj0 = M(x0,y0)
            x_prj1, y_prj1 = M(x1,y1)

            #-----------------
            # CAUSION
            # drawgreqatcircle does not work 
            # properly for zonal line on robinson projection
            #-----------------
            if y0 != y1:
                M.drawgreatcircle(x0,y0,x1,y1,linewidth=1.3,color="0.2",alpha=0.8) 
            else:
                x_prj0, y_prj0 = M(x0,y0)
                x_prj1, y_prj1 = M(x1,y1)
                M.plot((x_prj0,x_prj1),(y_prj0,y_prj1),linewidth=1.3,color="0.2",alpha=0.8) 
        # plot region code
        x_txt, y_txt = max(xx)-15,  min(yy)+2

        if regionnum==1:
            x_txt = x_txt - 10
        elif regionnum==3:
            x_txt = x_txt - 5
        elif regionnum==6:
            x_txt = x_txt - 10
        elif regionnum==9:
            x_txt = x_txt - 15
        elif regionnum==11:
            x_txt, y_txt = min(xx)+2,  max(yy)-12
        elif regionnum==12:
            x_txt, y_txt = min(xx)+32,  max(yy)-12
        elif regionnum==18:
            x_txt, y_txt = min(xx)+9,  y_txt
        elif regionnum==23:
            x_txt, y_txt = min(xx)+3,  min(yy)+2
        elif regionnum==24:
            x_txt, y_txt = max(xx)-13,  max(yy)-8
        elif regionnum==26:
            x_txt, y_txt = min(xx)+3,  min(yy)+2






        x_txt, y_txt = M(x_txt,y_txt)
        plt.text(x_txt, y_txt, "%s"%(regionnum), color="k", fontsize=12, path_effects=[patheffects.withStroke(linewidth=3, foreground="w")])
 
    # Title
    if stitle !=None:
        plt.title(stitle)
    
    # Save
    plt.savefig(figPath)
    print figPath
    
    # Colorbar
    if type(cbarPath) != bool:
        if cbarOrientation=="horizontal":
            #figcbar  = plt.figure(figsize=(1.8,0.5))
            figcbar  = plt.figure(figsize=(2.5,0.5))
            axcbar   = figcbar.add_axes([0.1,0.5,0.8,0.48])
        elif cbarOrientation=="vertical":

            #figcbar  = plt.figure(figsize=(0.8,1.6))
            figcbar  = plt.figure(figsize=(0.8,2.0))
            axcbar   = figcbar.add_axes([0.01,0.05,0.25,0.9])

 

        cb = plt.colorbar(fill, boundaries = bnd,orientation=cbarOrientation, cax=axcbar)

        figcbar.savefig(cbarPath) 
        print cbarPath


