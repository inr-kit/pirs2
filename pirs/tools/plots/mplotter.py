"""
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

Functions to plot zmesh.

It is realized outside zmesh to make possible the general model specifications
even if matplotlib is not installed.
"""
# first, specify pdf backend:
# from matplotlib import use
# use('Cairo.pdf')
# use('cairo')
import matplotlib.pyplot as pyplot


def zmesh_to_xye(zmesh, xtype='z'):
    """
    Returns three lists containing x, y and e for errorbar

    xtype defines what values go to the x list. Can be 'z' or 'k'.

    """
    if xtype == 'z':
        xc = map(lambda v: v[2], zmesh.element_coords('abs'))
    else:
        xc = range(len(zmesh.get_grid()))
    yvals = zmesh.values()
    if hasattr(yvals[0], 'nominal_value'):
        y = map(lambda x: x.nominal_value, yvals)
        e = map(lambda x: 2.*x.std_dev,  yvals) # *2 for the 95% confidence interval. Better to see on the graph for big statistics.
    elif isinstance(yvals[0], tuple) and len(yvals[0]) == 2:
        y = map(lambda x: x[0], yvals)
        e = map(lambda x: 2.*x[1]*x[0], yvals)
    else:
        y = yvals
        e = None # [0.] * len(yvals)
    return xc, y, e

def zmesh_to_step(zmesh, xtype='z'):
    """
    Returns x and y to plot a piece-wise constant line by the pyplot.plot() function.
    """
    z, v, _ = zmesh_to_xye(zmesh, xtype)

    if xtype == 'z':
        zb = zmesh.boundary_coords('abs')
    else:
        zb = map(lambda x: x+0.5, [-1] + z)
         
    x = []
    y = []
    for (z1, z2, val) in zip(zb[:-1], zb[1:], v):
        x += [z1, z2]
        y += [val, val]

    return x, y

