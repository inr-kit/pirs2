"""

"""

from mctal import read_values, _MctalTally


def read_mctal(fn):
    """
    fn is a file name. This file is opened inside the function to ensure that the
    file cursor is placed to the begin of file.

    This function reads mctal file as written by MCNP version 5.
    """
    f = open(fn, 'r')
    kod = read_kod(f)
    pil = read_pil(f)
    ntal, tals = read_ntal(f)

    print kod
    print repr(pil)
    print ntal, tals

    # dictionary of tallies
    td = {}
    for nt in tals:
        td[nt] = _MctalTally()

    # loop over talliies in mctal
    for i in range(ntal[0]):
        print i
        tal = read_tally(f)
        mij = read_t_tally(f)
        fc  = read_t_fc(f)

def read_t_tally(f):
    """
    read TALLY line -- the 1-st line of the tally.
    """
    l = f.next()
    t = map(int, l.split()[1:])
    m = t.pop(0) # tally name
    i = t.pop(0) # particle type
    j = t.pop(0) # type of detector
    assert 'tally' in l.lower()
    return m, i, j


def read_t_fc(f):
    """
    read tally comments: Zero or more lines starting with 5 spaces.
    """
    # TODO: add reading of FC lines.
    cp = f.tell()
    l = f.next()

    return []


# ------------------------------------------------------------------------------------------------------------------



def read_tally(f):
    """
    read TALLY line -- the 1-st line of the tally.
    """
    l = f.next()
    t = map(int, l.split()[1:])
    m = t.pop(0) # tally name
    i = t.pop(0) # particle type
    j = t.pop(0) # type of detector

    # mcnp6 mctal contains also for some tallies additional term
    # that is not documented in the manual.

    if i < 0:
        # mcnp6 feature: negative i is the number of particles
        pl = map(int, f.next().split())

    fc = read_tally_fc(f)
    fn, cells = read_tally_fn(f, j)
    dn = read_tally_dn(f)
    un = read_tally_un(f)
    sn = read_tally_un(f)
    mn = read_tally_un(f)
    cn = read_tally_cn(f)
    en = read_tally_cn(f)


def read_tall_cn(f):
    l = f.next()
    t = l.split() + [0] # the last entry is optional, if 0. If it is given, this 0 is not used.
    c = t.pop(0)[1:]
    n, f = map(int, t[:2])
    # read bin boundaries or variable values
    v = read_values(f, n, float, True)
    return n, f, c, v



def read_tally_un(f):
    """
    read u line of the tally.
    """
    l = f.next()
    t = l.split()
    c = t.pop(0)[1:]
    n = int(t.pop(0))
    # It seems that n=0 instead of n=1 is walid only for standard tallies. For
    # mesh tallies, u line can contain 1.
    if n == 0:
        n = 1
    return n, c



def read_tally_dn(f):
    """
    read d line of a tally
    """
    l = f.next()
    return int(l.split()[-1])


def read_tally_fn(f, j):
    """
    read number of cells and cell names.

    j -- type of tally (detector?).
    """
    l = f.next()
    t = l.split()
    assert t[0] in 'fF'
    t = map(int, t[1:])
    n = t # number of cells, followed by the mesh size in each direction for tmesh tallies
    if len(n) == 1 and j == 0:
        # n is the number of cells. Read cell names
        cells = read_values(f, n[0], int, True)
        return n, cells
    elif len(n) == 4:
        # this is a tmesh tally.
        cor = []
        for nn in n[2:]:
            cor.append( read_values(f, nn+1, float, True))
        return n, cor


def read_ntal(f):
    """
    read line with ntal and npert
    """
    l = f.next()
    n = map(int, l.split()[1::2])
    tals = read_values(f, n[0], type_=int, True)
    return n, tals

def read_pil(f):
    """
    Problem identification line, followed by 1 space.
    """
    l = f.next()
    assert l[0] == ' '
    return l[1:-1].rstrip() # newline and trailing spaces are stripped.


def read_kod(f):
    """
    1-st line of the mctal file.
    """
    l = f.next()
    t = l.split()
    kod = t.pop(0)
    ver = t.pop(0)
    # probid can have spaces. Therefore, first read all other entries -- the rest will be probid.
    rnr = t.pop(-1)
    nps = t.pop(-1)
    knd = t.pop(-1)
    prb = ' '.join(t)
    assert prb in l
    return kod, ver, prb, knd, nps, rnr


if __name__ == '__main__':
    # try mcnp6 and mcnp5
    for fn in ['c6_m', 'c5_m']:
        read_mctal(fn)



