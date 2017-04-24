"""
Classes to represent geometry in MCNP.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from .auxiliary import Counter, Collection
from . import formatter

class Surface(object):
    """MCNP surface.

    Instances are immutable. 

    """
    #: Precision of surface parameters. Parameters rounded to this number of digits
    #: when printed to the card or when two surfaces are compared.
    PRECISION = 9

    #: Known macrobodies
    MBTYPES = ['rpp', 'rcc']                                  #: Known macrobody surfaces

    #: Known simple surface types
    SSTYPES = ['px', 'py', 'pz', 'cz', 'c/z', 'so', 's']      #: Known simple surfaces

    __PLLEN = [6, 7, 1, 1, 1, 1, 3, 1, 4]                     #: number of parameters for different surface types, the order as in MBTYPES + SSTYPES

    def __init__(self, card=None, **kwargs):
        """
        The constructor takes a string with usual definition of a surface as
        appears in an input file, except the surface ID. Alternatively, parameters
        of a surface can be specified as keyword arguments.


        :param str card: 
            is a string representing the surface card of the MCNP input,
            except the surface number should not be specified, for example
            ``'+ px 1.0'``.

        :param str type: 
            a string representing the surface type, for example 'px'.

        :param char refl:
            a character representing the reflection of the surface, for example '*'.

        :param list plst: 
            a list or tuple  of parameters of the surface.

        :param str cmnt: 
            a string representing the surface comment.

        """
        self.__p = tuple()  # tuple of parameters
        self.__t = ''       # surface type
        self.__r = ''       # reflection
        self.__c = ''       # comment

        if card is not None:
            v = card.lower()
            if '$' in v:
                card, comment = v.split('$')
            else:
                card = v
                comment = ''
            tokens = card.lower().split()
            if tokens[0] in ['*', '+']:
                self.__r = tokens.pop(0)
            else:
                self.__r = ''
            self.__t = tokens.pop(0)
            self.__p = tuple( map(float, tokens) )
            self.__c = comment

        for (n, v) in kwargs.items():
            if n == 'type':
                self.__t = v.lower()
            elif n == 'refl':
                self.__r = v.lower()
            elif n == 'plst':
                self.__p = tuple(v)
            elif n == 'cmnt':
                self.__c = str(v)
            else:
                raise TypeError('Got an unexpected keyword argument ', n)

        # simplify, if necessary
        if self.__t == 'c/z' and self.__p[0] == 0. and self.__p[1] == 0.:
            self.__t = 'cz'
            self.__p = tuple([self.__p[2]])
        elif self.__t == 's' and self.__p[:-1] == [0., 0., 0.]:
            self.__t = 'so'
            self.__p = (self.__p[-1])
            

        # check the type
        if self.__t not in self.MBTYPES + self.SSTYPES:
            raise ValueError('Unknown surface type', self.__t)
        # check the number of parameters
        if len(self.__p) != self.__PLLEN[(self.MBTYPES + self.SSTYPES).index(self.__t)]:
            raise IndexError('Wrong number of parameters for the surface type ', self.__t, self.__p)
        # check particular parameters
        if self.__t == 'rcc' and self.__p[0] != 0. and self.__p[1] != 0. and self.__p[3] != 0. and self.__p[4] != 0.:
            raise ValueError('Parameters of an rcc do not correspond to a cylinder along z axis ', self.__p)

        return

    @property
    def tpe(self):
        """
        Type of the surface, for expample, ``'px'``
        """
        return self.__t

    @property
    def prm(self):
        """
        The tuple of surface parameters.
        """
        return self.__p

    @property
    def rfl(self):
        """
        Reflection of the surface. Can be ``''`` (empty string), ``'*'`` or ``'+'``.
        """
        return self.__r

    def volume(self, mapp=lambda x:x):
        """Volume 'above' the surface.

        :param func mapp: 
            a mapping applied to the surface facets before passing to the
            ``Volume()`` constructor.

        :return:
            an instance of the ``Volume`` class. The Volume() class defines
            operations of union, intersect and nagation.

        Instances of the Volume() class returned by this method are always
        defined via simple (not macrobody) surfaces.  To get an instance of the
        Volume() class defined via a macrobody surface, use the constructor
        Volume() directly.

        """
        flist = self.facets(mapp)
        v = flist.pop(0)
        for vv in flist:
            v = v | vv
        return v

    def is_macrobody(self):
        """
        Returns True if the surface is a macrobody.
        """
        return (self.__t in self.MBTYPES)


    def facets(self, mapp=lambda x:x):
        """Returns the list of volumes for each facet of the surface.

        :param func mapp:
            a mapping applied to the facets before passing to the
            ``Volume()`` constructor.

        :return: list of volumes.

        If the surface is a simple surface, the returned list contains single
        element.

        """
        if self.__t in self.SSTYPES:
            return [Volume(1, mapp(self))]
        elif self.__t == 'rcc':
            s1 = Surface(type='c/z', 
                         refl=self.__r, 
                         plst=self.__p[0:2] + self.__p[6:7], 
                         cmnt=self.__c)
            s2 = Surface(type='pz',  
                         refl=self.__r,
                         plst=[self.__p[5] + self.__p[2]],
                         cmnt=self.__c)
            s3 = Surface(type='pz',  
                         refl=self.__r,
                         plst=self.__p[2:3],
                         cmnt=self.__c)
            return [Volume( 1, mapp(s1)), Volume( 1, mapp(s2)), Volume(-1, mapp(s3))]
        elif self.__t == 'rpp':
            s1 = Surface(type='px', refl=self.__r, plst=self.__p[1:2], cmnt=self.__c)
            s2 = Surface(type='px', refl=self.__r, plst=self.__p[0:1], cmnt=self.__c)
            s3 = Surface(type='py', refl=self.__r, plst=self.__p[3:4], cmnt=self.__c)
            s4 = Surface(type='py', refl=self.__r, plst=self.__p[2:3], cmnt=self.__c)
            s5 = Surface(type='pz', refl=self.__r, plst=self.__p[5:6], cmnt=self.__c)
            s6 = Surface(type='pz', refl=self.__r, plst=self.__p[4:5], cmnt=self.__c)
            return [Volume( 1, mapp(s1)), Volume(-1, mapp(s2)), Volume( 1, mapp(s3)), Volume(-1, mapp(s4)), Volume( 1, mapp(s5)), Volume(-1, mapp(s6))]

    def card(self, formatted=True):
        """
        Returns string representing the surface, valid for an MCNP
        input file, except the surface ID.

        If optional argument formatted set to True (default), the
        returned string can contain new-line characters, so that
        the lines fit to 80-characters limit required by the MCNP
        input file syntax.

        This method is used to transform an instance of the ``Surface()`` class to a string.

        """ 

        res = self.__r + '{0} ' +  self.__t 
        for p in self.__p: 
            res += '  {0}'.format(str(round(p, self.PRECISION))) 
        if self.__c:
            res += ' $ ' + self.__c
        if formatted: 
            res = formatter.format_card(res)
        return res
            
    def __str__(self): return self.card(formatted=True)

    def __eq__(self, othr):
        if othr is None:
            return False
        if not isinstance(othr, self.__class__):
            raise TypeError('Cannot compare Surface and ', othr.__class__.__name__)
        if self.__t not in self.MBTYPES and othr.__t in self.MBTYPES:
            return othr == self

        # check exact equality.
        if self.__t == othr.__t:
            for (v1, v2) in zip(self.__p, othr.__p):
                if round(v1 - v2, self.PRECISION) != 0.0:
                    return False
            return True
        return False


class Volume(object):
    """
    Representation of the cell geometry using signed surfaces and
    union, intersection and negation operations. 
    
    A new volume instance is created by specifying the sign and the surface
    description. The surface description can be of any type (although in real
    MCNP applications, an instance of the Surface class must be used):
    
    >>> v1 = Volume(1, 'a')  # 'a' here is an abstract surface definition 
    >>> print v1
    a

    There are two special volumes representing by tuples (1,) and (-1,). The first 
    means 'empty set', the second is 'whole space'. To create the emtpy set, multiply
    usual volume by 0. To create whole space, multiply empty set by -1:

    >>> e = Volume()*0   # empty set
    >>> print e
    Empty Set
    >>> w = -e           # whole space
    >>> print w
    Whole space

    Instances of the Volume() class support operations of union '|', intersection '&' and negation '-'.

    """
    def __init__(self, sign=1, surface=None):
        if sign not in [0, 1, -1]:
            raise ValueError('Sign can be 0, 1 or -1, but recieved ', sign)

        if sign is 0:
            # return an empty set:
            self.__a1 = (1, )
            self.__op = None
            self.__a2 = None
        elif isinstance(surface, Volume):
            # do not allow definitions to be of the Volume class
            # Instead, make copy of it.
            v = surface*sign
            self.__a1 = v.a1
            self.__a2 = v.a2
            self.__op = v.op
        else:
            self.__a1 = (sign, surface)
            self.__op = None
            self.__a2 = None # 0
        return

    @property
    def a1(self):
        """
        Returns the first operand of the volume, if the volume was defined
        using intersection or union operators. For a simple volume, i.e.
        defined directly by the Volume() constructor, this is a tuple (sign,
        surface).

        >>> v = Volume(1, 'a')
        >>> v.a1
        (1, 'a')
        >>> v = Volume(1, 'a') & Volume(1, 'b')
        >>> v.a1                               # doctest: +ELLIPSIS
        <__main__.Volume object at ...>
        """
        return self.__a1

    @property
    def a2(self):
        """
        Returns the second operand of the Volume class, if the volume was
        defined using union or intersection. For a simple Volume returns 0.

        >>> Volume(1, 'a').a2
        0
        >>> (Volume(1, 'a') & Volume(1, 'b')).a2    # doctest: +ELLIPSIS
        <__main__.Volume object at ...>
        """
        return self.__a2

    @property
    def a(self):
        """
        Returns the list of operands, [self.a1, self.a2].
        """
        return [self.__a1, self.__a2]

    @property
    def op(self):
        """
        Returns the operator used to create the volume. For a simple volume
        returns None.

        >>> print Volume(1, 'a').op
        None
        >>> (Volume(1, 'a') & Volume(1, 'b')).op
        'and'
        >>> (Volume(1, 'a') | Volume(1, 'b')).op
        'or'
        """
        return self.__op

    def __neg__(self):
        """
        Returns a new Volume instance. In a simple volume, the sign is
        changed. In a compound volume, the sign of its oparands are changed and
        the operator is changed.

        >>> v = Volume(1, 'a')
        >>> (-v).a1
        (-1, 'a')
        >>> v = Volume(1, 'a') & Volume(1, 'b') | Volume(1, 'c')
        >>> print v
        (a b):c
        >>> print -v
        (-a:-b) -c

        """
        if self.__op is None:
            if len(self.__a1) == 1:
                # special case of whola space or empty set.
                v = Volume(0)
                v.__a1 = (-self.__a1[0],)
                return v
            else:
                return Volume(-self.__a1[0], self.__a1[1])
        else:
            if self.__op == 'and':
                op = 'or'
            elif self.__op == 'or':
                op = 'and'
            res = Volume()
            res.__a1 = -self.__a1
            res.__op = op
            res.__a2 = -self.__a2
            return res

    def __mul__(self, c):
        """
        Volume can be multiplied by 0, 1 or -1 only. 
        
        If multiplied by 0, returns the empty set.
        
        If multiplied by -1, returns a new volume that uses the same definition as the original one.
        
        If multiplied by 1, returns the volume itself. To copy a volume, use the .copy() method.
        

        >>> v = Volume(1, 'a')
        >>> print -1*v, v*-1, 1*v, v*1
        -a -a a a
        """
        if c == -1:
            return -self
        elif c == 1:
            return self
        elif c == 0.:
            return Volume(0)
        else:
            raise ValueError('Can multiply Volume only by 0, 1 or -1, but not by ', str(c))

    def __rmul__(self, c):
        return self*c

    @staticmethod
    def sort_operands(op1, op2):
        """
        Sorts operands for the & and | operations.
        """
        return (op1, op2)

        if op1.__op is None:
            return (op1, op2)
        elif op2.__op is None:
            return (op2, op1)
        elif op1.__op == 'and':
            return (op1, op2)
        elif op2.__op == 'and':
            return (op2, op1)
        else:
            return (op1, op2)

    # Result of an intersection or union of two usual volumes is a new volume, whose definition contains links
    # to the operands. Thus, if an operand is changed later, it can affect the meaning of the operation.

    # Intersection of a usual volume with an universal Set returns the same usual volume, not its copy.
        
    def __and__(self, othr):
        """
        Returns the intersection of two volumes.

        >>> v1 = Volume( 1, 'a')
        >>> v2 = Volume(-1, 'b')
        >>> print v1, v2
        a -b
        >>> print (v1 & v2)
        a -b
        """
        if not isinstance(othr, self.__class__):
            raise TypeError('Wrong type of right operand ', othr.__class__.__name__)

        # if one of the operands is the empty set (1, ), return the empty set:
        if self.__a1 == (1, ):
            return self# .__a1 
        if self.__a2 == (1, ):
            return self# .__a2 
        # if one of the operands is the whole space (-1, None), return the copy of the other operand:
        if self.__a1 == (-1, ):
            return othr
        if othr.__a1 == (-1, ):
            return self

        # if two operands are usual volumes, return a compound volume.
        res = Volume()
        res.__a1, res.__a2 = Volume.sort_operands(self, othr)
        res.__op = 'and'
        return res

    def __or__(self, othr):
        """
        Returns the union of two volumes.

        >>> v1 = Volume(1, 'a')
        >>> v2 = Volume(1, 'b')
        >>> print v1 | v2
        a:b
        """
        if not isinstance(othr, self.__class__):
            raise TypeError('Wrong type of right operand ', othr.__class__.__name__)
        # if one of the operands is the empty set, return the other operand:
        if self.__a1 == (1, ):
            return othr
        if othr.__a1 == (1, ):
            return self
        # if one of the operands is the whole space, return it:
        if self.__a1 == (-1, ):
            return self
        if othr.__a1 == (-1, ):
            return othr
        # if both operands are usual volumes, return a compound volume:
        # ensure that if one of operands is simple and the other one is compound, the simple goes to a1:
        res = Volume()
        res.__a1, res.__a2 = Volume.sort_operands(self, othr)
        res.__op = 'or'
        return res

    def __str__(self):
        """
        Parentheses used only if the operands are not simple surfaces and if
        their operators differ.

        >>> v0 = Volume(-1, 'a0')
        >>> v1 = Volume(1, 'a1') & Volume(-1, 'b1')
        >>> v2 = Volume(1, 'a2') | Volume(-1, 'b2')
        >>> v3 = Volume(1, 'a3') & Volume(-1, 'b3')

        >>> print v0 & v1
        -a0 a1 -b1
        >>> print v0 & v2
        -a0 (a2:-b2)
        >>> print v0 | v1
        -a0:(a1 -b1)
        >>> print v0 | v2
        -a0:a2:-b2

        >>> print v1 & v2
        a1 -b1 (a2:-b2)
        >>> print v1 | v2
        (a1 -b1):a2:-b2
        >>> print v1 & v3
        a1 -b1 a3 -b3
        >>> print v1 | v3
        (a1 -b1):(a3 -b3)

        """
        if self.__a1 == (1, ):
                return 'Empty Set'
        if self.__a1 == (-1, ):
                return 'Universal Set'
        if self.__op is None:
            if self.__a1[0] == -1:
                # not just add the minus sign, but change the sign of the
                # definition a1[1].  This allows to use other simple volumes as
                # definitions.
                try:
                    a1 = str(-self.__a1[1])
                except TypeError:
                    a1 = str(self.__a1[1])
                    if a1.lstrip()[0] == '-':
                        # remove the minus sign
                        a1 = a1.replace('-', '', 1)
                    else:
                        # add the minus sign.
                        a1 = '-' + a1
            else:
                a1 = str(self.__a1[1])
            return a1
        else:
            # volume is compound, i.e. a1 and a2 are defined.
            # If a1 or a2 is speciall, try to simplify self by passing again through the operation definition:
            if self.__a1.is_special() or self.__a2.is_special():
                if self.__op == 'or':
                    vol = self.__a1 | self.__a2
                elif self.__op == 'and':
                    vol = self.__a1 & self.__a2
                return str(vol)
                
            a1 = str(self.__a1)
            p1 = self.__a1.__op
            a2 = str(self.__a2)
            p2 = self.__a2.__op

            if self.__op == 'or':
                op = ':'
            elif self.__op == 'and':
                op = ' '
            if p1 is not None and p1 != self.__op:
                a1 = '({0})'.format(a1)
            if p2 is not None and p2 != self.__op:
                a2 = '({0})'.format(a2)

            return '{0}{1}{2}'.format(a1, op, a2)

    def __eq__(self, othr):
        if not isinstance(othr, self.__class__):
            return False
        else:
            return ( self.__a1 == othr.__a1 and 
                     self.__op == othr.__op and 
                     self.__a2 == othr.__a2 )

    def __hash__(self):
        """
        From the help for hash(): Two objects with the same value have the same
        hash value. The reverse is not necessarily true, but likely.

        >>> v1 = Volume(1, 'a')
        >>> v2 = v1.copy()
        >>> v3 = v1.copy(lambda x: x.upper())
        >>> v4 = v3.copy(lambda x: x.lower())
        >>> for a in [v1, v2, v3, v4]:
        ...     for b in [v1, v2, v3, v4]:
        ...         print a, b, (a is b), (hash(a) == hash(b)), (a == b)
        a a True True True
        a a False True True
        a A False False False
        a a False True True
        a a False True True
        a a True True True
        a A False False False
        a a False True True
        A a False False False
        A a False False False
        A A True True True
        A a False False False
        a a False True True
        a a False True True
        a A False False False
        a a True True True

        """
        return hash((self.__a1, self.__op, self.__a2))

    def surfaces(self):
        """
        Returns a list of surface definitions used to define the volume.

        >>> v1 = Volume( 1, 'a')
        >>> v2 = Volume(-1, 'b')
        >>> v = v1 & v2
        >>> v.surfaces()
        ['a', 'b']
        >>> v = Volume(1, 'c') | v
        >>> v.surfaces()
        ['c', 'a', 'b']
        """
        res = []
        if isinstance(self.__a1, tuple):
            if len(self.__a1) == 1:
                # this is the special volume, it contians no definition.
                pass
            else:
                res.append(self.__a1[1])
        else:
            res += self.__a1.surfaces()
            res += self.__a2.surfaces()
        return res

    def volumes(self, reference=None):
        """
        Returns the list of simple volumes used to define the volume.

        TODO: describe the `reference` optional argument.

        """
        res = []
        if self.__op is None:
            if reference is None:
                res.append(self)
            else:
                res.append(reference)
        else:
            if reference is None:
                res += self.__a1.volumes()
                res += self.__a2.volumes()
            else:
                res += self.__a1.volumes((self, 0))
                res += self.__a2.volumes((self, 1))

        return res

    def copy(self, mapp=lambda x:x):
        """
        Returns a (deep) copy of the volume.

        The returned volume has the same structure as the original one. The
        surface definitions are defined using the  mapping mapp applied to the
        original surface definitions.

        UPD: mapp can be a dictionary.

        Lets create a complex volume:

        >>> v = Volume(1, 'a')
        >>> for c in ['b', 'c']:
        ...     v = v & Volume(-1, c)
        ...     v = v | v
        ...
        >>> print v
        (((a -b):(a -b)) -c):(((a -b):(a -b)) -c)

        A copy of v with the upper() method of a string upplied:

        >>> print v.copy( lambda x: x.upper() )
        (((A -B):(A -B)) -C):(((A -B):(A -B)) -C)

        """
        if isinstance(mapp, dict):
            mpp = lambda x: mapp[x]
        else:
            mpp = mapp

        if isinstance(self.__a1, tuple):
            # new definition:
            if len(self.__a1) == 1:
                # this is the special volume. Ruturn its copy:
                return self*1
            else:
                ndef = mpp(self.__a1[1]) # new definition
                return Volume(self.__a1[0], ndef)
        else:
            a1 = self.__a1.copy(mpp)
            a2 = self.__a2.copy(mpp)
            if self.__op == 'and':
                return a1 & a2
            else:
                return a1 | a2

    def is_union(self):
        """
        True if self was obtained only by union operations.
        """
        if self.__op == 'or':
            return self.__a1.is_union() and self.__a2.is_union()
        elif self.__op == 'and':
            return False
        elif self.__op is None:
            return True

    def is_intersection(self):
        """
        True if self was obtained only by intersection operations.
        """
        if self.__op == 'and':
            return self.__a1.is_intersection() and self.__a2.is_intersection()
        elif self.__op == 'or':
            return False
        elif self.__op is None:
            return True

    def is_simple(self):
        """Checks if the volume is simple, i.e. not a result of operation on another volumes.
        """
        return  self.__op is None

    def is_special(self):
        """Checks if the volume is the whole or empty volume.
        """
        return self.__op is None and len(self.__a1) == 1

    def is_empty(self):
        """Checks if the volume is the specifal empty volume.
        """
        if self.is_special() and self.__a1[0] == 1:
            return True
        return False

    def is_universal(self):
        """Checks if the volume is the whole volume (universal set).
        """
        if self.is_special() and self.__a1[0] == -1:
            return True

    def intersection_operands(self):
        """
        If a volume is an intersection of simple or compound volumes, returns two lists. 
        
        The first contains simple volumes, the second -- compound volumes that defined as a union.
        """

        # second implementation that does not require sorting of operands.
        if self.__op == 'and':
            # both operands should go to the lists.
            sl = [] # simple volumes
            ul = [] # union volumes
            ol = [] # other volumes

            for a in [self.__a1, self.__a2]:
                l1, l2, l3  = a.intersection_operands()
                sl.extend(l1)
                ul.extend(l2)
                ol.extend(l3)
            return (sl, ul, ol)
        elif self.__op is None:
            # self is simple. It is a union of itself.
            return ([self], [], [])
        elif self.is_union():
            # note that for simple volumes is_union is True as well, therefore
            # the previous clause should preceede this one.

            # self as a whole goes into the ul list:
            return ([], [self], [])
        else:
            # self is not a simple union.
            return ([], [], [self])
            
            

    def _simplify(self):
        """
        Replaces some simple volumes by special sets.
        """
        res = self.copy()
        ls, lc = res.intersection_operands()
        for c in lc:
            # c's second operand is a pure union, try to simplify it against the list ls.
            for (p,i) in c.a2.volumes((c, 1)):
                v = p.a[i]
                vc = -v
                for lse in ls:
                    if v == lse:
                        # the whole compound volume can be skipped. For the intersection operation,
                        # this is like intersect with the universal set
                        c.__a2 = -Volume(0)
                        break
                    if vc == lse:
                        # replace -v in p by the empty set:
                        if i == 0:
                            p.__a1 = Volume(0)
                        elif i == 1:
                            p.__a2 = Volume(0)
                        else:
                            raise ValueError('Index i cannot be other that 0 or 1')

        return res



class SurfaceCollection(Collection):
    """
    Class to describe a collection of simple surfaces (SS) and macrobodies
    (MB).

    One can ask for a surface index using the ``index()`` method of the collection. If a surface
    passed to this method is not in the collecion yet, it is
    added with a unique index. 

    The ``index()`` method adds only the surfaces (or facets of MB) that
    are not already in the collection.

    The ``index()`` method can take as argument an instance of the
    Surface class, or arguments valid for the ``Surface()`` constructor.

    When a SS is added to the collection, it is compared to the previously
    added surfaces, including MB facets. Only if it is not found, a new entry is
    added to the collection.

    When a MB is added to the collection, it is compared to the previously
    added SSs, MBs and MB facets. If all facets of MB are allready defined,
    nothing is added. If some of the facets are defined and some are not, the
    missing facets are added as simple surfaces.  If none of the MB facets are
    defined, the MB is added to the collection as MB.

    """
    def index(self, s, **kwargs):
        """
        Returns the ID of the surface s.

        If s or some of its facets are not in the collection, they are added with a unique ID.

        """
        surf = self._prepare_surface(s, **kwargs)
        vID = self._find(surf)
        if vID is None:
            if surf.is_macrobody():
                # MB surf was not found in the collection. Check its facets
                vID = surf.volume(self._find) # vID by facets
                Lst = vID.surfaces()
                if None in Lst:
                    # some or all facets were not defined yet.
                    if set(Lst) == set([None]):
                        # there is no facet defined previously.
                        # one can define surf as MB
                        vID = self._add(surf)
                    else:
                        # there are some facets already defined.
                        # Add missing facets as simple surfaces.
                        for v in surf.facets():
                            self.index(v.a1[1])
                        vID = surf.volume().copy(self._find)
            else:
                vID = self._add(surf)
        return vID

    def _prepare_surface(self, surf=None, **kwargs):
        """
        If surf is not of the Surface class, pass it and kwargs to the Surface
        constructor.
        """
        if not isinstance(surf, Surface):
            return Surface(surf, **kwargs)
        else:
            return surf

    def _add(self, surf):
        """
        Adds unconditionally surf to the dictionary. If surf is a MB, adds also
        its facets.

        >>> sS = SurfaceCollection()
        >>> print sS._add(Surface('pz 1'))
        1
        >>> print sS._add(Surface('pz 2'))
        2
        >>> print sS._add(Surface('rpp 0 1 2 3 4 5'))
        3
        >>> print sS
        1 pz  1.0
        2 pz  2.0
        3 rpp  0.0  1.0  2.0  3.0  4.0  5.0
        >>> for s in sS.cards(lambda x: True):
        ...     print s
        ...
        1 pz  1.0
        2 pz  2.0
        3 rpp  0.0  1.0  2.0  3.0  4.0  5.0
        3.1 px  1.0
        -3.2 px  0.0
        3.3 py  3.0
        -3.4 py  2.0
        3.5 pz  5.0
        -3.6 pz  4.0
        """
        vID = super(SurfaceCollection, self)._add(surf, mapping = lambda x: Volume(1, x))

        # add facet surfaces, if there are any:
        flist = surf.facets() # list of facet volumes.
        ll = len(flist)
        if ll > 1:
            # surf is a MB. Add their facets.
            for (i, f) in zip(range(ll), flist):
                fID = Volume(f.a1[0], '{0}.{1}'.format(vID.a1[1], i+1))
                self._Collection__d[fID] = flist[i].a1[1]
        return vID

    def cards(self, filter_=lambda ID: isinstance(ID, int), formatted=True):
        """
        Returns a list of surface cards to represent surfaces in the collection
        in an MCNP input file.

        Optional argument ``filter_`` specifies a boolean-valued mapping, which
        defines whether to print surface with index ID passed to the mapping,
        or not.

        By default it filters out the facets of MBs.

        If the optional argument formatted set to True (default),
        the surface cards are splitted to several lines to fit to
        80 characters, allowed by the MCNP input file syntax.
        """
        res = []
        for (ID, s) in sorted(self.items(), key=lambda x:x[0].a1[1]):
            n = ID.a1[1]
            if filter_(n):
                res.append(str(s).format(ID))
        return res

    def __str__(self):
        return '\n'.join(self.cards(formatted=True))



