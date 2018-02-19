
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

try:
    from uncertainties import Variable
    _uncertainties_package = True
except ImportError:
    _uncertainties_package = False

from ..core.trageom import Vector3
from . import formatter
from .auxiliary import Counter, Collection
from .mctal import str2float

class MeshTally(object):
    """Representation of mesh tally.

    Object-oriented representation of mesh tally data needed for MCNP input
    file, as implemented in MCNP 5.  On the same time, an instance of this
    class is a container for the mesh tally results. 

    WARNING: Currently there is no protection from inconsistency between the
    array of results and tally specification.

    Differences from the MCNP manual: 
    
        * there are default values for the coarse meshes coordinates.

        * there is other than flux tally type: one can specify also tally types 6
          and 7. They are represented in the MCNP input file by specifying tally multiplyer cards.


    >>> mt = MeshTally()
    >>> print mt
    fmesh{0:<}:n $ 
         geom=xyz
         origin=0.0 0.0 0.0
         imesh= 1.0
         jmesh= 1.0
         kmesh= 1.0

    """
    PRECISION = 9

    def __init__(self):
        self.__geo = 'xyz'
        self.__ori = Vector3((0,0,0))
        self.__axs = Vector3((0,0,1))
        self.__vec = Vector3((1,0,0))
        self.__ime = [1.]
        self.__iin = [1]
        self.__jme = [1.]
        self.__jin = [1]
        self.__kme = [1.]
        self.__kin = [1]
        self.__eme = [0]
        self.__ein = [1]
        self.__fac = 1.
        self.__out = 'col'
        self.__tr = None
        self.__cmt = ''   # comment to be printed after the first line of the mesh tally card.
        self.__par = 'n'  # tallying particles
        self.__typ = 4    # tally type
        self.__fmt = None # tally multiplier
        self.__val = []   # place for result values.
        self.__err = []   # place for result rel.errors
        return

    @property
    def geom(self):
        """
        Mesh geometry, either cartesian ('xyz' or 'rec') or cylindrical ('rzt' or 'cyl').
        """
        return self.__geo

    @geom.setter
    def geom(self, value):
        clst = ['xyz', 'rec']
        rlst = ['cyl', 'rzt']
        v = str(value).lower()
        if v in clst:
            self.__geo = clst[0]
        elif v in rlst:
            self.__geo = rlst[0]
        else:
            raise ValueError('Unknown geometry type ', value)
        return

    @property
    def origin(self):
        """
        Coordinates of the origin.
        """
        return self.__ori

    @origin.setter
    def origin(self, value):
        self.__ori = Vector3(value)
        return

    @property
    def axs(self):
        """
        Vector giving the direction of the axis of the cylindrical mesh.

        When it is set, the geometry type of the mesh tally is changed to
        cylindrical, automatically.

        This property is an instance of the mcnp.core.trageom.Vector3() class.
        The setter method accepts also a tuple of coordinates that are passed
        to the Vector3() class constructor.
        
        """ 
        return self.__axs

    @axs.setter
    def axs(self, value):
        self.__axs = Vector3(value)
        self.geom = 'cyl'
        return

    @property
    def vec(self):
        """
        Vector defining, along with axs, the plane for theta=0.

        When set, the geometry type is changed to cylindrical, automatically.

        This property is an instance of the mcnp.core.trageom.Vector3() class.
        See also description of axs property. 

        """
        return self.__vec

    @vec.setter
    def vec(self, value):
        self.__vec = Vector3(value)
        self.geom = 'cyl'
        return

    @property
    def imesh(self):
        """
        A list with locations of the coarse meshes in the x direction or in the r direction.

        """
        return self.__ime

    @property
    def jmesh(self):
        """
        A list with locations of the coarse meshes in the y direction or in the z direction.

        """
        return self.__jme

    @property
    def kmesh(self):
        """
        A list with locations of the coarse meshes in the z direction or in the theta direction.

        """
        return self.__kme

    @property
    def iints(self):
        """
        Number of fine meshes within corresponding coarse meshes of imesh.
        """
        return self.__iin

    @property
    def jints(self):
        """
        Number of fine meshes within corresponding coarse meshes of jmesh.
        """
        return self.__jin

    @property
    def kints(self):
        """
        Number of fine meshes within corresponding coarse meshes of kmesh.
        """
        return self.__kin

    @property
    def out(self):
        """
        The output format. Can be 'col', 'cf', 'ij', 'ik' or 'jk'.

        Note that currently only 'col' and 'cf' formats can be read by the
        read_meshtal function. 
        """
        self.__out

    @out.setter
    def out(self, value):
        v = str(value).lower()
        if v in ['col', 'cf', 'ij', 'ik', 'jk']:
            self.__out = v
        else:
            raise ValueError('Unsupported value for output format ', value)
        return

    @property
    def emesh(self):
        """
        A list with values of the coarse meshes in energy, in MeV

        Example::

            emesh 5 20
            eints 5 3

        creates five 1-MeV bins (0,1), (1,2), (2,3), (3,4) and (4,5), and
        three 5-MeV bins (5,10), (10, 15) and (15, 20).
        """
        return self.__eme

    @property
    def eints(self):
        """
        List with numbers of fine meshes within the corresponding coarse meshes in energy.

        See `emesh` property.
        """
        return self.__ein

    @property
    def cmt(self):
        """
        Comment to be printed at the end of the first line of the mesh tally card.
        """
        return self.__cmt

    @cmt.setter
    def cmt(self, value):
        self.__cmt = str(value)
        return

    @property
    def par(self):
        """
        Tallying particles. Can be 'n', 'p' or 'np'
        """
        return self.__par

    @par.setter
    def par(self, value):
        v = str(value).lower()
        if v in ['n', 'p', 'np', 'pn']:
            self.__par = v
        else:
            raise ValueError('Unknown particle type ', value)
        return

    @property
    def ttype(self):
        """
        Tally type. Can be 4 (default), 6 or 7.
        """
        return self.__typ

    @ttype.setter
    def ttype(self, value):
        v = int(value)
        if v == 4:
            # remove multiplier, if any
            self.__fmt = None
            self.__typ = 4
        elif v == 6:
            # energy deposition over the mesh
            self.__typ = 6
            self.__fmt = 'fm{0:<} -1 0 1 -4' # average heating numbers (MeV/collision)
        elif v == 7:
            # fission energy. 
            self.__par = 'n'
            self.__typ = 7
            self.__fmt = 'fm{0:<} -1 0 -6 -8' # Sf * Qfiss
        return

    @property
    def values(self):
        """
        Returns list of (value, err) tuples, in the same order as in the
        meshtal file with 'col' format.

        Returns [] by default.
        """
        return self.__val

    @property
    def errors(self):
        """
        Returns list of errors, in the same order as values attribute.
        """
        return self.__err

    def items(self):
        """
        Returns list of ((E, x, y, z), (val, err)) tuples. The order is the same as in the meshtal file with 'col' format.
        """
        return NotImplemented

    def value(self, **kwargs):
        """
        Returns (value, err) pair specified by the arguments. Acceptable
        arguments are x, y, z, r, t (for theta) and E.

        The mesh element is defined from specified coordinates and the
        correspondent tally result is returned. If E is given, the result from
        the correspondent energy bin is returned, if E is not specified, the
        total value is returned.
        """
        return NotImplemented

    def card(self, formatted=True):
        """
        Returns a multi-line string with the mesh tally card for MCNP input.

        If optional argument formatted set to True (default), the
        returned string can contain additional new-line characters,
        so that lines fit to the 80-charachters limit imposed by
        the MCNP input file syntax.
        """
        space1 = ' '*5
        res = ['fmesh{0}:{1} $ {2}'.format('{0:<}', self.__par, self.__cmt)]
        res.append(space1 + 'geom={0}'.format(self.__geo))
        res.append(space1 + 'origin={0} {1} {2}'.format(*self.__ori.car))
        if self.__geo == 'cyl':
            res.append(space1 + 'axs={0} {1} {2}'.format(*self.__axs.car))
            res.append(space1 + 'vec={0} {1} {2}'.format(*self.__vec.car))
        for n in ['imesh', 'jmesh', 'kmesh']:
            res.append(space1 + n + '=')
            for v in getattr(self, n):
                res[-1] += ' {0}'.format(round(v, self.PRECISION))
        for n in ['iints', 'jints', 'kints']:
            lst = getattr(self, n)
            if lst != [1]:
                res.append(space1 + n + '=')
                for v in lst:
                    res[-1] += ' {0}'.format(v)
        if self.__eme != [0]:
            res.append(space1 + 'emesh=')
            for v in self.__eme:
                res[-1] += ' {0}'.format(v)
        if self.__ein != [1]:
            res.append(space1 + 'eints=')
            for v in self.__ein:
                res[-1] += ' {0}'.format(v)
        if self.__fmt is not None:
            res.append(self.__fmt)
        res = '\n'.join(res)
        if formatted:
            res = formatter.format_card(res) #### multiline(res)
        return res

    def __eq__(self, othr):
        return ( self.__geo == othr.__geo and
                 self.__ori == othr.__ori and
                 self.__axs == othr.__axs and
                 self.__vec == othr.__vec and
                 self.__ime == othr.__ime and
                 self.__iin == othr.__iin and
                 self.__jme == othr.__jme and
                 self.__jin == othr.__jin and
                 self.__kme == othr.__kme and
                 self.__kin == othr.__kin and
                 self.__eme == othr.__eme and
                 self.__ein == othr.__ein and
                 self.__fac == othr.__fac and
                 self.__out == othr.__out and
                 self.__tr  == othr.__tr  and
                 self.__cmt == othr.__cmt and
                 self.__par == othr.__par and
                 self.__typ == othr.__typ and
                 self.__fmt == othr.__fmt)

    def __str__(self):
        return self.card(True)


