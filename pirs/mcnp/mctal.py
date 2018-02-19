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

Representation of mctal files.

TODO: incomplete.
"""

# numpy is useful, but not always present. Use optionally.
try:
    import numpy
    numpy_exists = True
except ImportError:
    numpy_exists = False

import re
def add_e_to_exp(s, e='e'):
    """
    MCNP uses float point format without 'E' when exponent has 3 digits, 
    i.e. 1.2e-123 is printed out as 1.2-123.

    This function adds 'e' or 'E' to such strings.
    """

    # Expression to search for exponent without "e" or "E". 
    large_exp = re.compile('\d([-+]\d)')
    r = large_exp.search(s)
    if r:
        ss = r.groups()[0]
        return s.replace(ss, e+ss)
    else:
        return s[:]

def str2float(s):
    return float(add_e_to_exp(s))

def read_values(lines, N, type_=str, check=True):
    """
    Reads N space-separated values from lines. Values can span to several
    elements of lines.

    The `lines` argument is a list-like object (should have `pop` method).

    Returns a tuple of N values. of type `type_`.

    The lines needed to read N values are removed from the list. If only part of 
    the line is necessary, it is truncated and the rest is still in lines.


    Note that this function changes the first argument, lines!

    UPD: previous implementation was written also for files. It used the `next`
    method, which could interfere with `readline` needed to read tally
    comments. Therefore, I removed support for file objects here and use only
    list of lines. THis mean that the whole mctal file is first read into a
    list of lines and than this list is processed. This should not cause memory
    problems: for example, a 800MB file is read with `readlines` within several
    seconds and fits to about 6 GB memory. 

    """
    res = []
    tokens = []
    while len(res) < N:
        if tokens:
            t = tokens.pop(0)
            res.append(t)
            cline.replace(t, '', 1)
        else:
            cline = lines.pop(0) # the whole line is needed to accurately put back the rest, if any.
            tokens = cline.split()

    if type_ is float:
        # check special format used for float values with large exponent: 
        # the exponent part starts with the sign only, without "e" or "E".
        res = map(add_e_to_exp, res)
        
    res = map(type_, res)
    if not check:
        # put the rest of tokens to lines:
        if tokens:
            lines.insert(0, cline.lstrip()) 
    else:
        assert tokens == []
    return res

class KcodeArray(object):
    """
    Representation of the kcode array in mctal file.
    """
    def __init__(self):
        self.nc = 0
        self.ikz = 0
        self.mk = 0
        self.array = []
        return

    def __str__(self):
        res = ['kcode {0} {1} {2}'.format(self.nc, self.ikz, self.mk)]
        for a in self.array:
            s = ''
            for v in a:
                s += ' {0}'.format(v)
            res.append(s)
        return '\n'.join(res)

    def final(self):
        """
        Returns (Keff, stdev).

        Returns 12-th and 13-th entries of the RKPL array.
        """
        if self.mk == 19:
            return self.array[-1][11:13]
        else:
            raise NotImplementedError


class _MctalTally(object):
    # see attributes in Mctal.read_complete()
    pass
                

class Mctal(object):
    def __init__(self):
        self.__kcode = KcodeArray()
        return

    @property
    def kcode(self):
        return self.__kcode

    def final(self):
        return self.__kcode.final()

    def read(self, filename):
        """
        Reads kcode array from mctal file.
        """
        f = open(filename)
        section = ''
        for l in f:
            if section != 'kcode' and 'kcode' in l[:10].lower():
                # read first line of the kcode section
                nc, ikz, mk = map(int, l.split()[1:])
                section = 'kcode'
                # read all other lines of the kcode section:
                vals = []
                while len(vals) < nc*mk:
                    l = f.next()
                    vals += map(float, l.split())
                # rearrange list to a list of lists.
                kcode = []
                while len(kcode) < nc:
                    a = []
                    for i in range(mk):
                        a.append(vals.pop(0))
                    kcode.append(a)
                self.__kcode.nc = nc
                self.__kcode.ikz = ikz
                self.__kcode.mk = mk
                self.__kcode.array = kcode
        f.close()
        return

    def read_complete(self, fname, ver=5):
        """
        Reads mctal file as written by MCNP.

        Mctal file format is different for MCNP5 and MCNP6.
        """
        with open(fname, 'r') as f:
            lines = f.readlines()
            # 1-st line with code and nps. probid can have spaces, thus it is analysed last.
            t = lines.pop(0).split()
            kod = t.pop(0)
            ver = t.pop(0)
            rnr = int(t.pop(-1))
            nps = int(t.pop(-1))
            knod = int(t.pop(-1))
            probid = ' '.join(t)
            # try to get mcnp version.
            if '6' in ver:
                ver = 6
            elif '5' in ver:
                ver = 5
            else:
                # use optional argument value
                pass

            # Problem title
            prtitle = lines.pop(0)
            # NTAL NPERT
            t = lines.pop(0).lower().split()
            
            ntal = int(t[1])
            if 'npert' in t:
                npert = int(t[3])
            else:
                npert = 0
            # List of tally names
            tals = read_values(lines, ntal, int) # list of tally names
            # 
            self.kod = kod
            self.ver = ver
            self.probid = probid
            self.knod = knod
            self.nps = nps
            self.rnr = rnr
            self.title = prtitle
            self.ntal = ntal
            self.npert = npert
            self.tals = tals
            tallies = {}
            for tname in tals:
                # placeholder for all tally parameters. Some paramters are optional
                tll = _MctalTally()
                # tally name, particle type and tally type
                tmp, m, i, j = lines.pop(0).split()[:4]  # mcnp6 writes more than 4 entries, but only 4 are describen in the manual.
                m = int(m)
                i = int(i)
                j = int(j)
                if ver == 6 and i < 0:
                    plist = lines.pop(0)  # line specifying which particles are used by the tally
                # FC card, if any
                fc = []
                while lines[0][:5] == ' '*5:
                    fc.append(lines.pop(0))
                # f: number of cell or surface bins
                fparam = lines.pop(0).split()
                fn = int(fparam[1])   # number of cells in a standard tally or mesh elemetrs in a meshtally of type A
                # list of cell or surface numbers
                if j == 0:
                    fnl = read_values(lines, fn, int)
                if j == -1:
                    # this seems to define a meshtally of type A in MCNP6.
                    na, nb, nc = map(int, fparam[3:])  # number of mesh elemetns in each direction
                    b = read_values(lines, na+nb+nc+3, float) # read mesh element boundaries in each direction
                    ba = b[:na+1]
                    bb = b[na+1:na+nb+2]
                    bc = b[na+nb+2:]
                    tll.ba = ba
                    tll.bb = bb
                    tll.bc = bc
                    tll.na = na
                    tll.nb = nb
                    tll.nc = nc

                # d: number of total vs. direct or flagged vs. unflagged bins.
                tmp, dn = lines.pop(0).split()
                dn = int(dn)
                # u: number of user bins, including the total bin if there is one.
                ufl, un = lines.pop(0).split()
                un = int(un)
                un = 1 if un == 0 else un
                # s: number of segment bins
                sfl, sn = lines.pop(0).split()
                sn = int(sn)
                sn = 1 if sn == 0 else sn
                # m: number of multiplier bins
                mfl, mn = lines.pop(0).split()
                mn = int(mn)
                mn = 1 if mn == 0 else mn
                # c: cosine bins
                cfl = lines.pop(0).split()
                cf = int(cfl.pop()) if len(cfl) == 3 else 0
                cn = int(cfl.pop())
                cfl = cfl.pop()
                # cosine values
                if cn > 0:
                    cvl = read_values(lines, cn, float)
                else:
                    cvl = []
                cn = 1 if cn == 0 else cn
                # e: Energy bins
                efl = lines.pop(0).split()
                # print 'efl', efl
                ef = int(efl.pop()) if len(efl) == 3 else 0
                en = int(efl.pop())
                efl = efl.pop()
                # print 'ef, en, efl', ef, en, efl
                # 
                if en > 0:
                    # number of energy values depends on the total bin 
                    if 't' in efl:
                        # there is total bin, so number of energy values is en - 1
                        nev = en - 1
                    else:
                        # there is no total bin, the number of energy values is en
                        nev = en
                    evl = read_values(lines, nev, float)
                else:
                    evl = []
                en = 1 if en == 0 else en
                # t: Time bins
                tfl = lines.pop(0).split()
                tf = int(tfl.pop()) if len(tfl) == 3 else 0
                tn = int(tfl.pop())
                tfl = tfl.pop()
                # 
                if tn > 0:
                    tvl = read_values(lines, tn, float)
                else:
                    tvl = []
                tn = 1 if tn == 0 else tn
                # VALS
                tmp = lines.pop(0).split()
                #
                vals = read_values(lines, 2*tn*en*cn*mn*sn*un*dn*fn, float)

                val2 = zip(vals[0::2], vals[1::2])
                # TFC
                tfcl = lines.pop(0).split()
                ntfc = int(tfcl[1])
                jtf = map(int, tfcl[2:])
                tfc = read_values(lines, ntfc*4, float)

                # put all into an object
                tll.name = m
                tll.ptyp = i
                tll.ttyp = j
                tll.fc = fc
                tll.fn = fn
                tll.fnl = fnl
                tll.dn = dn
                tll.ufl = ufl
                tll.un = un
                tll.sfl = sfl
                tll.sn = sn
                tll.mfl = mfl
                tll.mn = mn
                tll.cfl = cfl
                tll.cf = cf
                tll.cn = cn
                tll.cvl = cvl
                tll.en = en
                tll.ef = ef
                tll.efl = efl
                tll.evl = evl
                tll.tf = tf
                tll.tn = tn
                tll.tfl = tfl
                tll.tvl = tvl
                tll.vals = val2
                tll.tfc = tfc
                if numpy_exists:
                    nv = numpy.array(vals)
                    Ivals = [2, tn, en, cn, mn, sn, un, dn, fn]
                    Inams = 'v t e c m s u d f'.split()
                    Ivn = []
                    Inn = []
                    for Iv, In in zip(Ivals, Inams):
                        if Iv > 1:
                            Ivn.append(Iv)
                            Inn.append(In)
                    nv = nv.reshape(Ivn, order='F')
                    tll.vals_numpy = nv
                    tll.vals_numpy_order = ' '.join(Inn)
                    tll.fnl_numpy = numpy.array(fnl)
                tallies[tll.name] = tll

            self.mctaltallies = tallies




if __name__ == '__main__':
    # test read_complete for mcnp6 mesh tallies of type B
    m = Mctal()
    m.read_complete('c_m')

    exit()

    f = open('test.txt', 'r')
    l = f.readlines()
    f.seek(0)
    for o in [f, l, f]:
        print read_values(o, 2, int)
        print read_values(o, 5, int)

    
    # m = Mctal()
    # m.read('mctal')
    # print m.final() 

