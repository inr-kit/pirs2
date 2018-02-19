"""
Plot geometry as a colormap.
"""

import matplotlib
import matplotlib.pyplot as pyplot
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from numpy import array

from .intersections import ssect, toshapely, extensions
from ...mcnp.auxiliary.counters import SimpleCollection
from .plot_shapely import ShapelyToArtist
from .color_list import cgen

_prevcolors = {} # here previously defined autocolors are stored.

def colormap(model, plane={'z':0}, axis=None, var=None, filter_=None, 
             aspect='equal', colors=None, nmarker={}, mmarker={}, legend=True, filename=None, **kwargs):
    """
    Returns an instance of the matplotlib Axes class containing colormap that
    shows distribution of the system variable var on the cross-section plane
    defined by the argument ``plane``.

    :param model: Model to be plotted. Instance of Box, Cylinder or Sphere class.

    :param dict plane: Dictionary describing the cut plane.

    :param axis: Instance of the :class:`matplotlib.axes.Axes` class where geometry plot will be added. If not specified,
               a new instance will be created.

    :param str var: Variable name, one of 'material', 'temp', 'heat' or 'dens' which will be used to color the geometry.

    :param func filter_: boolean function taking a solid as argument. A solid will be plotted only if this function returns True for it.
                         By default, all solids are plotted.

    :param str aspect: string 'equal' or 'auto'.

    :param dict colors: dictionary for colors used for material names.

    :param dict nmarker: dictionary specifying solids names to be marked on the plot. 'name':'*' or 'name':dict, where '*' or dict defines
                         the marker shape, as in the :func:`maptlotlib.pyplot.plot` function.

    :param dict mmarker: as nmarker, but to mark solids with particular material names.

    :param bool legend: Show the legend on the plot.

    :param str filename: File name where the plot will be stored. This attribute is passed to the :meth:`matplotlib.pyplot.Figure.savefig` method.

    :param **kwargs: keyword arguments describing contour lines. 


    """
    if filter_ is None:
        # use trivial filter
        filter_ = lambda x: True 

    # if several plane coordinates are given, call colormap to every one:
    try:
        vl = plane.values()[0][:]
    except TypeError:
        pass
    else:
        f, axs = pyplot.subplots(ncols=1, nrows=len(vl))
        f.set_size_inches(8, 6*len(vl))
        for v, a in zip(vl, axs):
            colormap(model, plane={plane.keys()[0]:v}, axis=a, var=var, filter_=filter_, aspect=aspect, colors=colors)
        return axs[0]

    if axis is None:
        # create new axes instance
        axis = pyplot.figure().add_subplot(111) 
        axis.set_aspect(aspect, 'box')

    if var is None:
        var = 'material'

    def _colors():
        # lst0 =  ['red', 'green', 'blue', 'cyan', 'yellow', 'grey']
        # standard web color names, except black and grey used for edges, and white.
        lst0 = ['aqua', 'blue', 'fuchsia', 'navy', 'olive', 'purple', 'red', 'green', 'lime', 'maroon', 'silver', 'teal', 'yellow']
        lst = lst0[:]
        while lst:
            yield lst.pop(0)
            if not lst:
                lst = lst0[:] 
    clr = _colors()
    clr = cgen()

    xmin, xmax, ymin, ymax = None, None, None, None

    # ensure that parent of the model, if any, will cut the model:
    model.root.__zo = 0
    for p in reversed(list(model.parents())):
        sh = ssect(p, plane)
        if sh:
            spl = toshapely(sh)
            if p.parent:
                spl = spl.intersection(p.parent.__shapely)
                p.__zo = p.parent.__zo + 1
            p.__shapely = spl

    if var in ['material', 'name']:
        if colors is None:
            colors = {}
            colors.update(_prevcolors)
            for v in model.values(True):
                    vv = getattr(v, var)
                    c = colors.get(vv)
                    if c is None:
                        c = clr.next()
                    colors[vv] = c
        _prevcolors.update(colors)

        # marker coordinates for name and material markers
        nmc = {}
        for k in nmarker.keys():
            nmc[k] = [[], []]
        mmc = {}
        for k in mmarker.keys():
            mmc[k] = [[], []]
        zomax = 0
        used_colors = {}
        for v in model.values(True):
            sh = ssect(v, plane)
            if sh and filter_(v):
                spl = toshapely(sh)
                if v.parent:
                    spl = spl.intersection(v.parent.__shapely)
                    v.__zo = v.parent.__zo + 1
                    zomax = max(zomax, v.__zo)
                v.__shapely = spl
                if v is model:
                    xmin, ymin, xmax, ymax = extensions(sh)
                for a in ShapelyToArtist(v.__shapely, axis=axis):
                    value = getattr(v, var)
                    color = colors[value]
                    a.set_facecolor(color)
                    used_colors[value] = color
                    a.set_edgecolor('black')
                    a.set_linewidth(kwargs.get('linewidth', 0.1))
                    a.set_zorder(v.__zo)

                # marker coordinates:
                if v.name in nmc.keys():
                    xmn, ymn, xmx, ymx = extensions(sh)
                    nmc[v.name][0].append((xmn+xmx)*0.5)
                    nmc[v.name][1].append((ymn+ymx)*0.5)
                if v.material in mmc.keys():
                    xmn, ymn, xmx, ymx = extensions(sh)
                    mmc[v.name][0].append((xmn+xmx)*0.5)
                    mmc[v.name][1].append((ymn+ymx)*0.5)

        # add markers to the plot
        for n, (xl, yl) in nmc.items():
            if xl:
                args = []
                kwa = {'zorder':zomax+1}
                if isinstance(nmarker[n], str):
                    args.append(nmarker[n])
                else:
                    # assume it is a dictionary with kwa.
                    kwa.update(nmarker[n])
                axis.plot(xl, yl, *args, **kwa)
        for m, (xl, yl) in mmc.items():
            if xl:
                args = []
                kwa = {'zorder':zomax+1}
                if isinstance(mmarker[n], str):
                    args.append(mmarker[n])
                else:
                    # assume it is a dictionary with kwa.
                    kwa.update(mmarker[n])
                axis.plot(xl, yl, *args, **kwa)

        if legend:
            # a legend specifying color and corresponding materials/names.
            artists = []
            labels = []
            for s, c in used_colors.items():
                p = Rectangle((0,0), 1, 1, facecolor=c, edgecolor='none')
                artists.append(p)
                labels.append(s)
            if artists:
                axis.get_figure().legend(artists, labels, 'right', title=var)

                    


    addbar = False
    if var in ['temp', 'heat', 'dens']:
        # generate patches for each zmesh element
        plst = [] # list of added collections
        vmin = None
        for v in model.values(True):
            sh, zl, vl = ssect(v, plane, var)
            if sh and filter_(v):
                spl = toshapely(sh)
                if v.parent:
                    spl = spl.intersection(v.parent.__shapely)
                    v.__zo = v.parent.__zo + 1
                v.__shapely = spl
                if v is model:
                    xmin, ymin, xmax, ymax = extensions(sh)
                bpatch, pcol = ShapelyToArtist(v.__shapely, axis=axis, zl=zl, vl=vl)
                bpatch.set_facecolor('none')
                bpatch.set_edgecolor('black')
                bpatch.set_linewidth(0.1)
                bpatch.set_zorder(v.__zo)
                pcol.set_clip_path(bpatch)
                pcol.set_cmap(matplotlib.cm.gist_heat)
                pcol.set_linewidth(0)
                plst.append(pcol)
                v = min(vl)
                V = max(vl)
                if not vmin:
                    vmin = v
                    vmax = V
                else:
                    vmin = min(vmin, v)
                    vmax = max(vmax, V)
                
        if vmin == vmax:
            vmin, vmax = vmin * 0.9, vmin * 1.1
        for pc in plst:
            pc.set_clim([vmin, vmax])
        addbar = True

    if addbar and plst and legend:
        axis.get_figure().colorbar(plst[0])

    # set limits
    dx = (xmax - xmin) * 0.05
    dy = (ymax - ymin) * 0.05
    axis.set_xlim(xmin-dx, xmax+dx)
    axis.set_ylim(ymin-dy, ymax+dy)

    axis.set_title('Plane {}, {}'.format(plane, var))
    if filename:
        axis.get_figure().savefig(filename)

    return axis


