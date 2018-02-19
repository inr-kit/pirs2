"""
Functions to visualize shapely objects.
"""

import matplotlib.pyplot as mpl
from matplotlib.patches import Polygon, Circle
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from numpy import asarray, array

from shapely.geometry import Point as ShapelyPoint # only to workaround the bug in shapely
from shapely.geometry import Polygon as ShPolygon

def ShapelyToArtist(shapely, axis=None, zl=None, vl=None):
    """
    Returns an artist representing the shapely object.

    Optional axis -- axis instance to which the artist will be added.

    For some shapely objects (Point, line), artist is created by a method 
    of an axis. For this method to call, one needs an instance of axis.

    If zl and vl lists are given, returned object is a patchcollection of
    matplotlib Rectangles cutted by the shapely. This works only if shapely is 
    of the Polygon geometry type. The PatchCollection object is the last entry in 
    the returned list.
    """

    if shapely.geom_type == 'Point':
        if axis is None:
            f, axis = mpl.subplots(nrows=1, ncols=1)
        artist, = axis.plot([shapely.x], [shapely.y])
        artists = [artist]

    elif shapely.geom_type in ['LineString', 'LinearRing']:
        artist = Line2D(shapely.xy[0], shapely.xy[1])
        if axis is not None:
            axis.add_artist(artist)
        artists = [artist]

    elif shapely.geom_type == 'Polygon':
        a = asarray(shapely.exterior)
        artist = Polygon(a, closed=True)
        artists = [artist]

        if zl:
            # bounding box of the shapely:
            minx, miny, maxx, maxy = shapely.bounds
            # lower and upper coordinates
            lmin = zl[:-1]
            lmax = zl[1:]
            patches = []
            for (zmin, zmax) in zip(lmin, lmax):
                s = ShPolygon([(minx, zmin), (maxx, zmin), (maxx, zmax), (minx, zmax)]).intersection(shapely)
                p = ShapelyToArtist(s, axis=None)[0]
                patches.append(p)
            pcol = PatchCollection(patches)
            pcol.set_array(array(vl))
            artists.append(pcol)
        elif vl:
            # zl is empty. In this case vl has only one entry.
            minx, miny, maxx, maxy = shapely.bounds
            patches = []
            p = ShapelyToArtist(shapely, axis=None)[0]
            patches.append(p)
            pcol = PatchCollection(patches)
            pcol.set_array(array(vl))
            artists.append(pcol)

        if axis is not None:
            for artist in artists:
                axis.add_artist(artist)

    elif shapely.geom_type == 'GeometryCollection' or 'Multi' in shapely.geom_type:
        artists = []
        for sh in shapely.geoms:
            artists.append( ShapelyToArtist(sh, axis=axis))

    else:
        raise NotImplementedError('ShapelyToArtist function not implemented for shapely.geom_type {}'.format(shapely.geom_type))

    return artists

