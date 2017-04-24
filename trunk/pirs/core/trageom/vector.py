
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


from math import atan, acos, copysign, cos, sin, pi

#: Pi/2
pi2 = pi*0.5

# machine epsilon. Used to compare vectors and test if objects belong to other.
from sys import float_info
_E = float_info.epsilon
# _E = pow(2, -53)

# check if two values are close to each other
def _are_close(v1, v2, epsilon_multiplier=10., rel_err=None, abs_err=None):
    """
    Checks if v1 is close to v2. 
    
    Should be used instead of v1 == v2, which works bad for float operands. 
    
    Returns True, if |v1-v2| less or equal than max(v1, v2, 1) multiplied with
    machine epsilon. The latter is taken form sys.float_info.

    >>> v1 = 0.3
    >>> v2 = 0.1 + 0.1 + 0.1
    >>> v1 == v2
    False
    >>> _are_close(v1, v2)
    True
    """
    # First, check if v1 and v2 are equal, and if not, check if they are within machine epsilon
    if v1 == v2: 
        return True
    else:
        if rel_err != None:
            vmax = float(max( abs(v1), abs(v2) ))
            return abs(v1 - v2) <= rel_err * vmax
        if abs_err != None:
            return abs(v1 - v2) <= abs_err

        vmax = float(max( abs(v1), abs(v2), 1. ))
        return abs(v1 - v2)/vmax <=  _E * epsilon_multiplier

def _theta(x, y):
    """
    Returns the angle between the x-axis and the vector (x,y), in radians.

    The atan function to calculate theta as atan(y/x) cannot be used for x = 0. This case is
    processed separately:

    >>> x, y = 0., 5.
    >>> atan(y/x)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: float division by zero

    >>> _theta(x, y)    #doctest: +ELLIPSIS
    1.5707...

    In the case both y and x are zero, theta is also zero by definition,

    >>> _theta(0., 0.)
    0.0

    Also the case when y is zero and x not, is treated separately:

    >>> x, y = 5., 0.
    >>> atan(y/x)
    0.0
    >>> _theta(x,  y)
    0.0
    >>> _theta(x, -y)
    0.0

    In the case when x and y are non-zero, the resulting value lies in [0, 2pi]:

    >>> _theta( 1.,  1.)   #doctest: +ELLIPSIS
    0.785...
    >>> _theta(-1.,  1.)   #doctest: +ELLIPSIS
    2.356...
    >>> _theta(-1., -1.)   #doctest: +ELLIPSIS
    3.926...
    >>> _theta( 1., -1.)   #doctest: +ELLIPSIS
    5.497...
    
    """
    if x == 0. and y == 0.:
        # By default, this means theta = 0, i.e. zero
        # vector looks to x axis.
        t = 0.
    elif x == 0.:
        # in this case y is nonzero and theta is +-pi/2
        t = copysign( pi2, y) 
    elif y == 0.:
        # in this case x is nonzero and theta is 0 or pi
        if x > 0.:
            t = 0.
        else:
            t = pi
    else:
        # nondegenerated case,  both x and y are nonzero. Use atan()
        t = atan( y/x )
        if x < 0. and y > 0.:
            t = t + pi
        elif x < 0. and y < 0.:
            t = t + pi
    if 0. < t < pi2: return t
    else:            return _base_theta(t)

def _phi(r, z):
    """
    Returns the angle between the z-axis and the vector with cylinder coordinates (r,z).

    A zero vector "looks" to the x-axis, i.e. _phi is pi/2

    >>> _phi(0., 0.)  #doctest: +ELLIPSIS
    1.570...

    The resulting angle lies in the interval [0, pi]:

    >>> _phi(0., 1.)
    0.0
    >>> _phi(1., 1.)   #doctest: +ELLIPSIS
    0.785...
    >>> _phi(1., -1.)  #doctest: +ELLIPSIS
    2.356...
    >>> _phi(-1., -1.) # negative r makes no sensebut can be used. #doctest: +ELLIPSIS
    2.356...
    >>> _phi(0., -1.) #doctest: +ELLIPSIS
    3.141...
    """
    if r == 0. and z == 0.:
        # By default, set phi=pi/2, i.e. zero vector looks to x axis (see above
        # for theta)
        p = pi2
    elif z == 0.:
        # here x and/or y are nonzero, therefore phi is pi/2.:
        p = pi2
    elif r == 0.:
        # here x and y are zero and z is nonzero. Phi can be 0 or pi.
        if z > 0.:
            p = 0.
        else:
            p = pi
    else:
        # nondegenerate case. use atan to get phi:
        p = atan( r/z )
        if z < 0.:
            p = p + pi
    if 0. < p < pi: return p
    else:           return _base_phi(p)

