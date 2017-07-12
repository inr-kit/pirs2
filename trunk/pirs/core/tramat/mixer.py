"""
Definition of the Nuclide and Mixture classes.
"""

# at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
# at

from .data_masses import xsdir1 as AWR_SET
from .data_names import name as _chemical_names
# from .data_names import charge as _chemical_names_rev
from .data_names import zai, ZAID2ZAI, str2ZAI, ZAI2ZAID
from .natural import formula_to_tuple

from . import natural


AMU_AWR = 1.008664967  #: Conversion factor from AMU to AWR, amu/awr
NAVOGAD = 6.02214129e23  #: Avogadro number, 1/mol
G_AMU = 1.660538921e-24  #: Conversion factor gram to amu, g/amu
G_MOL_AWR = AMU_AWR * G_AMU * NAVOGAD  # Conversion factor g/mol/awr

_nMix = 0


class Nuclide(object):
    """
    Representation of a nuclide. A nuclide is defined by its mass and charge
    numbers, A and Z, isomeric state I, and by its molar mass M.

    The A, Z and I properties of a nuclide instance can be changed. The nuclide
    mass, represented by the property M, cannot be changed.

    The constructor argument ID specifies Z, A and I and can be given in
    several forms:

        * a tuple (Z, A, I),
        * a string of the form 'cc-AAA[m[I]]', for example, 'Pu-241', 'O-16',
          'Te-129m'
        * an integer of the form ZZAAA.
        * another instance of Nuclide class; in this case, the copy of
          ID is created.

    If M is not specified, values derived from xsdir file will be used (the
    xsdir file is not read. Mass is actually taken from the data_masses
    module, where nuclide masses in awr units are stored. These values are
    originally taken from an xsdir file).

    The class supports some arithmetical operations:

        * An instance of the Nuclide class can be multiplied by a scalar c.
          The result is an instance of the Mixture class meaning c moles of
          the nuclide.

        * Two Nuclide instances can be added, n1 + n2. This creates a Mixture
          representing one mole of n1 mixed with one mole of n2.
    """

    # Set of default awr masses
    AWR_SET = AWR_SET

    def __init__(self, ID, M=None):
        if isinstance(ID, self.__class__):
            self.__a = ID.__a
            self.__z = ID.__z
            self.__i = ID.__i
            self.__m = ID.__m
        else:
            z, a, I = zai(ID)
            self.__a = a
            self.__z = z
            self.__i = I

        if M is None:
            self.__m = None
        else:
            self.__m = float(M)

        # For consistency with Mixture:
        self.__c = None

    @property
    def conc(self):
        """
        Rear-only property, returning None.

        Introduced for consistency with the Mixture class
        """
        return self.__c


    @property
    def ZAID(self):
        """
        ZAID (integer) of the nuclide. Can be set to any integer of the form
        AAZZZ.

        Support for isomeric states.

        """
        return ZAI2ZAID(self.__z, self.__a, self.__i)

    @ZAID.setter
    def ZAID(self, value):
        z, a, i = ZAID2ZAI(value)
        self.__z = z
        self.__a = a
        self.__i = i

    @property
    def A(self):
        """
        Mass number A of the nuclide (integer). Can be set.

        >>> n1 = Nuclide('H-1')
        >>> n1.A = 5
        >>> n1.ZAID
        1005
        """
        return self.__a

    @A.setter
    def A(self, value):
        self.__a = int(value)

    @property
    def Z(self):
        """
        Charge number, Z, of the nuclide. Can be set.

        >>> n1 = Nuclide('O-16')
        >>> n1.Z = n1.Z/2
        >>> n1.name
        'Be-016'
        """
        return self.__z

    @Z.setter
    def Z(self, value):
        self.__z = int(value)

    @property
    def name(self):
        """
        The name (string) of the nuclide in the form 'Cc-AAA[m[I]]'. For
        example, 'Pu-241'.

        Can be set. in this case, attributes A, Z and I wil be changed
        accordingly.

        """
        res = '{0:2s}-{1:03d}'.format(_chemical_names[self.__z], self.__a)
        if self.__i == 1:
            res += 'm'
        elif self.__i > 1:
            res += 'm{}'.format(self.__i)
        return res

    @name.setter
    def name(self, value):
        # check name format and extract ZAID from there.  See definition of
        # the name property above.  it can be generalized to the
        # following: %s-%i. Note that _chemical_names have spaces in the
        # element names, if the element is named only with one letter.
        z, a, i = str2ZAI(value)
        self.__z = z
        self.__a = a
        self.__i = i
        return

    @property
    def I(self):
        """Nuclide isomeric state.
        """
        return self.__i

    @I.setter
    def I(self, value):
        self.__i = int(value)

    # @property Usual method, not a property, for consistency with recipe class.
    # In the Mixture class, the m property cannot be changed, and therefore it
    # is more clear to access this attribute as m(), not as just m.
    def M(self):
        """
        Returns the nuclide molar mass. If the molar mass was not specified at
        the initialization of the instance, the value in AWR will be set
        depending on the nuclide ID:

        >>> n1 = Nuclide(1001, 1.)
        >>> n1.M()
        1.0
        >>> n2 = Nuclide(1001)
        >>> n2.M()
        0.999167
        """
        if self.__m is None:
            self.__m = self.AWR_SET[self.ZAID]
        return self.__m

    def __mul__(self, value):
        try:
            fval = float(value)
        except ValueError:
            return NotImplemented
        return Mixture((self, fval, 1))

    def __rmul__(self, value):
        return self * value

    def __add__(self, othr):
        if isinstance(othr, Nuclide):
            return Mixture((self, 1., 1), (othr, 1., 1))
        else:
            return NotImplemented

    def __str__(self):
        return '<{0:8d} {1:8.4f}>'.format(self.ZAID, self.M())

    def __repr__(self):
        return '<Nuclide({})>'.format(self.ZAID)

    def check_attributes(self, **kwargs):
        """
        Check conditions specified in kwargs in the form ATTR=VAL. Attr can be
        usual attribute or a method. In the latter case, the result returned by
        the method is compared against VAL.  Only methods without arguments can
        be checked.

        >>> n1 = Nuclide(1001)
        >>> n1.check_attributes(A=1, Z=1)
        True
        >>> n1.check_attributes(M=0.999167)
        True
        """
        for (attr, value) in kwargs.items():

            attr = getattr(self, attr)
            if (isinstance(attr, self.check_attributes.__class__) or
               isinstance(attr, self.__class__.__init__.__class__)):
                attr = attr()
            elif isinstance(value, list):
                if attr not in value:
                    return False
            elif isinstance(value, basestring):
                if value not in attr:
                    return False
            else:
                if not attr == value:
                    return False
        return True

    def __eq__(self, othr):
        """
        Two Nuclide instances are equal, if they have equal ZAID and M.
        """
        if isinstance(othr, self.__class__):
            return self.ZAID == othr.ZAID and self.__m == othr.__m
        else:
            return NotImplemented

    def __hash__(self):
        """
        this is to prohibit the usage of nuclide instances as dictionary keys.
        """
        return None

    def isfuel(self):
        """
        Returns True if one of the fissionable isotopes 92235, 94239 or 94241.
        """
        za = self.__z*1000 + self.__a
        return za in (92235, 94239, 94241)