def read_meshtal(fname, use_uncertainties=True):
    """Reads meshtal file.
    
    Meshtal file to read is given by its name in the argument fname. Optional
    argument use_uncertainties specifies whether to use the Uncertainties
    package to store statistical error.

    Returns a tuple (t, n, r), where:
    
        t: problem title
        n: number of histories,
        r: dictionary with results.

    >>> t, n, r = read_meshtal('meshtal')
    >>> print t        # title
    >>> print n        # number of histories
    >>> print r.keys() # dictionary with results.
    >>> for (n, mt) in r.items():
    ...     print n
    ...     print mt.values

    """
    Noh = 0
    res = {}
    tit = [] # title
    data_block = False          # flag to specify if results (True) or tally specs (False) are read
    for l in open(fname, 'r'):
        if len(tit) < 2:
            # first two lines go to the tit list.
            tit.append(l)
        elif not data_block:
            # this is tally specifications block
            if Noh == 0 and ' Number of histories' == l[0:20]:
                Noh = str2float(l.split()[-1])  # in meshtal number of histories is written with two zeroes after the decimal point
            if l == '\n':
                pass
            if ' Mesh Tally Number' == l[0:18]:
                tid = int(l.split()[-1])
                mt = MeshTally()
                res[tid] = mt
            if '  Cylinder origin at' == l[0:20]:
                mt.geom = 'cyl'
                ll = l.split()
                mt.origin = ( ll[3], ll[4], ll[5][:-1] ) # the last entry followed by comma
                mt.axs = tuple( ll[8:11] )
            if '    X direction:' == l[0:16]:
                mt.imesh.pop(0) # when initialized, it is set to [1.]
                for ll in l.split()[2:]:
                    mt.imesh.append(str2float(ll))
                mt.origin.x = mt.imesh.pop(0)
            if '    Y direction:' == l[0:16]:
                mt.jmesh.pop(0) # when initialized, it is set to [1.]
                for ll in l.split()[2:]:
                    mt.jmesh.append(str2float(ll))
                mt.origin.y = mt.jmesh.pop(0)
            if '    Z direction:' == l[0:16]:
                if mt.geom == 'xyz':
                    mt.kmesh.pop(0) # when initialized, it is set to [1.]
                    for ll in l.split()[2:]:
                        mt.kmesh.append(str2float(ll))
                    mt.origin.z = mt.kmesh.pop(0)
                elif mt.geom == 'cyl':
                    for ll in l.split()[2:]:
                        mt.jmesh.append(str2float(ll))
                else:
                    raise ValueError('Cannot read Z direction boundaries for geometry type ', mt.geom)

            if '    R direction:' == l[0:16]:
                for ll in l.split()[2:]:
                    mt.imesh.append(str2float(ll))
            if '    Theta direction:' == l[0:20]:
                for ll in l.split()[3:]:
                    mt.kmesh.append(str2float(ll))
            if '    Energy bin bound' == l[0:20]:
                lll = l.split()
                if lll[-2:] == ['0.00E+00', '1.00E+36']:
                    # this is default.
                    pass
                else:
                    for ll in lll[3:]:
                        mt.emesh.append(str2float(ll))
            if 'Result     Rel Error' in l:
                # this is the head line for the table with results.
                data_block = True
                # define the column indices containing Result and Error:
                l = l.replace('Rel Error', 'Err')    # ensure that number of tokens after split() is equal to the number of data columns
                l = l.replace('Rslt * Vol', 'RxV')
                columns = l.split()
                iv = columns.index('Result')
                ir = columns.index('Err')
        else:
            # reading the table with tally results.
            if l == '\n':
                # this is the end of table with results.
                data_block = False
            else:
                l = l.replace('Total', '-1') # "Total" appears when emesh is used
                ll = l.split()
                v = str2float(ll[iv])
                r = str2float(ll[ir])
                # Variable requires std_dev of the variable. In MCNP, r is a
                # relative error, r = S/v, where S is the estimated standard
                # deviation.
                if use_uncertainties and _uncertainties_package:
                    value = Variable(v, r*v)
                else:
                    # value = (v, r)
                    value = v
                mt.values.append(value)
                mt.errors.append(r)
    return tit[-1], Noh, res