def _cossin(a):
    """Returns a tuple with cos(a) and sin(a).

    Standard functions cos() and sin() give, in some cases, non-exact results.
    Particularly, instead of returning exact zero, cos(pi/2) and sin(pi) return
    small but nonzero values. At the same time, sin(pi/2) and cos(pi) give exact
    1.

    >>> for c in [0, 1./4, 1./2, 1, 3./2, 2]:
    ...     a = pi*c
    ...     print '{0:3.2f} {1:9.1e}  {2:9.1e} {3[0]:9.1e} {3[1]:9.1e}'.format(c, cos(a), sin(a), _cossin(a))
    ...
    0.00   1.0e+00    0.0e+00   1.0e+00   0.0e+00
    0.25   7.1e-01    7.1e-01   7.1e-01   7.1e-01
    0.50   6.1e-17    1.0e+00   0.0e+00   1.0e+00
    1.00  -1.0e+00    1.2e-16  -1.0e+00  -0.0e+00
    1.50  -1.8e-16   -1.0e+00  -1.8e-16  -1.0e+00
    2.00   1.0e+00   -2.4e-16   1.0e+00   0.0e+00

    """
    a = a % (2*pi)
    if a < pi:
        # use sin
        s = sin( a )
        c = (1. - s**2.)**0.5
        # cos(a) for a in 0,pi can take positive or negative values.
        c = copysign(c, pi2-a)
    else:
        # use cos:
        c = cos( a )
        # sin(a) for a in pi,2pi is allways negative
        s = -(1. - c**2.)**0.5
    return (c,s)        

def _car2(x, y, z):
    """
    Given cartesian coordinates x, y, z, returns a 4-tuple with coordinates in cylindrical and spherical systems.

    >>> r,t,R,p = _car2( 0,0,0 ) # zero vector "looks" along x-axis.
    >>> r                        # radius in cylinder CS
    0.0
    >>> t                        # angle theta in cylinder CS
    0.0
    >>> R                        # radius in spherical CS
    0.0
    >>> p                        # angle phi in spherical CS #doctest: +ELLIPSIS
    1.57...
    """
    r = (x**2. + y**2.)**0.5

    t = _theta(x, y)

    R = (r**2 + z**2)**0.5
    p = _phi(r, z)
    return (r,t,R,p)            

def _cyl2(r,t,z):
    """
    Given cylindrical coordinates r, t, z, returns a 4-tuple with coordinates in  cartesian and spherical systems.

    >>> x,y,R,p = _cyl2(0,0,0)
    >>> x,y
    (0.0, 0.0)
    >>> R, p                    #doctest: +ELLIPSIS
    (0.0, 1.57...)

    """
    x,y = _cossin(t)
    x *= r
    y *= r

    R = (r**2 + z**2)**0.5
    p = _phi(r, z)

    return (x,y,R,p)            


def _sph2(R,t,p):
    """
    Given shperical coordinates R, t, p, returns a 4-tuple with coordinates in cartesian and cylindrical systems.

    >>> x,y,r,z = _sph2(0,0,pi2)     # zero vector in direction of x-axis
    >>> x, y
    (0.0, 0.0)
    >>> r, z
    (0.0, 0.0)

    """
    # for p=pi/2, sin(p) gives exact result, while cos(p) gives 6.123e-17.
    # I avoid here the usage of cos():
    z,r = _cossin(p)
    z *= R
    r *= R

    x,y = _cossin(t)
    x *= r
    y *= r

    return (x, y, r, z)