class Amount(object):
    """
    Is a set of two entries: value and its unit. The value must be a float (or
    convertable to float) and the unit can be specified by an integer, or by a
    string:

    All these instences represent "one mole"
    >>> m1 = Amount(1, 'mol')
    >>> m2 = Amount(1, 1)
    >>> m3 = Amount(1, 'm')
    >>> print m1, m2, m3
    1.0 mol 1.0 mol 1.0 mol

    The following are definitions of "two grams":
    >>> g1 = Amount(2, 2)
    >>> g2 = Amount(2, 'g')
    >>> g3 = Amount(2, 'gram')
    >>> print g1, g2, g3
    2.0 g 2.0 g 2.0 g

    One can alse define cubic centimeters. The following instances all represent
    "three cc":
    >>> v1 = Amount(3, 3)
    >>> v2 = Amount(3, 'cc')
    >>> v3 = Amount(3, 'cm3')
    >>> print v1, v2, v3
    3.0 cc 3.0 cc 3.0 cc


    Instances can be multiplied by a scalar and added.

    >>> m1 = Amount(1,1)
    >>> print m1 + m1*5
    6.0 mol
    >>> m2 = Amount(1,2)
    >>> m1 + m2
    Traceback (most recent call last):
       ...
    TypeError: Cannot add different units: mol and g
    >>> m2.t = 1
    >>> for m in (m1, m2, 4*m2 - m1, m2/8, m2/8.):
    ...     print m
    ...
    1.0 mol
    1.0 mol
    3.0 mol
    0.125 mol
    0.125 mol

    """

    # Aliases for unit names:
    type_alias = {
            1: ('m', 'mol', 'mole', 'moles', 1),
            2: ('g', 'gr', 'gram', 'grams', 2),
            3: ('cc', 'cm3', 3)}

    def __init__(self, value=0., unit=1):
        """
        Amount is specified by providing a value and its units.

        Possible argument types are:

        If value is another instance of the Amount class, its copy is created.

        If value is a tuple, its first two elements are considered as the value
        and the unit type name or ID.

        If value can be converted to a float, than its type (units) is taken
        from the unit argument.

        """

        if isinstance(value, self.__class__):
            self.__v = value.__v
            self.__t = value.__t
        elif isinstance(value, tuple):
            self.v = value[0]
            self.t = value[1]
        else:
            # run through setter functions, to check that value and unit are
            # valid
            self.v = value
            self.t = unit

    @property
    def v(self):
        """
        Value of the amount. Can be set to a value, which will be converted to
        float.

        >>> a = Amount(3, 1)    # value is 3, units is 1, which means 'mol'
        >>> a.v = 1
        >>> print a
        1.0 mol
        >>> a.v = 'f'
        Traceback (most recent call last):
            ...
        ValueError: could not convert string to float: f
        """
        return self.__v

    @v.setter
    def v(self, value):
        """Must be convertable to float"""
        self.__v = float(value)

    @property
    def t(self):
        """
        Attribute defining the units of the amount. Can be integer or string.
        """
        return self.__t

    @t.setter
    def t(self, value):
        for tid, tnames in self.type_alias.items():
            if value in tnames:
                self.__t = tid
                break
        else:
            raise ValueError('Unknown unit: ', value)

    def __str__(self):
        return '{0} {1}'.format(self.__v, self.name)

    def __repr__(self):
        return 'Amount({}, {})'.format(self.__v, self.__t)

    @property
    def name(self):
        return self.type_alias[self.__t][0]

    def __mul__(self, value):
        fval = float(value)
        return self.__class__(self.v*fval, self.t)

    def __add__(self, othr):
        if isinstance(othr, self.__class__):
            if othr.t == self.t:
                return self.__class__(self.v + othr.v, self.t)
            else:
                raise TypeError('Cannot add different units: ' +
                                self.name +
                                ' and ' + othr.name)
        else:
            raise TypeError('unsupported operand types: ' +
                            self.__class__.__name__ +
                            ' and ' + othr.__class__.__name__)

    def __rmul__(self, value):
        return self*value

    def __radd__(self, othr):
        return self + othr

    def __neg__(self):
        return self * (-1.)

    def __sub__(self, othr):
        return self + (othr*(-1.))

    def __div__(self, value):
        if isinstance(value, self.__class__) and value.t == self.t:
            return self.v / value.v
        else:
            return self * (1./float(value))

    def __eq__(self, othr):
        """
        Two amounts are equal, if they have equal v and t attributes.
        """
        if isinstance(othr, self.__class__):
            return self.__v == othr.__v and self.__t == othr.__t
        else:
            return NotImplemented


