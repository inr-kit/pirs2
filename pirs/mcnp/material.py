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

Classes to describe MCNP material composition and a collection of materials in
MCNP.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import autologging

from ..core import tramat
from . import xsdir as xsdir_module
# from .auxiliary import xs_interpolation as xs_int
# from .auxiliary import Counter, Collection
from . import auxiliary
from . import formatter


@autologging.traced
class Material(tramat.Mixture):
    """
    Object-oriented representation of material composition for MCNP.

    Constructor arguments are passed to the constructor of the parent class, see
    description of available arguments there.

    One can setup material composition, temperature and specify xsdir file,
    which is used to find cross-section data suffixes.

    """
    def __new__(cls, *args, **kwargs):
        r = super(Material, cls).__new__(cls, *args, **kwargs)
        return r

    def __init__(self, *args, **kwargs):
        super(Material, self).__init__(*args, **kwargs)
        self.__sdict = {}
        self.__xsdir = None  # xsdir_module.XSDIRFILE
        self.__t = 300.
        self.__Tif = auxiliary.xs_interpolation.sqrT
        self.__fmt = {}
        self.__fmt['zaid'] = '{0}'
        self.__fmt['fraction'] = '{0:12.5e}'
        self.__th = None  # thermal data name.

    def copy(self):
        new = super(Material, self).copy()
        new.__sdict.update(self.__sdict)
        new.__xsdir = self.__xsdir
        new.__t = self.__t
        new.__Tif = self.__Tif
        new.__fmt = self.__fmt
        new.__th = self.__th
        return new

    @classmethod
    def read_from_input(cls, fname):
        """
        Return a dictionary of mixtures defined by material cards `n` in the
        input file `fname`.
        """
        from numjuggler.parser import get_cards, CID
        # All data cards from fname:
        cards = filter(lambda c: c.ctype == CID.data, get_cards(fname))
        # All material cards from fname:
        for c in cards:
            c.get_values()
        cards = filter(lambda c: c.dtype == 'Mn', cards)

        dm = {}
        for c in cards:
            m = cls.parseCard(c)
            m.name = 'M{} from {}'.format(c.name, fname)
            m.T = None
            dm[c.name] = m
        return dm

    @classmethod
    def parseCard(cls, card):
        """
        Returns a new instance of Material class representing the card -- as
        given by numjuggler's card.input after applying get_values() method.
        """
        # Original code taken from to5/set4/read_clite
        tokens = ' '.join(card.input).replace('=', ' ').lower().split()
        # pop name
        tokens.pop(0)
        it = iter(tokens)
        recipe = []
        for zaid in it:
            if 'nlib' in zaid:
                # skip next entry
                it.next()
                continue
            fr = float(it.next())  # fraction always follow zaid.
            if fr >= 0:
                unit = 'moles'
            else:
                unit = 'grams'

            if '.' in zaid:
                zaid, _ = zaid.split('.')
            recipe.extend([int(zaid), (abs(fr), unit)])
        mat = cls(*recipe)
        mat.name = card.values[0][0]
        return mat

    @property
    def thermal(self):
        """Part of the cross-section data set name for thermal scattering.

        When this property is given, the string representing material in the
        MCNP input file, contains additionaly to ``m`` card also ``mt`` card.
        The xsdir file is searched for thermal data with names containing
        `thermal` as a substring. If several data sets are found, the one with
        the closest temperature is chosen.

        """
        return self.__th

    @thermal.setter
    def thermal(self, value):
        v = str(value)
        self.__th = v
        return

    @property
    def xsdir(self):
        """
        Instance of Xsdir() class.

        Suffices to represent material in the MCNP input are defined based on
        the content of this xsdir file and value of attribute T.

        This property can be set to a string, in which case this string should
        represent path to existing xsdir file, or to an instance of the Xsdir()
        class.
        """
        if self.__xsdir is None:
            self.__xsdir = xsdir_module.Xsdir.default()
        return self.__xsdir

    @xsdir.setter
    def xsdir(self, value):
        if isinstance(value, str):
            self.__xsdir = xsdir_module.Xsdir(value)
        elif isinstance(value, xsdir_module.Xsdir):
            self.__xsdir = value
        else:
            raise TypeError('Wrong type of xsdir: ' + value.__class__.__name__)

    @property
    def T(self):
        """Temperature of material, K

        Material temperature is used to find proper suffix (or the pair of
        suffices) in xsdir file.

        It is also used to find the most close thermal data, if the
        `self.thermal` attribute is specified.

        """
        return self.__t

    @T.setter
    def T(self, value):
        # self.__t = float(value) # cannot be used if value is of uncertainties.Variable class
        self.__t = value

    @property
    def Tif(self):
        """Tempareture interpolating function.

        A function that takes as arguments temperatures T, T1 and T2, and
        returns fractions f1 and f2 of cross-sections evaluated at temperatures
        T1 and T2 used to represent a material at temperature T.  It must have
        the following signature::

            f1, f2 = func(T, T1, T2)

        This function is used when the temperature of material is set to a
        value than cannot be found in the xsdir file. In this case, each
        isotope of the material at temperature T is represented as a mixture of
        two, at temperatures T1 and T2. The temperatures T1 and T2 are found in
        xsdir automatically, being the closest to T from below and above.


        Note that values T1 and T2 are usually defined from the xsdir file,
        where temperature is given originally in MeV (as kT), and the material
        temperature T is given in Kelvin. Thus, even if one specifies T as "a
        temperature from xsdir", it will not much T1 or T2 exactly. To avoid
        unnecessary cross-section data in the material specification, the user
        is responsible to provide the logic inside func to set f1 or f2 exactly
        to 1.0 or to 0.0 even if T does not match exactly, but is close to T1 or
        T2.

        Cross sections at temperature T1 and T2 appear in the material
        specification only if the correspondent fraction, f1 or f2, is nonzero.

        By default, the `auxiliary.xs_interpolation.sqrT()` function is used,
        which describes the sqrt(T) interpolation.
        """
        return self.__Tif

    @Tif.setter
    def Tif(self, value):
        # first try
        f1, f2 = value(350, 300, 400)
        # and than set
        self.__Tif = value

    @property
    def fmt(self):
        """Dictionary of format strings used to generate card representation of the material.

        The following keys have sense:

        'zaid': format string for ZAIDs
        'fraction': format string for fraction.

        If explicit field index is used (for Python versions < 2.6), it should be set to 0.
        """
        return self.__fmt


    def card(self, formatted=True, suffixes=True, smin=None, smax=None, comments=True, sort=False):
        """Returns a multi-line string with the material cards for MCNP input.

        The returned string generally represents two cards, m and mt.

        The `formatted` optional argument defines if the lines in the string
        are wrapped to fit to 80 characters.

        The `suffixes` optional argument defines if suffixes for particular
        cross-section sets are printed or not.

        Optional parameters smin and smax can take integer values. If they are
        specified, only cross-sections with suffix numbers satisfying smin <=
        XX <= smax are returned.

        The material number is NOT defined explicitly, there is just a
        placeholder for it. Use the format() method of the returned string to
        put particular material ID:

        >>> m = Material(1001)
        >>> print m.card().format(1)   # put 1 as material number
        m1 $ mixture  H-001 at 300.0 K
               1001.31c 1.0000000e+00

        """
        space1 = ' '*5
        space2 = ' '*3
        matID = '{0:<}'  # placeholder for material ID
        res = ['m{0:<} $ {1} '.format(matID, self.name, self.__t)]
        if suffixes:
            res[0] += 'at {0} K '.format(self.__t)

        # append density and concentration, if they are set:
        if self.conc is not None:
            res.append('c density {0:20.14e} g/cc, '
                       '{1:20.14e} 1/cm-barn'.format(self.dens, self.conc*1e-24))

        # Temperature
        if suffixes:
            Txsdir = self.__t
        else:
            Txsdir = None

        # format strings
        zfmt = self.__fmt['zaid']      # for zaid
        sfmt = '.{0}'                  # for suffix
        ffmt = self.__fmt['fraction']  # for fraction
        try:
            if suffixes:
                me = self._expanded()
            else:
                me = self.expanded()
        except ValueError:
            res.append('c ERROR: cannot define nuclide cmposition')
            return '\n'.join(res)

        itre = me.recipe()
        for n in itre:
            a = itre.next()
            zaid = n.ZAID
            av = a.v
            # amount of a can be of the uncertainties.Variable class. Use its
            # nominal value:
            if hasattr(av, 'nominal_value'):
                av = av.nominal_value
            elif isinstance(av, tuple) and len(av) == 2:
                av = av[0]

            if suffixes:
                TS1, TS2 = self.xsdir.suffix(zaid, Txsdir, smin=smin, smax=smax)
                if self.__t is None:
                    f1 = 1.0
                    f2 = 0.0
                else:
                    f1, f2 = self.__Tif(self.__t, TS1[0], TS2[0])
                try:
                    f1 = f1.nominal_value
                    f2 = f2.nominal_value
                except AttributeError:
                    pass
            else:
                f1, f2 = 1., 0.

            szd = zfmt.format(zaid)
            sf1 = ' ' + ffmt.format(av*f1) # space to ensure that fraction is separated from previous entry
            sf2 = ' ' + ffmt.format(av*f2)
            if suffixes:
                ss1 = sfmt.format(TS1[1])
                ss2 = sfmt.format(TS2[1])
            else:
                ss1, ss2 = '', ''
            if f1:
                line = space1 + szd + ss1 + sf1 + space2
            else:
                line = space1
            if f2:
                line += szd + ss2 + sf2
            if av != 0:
                res.append(line)
        # append comment with temperatures and fractions
        if suffixes and f1 and f2:
           res[0] += ' as mix {0:.3G} {1:.2f} K,  {2:.3G} {3:.2f} K'.format(f1, TS1[0], f2, TS2[0])
        # sort:
        if sort:
            res = [res[0]] + sorted(res[1:])
        # append mt card, if necessary:
        if self.__th is not None:
            thname, T = self.xsdir.find_thermal(self.__th, self.T)
            res.append('mt{0:<} {1} $ thermal data at {2:.3f}K'.format(matID, thname, T))
        # format if necessary:
        res = '\n'.join(res)
        if formatted:
            return formatter.format_card(res, propagate_comments=comments) #### multiline(res)
        else:
            return res

    def _expanded(self, Nr=0):
        """Returns new instance of the Material() class, with all ingredients expanded to nuclides.

        Like expanded() method, but checks the presence of nuclides in xsdir
        and, if necessary, replaces them according to the sdict attribute.

        """
        Nrmax = 3
        nrec = []
        again = False
        itre = self.expanded().recipe() # iterator
        for n in itre: # (n, a) in self.expanded().recipe():
            a = itre.next()
            #print '_expanded: nuclide ', n.ZAID,
            try:
                ts1, ts2 = self.xsdir.suffix(n.ZAID, None)
                nnew = n
                #print ' found with suffixes ', ts1, ts2
            except ValueError:
                # nuclide n not in xsdir.
                if Nr > Nrmax:
                    raise ValueError('Nuclide {0} not found in xsdir'.format(n.ZAID))
                else:
                    nnew = self.__sdict[n.ZAID]
                    #print ' not found. Replaced with {}'.format(nnew)
                    again = True
            # nrec.append((nnew, a))
            nrec.extend([nnew, a])
        nmat = self.__class__(*nrec)
        if not again:
            return nmat
        else:
            nmat.__sdict.update(self.__sdict)
            return nmat._expanded(Nr=Nr+1)



    @property
    def sdict(self):
        """Substitution dictionary.

        A dictionary of the form {ZA1:za1, ZA2:za2, ...}, where
        ZAi and zai are integer numbers representing ZAIDs.

        If a nuclide with ZAID ZAi is not found in xsdir, it is substituted
        with cross-sections for nuclide zai.

        By default, there is no substitutions, the dictionary
        is empty.

        """
        return self.__sdict

    def __eq__(self, othr):
        """
        Redefinition of the tramat.Mixture.__eq__ method!
        """
        if self is othr: return True

        if isinstance(othr, Material):
            return ( self.recipe() == othr.recipe() and
                     self.__t == othr.__t and
                     self.__xsdir == othr.__xsdir and
                     self.__Tif == othr.__Tif and
                     self.name == othr.name and
                     self.__sdict == self.__sdict)
        else:
            return False


