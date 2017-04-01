from numpy import *
from myfunc.fig import BoundaryNorm, BoundaryNormSymm
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib
from mpl_toolkits.basemap import Basemap, maskoceans
from bisect import bisect
#********************************************************
def lon2ixpy(a1lon, lon):
  i = bisect(a1lon, lon)
  if i==0:
    ix = i
  elif i == len(a1lon):
    ix = i-1
  else:
    if   ( lon < (a1lon[i-1]+a1lon[i])*0.5 ):
      ix = i-1
    else:
      ix = i
  return ix

#********************************************************
def lat2iypy(a1lat, lat):
  i = bisect(a1lat, lat)
  if i==0:
    iy = i
  elif i == len(a1lat):
    iy = i-1
  else:
    if   ( lat < (a1lat[i-1]+a1lat[i])*0.5 ):
      iy = i-1
    else:
      iy = i
  return iy


#********************************************************
def DrawMap_dotshade(a2in, a2dot, a1lat, a1lon, BBox=[[-90., 0.],[90., 360.]], bnd=False, vmin=False, vmax=False, cmap="Spectral",extend="neither", white_minmax="neither", figname="./temp.png", cbarname=False, stitle=False, parallels=arange(-90,90+0.1, 30), meridians=arange(-180,360+0.1,30) ,maskcolor=False, dotcolor="k", dotstep=1, markersize=3, miss=-9999.):

  """
  extend= "neither","both","min","max"
  white_minmax = "neither","both","min","max"
  """

  # Lat, Lon ------
  a1lat = array( a1lat )
  a1lon = array( a1lon )

  latmin = a1lat[0]  - (a1lat[1]  - a1lat[0])*0.5
  latmax = a1lat[-1] + (a1lat[-1] - a1lat[-2])*0.5
  lonmin = a1lon[0]  - (a1lon[1]  - a1lon[0])*0.5
  lonmax = a1lon[-1] + (a1lon[-1] - a1lon[-2])*0.5

  a1LAT = r_[ array([latmin]), (a1lat[1:] + a1lat[:-1])*0.5, array([latmax])]
  a1LON = r_[ array([lonmin]),   (a1lon[1:] + a1lon[:-1])*0.5, array([lonmax])]

  X,Y   = meshgrid(a1LON, a1LAT)
  Xmid, Ymid = meshgrid(a1lon, a1lat)
  # BBox --------
  [lllat,lllon],[urlat,urlon] = BBox

  # vmax, vmin --
  if type(vmax) == bool:
    vmax = a2in.max()
  if type(vmin) == bool:
    vmin = a2in.min()

  ##-- color ---------------
  if (type(bnd) != bool):
    if extend == "neither":
      bnd  = bnd
    elif extend == "both":
      bnd  = [-1.0e+40] + bnd + [1.0e+40]
    elif extend == "min":
      bnd  = [-1.0e+40] + bnd
    elif extend == "max":
      bnd  = bnd + [+1.0e+40]

    cminst   = matplotlib.cm.get_cmap(cmap, len(bnd))

    if extend == "neither":
      acm      = cminst( arange( len(bnd)) )
    elif extend == "both":
      acm      = cminst( arange( len(bnd)+2 ) )
    elif extend in ["min","max"]:
      acm      = cminst( arange( len(bnd)+1 ) )

    if   white_minmax=="min":
      lcm      = [[1,1,1,1]]+ acm.tolist()[1:]
    elif white_minmax=="max":
      lcm      = acm.tolist()[:-1] + [[1,1,1,1]]
    elif white_minmax=="both":
      lcm      = [[1,1,1,1]] + acm.tolist()[1:-1] + [[1,1,1,1]]
    else:
      lcm      = acm.tolist()

    cmap     = matplotlib.colors.ListedColormap( lcm )


  # BoundaryNorm
  #norm   = colors.BoundaryNorm(boundaries=bnd, ncolors=256)
  norm   = colors.BoundaryNorm(boundaries=bnd, ncolors=len(bnd)+1)


  ## landsea mask
  #Lon, Lat = meshgrid(a1lon, a1lat)
  #a2in   = maskoceans(Lon, Lat, a2in)


  # Draw Map ----
  fig  = plt.figure(figsize=(6,3))
  # color for masked grids --
  if type(maskcolor) == bool:
    maskcolor = "w"
  else:
    maskcolor = maskcolor

  ax   = fig.add_axes([0.1,0.1,0.85,0.8], axisbg=maskcolor)
  
  M    = Basemap( resolution="l", llcrnrlat = lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=ax)
  im   = M.pcolormesh(X,Y,a2in, vmin=vmin, vmax=vmax, cmap=cmap, norm=norm)

  # Dot
  Xdot = ma.masked_where(a2dot==miss, Xmid)[::dotstep,::dotstep]
  Ydot = ma.masked_where(a2dot==miss, Ymid)[::dotstep,::dotstep]
  #im   = M.plot(Xdot, Ydot, "o", markersize=3, color=dotcolor="k")
  M.plot(Xdot, Ydot, "o", markersize=3, color=dotcolor)

  # coastline ---
  M.drawcoastlines()

  # meridians and parrallels -
  if type(parallels) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  if type(meridians) != bool:
    M.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=1)
  M.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=1)

  # title -------
  if type(stitle) != bool:
    ax.set_title("%s"%(stitle))

  # Save -------------
  plt.savefig(figname)
  print figname


  # colorbar ----
  if type(cbarname) != bool:
    figcbar    = plt.figure(figsize=(5, 0.6))
    axcbar     = figcbar.add_axes([0,0.4,1.0,0.58])
    boundaries = bnd
    plt.colorbar(im, boundaries=boundaries, extend=extend, cax=axcbar, orientation="horizontal")
    figcbar.savefig(cbarname)
    print cbarname
#********************************************************

