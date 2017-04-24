# plot power map for specified dump file:

# for loading dumps:
from sys import argv
from pirs.tools import load

# for plotting without x tunneling
from matplotlib import use
# use('Cairo.pdf')
use('cairo')

from numpy import array
import matplotlib.cm 
import matplotlib.colors
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

def plot_circles(xyr, values, filename=None, cmapname='autumn', axes=None, cblabel='', linewidth=0.01, tile=None):
    if axes is None:
        fig = plt.figure()# figsize=(8,16))
        ax = fig.add_subplot(111)
    else:
        ax = axes
        fig = ax.get_figure()

    patches = []
    if tile is None:
        for x,y,r in xyr:
            circle = Circle((x,y), r)
            patches.append(circle)
    else:
        X, Y = tile
        X2 = X*0.5
        Y2 = Y*0.5
        for x,y,r in xyr:
            rect = Rectangle((x-X2, y-Y2), X, Y)
            patches.append(rect)

    p = PatchCollection(patches, cmap=matplotlib.cm.get_cmap(cmapname), linewidth=linewidth)
    p.set_array(array(values))

    ax.add_collection(p)
    ax.set_aspect('equal', 'box')
    ax.relim()
    ax.autoscale_view(True, True, True)
    cb = fig.colorbar(p, fraction=0.15, aspect=40)
    cb.set_label(cblabel)
    
    if filename is not None:
        fig.savefig(filename)
        print '***figure {} generated'.format(filename)
    return ax

def plot_rectangles(cxyXY, cvalues1,  # channel data
                    txyr, tvalues2,   # tube data
                    filename=None, cmapname='winter', cblabel='', linewidth=0.01):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    patches = []
    for x,y,X,Y in cxyXY:
        x = x - X/2.
        y = y - Y/2.
        rect = Rectangle((x,y), X, Y)
        patches.append(rect)
    for x, y, r in txyr:
        circle = Circle((x,y), r)
        patches.append(circle)

    cmap = matplotlib.cm.get_cmap(cmapname)
    cmap.set_over('w')
    cmap.set_under('k')
    p = PatchCollection(patches, cmap=cmap, linewidth=linewidth)
    p.set_array(array(cvalues1 + tvalues2))
    p.set_clim([min(cvalues1), max(cvalues1)])

    ax.add_collection(p)
    ax.set_aspect('equal', 'box')
    ax.relim()
    ax.autoscale_view(True, True, True)
    cb = fig.colorbar(p, fraction=0.15, aspect=40)
    cb.set_label(cblabel)
    
    if filename is not None:
        fig.savefig(filename)
        print '***figure {} generated'.format(filename)
    return ax
        
if len(argv) < 2:
    print """
    Script generates power and temperature color maps at specified 
    assembly height.

    > python plot_maps.py   z  dump

    where z is the axial level at which results from dump will be plotted
    on a map.
    """

# read model from dump:
dfile = argv[-1]
try:
    zlevel = float(argv[-2])
    zstr = argv[-2].replace('.', '_')
except ValueError:
    zlevel = 0.
    zstr = '0'
print 'Color map will be plotted for height {}'.format(zlevel)

if '.dump' in dfile:
    print 'reading {}... '.format(dfile),
    d = load(dfile)
    sres = d['scf_result'] # model with last SCF results and relaxed power density
    Keff = d['Keff'][-1]
    Kerr = d['Kerr'][-1]
    Ic = d['Ic']
    print 'ok.'
else:
    # produce simple SCF result:
    dfile = 'plot_simple'
    from a_scf import si as SI
    sres = SI.run('R')


# read data from the model:
fxyr = [] # fuel positions and radii
ftemp = [] # fuel temperature
fheat = [] # fuel heat

cxyXY = [] # channel positions and dimensions
ctemp = [] # channel temperature
cdens = [] # channel density

txyr = [] # tube positins and radii
ttemp = []
tdens = []


def is_sc(e):
    # return e.local_key is not None and 'scf_c' in e.local_key
    return e.name == -1

def is_fuel(e):
    # return e.local_key == 'fuel'
    return e.name == 'fuel'

hv, hk = sres.max('heat')
print 'max heat: ', hv, hk
fv, fk = sres.max('temp', is_fuel)
print 'max temp in fuel: ', fv, fk
cv, ck = sres.max('temp', is_sc)
print 'max temp in sc: ', cv, ck

try:
    fhmax = [hk[0], hv]
    ftmax = [fk[0], fv]
    ctmax = [ck[0], cv]

    print 'Tfuel max:        ', ftmax
    print 'Power dens max:   ', fhmax
    print 'Coolant temp max: ', ctmax
except:
    print 'there were problems to define max parameters'
        

