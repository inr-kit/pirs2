"""
Read mctal as written by mcnp5.
"""
from mctal import read_values
import numpy


class DTally(object):
    """
    Dummy class to store tally information as instance attributes.
    """

    def __init__(self, lines):
        """
        Read all tally parameters from lines -- part of the mctal file that starts with the 'TALLY' keyword.
        """
        self._read_t_tally(lines.pop(0))
        self._read_t_fc(lines)
        self._read_t_fn(lines)
        self._read_t_d(lines.pop(0))
        self._read_t_usm(lines)
        self._read_t_cet(lines)
        self._read_t_vals(lines)
        return None

    def _read_t_vals(self, lines):
        """
        Read tally values. lines should start with the line containing the 'VALS' keyword.
        """
        # tuple of dimensions
        s = (2, self.t[1], self.e[1], self.c[1], self.m[1], self.s[1], self.u[1], self.d, self.f[0])
        s = filter(lambda x: x>0, s)
        v = numpy.zeros(s)
        t = read_values(lines, v.size, float)
        t = numpy.array(t)
        t.
        print s

        return

    def __read_cet(self, lines):
        cnf = lines.pop(0).split()
        if len(cnf) == 3:
            c, n, f = cnf
        else:
            c, n = cnf
            f = 0
        n = int(n)
        f = int(f)
        if f == 0:
            nv = n
        else:
            nv = n + 1
        if nv > 0:
            bvl = read_values(lines, nv, float)
        else:
            bvl = []
        return c, n, f, bvl


    def _read_t_cet(self, lines):
        self.c = self.__read_cet(lines)
        self.e = self.__read_cet(lines)
        self.t = self.__read_cet(lines)
        return


    def _read_t_usm(self, lines):
        u, un = lines.pop(0).split()
        s, sn = lines.pop(0).split()
        m, mn = lines.pop(0).split()
        un = int(un)
        sn = int(sn)
        mn = int(mn)
        self.u = u, un
        self.s = s, sn
        self.m = m, mn
        return


    def _read_t_d(self, l):
        n = int(l.split()[1])
        self.d = n
        return


    def _read_t_fn(self, lines):
        """
        Read Fn and the following list of cell/surface numbers
        """
        l = lines.pop(0)
        fn = int(l.split()[1])
        if self.mij[-1] == 0:
            fnl = read_values(lines, fn, int) 
        else:
            fnl = []
        self.f = fn, fnl
        return


    def _read_t_fc(self, lines):
        """
        Read tally comments. These are lines starting with 5 spaces.
        """
        fc = []
        while lines[0][:5] == ' '*5:
            fc.append(lines.pop(0))
        self.fc = fc
        return


    def _read_t_tally(self, l):
        """
        read TALLY line -- the 1-st line of the tally.
        """
        t = map(int, l.split()[1:])
        m = t.pop(0) # tally name
        i = t.pop(0) # particle type
        j = t.pop(0) # type of detector
        assert 'tally' in l.lower()
        self.mij = m, i, j
        return


    def report(self):
        # print all attributes:
        for k, v in sorted(self.__dict__.items()):
            print k, v



def read_mctal(fn):
    """
    fn -- name of the mctal file.
    """

    # THe whole file is read to the list. This simplifies its parsing and
    # usually does not brings problems with memory
    lines = open(fn, 'r').readlines()

    # header
    kod = read_kod(lines.pop(0))
    pil = read_pil(lines.pop(0))
    ntal, tals = read_ntal(lines)

    print 'kod', kod
    print 'pil', pil
    print 'ntal', ntal, tals

    # loop over tallies
    for i in range(ntal[0]):
        t = DTally(lines)
        t.report()
        print '-'*80

        while lines and 'tally' not in lines[0].lower():
            lines.pop(0)

    

def read_ntal(lines):
    """
    read line with ntal and npert,  and all following tally names.
    """
    l = lines.pop(0)
    n = map(int, l.split()[1::2])
    tals = read_values(lines, n[0], int, True)
    return n, tals


def read_pil(l):
    """
    Problem identification line, preceeded by 1 space.
    """
    assert l[0] == ' '
    return l[1:-1].rstrip() # newline and trailing spaces are stripped.


def read_kod(l):
    """
    l -- is the 1-st line of the mctal file.
    """
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
    fn = 'c5_m'

    read_mctal(fn)



