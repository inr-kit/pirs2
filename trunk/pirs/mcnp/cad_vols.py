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

def compare(s1, s2, deviations=(1, 2, 3)):
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



def _prepare(s1, s2):
    d = {}
    for s in (s1, s2):
        if s.shape[1] == 2:

    for :
        d[int(n)] = ()





def _prepare_data(m1, m2):
    if len(m1.shape) > 1:
        m1 = m1[0, :]

    # remove values corresponding to zero rel.er in m2
    mask = m2[1, :] > 0
    m2 = m2[:, mask]
    m1 = m1[mask]

    # Remove values that correspond to zero values in m1
    mask = m1 > 0
    m1 = m1[mask]
    m2 = m2[:, mask]

    return m1, m2



def compare(m1, m2, groups = (0, 1, 2, 3)):
    """
    Return a matplotlib figure.

    m1, m2 -- arrays with mcnp volumes from two independent runs.

    m1[N, 2], m2[N, 2], where N -- number of cell volumes to compare.
    """

    m1, m2 = _prepare_data(m1, m2)
    # # Use only values form the 1-st set:
    # if len(m1.shape) > 1:
    #     m1 = m1[0, :]

    # # Remove zero values from m1
    # zm = m1 > 0
    # m1 = m1[zm]
    # m2 = m2[:, zm]
    print m1.shape

    g = m2[0, :] / m1 - 1.0
    r = m2[1, :]

    gabs = abs(g)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 6))
    axs = fig.add_subplot(1, 1, 1)

    l1 = ''
    for u  in reversed(groups):
        m = gabs >= u * r
        if len(m1[m]) > 0:
            l0 = r'{} \leq |\gamma|'.format(u)
            label = '$' + l0 + l1 + '$' + '({})'.format(len(m1[m]))
            print repr(label)
            axs.errorbar(x = m1[m], y = g[m], yerr = r[m], fmt='.', label = label)
        l1 = r'< {}'.format(u)

        m = ~m
        m1 = m1[m]
        g = g[m]
        r = r[m]
        gabs = gabs[m]
        # axs.errorbar(x = m1, y = g, yerr = r, fmt='.', label = r'$|\gamma| < {}$: {}'.format(u, len(m1)))
    axs.set_xscale('log')
    axs.legend()

    axs.set_xlabel('CAD volume, $cm^3$')
    axs.set_ylabel('$\gamma = V_M/V_C - 1$')
    return fig

def compare_txt(m1, m2, f, groups=(0, 1, 2, 3), cells=None):
    """
    Print comparison to a file f
    """

    m1, m2 = _prepare_data(m1, m2)
    # # Use only values form the 1-st set:
    # if len(m1.shape) > 1:
    #     m1 = m1[0, :]

    # # Remove zero values from m1
    # zm = m1 > 0
    # m1 = m1[zm]
    # m2 = m2[:, zm]
    print m1.shape

    g = m2[0, :] / m1 - 1.0
    r = m2[1, :]

    gabs = abs(g)

    with open(f, 'w') as ff:
        for i in range(len(g)):
            gi = g[i]
            ci = m1[i]
            ri = r[i]
            ai = gabs[i]
            for u in reversed(groups):
                if ai > u * ri:
                    break
            if u >= 3:
                j = '{} *'.format(u)
            else:
                j = '{}'.format(u)

            # else:
            #     j = '-'
            print >> ff, '{:6d} {:12.4e} {:12.4e} {:12e} {}'.format(i + 1, ci, gi, ri, j)




if __name__ == '__main__':
    from pirs.mcnp.mctal import Mctal
    from sys import argv

    # get CAD volumes
    from numpy import loadtxt
    cells = loadtxt('DEMO_TBM_PP1.cad', dtype=int, usecols=(0, ))
    cvols = loadtxt('DEMO_TBM_PP1.cad', dtype=float, usecols=(1, )) * 1e-3


    t0 = None
    for f in argv[1:]:
        m = Mctal()
        m.read_complete(f)
        mvols = m.mctaltallies[4].vals_numpy[:, 0:cells.shape[0]]
        mcells = m.mctaltallies[4].fnl_numpy[0:cells.shape[0]]

        if all(cells == mcells):
            fig = compare(cvols, mvols)
            fig.savefig('{}.pdf'.format(f))
            compare_txt(cvols, mvols, '{}.txt'.format(f), cells=cells)