for e in sres.children:
    # if not e.heat.is_constant():
    if 'uox' in e.local_key or 'ifba' in e.local_key or 'mox' in e.local_key:
        # e is a pin or ifba-pin. 
        # Read fuel temperature and power density from fuel element
        for f in e.values():
            if f.local_key == 'fuel':
                break
        x,y,z = f.abspos().car # coordinates
        t = f.temp.get_value_by_coord((x,y,zlevel), 'abs') # temperature
        h = f.heat.get_value_by_coord((x,y,zlevel), 'abs') # power density
        try:
            # heat can be of uncertainties class
            h = h.nominal_value
        except:
            pass
        r = f.R # radius
        fxyr.append((x, y, r))
        ftemp.append(t)
        fheat.append(h)
    elif 'tube' in e.local_key or 'chan' in e.local_key or 'waba' in e.local_key:
        # e is a tube
        x,y,z = e.abspos().car
        r = e.R
        txyr.append((x, y, r))
        # get water temperature and density:
        w = list(e.values())[-1]
        t = w.temp.get_value_by_coord((x,y,zlevel), 'abs') # temperature
        d = w.dens.get_value_by_coord((x,y,zlevel), 'abs') # density
        ttemp.append(t)
        tdens.append(d)
    elif 'scf_c' in e.local_key:
        # e is a channel. Read temperature and density
        x,y,z = e.abspos().car # coordinates
        t = e.temp.get_value_by_coord((x,y,zlevel), 'abs') # temperature
        d = e.dens.get_value_by_coord((x,y,zlevel), 'abs') # density
        X = e.X # channel dimensions
        Y = e.Y
        cxyXY.append((x,y, X,Y))
        ctemp.append(t)
        cdens.append(d)

# 
x1, x2 = sres.extension('x')
y1, y2 = sres.extension('y')
dx = (x2-x1)*0.05
dy = (y2-y1)*0.05
x2 +=  dx
x1 += -dx
y2 +=  dy
y1 += -dy

prefix = dfile[:-5]

if False:
    # fuel and coolant distributions on the same plot:
    tplot = plot_rectangles(cxyXY, ctemp, txyr, ttemp, cmapname='winter', cblabel='Coolant temperature')
    dplot = plot_rectangles(cxyXY, cdens, txyr, tdens, cmapname='Blues', cblabel='Coolant density')

    tplot = plot_circles(fxyr, ftemp, axes=tplot, cblabel='Fuel temperature')
    dplot = plot_circles(fxyr, fheat, axes=dplot, cblabel='Rel. power density')

    plots = [tplot, dplot]
    fnams = ['temp', 'den']


else:
    # fuel and coolant distributions on separate plots:
    tile = (sres.grid.x, sres.grid.y)
    ftplot = plot_circles(fxyr, ftemp + [810, 1250], cblabel='Fuel temperature, K', tile=tile)
    ftplot.set_xlim([x1, x2])
    ftplot.set_ylim([y1, y2])
    
    # find min and max temperatures:
    Tmin = min(ftemp)
    Tmax = max(ftemp)
    xmin, ymin = fxyr[ftemp.index(Tmin)][:2]
    xmax, ymax = fxyr[ftemp.index(Tmax)][:2]
    ftplot.set_title('z {:4.2f}, {:5.1f} at ({:4.1f}, {:4.1f}), {:5.1f} at ({:4.1f}, {:4.1f})'.format(zlevel, Tmin, xmin, ymin, Tmax, xmax, ymax))
    filename = prefix + '_ftemp' + '_{}.pdf'.format(zstr)
    ftplot.get_figure().savefig(filename)
    print '***figure {} generated'.format(filename)

    exit()
    fdplot = plot_circles(fxyr, fheat, cblabel='Rel. power density',  tile=tile)

    if ctemp and ttemp:
        ctplot = plot_rectangles(cxyXY, ctemp, txyr, ttemp, cmapname='winter', cblabel='Coolant temperature')
    else:
        ctplot = None
    if cdens and tdens:
        cdplot = plot_rectangles(cxyXY, cdens, txyr, tdens, cmapname='Blues', cblabel='Coolant density')
    else:
        cdplot = None

    plots = [ftplot, fdplot, ctplot, cdplot]
    fnams = ['ftemp', 'fpow', 'ctemp', 'cden']

for (p, s) in zip(plots, fnams):

    if p:
        p.set_xlim([x1, x2])
        p.set_ylim([y1, y2])

        p.set_title('z={0}, iteration {1}'.format(zlevel, Ic))

        filename = prefix + '_' + s + '_{}.pdf'.format(zstr)
        p.get_figure().savefig(filename)
        print '***figure {} generated'.format(filename)