class MeshPlotter(object):
    """
    Simplifies generation of figures representing heat, temperature and density
    of general model elements.

    Generated figure can have one ore more plots arranged in one column.

    Data to be plotted is taken from general models passed as arguments to the
    figure() method. The layout of the figure, i.e. which data of which element
    appears on which plot, is defined by the add_line() method.

    """
    def __init__(self, figsize=(12, 16)):
        self.__s = {} # setup dict
        self.figsize = figsize

        self.__xlim = None
        self.__ylim = {}
        self.__xlabel = {}
        self.__ylabel = {}
        self.__atitle = {}
        return

    def copy(self):
        """
        Returns a new instance of Plotter, a copy of self.
        """
        res = MeshPlotter()
        res.__s.update(self.__s)
        res.figsize = self.figsize[:]
        res.__xlim = self.__xlim
        res.__ylim.update(self.__ylim)
        res.__xlabel.update(self.__xlabel)
        res.__ylabel.update(self.__ylabel)
        res.__atitle.update(self.__atitle)
        return res

    def add_line(self, Iaxis, Imod, ckey, what, Iprev, sharex=0, sharey=None, **line2Dprop):
        """
        Add line to one of plots on the figure. 

        Iaxis -- the plot index. 0 corresponds to the most upper plot.

        Imod -- model index. 0 corresponds to the first model passed to figure() method.

        ckey -- compound key specifying the element, which data is plotted. 

        what -- string name specifying one of the elemnt's attributes: 'heat', 'temp', or 'dens', or
                the same but prefixed with 'k', 'kheat', 'ktemp', 'kdens'. In
                the latter case, the x coordinate will be the index of axial
                mesh element, not its position.

        Iprev -- the Plotter remembers previously plotted data and can add them. This
                 integer value specifies how many of the previous data should
                 appear on the plot.  For example, -1 means to plot the data
                 actually specified and to add data plotted in the previous
                 call to figure. In this way one can easily see how a state
                 variable changes from iteration to iteration.

        sharex -- Index of the plot whose x axis should be shared with.

        sharey -- Index of the plot whose y axis should be shared with.

        line2Dprop -- additionally one can pass keyword arguments specifying line
                      properties, as the shape of the marker, its color, etc. See
                      description of matplotlib.pyplot.plot() function.

        """
        if Iaxis not in self.__s.keys():
            self.__s[Iaxis] = []

        if what[0] == 'k':
            what = what[1:]
            xtype = 'k'
        else:
            xtype = 'z'
        self.__s[Iaxis].append(  [[], [], Imod, ckey, what, xtype, Iprev, line2Dprop, sharex, sharey]  )
        return

    @property
    def xlim(self):
        """
        Tuple specifying limits of the plots x axis. 
        
        Note that all plots on the figure share the same x axis, therefore
        setting this value affects all plots.

        If None, default setings apply.
        """
        return self.__xlim

    @xlim.setter
    def xlim(self, value):
        self.__xlim = value

    @property
    def ylim(self):
        """
        A dictionary to store limits of the vertical axis.

        Keys are axes indices, values -- tuples (min, max).
        """
        return self.__ylim

    @property
    def ylabel(self):
        """
        A dictionary to store vertical axis labels.

        Keys are axes indices, values -- strings.
        """
        return self.__ylabel

    @property
    def xlabel(self):
        """
        A dictionary to store horizontal axis labels.

        Keys are axes indices, values -- strings.

        Note that the plots share their x axes, so usually it is enough to set
        only one xlabel, for the lowest plot.
        """
        return self.__xlabel

    @property
    def atitle(self):
        """
        A dictionary to store axes titles.

        Keys are axes indices, values -- strings.
        """
        return self.__atitle


    def figure(self, *models, **kwargs):
        """
        Returns matplotlib.pyplot.figure instance.

        *models is a list of models containing data to plot.

        UPD: Instead of a model, one can pass values to plot as list (or tuple)
        of the structure, [lx, ly, le], where lx -- list of x values, ly --
        list of y values and le is (optional) list of rel.err values.

        UPD: optional keyword argument xtran is a mappable defining
        transformation of x values, or a list of mappables.

        """
        kl = self.__s.keys()
        Iaxmin = min(kl)
        Iaxmax = max(kl)

        # kw arguments:
        kw = {}
        kw['xtrans'] = None
        kw['label'] = None
        kw.update(kwargs)

        # x transformations. Can be a callable or list of callables or None
        # TODO 
        xtr = kwargs.get('xtrans', None)

        # labels
        lbl = {}
        if kw['label'] is not None:
            lbl.update(kw['label'])


        fig = pyplot.figure(figsize=self.figsize)

        axs = {}
        Nax = Iaxmax - Iaxmin + 1
        for i in range(Iaxmin, Iaxmax + 1):
            shx, shy = self.__s[i][0][8:]
            shx = axs.get(shx, None)
            shy = axs.get(shy, None)
            
            a = fig.add_subplot(Nax, 1, i - Iaxmin + 1, sharex=shx, sharey=shy)
            axs[i] = a
        

        for (Iax, ax) in axs.items():
            # Iax = i + Iaxmin
            put_legend = False
            for s in self.__s[Iax]:
                # default line2D properties for scatters
                Lprp = {}
                Lprp['alpha'] = 0.
                Lprp['fmt'] = '.k'
                Hlst = s[0]  # list of the previous data
                Lval = s[1]  # list of the previous label values
                Imod = s[2]  # Imod, model index
                ckey = s[3]  # ckey, element's compound key
                attr = s[4]  # what, attriburte: heat, temp or dens
                xtyp = s[5]  # xtype, type of horizontal axis: axial coordinate or axial mesh index.
                Iprv = s[6]  # Iprev, Index of the previous data to be plotted. Must be negavite, 0 corresponds to the current data.
                Lprp.update(s[7])  # line2d properties, including legend

                # add current data to the history list:
                try:
                    e = models[Imod].get_child(ckey)
                except AttributeError:
                    # v is a list or tuple of lists with x y and e data.
                    v = models[Imod][:]
                    # data for points:
                    xp = v[0][:]
                    yp = v[1][:]
                    # 
                    if len(v) == 3:
                        ep = v[2][:]
                    else:
                        ep = None
                    # data for line:
                    xl = None
                    yl = None
                    # apply xtrans:
                    xp = map(xtr, xp)

                else:
                    # e is a solid
                    v = getattr(e, attr).copy()
                    # data for points:
                    xp, yp, ep = zmesh_to_xye(v, xtyp)
                    # data for line:
                    xl, yl = zmesh_to_step(v, xtyp)
                    # apply xtrans:
                    xl = map(xtr, xl)
                    xp = map(xtr, xp)

                Hlst.append((xl, yl, xp, yp, ep))
                Lval.append(lbl)

                # TODO add default line2D properties
                dalpha = 0.9/(1. - Iprv)
                if 'label' in Lprp.keys():
                    put_legend = True
                Hpart = Hlst[Iprv-1:] # part of the history to be plotted
                while len(Hpart) > 0:
                    # data to be plotted
                    xl, yl, xp, yp, ep = Hpart.pop(0)
                    # transparency 
                    Lprp['alpha'] += dalpha
                    # legend
                    lbl['i'] = -len(Hpart)  # data index, the latest being 0
                    lorig = None
                    if 'label' in Lprp.keys():
                        lorig = Lprp['label'][:]
                        Lprp['label'] = lorig.format(**lbl)
                    # plot line
                    if xl is not None:
                        lline = ax.plot(xl, yl, '-')
                    else:
                        lline = []
                    # plot points:
                    pline, caps, bars = ax.errorbar(xp, yp, ep, **Lprp)
                    # put back original legend template
                    if lorig is not None:
                        Lprp['label'] = lorig
                    alpha = pline.get_alpha()
                    color = pline.get_color()
                    for c in caps + bars + tuple(lline):
                        c.set_alpha(alpha)
                        c.set_color(color)

            if put_legend:
                ax.legend()

            if Iax in self.__xlabel.keys():
                ax.set_xlabel(self.__xlabel[Iax])
            if Iax in self.__ylabel.keys():
                ax.set_ylabel(self.__ylabel[Iax])
            if Iax in self.__ylim.keys():
                ax.set_ylim(self.__ylim[Iax])
            if Iax in self.__atitle.keys():
                ax.set_title(self.__atitle[Iax])

            if self.__xlim is not None:
                ax.set_xlim(self.__xlim)

        self.axdict = axs
        return fig
                



        





if __name__ == '__main__':
    import doctest
    doctest.testmod()