class TallyCollection(Collection):
    """Collection of tallies.

    Adding a tally instance to the collection provides for this tally a
    unique number. The last digit of the number is defined by the tally type,
    the other -- are 10x multiples of the added tally.

    """
    def __init__(self):
        super(TallyCollection, self).__init__()
        self.__use_uncert = False

    def index(self, tally):
        """Returns index of tally in the collection.

        If tally is allready in the collection, its index is returned. If tally
        is not in the collection, it is added to the collecion under a unique index, 
        that can be used as tally number in the MCNP input file.

        """

        if isinstance(tally, int):
            if tally in self.keys():
                return tally
            else:
                raise IndexError('Collection has no element with index ', tally)
        elif isinstance(tally, MeshTally):
            i = self._find(tally)
            if i is None:
                i = self._add(tally, lambda x: 10*x + 4)
            return i
        else:
            raise TypeError('Cannot add tally of type ', tally.__class__.__name__)

    def add(self, tally):
        self.index(tally)
        print "WARNING: use of TallyCollection.add() method is deprecated. Use index() method instead."
        return

    def cards(self, formatted=True):
        """
        Returns a list of multi-line strings with mesh tally cards for the tallies
        in the collection.
        """
        c = ['c tallies']
        for (ID, t) in self.items():
            c.append(t.card(formatted).format(ID))
        return c

    def __str__(self):
        return '\n'.join(self.cards(True))

    @property
    def use_uncertainties(self):
        """
        Boolean flag. If True, the uncertainties package is used to 
        handle statistical errors.

        This can result in memory runout.
        """
        return self.__use_uncert

    @use_uncertainties.setter
    def use_uncertainties(self, value):
        self.__use_uncert = value

    def read(self, meshtal='meshtal', mctal=None):
        """
        Reads meshtal and mctal and loads data to correspondent tally instances.
        """
        if meshtal is not None:
            title, noh, d = read_meshtal(meshtal, self.__use_uncert)
            # if meshtal was read, remove previous entries.

            for nt in list( set(d.keys()) & set(self.keys())):
                # clear old meshtally data
                while len(self[nt].values) > 0:
                    self[nt].values.pop()
                for r in d[nt].values:
                    # self[nt].values.append((str2float(r[0]), str2float(r[1])))
                    self[nt].values.append(r)
        if mctal is not None:
            raise NotImplemented('reding of mctal file not implemented yet')
        return 


