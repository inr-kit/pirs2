"""
Fucntions to visually represent comparison of volumes.

Compared are a set of MCNP-computed volumes with a set obtained from CAD or
another MCNP calculations. A list of correspondent cells is necessary. Each MCNP
set contains statistical errors, while CAD sets not.

The result of comparison -- is a Matplotlib figure showing relative deviation of
two sets as function of volume. Optionally:

    * Use different colors to specify deviation from expected values. Generate
    optionally a label with this information

    * Generate text output with most deviating cell numbers

"""

"""
TODO: transform to a class with the following API:
    c = CompareClass()
    nc = c.add_cad('model_cad_volumes.txt')
    nm1 = c.add_mctal('mctal1')
    nm2 = c.add_mctal('mctal2')

    axs = c.compare(nc, nm1, excludecells = (10050, 10051), labellimit = 100)
    axs.get_figure().savefig('{}_{}.pdf'.format(nc, nm1))
"""

import numpy

def get_cad(filename):
    """
    Read CAD volumes from a file. The file should have 2 columns, cell numbers
    and cell volumes.

    Volumes are multiplied by 1e-3.

    Returns two numpy arrays, with cell numbers (int type) and cell volumes
    (float type).
    """
    import numpy
    try:
        n = numpy.loadtxt(filename, usecols=(0,), dtype=int)
        v = numpy.loadtxt(filename, usecols=(1,), dtype=float)
        return (n, v *1e-3)
    except:
        return None


def get_mctal(filename, tally=4):
    """
    Read MCNP computed volumes from tally in mctal.

    Returns two numpy arrays, with cell numbers (int type) and comuted volumes
    (float type, with rel.errors).
    """
    from pirs.mcnp.mctal import Mctal

    m = Mctal()
    m.read_complete(filename)
    t = m.mctaltallies[tally]
    nl = t.fnl_numpy
    vl = t.vals_numpy

    return nl, vl.transpose()

def compare(s1, s2, exclude_cells = ()):
    """
    s1, s2:
        Sets with cell volumes. It is a 2 dimensional array, with shape (N, 2)
        for CAD data or (N, 3) for MCNP data.

    deviations:
        a list (tuple) or 1-dimensional array of deviation values, which
        will be used as limit of the deviation groups to compute the number
        of cells in each group and to choose colors.
    """

    # Ensure that the set of cell numbers is the same
    na, va = _prepare(s1, s2)

    u = va[:, 0]
    v = va[:, 1]
    r = va[:, 2]

    x = u
    y = (u/v - 1.0)/r


    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter

    fig = plt.figure(figsize=(10, 6))
    # axs = fig.add_subplot(1, 1, 1)

    # Axes for the scatter and histogram
    asctr = fig.add_axes((0.1, 0.1, 0.7, 0.8))
    ahist = fig.add_axes((0.85, 0.1, 0.1, 0.8))

    # Mask cells to exclude:
    mc = na > 0   # set all to True
    for c in exclude_cells:
        mc = mc ^ (na == c)


    asctr.plot(x[mc], y[mc], '.')


    # put labels onto most extending points:
    imax = y[mc].argmax()
    imin = y[mc].argmin()
    for i in (imin, imax):
        nl = na[mc][i]
        xl = x[mc][i]
        yl = y[mc][i]
        asctr.annotate(str(nl),
                       xy = (xl, yl),
                       xytext = (-20, 20),
                       ha = 'right',
                       va = 'bottom',
                       bbox = dict(boxstyle='round,pad=0.5',
                                   fc='yellow',
                                   alpha=0.3),
                       textcoords = 'offset points',
                       arrowprops = dict(arrowstyle='->',
                                         connectionstyle='arc3,rad=0')
                       )

    asctr.set_xscale('log')
    asctr.set_xlabel('volume, $cm^3$')
    asctr.set_ylabel(r'$\gamma = \frac{V_M/V_C - 1}{R_C}$')


    # Histogram does not need axis labels
    ahist.xaxis.set_major_formatter(NullFormatter())
    ahist.yaxis.set_major_formatter(NullFormatter())

    # Plot histogram
    ahist.hist(y[mc], orientation='horizontal')

    # Use the same limits
    ahist.set_ylim(asctr.get_ylim())

    return fig

def _prepare(s1, s2):

    # Resulting dictionary, mapping cell number to tuple (ui, vi, Ri).
    d = {}

    for s in (s1, s2):
        for n, a in zip(*s):
            try:
                v, rv = a
            except:
                v, rv = a, 0.0
            if n in d:
                u, ru = d[n]
                d[n] = (u, v, (ru**2 + rv**2)**0.5)
            else:
                d[n] = v, rv

    # remove keys in d with uncomplete data
    for n, uvr in d.items():
        if len(uvr) == 2:
            d.pop(n)

    na = numpy.zeros((len(d), ), dtype=int)
    va = numpy.zeros((len(d), 3), dtype=float)
    for (i, (n, (u, v, r)))  in enumerate(d.items()):
        na[i] = n
        va[i, :] = u, v, r

    # don't use data with v=0 or r=0
    m1 = va[:, 1] > 0.0
    m2 = va[:, 2] > 0.0

    na = na[m1 * m2]
    va = va[m1 * m2, :]

    return na, va