def _base_theta(t):
    """
    Returns the base value of angle t, i.e., which lies in the interval [0, 2pi).
    
    >>> _base_theta(0.)
    0.0
    >>> _base_theta(pi)    #doctest: +ELLIPSIS  
    3.14159...
    >>> _base_theta(pi + 2*pi)    #doctest: +ELLIPSIS  
    3.14159...
    >>> _base_theta(2*pi)
    0.0
    """
    return t % (2*pi)

def _base_phi(p):
    """
    Returns the base value of angle phi, i.e. which lies in the interval [0,pi].
    
    >>> _base_phi(0.)
    0.0
    >>> _base_phi(pi2)        #doctest: +ELLIPSIS
    1.57...
    >>> _base_phi(pi)         #doctest: +ELLIPSIS
    3.14159...
    >>> _base_phi(pi +2*pi)   #doctest: +ELLIPSIS
    3.14159...

    """
    p = p % (2*pi)
    if p > pi:
        p = 2*pi - p
    return p    

class Vector3(object):
    """Vector in three-dimensional space. 
    
    Coordinate conversion between cartesian (car), cylindrical (cyl)  and
    spherical (sph) coordinate systems is performed "on demand", i.e. when
    values of these coordinates are inquired by user.

    Vectors are created by specifying a 3-tuple containing coordinates in
    cartesian, cylinder, or spherical coordinate system (CS):

    >>> v1 = Vector3(  car=(1, 0, 0) )     # cartesian coordinates
    >>> v2 = Vector3(  cyl=(1, 0, 0) )     # cylinder coordinates
    >>> v3 = Vector3(  sph=(1, 0, pi2))    # spherical coordinates (pi2 is defined in the module as pi2 = pi/2)

    The order of values in tuples is the following::

        (x, y, z)       # for cartesian CS
        (r, theta, z)   # for cylinder CS
        (R, theta, phi) # for spherical CS

    Coordinates R and r used in the spherical and cylinder CS, have different meaning:
    R is the vector's length, r is the length of vector's projection onto xy plane.    

    If the type of coordinate system is not given explicitly, the cartesian is
    assumed. The following two definitions are equal:

    >>> v4 = Vector3(     (1, 0, 0)) 
    >>> v5 = Vector3( car=(1, 0, 0))
    >>> v4 == v5
    True

    If incomplete tuples are specified, they are augmented by zeroes:

    >>> v1 = Vector3((1,))
    >>> v2 = Vector3((1, 0, 0))
    >>> v1 == v2
    True

    If the 'car' argument is another Vector3 object, its copy is returned.
    This is to make Vector3() method a type convertor. 

    >>> v1 = Vector3( (1, 2, 3) )
    >>> v2 = Vector3( v1 )
    >>> v1 == v2
    True
    >>> v1 is v2
    False

    If no arguments are specified in the constructor, the argument car=(0,0,0) is
    assumed:

    >>> print Vector3()
    car (x=0, y=0, z=0)

    After a vector instance is created, their coordinates can be accessed by
    attributes x, y, z, r, t, R, p, which mean one of the coordinate in cartesian
    (x,y,z), cylindrical (r, t[heta], z), or spherical (R[ho], t[heta], p[hi])
    systems.

    >>> v = Vector3( (1,1,1) )
    >>> v.x, v.y, v.z            # cartesian coordinates
    (1.0, 1.0, 1.0)
    >>> v.r, v.t, v.z            # cylinder coordinates #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    (1.414...,  0.785...,  1.0)
    >>> v.R, v.t, v.p            # shperical coordinates #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    (1.732...,  0.785...,  0.955...)

    After a vector instance is created, it has at least one set of coordinates.
    Thus, they always can be used to get the coordinates in another system.

    The transition from one coordinate system to another is performed when a
    coordinate is set.  For example, 

       >>> v = Vector3( (0,0,0) )   
       >>> v.r                      
       0.0
       >>> v.r = 3

    In the first line, a vector instance is created. Since the cartesian
    coordinates are given (by default), the internal representation of the vector v
    uses cartesian system. In the second line, the radius in the cylindrical CS is
    requested. This results internaly in calculation of the coordinates in the
    cylindrical system, but the internal representation is still uses cartesian
    coordinates. In the third line, the cylundrical radius is set. Now, the
    internal representation is changed from cartesian to cylindrical.

    Each time a coordinate is read, it is recalculated from the internal
    representation. Each time coordinate of a new system is set, first the new
    system coordinates are updated using the current coordinate system and then the
    new coordinate is set and the internal system is changed.
    """

    ###   def __new__(cls, arg=None, *args, **kargs):
    ###       """
    ###       This method is necessary when existing Vector3 instance is passed
    ###       to the class constructor,
    ###           v1 = Vector3()
    ###           v2 = Vector3 (v1 )

    ###       The call to Vector3(v) acts also as type conversion. In the case v
    ###       is allready of type Vector3, a new instance is returned, i.e. 
    ###           Vector3(v)  is  v   =   False
    ###           Vector3(v) ==   v   =   True

    ###       """    
    ###       if isinstance(arg, cls):
    ###           # if the argument is of type Vector3, make copy of it.
    ###           return arg.copy()
    ###       # Otherwise, call the pre-class constructor    
    ###       return object.__new__(cls)

    @classmethod
    def Zero(cls):
        """
        Returns zero vector with cartesian internal coordinate system.

        >>> v1 = Vector3.Zero()
        >>> v2 = Vector3()
        >>> v3 = Vector3( car=(0,0,0) )
        >>> v1 == v2
        True
        >>> v2 == v3
        True
        
        """
        return cls( car=(0., 0., 0.) )

    @classmethod
    def UnitX(cls):
        """Returns unit vector along X axis"""
        return cls( car=(1., 0., 0.) )
    @classmethod
    def UnitY(cls):
        """Returns unit vector along Y axis"""
        return cls( car=(0., 1., 0.) )
    @classmethod
    def UnitZ(cls):
        """Returns unit vector along Z axis"""
        return cls( car=(0., 0., 1.) )

    ###   def __init__(self, car=None, cyl=None, sph=None):
    ###       if isinstance(car, self.__class__):
    ###           # in this case, the __new__ method returns a copy of it. 
    ###           # In this case nothing to do.
    ###           ###   pass
    ###           raise ValueError('Use of Vector3(Vector3()) deprecated. To copy use Vector3().copy()')
    ###           if car.__cs == 'car':
    ###               self.__z = car.__z
    ###               self.__y = car.__y
    ###               self.__x = car.__x
    ###           elif car.__cs == 'cyl':
    ###               self.__z = car.__z
    ###               self.__t = car.__t
    ###               self.__r = car.__r
    ###           else:
    ###               self.__p = car.__p
    ###               self.__t = car.__t
    ###               self.__R = car.__R
    ###           self.__cs = car.__cs
    ###       else:
    ###           self.set(car, cyl, sph)
    ###       return

    ###   def set(self, car=None, cyl=None, sph=None):
    def __init__(self, car=None, cyl=None, sph=None):
        """
        Sets coordinates of the vector. 
        
        Arguments car, cyl or sph must be a tuple specifying coordinates in the
        cartesian, cylinder or spherical coordinate systems, respectively.

        If the passed tuple contains less than 3 elements, it is augmented with
        zeroes.
        """
        if car != None:
            self.__cs = 'car'
            if len(car) < 3: car = car + (0.,0.) 
            self.__z = float(car[2])
            self.__y = float(car[1])
            self.__x = float(car[0])
        elif cyl != None:
            self.__cs = 'cyl'
            if len(cyl) < 3: cyl = cyl + (0.,0.)
            self.__z = float(cyl[2])
            self.__t = float(cyl[1])
            self.__r = float(cyl[0])
        elif sph != None:
            self.__cs = 'sph'
            if len(sph) < 3: sph = sph + (0.,0.)
            self.__p = float(sph[2])
            self.__t = float(sph[1])
            self.__R = float(sph[0])
        else:
            self.__cs = 'car'
            self.__z = 0.
            self.__y = 0. 
            self.__x = 0. 
        self.__rehash = True
        return

    def copy(self):
        """
        Returns a new instance with the same coordinates

        >>> v1 = Vector3((1,2,3))
        >>> v2 = v1.copy()
        >>> v1 is v2, v1 == v2
        (False, True)
        """
        if   self.__cs == 'car': new = Vector3( car=(self.__x, self.__y, self.__z) )
        elif self.__cs == 'cyl': new = Vector3( cyl=(self.__r, self.__t, self.__z) )
        elif self.__cs == 'sph': new = Vector3( sph=(self.__R, self.__t, self.__p) )
        return new

    def __all_coords(self):
        """
        Returns a 7-tuple of coordinates in all CS, (x,y,z,r,t,R,p)
        """
        if self.__cs == 'car':
            r,t,R,p = _car2(self.__x, self.__y, self.__z)
            x = self.__x
            y = self.__y
            z = self.__z
        elif self.__cs == 'cyl':
            x,y,R,p = _cyl2(self.__r, self.__t, self.__z)
            r = self.__r
            t = self.__t
            z = self.__z
        elif self.__cs == 'sph':
            x,y,r,z = _sph2(self.__R, self.__t, self.__p)
            R = self.__R
            t = self.__t
            p = self.__p
        #       0  1  2  3  4  5  6    
        return (x, y, z, r, t, R, p)

    @property
    def x(self):
        """
        Returns x coordinate in cartesian CS.
        
        When x is set, the vector internal representation is changed to
        cartesian (thus x, y and z are computed from cyl. or sph coordinates),
        and then new value is set to x.
        
        >>> Vector3( (1,1,1) ).x                   #doctest: +ELLIPSIS
        1.0
        >>> Vector3(cyl=(2**0.5, pi/4, 1.)).x      #doctest: +ELLIPSIS
        1.00...
        >>> Vector3(sph=(2**0.5, pi/4, pi/2)).x    #doctest: +ELLIPSIS
        1.00...

        >>> v = Vector3( sph=(1,0,0) )
        >>> v.x = 1
        >>> print v
        car (x=1, y=0, z=1)

        >>> v = Vector3( cyl=(2**0.5, pi/4, 1))
        >>> v.x = 4
        >>> print v
        car (x=4, y=1, z=1)
        
        """
        if self.__cs is 'car':
            return self.__x
        else:
            return self.__all_coords()[0]

    @x.setter
    def x(self, v):
        if self.__cs is 'car':
            self.__x = v
        else:
            c = self.__all_coords()
            self.__x = v
            self.__y = c[1]
            self.__z = c[2]
            self.__cs = 'car'
        self.__rehash = True

    @property
    def y(self):
        """
        Returns y coordinate in cartesian CS.
        
        When y is set, the vector internal representation is changed to
        cartesian (thus x, y and z are computed from cyl. or sph coordinates),
        and then new value is set to y.

        >>> Vector3( (1,1,1) ).y                   #doctest: +ELLIPSIS
        1.0
        >>> Vector3(cyl=(2**0.5, pi/4, 1.)).y      #doctest: +ELLIPSIS
        1.0
        >>> Vector3(sph=(2**0.5, pi/4, pi/2)).y    #doctest: +ELLIPSIS
        1.0

        >>> v = Vector3( sph=(1,0,0) )
        >>> v.y = 1
        >>> print v
        car (x=0, y=1, z=1)

        >>> v = Vector3( cyl=(2**0.5, pi/4, 1))
        >>> v.y = 4
        >>> print v
        car (x=1, y=4, z=1)
        """
        if self.__cs is 'car':
            return self.__y
        else:
            return self.__all_coords()[1]

    @y.setter
    def y(self, v):
        if self.__cs is 'car':
            self.__y = v
        else:
            c = self.__all_coords()
            self.__x = c[0]
            self.__y = v
            self.__z = c[2]
            self.__cs = 'car'
        self.__rehash = True

    @property
    def z(self):
        """
        Returns z coordinate in cartesian or cylinder CS.
        
        When z is set in a vector with spherical internal representation, the
        new CS will be cartesian. In other cases, i.e. when z is set to a
        cartesian or cylinder vector, its type is not changed.
        
        >>> Vector3( (1,1,1) ).z                   #doctest: +ELLIPSIS
        1.0
        >>> Vector3(cyl=(2**0.5, pi/4, 1.)).z      #doctest: +ELLIPSIS
        1.0
        >>> Vector3(sph=(2**0.5, pi/4, pi/2)).z    #doctest: +ELLIPSIS
        0.0

        >>> v = Vector3( sph=(1,0,pi/2) )
        >>> v.z = 1
        >>> print v
        car (x=1, y=0, z=1)

        >>> v = Vector3( cyl=(2**0.5, pi/4, 1))
        >>> v.z = 4
        >>> print v                                #doctest: +ELLIPSIS
        cyl (r=1.41..., t=0.785..., z=4)
        """
        if self.__cs in ['car', 'cyl']:
            return self.__z
        else:
            return self.__all_coords()[2]

    @z.setter
    def z(self, v):
        if self.__cs in ['car', 'cyl']:
            self.__z = v
        else:
            c = self.__all_coords()
            self.__x = c[0]
            self.__y = c[1]
            self.__z = v
            self.__cs = 'car'
        self.__rehash = True            

    @property
    def r(self):
        """r coordinate in cylinder CS.
        
        When r is set, the vector internal representation is changed to
        cylinder (thus r, t and z are computed from cartesian or spherical coordinates),
        and then new value is set to r."""
        if self.__cs is 'cyl':
            return self.__r
        else:
            return self.__all_coords()[3]

    @r.setter
    def r(self, v):
        if self.__cs is 'cyl':
            self.__r = v
        else:
            c = self.__all_coords()
            self.__r = v
            self.__t = c[4]
            self.__z = c[2]
            self.__cs = 'cyl'
        self.__rehash = True

    @property
    def t(self):
        """t (theta) coordinate in cylinder CS.
        
        When t is set to a vector with cylinder or spherical coordinates, the
        internal CS is not changed.  If t is set to a vector with cartesian
        coordinates, the spherical coordinates are computed from cartesian, and
        than the new value is set to t."""
        if self.__cs in ['cyl', 'sph']:
            return self.__t
        else:
            return self.__all_coords()[4]

    @t.setter
    def t(self, v):
        if self.__cs in ['cyl', 'sph']:
            self.__t = v
        else:
            c = self.__all_coords()
            self.__R = c[5]
            self.__t = v
            self.__p = c[6]
            self.__cs = 'sph'
        self.__rehash = True

    @property
    def R(self):
        """R coordinate in spherical CS.
        
        When R is set, the vector internal representation is changed to
        spherical (thus R, t and p are computed from cartesian or cylinder coordinates),
        and then new value is set to R."""
        if self.__cs is 'sph':
            return self.__R
        else:
            return self.__all_coords()[5]

    @R.setter
    def R(self, v):
        if self.__cs is 'sph':
            self.__R = v
        else:
            c = self.__all_coords()
            self.__R = v
            self.__t = c[4]
            self.__p = c[6]
            self.__cs = 'sph'
        self.__rehash = True

    @property
    def p(self):
        """p (phi) coordinate in spherical CS.
        
        When p is set, the vector internal representation is changed to
        spherical (thus R, t and p are computed from cartesian or cylinder coordinates),
        and then new value is set to p."""
        if self.__cs is 'sph':
            return self.__p
        else:
            return self.__all_coords()[6]

    @p.setter
    def p(self, v):
        if self.__cs is 'sph':
            self.__p = v
        else:
            c = self.__all_coords()
            self.__R = c[5]
            self.__t = c[4]
            self.__p = v
            self.__cs = 'sph'
        self.__rehash = True


    @property
    def car(self):
        """
        Returns a 3-tuple with cartesian coordinates, (x, y, z).
        """
        if self.__cs is 'car':
            return (self.__x, self.__y, self.__z)
        else:
            # c = self.__all_coords()
            # return (c[0], c[1], c[2])
            return self.__all_coords()[:3]

    @property
    def cyl(self):
        """
        Returns a 3-tuple with cylinder coordinates, (r, t, z).
        """
        if self.__cs is 'cyl':
            return (self.__r, self.__t, self.__z)
        else:
            c = self.__all_coords()
            return (c[3], c[4], c[2])

    @property
    def sph(self):
        """
        Returns a 3-tuple with spherical coordinates, (R, t, p).
        """
        if self.__cs is 'sph':
            return (self.__R, self.__t, self.__p)
        else:
            c = self.__all_coords()
            return (c[5], c[4], c[6])

    @property
    def all(self):
        """
        Returns a 7-tuple of coordinates in all systems, (x, y, z, r, t, R, p)
        """
        return self.__all_coords()

    @property
    def card(self):
        """
        Returns a dictionary with cartesian coordinates, {'x':x, 'y':y, 'z':z}.
        """
        x,y,z = self.car
        return {'x':x, 'y':y, 'z':z}

    @property
    def cyld(self):
        """
        Returns a dictionary with cylinder coordinates, {'r':r, 't':t, 'z':z}.
        """
        r,t,z = self.cyl
        return {'r':r, 't':t, 'z':z}

    @property
    def sphd(self):
        """
        Returns a dictionary with spherical coordinates, {'R':R, 't':t, 'p':p}.
        """
        R,t,p = self.sph
        return {'R':R, 't':t, 'p':p}

    @property
    def alld(self):
        """
        Returns a dictionary with coordinates in all systems,:: 

            {'x':x, 'y':y, 'z':z, 'r':r, 't':t, 'R':R, 'p':p}
        """
        x, y, z, r, t, R, p = self.__all_coords()
        return {'x':x, 'y':y, 'z':z, 'r':r, 't':t, 'R':R, 'p':p}

    def __getitem__(self, coordinate):
        """
        Returns value of coordinate, specified as a character::

            >>> v = Vector3()
            >>> v['x'] == v.x
            >>> v['y'] == v.y

        The expression v[c] is equal to v.alld[c].

        """
        return self.alld[coordinate]



    @property
    def own(self):
        """
        Returns a 3-tuple with coordinates in the internal CS.
        """
        if   self.__cs == 'car': return self.car
        elif self.__cs == 'cyl': return self.cyl
        elif self.__cs == 'sph': return self.sph

    def __add__(self, othr):
        """
        Method calculates the sum of two vectors. A new instance is returned,
        with cartesian coordinates.

        >>> v1 = Vector3.UnitX()
        >>> v2 = Vector3.UnitY()
        >>> print v1 + v2
        car (x=1, y=1, z=0)
        """
        # if othr is not of Vector3 type, it has no attributes x, y, and z.
        # This will cause the AttributeError. More logically, however, if the
        # addition will raise the TypeError, like, for example the command
        # 'abc' + 3.  THerefore, I substitute with this try-except construction
        # AttributeError with TypeError.
        ###   if not isinstance(othr, Vector3):
        ###       othr = Vector3(othr)
        try:
            # calculations are performed in cartesian CS
            x,y,z = self.car
            X,Y,Z = othr.car
        except AttributeError:
            raise TypeError('Cannot add ' + repr(othr) + ' to ' + repr(self) )
        return Vector3( car=(x+X,y+Y,z+Z) )

    def __radd__(self, othr):
        return self + othr

    def __neg__(self):
        """
        This method returns the -self vector. This is used to define
        subtraction of vectors, see __sub__.
        """
        # About the usage of try-except construction, see comment in __add__ method.
        try:
            if self.__cs == 'car':
                r = Vector3( car=(-self.__x, -self.__y,      -self.__z     ) )
            if self.__cs == 'cyl':
                r = Vector3( cyl=( self.__r,  self.__t + pi, -self.__z     ) )
            if self.__cs == 'sph':
                r = Vector3( sph=( self.__R,  self.__t + pi, pi - self.__p ) )
        except AttributeError:
            raise TypeError
        return r

    def __sub__(self, othr):
        return self + (-othr)

    def __rsub__(self, othr):
        return -self + othr

    def __mul__(self, v):
        """
        Multiplication by a scalar.
        """
        if self.__cs == 'car':
            res = Vector3( car=(self.__x*v, self.__y*v, self.__z*v) )
        elif self.__cs == 'cyl':
            res = Vector3( cyl=(self.__r*v, self.__t,   self.__z*v) )
        elif self.__cs == 'sph':
            res = Vector3( sph=(self.__R*v, self.__t,   self.__p  ) )
        return res

    def __div__(self, v):
        """divide by scalar"""
        return self * (1./v)

    def __rmul__(self, v):
        return self * v

    def __eq__(self, othr):
        # compare taking into account machine epsilon, see function _are_close() above.
        if not isinstance(othr, Vector3): 
            return False

        # compare in the coordinate system of self:
        c1 = self.__all_coords()
        c2 = othr.__all_coords()
        if self.__cs == 'car':
            return ( _are_close(c1[0], c2[0])  and
                     _are_close(c1[1], c2[1])  and
                     _are_close(c1[2], c2[2]))
        elif self.__cs == 'cyl':
            t1 = _base_theta(c1[4])
            t2 = _base_theta(c2[4])
            return ( _are_close(c1[3], c2[3])  and
                     _are_close(   t1,    t2)  and
                     _are_close(c1[2], c2[2]))
        else:
            t1 = _base_theta(c1[4])
            t2 = _base_theta(c2[4])
            p1 = _base_phi(c1[6])
            p2 = _base_phi(c2[6])
            return ( _are_close(c1[5], c2[5])  and
                     _are_close(   t1,    t2)  and
                     _are_close(   p1,    p2))

    def __ne__(self, othr):
        return not self == othr


    def dot(self, othr):
        """scalar product"""
        r = 0.
        for (c1,c2) in zip(self.car, othr.car):
            r += c1*c2
        return r

    def __hash__(self):
        """
        Returns hash(t), where t is a tuple containing the name of the internal
        CS followed by correspondent coordinates.

        The flag '__rehash' is used to decrease the number of hash(t)
        evaluations. This flag is set to True (meaning to reevaluate hash(t)),
        if any of coordinates are changed.  After the hash(t) value is
        obtained, it is saved to __hash for later use, and flag __rehash set to
        False.
        """
        if self.__rehash: 
            t =  (self.__cs,)
            if self.__cs == 'car': t += self.car
            if self.__cs == 'cyl': t += self.cyl
            if self.__cs == 'sph': t += self.sph
            self.__hash = hash(t)
            self.__rehash = False
        return self.__hash

    def cross(self, othr):
        """Vector product"""
        a = self.car
        b = othr.car
        return Vector3( ( a[1]*b[2] - a[2]*b[1],
                          a[2]*b[0] - a[0]*b[2],
                          a[0]*b[1] - a[1]*b[0]  ) )

    def is_perpendicular(self, othr):
        """ check that two vectors are perpendicular taking into account the machine epsilon."""
        return _are_close( self.dot(othr), 0.)

    def is_parallel(self, othr):
        """check if self and othr are parallel taking into account machine epsilon."""
        return _are_close( self.dot(othr), self.R*othr.R)