class Mixture(object):
    """Mixture of nuclides or other mixtures.

    A mixture is defined by specifying a recipe -- a sequence of ingredients (a
    nuclide or another mixture) each supplemented with certain amount.

    Since all ingredeints in the recipe have particular amount, the total amount
    of all ingrediants can be computed.  However, if a mixture is defined using
    another, previously defined mixture, the amount of latter is not
    "propagated".

    """
    # Instance counter
    nMix = 0

    # log level. Above 0 means additional log messages.
    logLevel = 0

    @classmethod
    def _print_log(cls, message):
        if cls.logLevel > 0:
            print message

    def __new__(cls, *args, **kwargs):
        """
        New instance is created only if args has more than 1 ingredient and if
        this ingredient is allready of Mixture class.
        """
        # print 'new', args, kwargs
        if len(args) == 1:
            # only one argument.
            arg = args[0]
            if isinstance(arg, cls):
                cls._print_log('new: bypass 1-st argument')
                res = arg
            elif isinstance(arg, tuple):
                cls._print_log('new: expand the 1-st argument')
                res = cls(*arg)
            elif isinstance(arg, int):
                cls._print_log('new: replace int with Nuclide')
                res = cls(Nuclide(arg), (1, 1))
            elif isinstance(arg, Nuclide):
                cls._print_log('new: One nuclide')
                res = cls(arg, (1, 1))
            elif isinstance(arg, basestring):
                cls._print_log('new: replace string with tuple')
                res = cls(*formula_to_tuple(arg, names=kwargs.get('names', {})))
            else:
                raise ValueError('Unsupported type of ingredient, ', type(arg))
        else:
            cls._print_log('new: create new')
            res = super(Mixture, cls).__new__(cls)
            cls.nMix += 1
        return res

    def __initialized(self):
        try:
            self.__m
            self.__a
            self.__c
            self.__name
            return True
        except AttributeError:
            return False

    def __init__(self, *args, **kwargs):
        """
        The constructor takes arbitrary amount of arguments specifying the
        mixture ingredients::

            m = Mixture(arg1, arg2, arg3, ... argN)

        UPD: new method signature is in conform with pirs.Material:

            m = Mixture(mat1, amount1, mat2, amount2, ...)

        Each argument must be a string, an integer or an instance of Nuclide or
        Mixture class, or a tuple of the form ``(MAT, a)`` or ``(MAT, v, t)``,
        where MAT can be an integer, a string or an instance of the Nuclide or
        Mixture class.  The other tuple elements represent the amount: ``a`` is
        an instance of the ``Amount()`` class, ``v``, ``t`` are value and unit
        to define the amount.

        If a mixture used as ingredient in a new mixture has itself only one
        ingredient, this ingredient will be used in the new mixture.

        If the argument is an integer, it is understood as ZAID of a nuclide.
        This argument adds one mole of the nuclide to the recipe.

        If the argument is a string, it is considered as the name of a chemical
        element. This argument defines one mole of the mixture of naturally
        occuring isotopes of this chemical element.

        When the argument is an instance of the ``Nuclide`` or ``Mixture``
        class, it denotes one mole of it.

        When a tuple is given, its first element is understood as described
        above. The second and third elements define amount and unit in which
        the amount is expressed, they both have default values 1. The third
        element is 1 for moles, 2 for grams and 3 for cubic centimeters.

        """

        if self.__initialized():
            # print 'init: already initialized'
            pass
        else:
            self.__class__._print_log('init: initialize self: {} ' +
                                      'args: {} ' +
                                      'kwargs: {}'.format(repr(self),
                                                          args, kwargs))
            # a new instance is returned, setup it.

            # a mixture is stored in two lists, specifying what to mix and how
            # much.
            self.__m = []            # ingredients (Materials)
            self.__a = []            # amount (instances of Amount class)
            self.__c = None          # recipe's concentration. See conc, dens.
            self.__name = None       # recipe's given name.

            # default units
            du = kwargs.get('units', 1)
            # default names:
            dn = kwargs.get('names', {})

            # New args interpretation
            if len(args) == 0 or len(args) % 2 != 0:
                # if there are more than 1 arguments, thier amount should be
                # even.
                raise TypeError('Method __init__ takes exactly one ' +
                                'or an odd number of arguments')

            # interprete each pair of arguments
            ai = iter(args)  # iterator on args, to get next element
            for mraw in ai:
                m = None
                # interprete definition of material
                if (isinstance(mraw, self.__class__) or
                   isinstance(mraw, Nuclide)):
                    # use the specified in arguments material directry as
                    # ingredient.
                    m = mraw
                elif isinstance(mraw, int):
                    # if integer, assume it is ZAID representation of a nuclide
                    m = Nuclide(mraw)
                elif isinstance(mraw, basestring):
                    # Assume that string gives a chemical name or a chemical
                    # formula.  Optional keyword argument with natural
                    # isotopical abundancies
                    # may be specified.
                    mraw = formula_to_tuple(mraw, names=dn)
                if isinstance(mraw, tuple):
                    m = self.__class__(*mraw, **kwargs)

                if m is None:
                    raise TypeError('Unsupported type of material definition, ',
                                    repr(mraw), type(mraw))

                # all possible forms of the amount definiton see in the
                # constructor of Amount() class
                araw = ai.next()
                a = Amount(araw, du)  # if araw is tuple, du is ignored

                self.__m.append(m)
                self.__a.append(a)
        return

    def elements(self, norm=1):
        """
        Return dictionary with chemical elements that are found in the material.

        Optional argument norm takes the following values:

            1: (default) sum of isotopes of each element is equal to 1.

            2: sum over all isotopes and all elements give 1.

            any other: sum of isotopes of each element is equal to frac. of this
            element in the material.


        """
        # collect isotopes into elements. ed: z -> el, where el: ZAID -> moles
        ed = {}
        mexp = self.expanded()
        mexp.remove_duplicates()
        for n, a in mexp.recipe(order=1):
            # n is a nuclide
            # a is an amount
            z = n.Z
            if z not in ed:
                ed[z] = {}
            el = ed[z]
            el[n.ZAID] = el.get(n.ZAID, 0.*a) + a
        # replace z numbers with chemical names and el dictionaries with lists,
        # ready to pass to Material() constructor.
        res = {}
        atot = mexp.amount()
        for z, el in ed.items():
            # sum() adds elements from 1-st argument to the 2-nd, which is by
            # def 0.
            # zl -- list of zaids,
            # vl -- list of fractoins
            zl, vl = zip(*sorted(el.items()))
            if norm == 1:
                att = sum(vl, 0.*vl[0])
                vl = map(lambda v: v/att, vl)  # normalized values
            elif norm == 2:
                vl = map(lambda v: v/atot, vl)
            else:
                pass
            res[_chemical_names[z]] = sum((e for e in zip(zl, vl)), ())
        return res

    def recipe(self, order=0):
        """
        Returns a list of tuples, representing the recipe of
        the mixture .

        The resulting list can be passed to the mixture
        constructor to create another mixture:

            >>> r1 = Mixture( 'O' )
            >>> r2 = Mixture( *r1.recipe() )
            >>> r1.recipe() == r2.recipe()
            True

        If order is not equal to 0, pairs (ingredient, amount) are returned.

        """
        # return list(zip( self.__m, self.__a ))
        if order == 0:
            for m, a in zip(self.__m, self.__a):
                yield m
                yield a
        else:
            for m, a in zip(self.__m, self.__a):
                yield(m, a)

    def index(self, i):
        """
        Returns index of the ingredient i in the mixture's recipe. Similar to
        the index method of a list.

        Argument i can be an instance of the ``Nuclide`` or ``Mixture`` class,
        in which case the index of this ingredient is returned (if any).

        If i is an integer, it is internally converted into ``Nuclide(i)``.

        >>> m = Mixture('Fe')
        >>> m.index(26054)
        0
        >>> m.index(26056)
        1
        >>> m.index(26058)
        3
        """
        if isinstance(i, self.__class__):
            return self.__m.index(i)
        elif isinstance(i, Nuclide):
            return self.__m.index(i)
        elif isinstance(i, int):
            n = Nuclide(i)
            for nn in self.__m:
                if nn == n:
                    return self.__m.index(nn)
            raise ValueError(str(i) + ' not in the recipe')
        else:
            raise ValueError('Wrong type of ingredient: ' +
                             i.__class__.__name__)

    def __mul__(self, value):
        """
        Multipying by a scalar c results in a new instance of the Mixture class,
        which represents 'c moles of self'.

        >>> r1 = Mixture('O')
        >>> r2 = 2*r1
        >>> r2.recipe()[0][0] is r1
        True
        >>> print r2.recipe()[0][1]
        2.0 mol
        """
        return self.__class__(self, (value, 1))

    def __rmul__(self, value):
        return self*value

    def expanded(self):
        """
        Returns a new mixture instance with all ingredients resolved down to
        nuclides with amounts expressed in moles.

        The sum of moles of each ingredient nuclide is equal to the amount of
        originally defined recipe.

        >>> r1 = Mixture( ('H', 2), ('O', 1) )
        >>> r2 = r1.expanded()
        >>> r1.amount() == r2.amount()
        True
        >>> for (m,a) in r2.recipe():
        ...     print m, a
        ...
        <    1001   0.9992> 1.99977 mol
        <    1002   1.9968> 0.00023 mol
        <    8016  15.8575> 0.99757 mol
        <    8017  16.8531> 0.00038 mol
        <    8018  17.8445> 0.00205 mol

        """
        res = []
        for (m, a) in zip(self.__m, self.__a):
            if isinstance(m, Nuclide):
                if a.t != 1:
                    a = Mixture((m, a)).moles()
                res += [m, a]
            else:
                em = m.expanded()
                em.normalize(a)
                #
                res += list(em.recipe())    # zip( em.__m, em.__a )
        res = self.__class__(*res)
        res.conc = self.conc
        return res

    def collapsed(self, units=1):
        """
        Return a new instance, which ingredients are mixtures representing
        chemical elements.
        """
        d = self.elements(norm=3)
        r = []
        for k, er in d.items():
            ei = self.__class__(*er)
            ea = ei.how_much(units)
            # ea = sum(er[1::2], er[1]*0)  # start must be of appropriate type
            ei.name = k.strip()
            r.extend((ei, ea))
        res = self.__class__(*r)
        res.name = self.name
        return res


    def remove_duplicates(self):
        """
        Check the mixture and join equal materials. Changes are made in-place.

        Only the materials specified directly in the recipe are compared.

        If a material is mentioned in the recipe several times, only one
        entry with the total amount will remain. The units are defined by the
        first mentioning of the material in the recipe.

        >>> r = Mixture('O', 'U', 'O')
        >>> r.remove_duplicates()
        >>> for (m,v) in r.recipe():
        ...    print m, v
        ...
        <O         15.8620> 2.0 mol
        <U        235.9841> 1.0 mol

        """
        mlist = []  # material list to remember the order
        alist = []  # list with material amounts.
        for (m, a) in zip(self.__m, self.__a):
            if m not in mlist:
                # m is mentioned for the first time:
                mlist.append(m)
                alist.append(a)
            else:
                # m was allready mentioned before. Recompute to old units, if
                # necessary, and add.
                ii = mlist.index(m)
                if alist[ii].t != a.t:
                    a = Mixture((m, a)).amount(alist[ii])
                alist[ii] += a
        self.__m = mlist[:]
        self.__a = alist[:]
        return None

    def normalize(self, a, t=1):
        """
        Change amount of ingredients in the recipe proportionally, so that
        the resulting amount is a (if a is a float, one has to specify also
        units by setting t=1, 2 or 3).

        >>> r = Mixture('O', 'U', 'O')  # r has 3 moles
        >>> r.dens = 10.                # set density so the cc amount has sense
        >>> r.normalize(1, 1)
        >>> print r.amount(1), r.amount(2), r.amount(3)
        1.0 mol 90.0092422778 g 9.00092422778 cc
        >>> r.normalize(1, 2)
        >>> print r.amount(1), r.amount(2), r.amount(3)
        0.0111099702063 mol 1.0 g 0.1 cc
        >>> r.normalize(1, 3)
        >>> print r.amount(1), r.amount(2), r.amount(3)
        0.111099702063 mol 10.0 g 1.0 cc

        """
        a = Amount(a, t)
        if a.t == 1:
            # moles
            c = self.moles()
        elif a.t == 2:
            # grams
            c = self.grams()
        elif a.t == 3:
            # cm3
            c = self.cc()
        else:
            raise ValueError('Unknown value of a.t: ', a.t)
        self.__a = map(lambda x: x*a.v/c.v, self.__a)
        return None

    def moles(self):
        """
        Returns total amount of moles of the ingredients, specified in the
        recipe definition.

        Returned value is an instance of the ``Amount`` class.

        """
        res = Amount(0, 1)
        for (m, a) in zip(self.__m, self.__a):
            if a.t == 2:
                a = a / m.M() / G_MOL_AWR
                a.t = 1
            elif a.t == 3:
                c = m.conc
                if c is None:
                    raise ValueError('Amount of ingredient cannot be derived')
                a = a * c / NAVOGAD
                a.t = 1
            res += a
        return res

    def grams(self):
        """
        returns total mass in grams of the ingredients, specified in the recipe
        defition.

        Returned value is an instance of the ``Amount`` class.

        """
        res = Amount(0., 2)
        for (m, a) in zip(self.__m, self.__a):
            if a.t == 1:
                # v in moles:
                a = a * m.M() * G_MOL_AWR  # [mol awr g/mol/awr ]
                a.t = 2
            elif a.t == 3:
                # v in cc:
                d = m.dens
                if d is None:
                    raise ValueError('Mass of ingredient cannot be derived')
                a = a * d
                a.t = 2
            res += a
        return res

    def cc(self):
        """
        returns total volume in cubic centimeters of the ingredients, specified
        in the recipe definition.

        Returned value is an instance of the ``Amount`` class.

        Some ingredients might have no density/concentration property, in this
        case the direct evaluation of the sum of ingredients volumes is not
        possible. In this case, the value ::

            self.grams() / self.dens

        will be returned. If the density/concentration of self is not defined,
        None is returned.

        """
        res = Amount(0, 3)
        for (m, a) in zip(self.__m, self.__a):
            if a.t == 1:
                c = m.conc
                if c is None:
                    raise ValueError('Volume of ingredient cannot be defined')
                if c != 0:
                    a = a * NAVOGAD / c
                else:
                    a = a * NAVOGAD
                    a.v = float('inf')
                a.t = 3
            elif a.t == 2:
                d = m.dens
                if d is None:
                    raise ValueError('Volume of ingredient cannot be defined')
                if d != 0:
                    a = a / d
                else:
                    a = a * 1.0
                    a.v = float('inf')
                a.t = 3
            res += a
        return res

    def amount(self, t=1):
        """
        Returns the total amount of ingredients, specified in the recipe
        definition. The t argument defines the units (moles, g or cc).

        Returned value is an instance of the ``Amount`` class.

        See also methods ``cc``, ``grams`` and ``moles``.

        """
        a = Amount(t, t)
        if a.t == 1:
            # in moles
            return self.moles()
        elif a.t == 2:
            return self.grams()
        elif a.t == 3:
            return self.cc()

    def M(self):
        """
        Effective molar mass of the recipe.

        """
        Smass = 0.
        Smole = 0.
        for (m, a) in zip(self.__m, self.__a):
            if a.t == 1:
                mole = a.v
            else:
                mole = Mixture((m, a)).moles().v
            Smass += m.M() * mole
            Smole += mole
        if Smass == 0.:
            raise ValueError('Recipe molar mass is 0 in material', self)
        if Smole == 0.:
            raise ValueError('Recipe amount is 0 in material', self)
        return Smass/Smole

    @property
    def dens(self):
        """Density of the mixture, g/cc.

        Density can be computed from the recipe ingredients, or set explicitly
        to the mixture. The computed value is returned only if the density is
        not set explicitly.

        Internally, density is saved as concentration. Thus, if a density was
        set to a recipe and than the molar mass of recipe (or its ingredients)
        was changed, the density will be changed also.

        """
        c = self.conc
        if c is None:
            return None
        else:
            return c * self.M() * AMU_AWR * G_AMU

    @dens.setter
    def dens(self, value):
        self.conc = value / self.M() / AMU_AWR / G_AMU

    @property
    def conc(self):
        """Concentration of the mixture, 1/cc.

        Concentration can be computed from the material inrgedients, or set
        explicitly. The computed value ( see derived_conc method) is used only
        if the concentration not set explicitly.

        Use the ``dens`` property to set concentration in terms of density
        [g/cc].
        """
        if self.__c is None:
            return self.derived_conc()
        else:
            return self.__c

    @conc.setter
    def conc(self, value):
        if value is None:
            self.__c = value
        else:
            fval = float(value)
            if fval < 0.:
                raise ValueError('Cannot set negative concentration/density')
            else:
                self.__c = fval

    def derived_conc(self):
        """
        Returns computed concentration of the recipe, 1/cc.

        This can be done only if all recipe ingredients have their
        conentration/density attributes either set explicitly or can be
        computed.
        """
        # For each ingredient, define its amount, Ni and its volume, Vi. The
        # derived conc is sum(Ni) / sum(Vi).

        Sv = 0.
        Sn = 0.

        for (m, a) in zip(self.__m, self.__a):
            mm = Mixture(m, a)
            try:
                n = mm.moles()
                v = mm.cc()
            except ValueError:
                return None

            Sv += v.v
            Sn += n.v * NAVOGAD
        return Sn/Sv

    def __str__(self):
        try:
            m = self.M()
        except ValueError:
            m = 0.0

        return '<{0:8s} {1:8.4f}>'.format(self.name, m)

    def report(self):
        """
        Returns a multi-line string, describing the mixture.

        """
        indent = ' '*8
        res = ['Mixture {0}'.format(self.name)]
        for (m, a) in zip(self.__m, self.__a):
            s = indent + '{0}: {1}'.format(str(m), str(a))
            res.append(s)
        # If possible, provide amount in other units:
        s = 'total: '
        for f in (self.moles, self.grams, self.cc):
            try:
                a = f()
            except ValueError:
                pass
            else:
                s += ' or {0}'.format(str(a))
        s = s.replace(':  or', ': ')
        res.append(s)

        res.append('Nuclide composition:')
        res.append(indent + '{0:>19s} {1:>13s} {2:>13s} {3:>13s} {4:>13s}'
                   ''.format('Nuclide', 'At.frac', 'Wgt.frac',
                             'amount, m', 'weight, g'))
        # print 'call expanded from report'
        try:
            e = self.expanded()
        except ValueError:
            res.append(indent + 'cannot define nuclide composition while '
                       'not all ingredients have conc set')
        else:
            e.remove_duplicates()
            e.normalize(1, 1)
            eG = e.grams()
            sG = self.grams().v
            sM = self.moles().v
            for (m, a) in sorted(zip(e.__m, e.__a), key=lambda x: x[0].ZAID):
                ww = e.how_much(2, m)
                s = (indent + '{0:>19s} {1:13.5e} {2:13.5e} {3:13.5e} {4:13.5e}'
                    ''.format(str(m), a.v, ww/eG, a.v*sM, ww/eG*sG))
                res.append(s)
        return '\n'.join(res)

    @property
    def name(self):
        """Name of the mixture, a string.

        The mixture name can be specified explicitly. If not specified
        explicitly, it will be derived from the recipe definition, see
        the ``derived_name()`` method.

        >>> r = Mixture(('O', 2), ('U', 1))
        >>> r.name
        'O-U'
        >>> r.name = 'mox'
        >>> r.name
        'mox'
        >>> steel = Mixture( 'Fe', 'Cr', 'Mo', 'Ni') # more than 4 elements.
        >>> steel.name
        'Fe-Cr-Mo-'

        """
        if self.__name is not None:
            return self.__name
        else:
            return self.derived_name()

    @name.setter
    def name(self, value):
        self.__name = str(value)

    def derived_name(self):
        """
        The derived name is composed from the element names entering the
        mixture. The general form of the derived name is

            'E1-E2-E3-'

        where E1, E2, E3 are the chemical element names of the mixture
        ingredients.  3 element names accounted at maximum. If there are other
        elements, the name ends with '-', as shown above.

        The element names are listed in the decreasing order of its molar amount
        in the mixture.

        If the mixture consists of only one nuclide, the nuclide name will be
        used.
        """
        e = self.expanded()
        if len(e.__m) == 1:
            return e.__m[0].name
        else:
            nlist = []
            vlist = []
            for (m, a) in zip(e.__m, e.__a):
                eName = m.name[:2].lstrip().rstrip()
                if eName not in nlist:
                    nlist.append(eName)
                    vlist.append(a.v)
                else:
                    i = nlist.index(eName)
                    vlist[i] += a.v

        # use first three element names, in the mole decreasing order
        lst = zip(nlist, vlist)
        lst.sort(key=lambda x: round(x[1], 4), reverse=True)
        if len(lst) > 3:
            lst = lst[:3] + [('', 0)]
        return '-'.join(map(lambda x: x[0], lst))

    def __add__(self, othr):
        """
        The sum of two materials is a new instance of the Mixture class
        representing the mixture of the summation terms in equal proportions.

        The summation argumets are not referenced in the result. Instead, they
        are resolved to the nuclide composition. For illustration, consider the
        following definitions:

            >>> n1 = Nuclide(1001)
            >>> n2 = Nuclide(1002)
            >>> n3 = Nuclide(2003)
            >>> r1 = n1 + n2
            >>> S1 = r1 + n3
            >>> S2 = Mixture(r1, n3)
            >>> print S1.report()     # doctest: +NORMALIZE_WHITESPACE
            Mixture H-He
                <    1001   0.9992>: 1.0 mol
                <    1002   1.9968>: 1.0 mol
                <    2003   2.9901>: 1.0 mol
                total: 3.0 mol or 6.0379562462 g
            Nuclide composition:
                            Nuclide       At.frac      Wgt.frac
                <    1001   0.9992>   3.33333e-01   1.66915e-01
                <    1002   1.9968>   3.33333e-01   3.33574e-01
                <    2003   2.9901>   3.33333e-01   4.99512e-01
            >>> print S2.report()     # doctest: +NORMALIZE_WHITESPACE
            Mixture H-He
                <H          1.4980>: 1.0 mol
                <    2003   2.9901>: 1.0 mol
                total: 2.0 mol or 4.52699276863 g
            Nuclide composition:
                            Nuclide       At.frac      Wgt.frac
                <    1001   0.9992>   2.50000e-01   1.11313e-01
                <    1002   1.9968>   2.50000e-01   2.22455e-01
                <    2003   2.9901>   5.00000e-01   6.66232e-01

        The definition of S1 is: "one mole of n1, one mole of n2, one mole of
        n3", i.e. it does not contain references to r1, during summation it was
        expanded to the nuclides.

        The definition of S2 is "one mole of r1 and one mole of n3". Since one
        mole of r1 contains 1/2 mole of n1 and 1/2 mole of n2, the nuclide
        composition of S1 and S2 differ.  There are also other important
        differences between S1 and S2. First, the amount of ingredients in S1
        is 3 moles, while it is only 2 moles in S2. Second, if r1 changes after
        S1 and S2 were defined, S2 will also change, but S1 will not.
        """
        if isinstance(othr, Mixture):
            # print 'call expanded two times from add'
            return self.__class__(*(list(self.expanded().recipe()) +
                                    list(othr.expanded().recipe())))
        if isinstance(othr, Nuclide):
            # print 'call expanded from add'
            return self.__class__(*(list(self.expanded().recipe()) +
                                    [othr, (1., 1)]))
        else:
            return NotImplemented

    def how_much(self, t, *args, **kwargs):
        """
        Computes amount of specified ingredients or nuclides entering the
        mixture.

        Computes the amount in units specified by the argument ``t`` of the
        mixture ingredients specified by ``*args``, or of nuclides specified by
        ``**kwargs``.

        Only t=1 (moles) or t=2 (grams) can be used.

        Returned value is an instance of the ``Amount`` class.

        Arguments ``*args`` and ``**kwargs`` cannot be used simultaneously. If
        ``*args`` are specified, the ``**kwargs`` have no effect.

        When ``*args`` are specified, they must be nuclides,  mixtures or
        integers (meaning ZAID) entering to the mixture recipe.  The returned
        value is the total amount of all specified in ``*args`` materials. The
        materials are searched only in the recipe, i.e. a nuclide will be
        accounted only if it was specified directly in the recipe. If it enters
        the mixture only indirectly, it is not accounted for:

        >>> r = Mixture( 'Fe', 8016 )
        >>> print r.how_much(1, 8016)
        1.0 mol
        >>> print r.how_much(1, 'Fe')
        1.0 mol
        >>> print r.how_much(1, 'Fe', 8016)
        2.0 mol

        The optional keyword arguments, ``**kwargs``, specify properties of
        nuclides that should be accounted for. In this case, the mixture first
        expanded so that nuclides of the mixture ingredients are also taken into
        account.

        >>> r = Mixture( 'Fe', 8016 )
        >>> print r.how_much(1, ZAID=8016)
        1.0 mol
        >>> print r.how_much(1, Z=26)
        1.0 mol

        If neither ``*args`` nor ``**kwargs`` are specified, how_much(t) is
        equal to amount(t).

        """
        tt = Amount(t, t)
        if tt.t not in [1, 2]:
            raise ValueError('Unsupported value of t argument: ' + str(t))
        if len(args) != 0:
            r = Amount(0, tt.t)
            for arg in args:
                for (m, a) in zip(self.__m, self.__a):
                    if (isinstance(arg, int) and
                       isinstance(m, Nuclide) and
                       m.ZAID == arg):
                        r += Mixture((m, a)).amount(tt)
                    elif isinstance(arg, basestring):
                        # e = Mixture( *natural.recipe(arg) )
                        e = Mixture(*formula_to_tuple(arg))
                        if isinstance(m, self.__class__) and e == m:
                            r += Mixture((e, a)).amount(tt)
                    elif arg == m:
                        r += Mixture((m, a)).amount(tt)
            return r
        elif len(kwargs) != 0:
            e = self.expanded()
            r = Amount(0, tt.t)
            # kitems = kwargs.items()
            for (m, a) in zip(e.__m, e.__a):
                if m.check_attributes(**kwargs):
                    if tt.t == 1:
                        r += a
                    else:
                        r += Mixture((m, a)).amount(tt)
            return r
        else:
            return self.amount(tt)

    def tune(self, objective, var, err=1e-5):
        """Changes the mixture recipe to satisfy objective function.

        The ``objective`` argument is a function taking as argument an instance
        of the ``Mixture`` class.

        The ``var`` argument is a list of two elements each of them can be a
        nuclide, mixture or an integer (meaning ZAID), that were used in the
        definition of the mixture.

        The method changes the amount of materials var[0] and var[1] in the
        mixture recipe, so that the objective function returns value with the
        module less than the ``err`` argument.

        >>> # mixture m contains several Fe isotopes.
        >>> m = Mixture('Fe')
        >>> # objective function. Returns 0 if amount of Fe-56
        >>> # and Fe-54 in its argument is equal.
        >>> def o(mix):
        ...     a4 = mix.how_much(1, 26054)
        ...     a6 = mix.how_much(1, 26056)
        ...     return (a4 - a6).v
        ...
        >>> # change mixture m in place, now it has the same
        >>> # fraction of Fe-54 and Fe-56.
        >>> m.tune(o, [26056, 26057])

        """

        # set up variable materials
        i1 = self.index(var[0])  # indices pointing to the variable material in recipe
        i2 = self.index(var[1])
        a1 = self.__a[i1] * 1  # Initial amount of variable material in recipe
        a2 = self.__a[i2] * 1
        # during the tuning, amounts of variable materials are in moles.
        if a1.t != 1:
            self.__a[i1] = Mixture(var[0], self.__a[i1]).moles()
        if a2.t != 1:
            self.__a[i2] = Mixture(var[1], self.__a[i2]).moles()
        Smol = (self.__a[i1] + self.__a[i2]).v

        # function to set new recipe definition with respect to the independent
        # variable.  The independent variable is f = moles(m1)/moles(m1+m2)
        # where m1 and m2 -- variable materials.
        def change_recipe(f):
            # f is the ratio of mole amount of var[0] to the mole amount of
            # var[0] and var[1] Thus, f can take values in the interval [0, 1].
            self.__a[i1].v = f * Smol
            self.__a[i2].v = (1. - f) * Smol

        def y(x):
            change_recipe(x)
            return objective(self)
            # return curr_val() - goal_val
        # searching loop. Starts at f=0. Uses bisection method
        x1 = 0.
        x2 = 1.
        y1 = y(x1)
        y2 = y(x2)
        break_loop = False
        while True:
            xnew = 0.5*(x2 + x1)
            ynew = y(xnew)
            # print 'x1={} x2={} y1={} y2={}   ' +
            #       'xnew={} ynew={}'.format(x1, x2, y1, y2, xnew, ynew)
            for (xx, yy) in [(x1, y1), (x2, y2), (xnew, ynew)]:
                if abs(yy) < abs(err):
                    change_recipe(xx)
                    break_loop = True
            if break_loop:
                break
            if y1*ynew < 0.:
                x2 = xnew
                y2 = ynew
            if y2*ynew < 0.:
                x1 = xnew
                y1 = ynew
            if y1*y2 > 0.:
                raise ValueError('Equal sign of y1 and y2, but x2-x1 > err: ' +
                                 'x1={0} x2={1} y1={2} y2={3}'.format(x1,
                                                                      x2,
                                                                      y1,
                                                                      y2))

        # go back to initial units for materials m1 and m2:
        if a1.t != 1:
            self.__v[i1] = Mixture((var[0], self.__a[i1]).amount(a1))
        if a2.t != 1:
            self.__v[i2] = Mixture((var[1], self.__a[i2]).amount(a2))

    def __eq__(self, othr):
        """
        Two mixture instances are equal, if they have equal recipies, names and
        concentrations.
        """
        if isinstance(othr, self.__class__):
            return (self.recipe() == othr.recipe() and
                    self.name == othr.name and
                    self.conc == othr.conc)
        else:
            return NotImplemented

    def __hash__(self):
        """
        this is to prohibit the usage of nuclide instances as dictionary keys.
        """
        return None

    def isfuel(self):
        """
        Returns True if the mixture contains one of the following
        nuclides: 92235, 94239, 94241.
        """
        for (n, a) in self.expanded().recipe():
            if n.isfuel():
                return True
        return False


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    n1 = Nuclide(1001)
    n2 = Nuclide(1002)
    n3 = Nuclide(1003)