def ShapelyToAxis(shapely, **kwargs):
    """
    Returns a matplotlib.axes.Axes  instance with shapely drawn on it. 

    Some of the keyword arguments:

    *order*: string containing characters i, b, v. Meaning depends on the
    geometry type of shapely object.

        For a Point, order has no sence.

        For a Line (LineString or LinearRing), i means to plot the line, v --
        to plot vertices. b has no sence.

        For a polygon, i -- plot interior, b -- plot boundary, v -- plot
        boundary's vertices.

    *indices*: string containing characters i, b, v. Meaning depends on the
    geometry type of the shapely object.

        For a point, does not matter.

        For a Line: i -- print indices of line segments, v -- print indices of
        the vertices, b -- has no sence.

        For a polygon: i -- has no sence, b -- print indices of the boundary
        segments, v -- print indices of the boundary vertices.

    *autoscale*: boolean.

    *color*: a matplotlib color specification.

    *axis*: None (by default) or an existing instance of the Matplotlib axes.
    If None, the shapely will be plotted on a new axes. Otherwise, it will be
    plotted on the given axis.

    *pointsize*: point radius in pixels.

    *linewidth*: linewidth in pixels.

    *alpha*: transparency. 0 -- transpoarent, 1 --opaque.

    *label*: a label that appears at the shapely's centroid.

    *fontsize*: size used to print label and indices.
    """

    # common default arguments:
    args = {'axis': None,
            'autoscale': True,
            'color': 'red',
            'pointsize': 10,
            'marker':'o',      # marker to represent point
            'linewidth': 0.05,
            'alpha': 0.2,
            'label': '',  # a label that will be printed on top of the shapely object
            'indices': 'ibV', # a string containing 'v' or/and 'b' (not implemented). For 'v', each vertex will be labeled with its index, etc.
            'ifontsize': 2,
            'lfontsize': 5,
            'order': 'ibv'}
    args.update(kwargs)

    axs = args['axis']
    if axs is None:
        axs = mpl.figure().add_subplot(1,1,1)
        axs.set_aspect('equal')
        axs.autoscale(True) # does not work for patch collections.
    assert isinstance(axs, Axes)

    if shapely.is_empty:
        return axs

    label = '{}'.format(args['label'])
    indices = args['indices'].lower()
    order = args['order'].lower()
    sh = shapely
    gt = sh.geom_type

    if gt is 'Point':
        # artist = Circle((sh.x, sh.y), radius=thick, facecolor=color, alpha=alpha, edgecolor='none')
        # axs.add_patch(artist)
        artist, = ShapelyToArtist(sh, axs)
        artist.set_markersize(args['pointsize'])
        artist.set_marker(args['marker'])
        artist.set_markerfacecolor(args['color'])
        artist.set_markeredgecolor(args['color'])
        artist.set_markeredgewidth(args['linewidth'])
        artist.set_alpha(args['alpha'])
        if label != '':
            axs.text(sh.x, sh.y, label, 
                     color=args['color'],
                     alpha=args['alpha'],
                     fontsize=args['lfontsize'])
    elif gt in ['LineString', 'LinearRing']:
        artist, = ShapelyToArtist(sh, axs)
        artist.set_linewidth(args['linewidth'])
        artist.set_color(args['color'])
        artist.set_alpha(args['alpha'])
        artist.set_markersize(args['pointsize'])
        if 'i' in order:
            # plot lines 
            artist.set_linestyle('-')
        else:
            artist.set_linestyle('')
        if 'v' in order:
            # plot vertices
            artist.set_marker(args['marker'])
            artist.set_markeredgecolor(args['color'])
        else:
            artist.set_marker(None)

        if 'i' in indices:
            for (i, (c1, c2)) in enumerate(zip(sh.coords[:-1], sh.coords[1:])):
                axs.text((c1[0] + c2[0])*0.5, (c1[1] + c2[1])*0.5, '{}'.format(i), 
                         color=args['color'],
                         alpha=args['alpha'],
                         fontsize=args['ifontsize'])
        if 'v' in indices:
            for (i, c) in enumerate(sh.coords):
                axs.text(c[0], c[1], '{}'.format(i), 
                         color=args['color'],
                         alpha=args['alpha'],
                         fontsize=args['ifontsize'])
        if label != '':
            c = sh.coords[0]
            axs.text(c[0], c[1], label, 
                     color=args['color'],
                     alpha=args['alpha'],
                     fontsize=args['lfontsize'])
    elif gt is 'Polygon':
        if 'i' in order:
            # polygon's interior.
            artist, = ShapelyToArtist(sh, axs)
            artist.set_color(args['color'])
            artist.set_alpha(args['alpha'])
            artist.set_edgecolor('none')
        if 'b' in order or 'v' in order:
            # plot polygon's boundary line and vertices:
            newargs = {}
            newargs.update(args)
            newargs['label'] = ''
            newargs['indices'] = ''
            if 'b' in indices:
                newargs['order'] += 'i'
            if 'v' in indices:
                newargs['order'] += 'v'
            newargs['order'] = ''
            if 'b' in order:
                newargs['order'] += 'i'
            if 'v' in order:
                newargs['order'] += 'v'
            newargs['axis'] = axs
            ShapelyToAxis(sh.boundary, **newargs)
        if label != '':
            c = sh.centroid
            axs.text(c.x, c.y, label, 
                     color=args['color'],
                     alpha=args['alpha'],
                     fontsize=args['lfontsize'])

    elif 'Multi' in gt or gt is 'GeometryCollection':
        newargs = {}
        newargs.update(args)
        newargs['axis'] = axs
        newargs['autoscale'] = False
        for i, s in enumerate(sh.geoms):
            if args['label'] != '':
                newargs['label'] = args['label'] + ' {}'.format(i)
            axs = ShapelyToAxis(s, **newargs)

    else:
        raise TypeError('Plotting of {} geometry type is not implemented'.format(shapely.geom_type))

    # autoscale taking into account all collections in the axes.
    if args['autoscale']:
        axs.autoscale_view() # this does not work for collections

    return axs





if __name__ == '__main__':
    
    from shapely.geometry import Point

    p1 = Point((2, 3))
    p2 = Point((4, 5))

    # Put points to separate plots 
    a1 = ShapelyToAxis(p1, thickness=1.)
    a2 = ShapelyToAxis(p2)

    a1.get_figure().savefig('p10.pdf')
    a2.get_figure().savefig('p20.pdf')

    # Put points to one plot
    a3 = ShapelyToAxis(p1, color='green')
    a3.get_figure().savefig('p31.pdf')
    a3 = ShapelyToAxis(p2, color='blue', axis=a3)
    a3.get_figure().savefig('p32.pdf')

    # plot lines
    p3 = p1.buffer(1, resolution=5).exterior
    p4 = p2.buffer(2, resolution=3).exterior

    a4 = ShapelyToAxis(p3, color='green')
    a4.get_figure().savefig('p40.pdf')
    a4 = ShapelyToAxis(p4, color='red', axis=a4)
    a4.get_figure().savefig('p41.pdf')

    # plot polygons
    p4 = p1.buffer(1, resolution=6)
    p5 = p2.buffer(2, resolution=20)
    a5 = ShapelyToAxis(p4, color='black')
    a5.get_figure().savefig('p50.pdf')
    a5 = ShapelyToAxis(p5, color='yellow', axis=a5)
    a5.get_figure().savefig('p51.pdf')

    # plot multi objects
    p6 = p4.symmetric_difference(p5)
    p7 = p4.exterior.intersection(p5)
    p8 = p4.exterior.intersection(p5.exterior)
    a6 = ShapelyToAxis(p6, color='green')
    a6.get_figure().savefig('p60.pdf')
    ShapelyToAxis(p7, color='blue', axis=a6)
    ShapelyToAxis(p8, color='red', axis=a6).get_figure().savefig('p61.pdf')