class MaterialCollection(auxiliary.Collection):
    """Collection of materials with common xsdir.

    Elementes of this collection are instances of the Material class augmented
    with a set of keyword arguments specifying additional attributes for this
    material.

    Giving attribute values separated from the material allows to use the same
    material instance to describe different temperatures, for example.

    One can pass an integer to the index() method. If the collection
    already contains a material with this index, its is just returned.
    Otherwise, an index error is raised. Index 0 is always in the collection.

    """
    def __init__(self, xsdir=None, *args):
        super(MaterialCollection, self).__init__(*args)
        # if xsdir is None:
        #     self.__xs = xsdir_module.Xsdir(xsdir_module.XSDIRFILE)
        # else:
        #     self.xsdir = xsdir
        self.__xs = xsdir
        return

    @property
    def xsdir(self):
        if self.__xs is None:
            # use default xsdir
            self.__xs = xsdir_module.Xsdir.default()
        return self.__xs

    @xsdir.setter
    def xsdir(self, value):
        if isinstance(value, str):
            self.__xs = xsdir_module.Xsdir(value)
        elif isinstance(value, xsdir_module.Xsdir):
            self.__awr = value.awr
            self.__dir = value.dir
            self.__pth = value.datapath + value.filename
        else:
            raise TypeError('Cannot set xsdir to ', value.__class__.__name__)


    def add(self, mat, **kwargs):
        self.index(mat, **kwargs)
        print 'WARNING: use of Material.Collection.add() method deprecated. Use index() instead.'
        return

    def index(self, mat, **kwargs):
        """Returns index of material mat.

        Argument `mat` can be an instance of the Material() class, or an integer.

        When `mat` is an instance of the Material() class:

            If mat not yet in the collecion, it is added. Optional arguments specify material
            attributes to be changed, when material `mat` is processed. In this way, materials
            that differ only by temperature, can be represented with the same instance of the Material()
            class.

        When `mat` is an integer:

            If a material with this index allready exists, this index is returned. If there is no
            element with this index, the IndexError is raised.



        """
        if isinstance(mat, int):
            if mat in self.keys() + [0]:
                return mat
            else:
                raise IndexError('Collection has no element with index ', mat)
        elif isinstance(mat, Material):
            # obj = (mat, kwargs)
            obj = (kwargs, mat)
        elif isinstance(mat, tuple):
            obj = (mat[1], mat[0])
        else:
            raise TypeError('Cannot add material of type ', mat.__class__.__name__)
        k = self._find(obj)
        if k is None:
            k = self._add(obj)
        return k

    def __getitem__(self, index):
        kwargs, mat = super(MaterialCollection, self).__getitem__(index)
        return (mat, kwargs)

    def items(self):
        for ID, (kwargs, mat) in super(MaterialCollection, self).items():
            yield ID, (mat, kwargs)

    def cards(self, formatted=True):
        """
        Returns a list of multi-line strings with material cards.

        If the optional argument formatted is True (default),
        the strings in the list are wrapped to fit to
        80 characters of the MCNP input line maximal length.

        """
        c = ['c materials']
        for (ID, (mat, kwargs)) in self.items():
            aold = {}
            for (n,v) in kwargs.items() + [('xsdir', self.__xs)]:
                aold[n] = getattr(mat, n)
                setattr(mat, n, v)
            c.append( mat.card(formatted).format(ID) )
            # return old attribute values
            for (n,v) in aold.items():
                setattr(mat, n, v)
        return c

    def __str__(self):
        return '\n'.join( self.cards(True) )


