"""
Fucntions to visually represent comparison of volumes.

Compared are a set of MCNP-computed volumes with a set obtained from CAD or
another MCNP calculations. A list of correspondent cells is necessary. Each MCNP
set contains statistical errors, while CAD sets not.

The result of comparison -- is a Matplotlib figure showing relative deviation of
two sets as function of volume.
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
    y = (u - v)/(r*v)


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

def report(s1, s2, limit=100):
    """
    Print out all cells with y above limit.
    """
    na, va = _prepare(s1, s2)

    u = va[:, 0]
    v = va[:, 1]
    r = va[:, 2]

    y = (u - v)/(r*v)

    mask = abs(y) > limit

    fmt =  '{:9d}' + ' {:15.4e}'*2 + ' {:10.7f}' + ' {:10.2g}'

    for n, (u, v, r), yy in zip(na[mask], va[mask], y[mask]):
        print fmt.format(n, u, v, r, yy)

def report_title():
    ttl = ('{:>9s}' + ' {:>15s}'*2 + ' {:>10s}'*2).format('Cell',
                                                       'Ref_vol', 'MCTAL_vol',
                                                       'Rel.err', 'Dev/sigma')
    print ttl


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


def main():
    import argparse

    # Define command line arguments
    parser = argparse.ArgumentParser(description='Compare CAD and MCNP volumes')

    parser.add_argument('--cad', default = '',
                        help = "File with cell numbers (1-st column) and cell volumes (2-nd column)",
                        type=str)
    parser.add_argument('--mctal', nargs='+', type=str,
                        help = 'MCTAL files to read MCNP computed volumes from')
    parser.add_argument('--tally', nargs='*', type=int, default=(4,),
                        help = 'Tally number containing volumes. One for all mctal files or per-mctal, in the same order as --mctal')
    parser.add_argument('--cells', nargs='*', type=int, default = (),
                        help = 'Cells to exclude from the plots.')
    parser.add_argument('--limit', type=int, default=100,
                        help = 'Limit for report')

    args = parser.parse_args()

    # Generator to extend list of tally numbers to the list of mctals.
    def tally_number(lst):
        l = list(lst)
        while l:
            yield l.pop(0)
            if not l:
                l.extend(lst)

    # Read all mctal files
    m = []
    for mfile, tn in zip(args.mctal, tally_number(args.tally)):
        m.append((mfile, get_mctal(mfile, tally=tn)))

    # Read file with CAD volumes
    c = get_cad(args.cad)
    cname = args.cad
    if c is None:
        cname, c = m.pop(0)
        print 'The first MCNP data is used as a reference'

    # Generate figures comparing CAD with each MCTAL
    for mfile, mm in m:
        fig = compare(c, mm, exclude_cells = args.cells)
        figname = '{}_{}.pdf'.format(cname, mfile)
        fig.savefig(figname)
        print 'Plot written to ', figname

    print '\n\n\nCells deviating more than {} sigma:'.format(args.limit)
    report_title()
    for mfile, mm in m:
        print 'In {}:'.format(mfile)
        report(c, mm, limit = args.limit)



if __name__ == '__main__':
    main()