#      def is_in_plane(self, P):
#         """
#         Point lies on the plane P if its
#         projection coincides with the point itself:
#         """            
#         op = P._project_point(self, cs='')
#         return  op == self
# 
#     def distance_to_plane(self, P):
#         """project self to P and return length of the vector from self to projection"""
#         pr = P._project_point(self, cs='')
#         return (self - pr).R

    def is_zero(self):
        """return true if length of self is zero"""
        return _are_close(self.R, 0.)

    def is_on_axis(self, axis='x'):
        """ test if self is on axis"""
        a = axis.lower()
        c = self.__all_coords()
        if   a == 'x':
            return _are_close(c[1], 0.) and _are_close(c[2], 0.)
        elif a == 'y':
            return _are_close(c[0], 0.) and _are_close(c[2], 0.)
        elif a == 'z':
            return _are_close(c[0], 0.) and _are_close(c[1], 0.)
        else:
            raise ValueError(axis)

    def __str__(self):
        """
        String representation
        """
        if self.__cs == 'car':
            coords = ' (x=%G, y=%G, z=%G)' % self.car
        if self.__cs == 'cyl':
            coords = ' (r=%G, t=%G, z=%G)' % self.cyl
        if self.__cs == 'sph':
            coords = ' (R=%G, t=%G, p=%G)' % self.sph
        return self.__cs + coords

    def __repr__(self):
        return self.__str__()

    def _arbitrary_normal(self):
        """return arbitrary vector, normal to self."""
        r = self.copy()
        if self.p < pi2:
            r.p += pi2
        else:
            r.p += -pi2
        return r    


