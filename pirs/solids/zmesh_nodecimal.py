
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

# import decimal
# import . solids3
# import . tree
from ..core.trageom.vector import _are_close

def _my_round(value, prec):
    return round(value/prec) * prec

class zmesh(object):
    """Class to represent axial mesh for density, temperature and heat in a solid with Z dimension.

    An axial mesh is defined by giving a solid (A reference solid)and by
    giving relative height of mesh elements (a relative grid).

    When a new instance of zmesh is created, an instance of one of the solids must be
    provided, which will be used to define the absolute height of the mesh
    elements.

        b = Box()       # default box with X,Y,Z = 1
        m = zmesh(b)    # axial mesh m with b as the reference solid. 

    Lenght of mesh elements is specified in relative units. For example,
        
        m.set_grid([0.5, 1., 0.5])

    sets number of mesh elements and their lengths. The argument is a list, which i-th element gives the relative length of the
    i-th mesh element along z axis. The absolute lenght is obtained first by
    normalizing the values in the list, so their sum gives one, and by
    multiplying by the dimension of the reference solid. For the above example,
    mesh elements along z will be 0.25 cm, 0.5 cm and 0.25 cm.
    
    """

    MINIMAL_OFFSET = 1.e-8

    def __init__(self, boundary):
        """Initialize the axial mesh. Boundary must be an object with
        attribute Z, which defines the absolute height of the
        mesh (this is, for example, instance of Box class).

        Initially, there is only one mesh element, and value is set to 0.
        """
        self.__b = boundary
        self.__z = [1.]
        self.__v = [0.]
        self.__p = 0.    # precision

    def __eq__(self, othr):
        if self is othr:
            return True
        if not isinstance(othr, self.__class__):
            return False
        if self.__z != othr.__z:
            return False
        if self.__v != othr.__v:
            return False
        return True

    def __ne__(self, othr):
        return not self == othr 

    @property
    def prec(self):
        return self.__p

    @prec.setter
    def prec(self, val):
        self.__p = float(val)

    def simplify(self):
        """
        Joins adjacent mesh elements if their values are within the precision prec.
        """
        if True: # self.__p != 0.:
            clusters = []
            vprev = self.__v[0]
            clusters.append([(vprev, self.__z[0])])
            for (v, d) in zip(self.__v[1:], self.__z[1:]):
                if abs(vprev - v) <= self.__p:
                    # add v, d to current list of clusters
                    clusters[-1].append((v, d))
                else:
                    # create new clusters entry
                    vprev = v
                    clusters.append([(v, d)])

            znew = []
            vnew = []
            for vdl in clusters:
                d = sum( map(lambda vd: vd[1], vdl) )
                v = sum( map(lambda vd: vd[0]*vd[1], vdl) ) / d
                znew.append(d)
                vnew.append(v)
            self.__z = znew
            self.__v = vnew
        return


    def convert(self, type_=float):
        """
        Converts values saved in zmesh to type_. Argument type_ must be a
        function.
        """
        self.__v = map(type_, self.__v)

    def has_zeroes(self):
        """
        Returns True if self.values() has one or more zeroes.
        """
        for v in self.__v:
            if v == 0.:
                return True
        return False

    def common_grid(self, othr):
        """
        Deprecated. Use unify()
        """
        raise UserWarning('Method deprecated. Use unify()')
        self.unify(othr)
        return


    def copy(self, boundary=None):
        """return copy of self."""
        if boundary is None:
            boundary = self.__b
        c = self.__class__(boundary)
        c.__z = self.__z
        c.__v = self.__v
        c.__p = self.__p
        return c

    def set_grid(self, lst=[1.]):
        """Set relative grid.
        
        lst is a list specifiying the number of grid elements and their
        relative length.
        """
        # currently, allow grid changes only if mesh value is constant.
        if self.is_constant():
            # use the decimal arithmetics:
            # lst = map( decimal.Decimal, lst)
            # remember the value:
            v = self.__v[0]
            # normalize lst:
            nrm = []
            s = float(sum(lst))
            for l in lst:
                nrm.append(l/s)
            # set relative mesh thickness:
            self.__z = nrm[:]
            # redefine dictionary of values:
            self.__v = [v] * len( self.__z )
        else:
            raise ValueError('cannot change grid of a mesh with non-constant values')

    def get_grid(self, rel=True):
        """Returns the list of mesh elements lengths"""
        if rel:
            return self.__z[:]
        else:
            # return list of absolute lenghts
            Z = self.__b.Z
            return map(lambda dz: dz*Z, self.__z)

    def is_constant(self):
        """Returns True if all values of the mesh are equal"""
        v0 = self.__v[0]
        for v in self.__v[1:]:
            if v != v0: return False
        return True            

    def element_coord(self, k=0, cs='rel'):
        """
        Returns coordinates of k-th mesh element's center.
        
        The optional argument cs accepts the following values:

        - 'rel' (default): the returned coordinates are in the coordinate system of
          the reference solid.
        - 'abs': the returned coordinates are in the coordinate system of the root of
          the reference solid.
        - '1': the returned coordinates are relative to the c.s. of the reference solid
          whose height is set to 1.

        Between rel, abs and 1 coordinates hold the following equalities:

            Zabs = Zrel - self.__b.abspos()

            Zrel = Z1 * self.__b.Z

        """
        # the element coordinate can be computed in two ways, which can give
        # different results due to the roundoff error:
        #        1) Xc = sum(xi) * X
        #        2) Xc = sum(xi*X)
        # the first variant is faster, but the second is consistent with the
        # abspos() method.

        # Implementation of the first variant:
        # z = self.__b.Z * ( -0.5 + sum(self.__z[:k])  +  self.__z[k]*0.5 )

        # implementation of the second variant:
        if cs == '1':
            Z = 1. 
        else:
            Z = self.__b.Z
        Z2 = Z * 0.5
        x = 0.
        y = 0.
        z = sum ( [-Z2] + map(lambda o:Z*o, self.__z[:k]) + [self.__z[k]*Z2] )
        z = float(z)
        if cs == 'abs':
            p = self.__b.abspos()
            x += p.x
            y += p.y
            z += p.z
        return (x,y,z)

    def element_coords(self, cs='rel'):
        """
        Returns the list of mesh-elements center coordinates.
        """
        xyz = []
        for k in range(len(self.__z)):
            xyz.append(self.element_coord(k, cs))
        return xyz

    def boundary_coords(self, cs='rel'):
        """
        Returns list of boundary coordinates of the grid. 
        
        The first and last elements in the returned list give coordinates of
        the facet of the reference solid.
        
        >>> b = solids.Box()
        >>> b.pos.z = 6
        >>> m = zmesh(b)
        >>> m.boundary_coords('abs')
        [5.5, 6.5]
        >>> m.boundary_coords('rel')
        [-0.5, 0.5]
        >>> m.set_grid( [1]*4 )
        >>> m.boundary_coords('rel')
        [-0.5, -0.25, 0.0, 0.25, 0.5]
        >>> m.boundary_coords('abs')
        [5.5, 5.75, 6.0, 6.25, 6.5]
        """
        r = [-0.5]

        for v in self.__z:
                r.append( r[-1] + v )
        if cs == 'abs':
            s = self.__b.abspos().z
            C = self.__b.Z
        elif cs == 'rel':
            s = 0.
            C = self.__b.Z
        elif cs == '1':
            s = 0.
            C = 1.
        r = map( lambda x: C*x + s, r)
        return r

    def element_index(self, z=0., cs='rel'):
        """
        Returns the index of the mesh element containing coordinate z, relative
        or absolute.
        """
        if cs == 'abs':
            p = self.__b.abspos()
            z -= p.z
        if cs != '1':
            # go to relative dimensions:
            z = z / self.__b.Z

        for (c, l, mesh) in [(z, 'z', self.__z)]:
            c = z
            l = 'z'
            mesh = self.__z

            if z < -0.5 or z > 0.5: raise IndexError('z coordinate lies outside mesh boundary, z={0}, bounding solid: {1}'.format(z, self.__b.get_key()))
            if z == 0.5           : raise IndexError('z coordinate lies on the mesh boundary, z={0}, bounding solid: {1}'.format(z, self.__b.get_key()))
            lb = -0.5
            for i in range( len(self.__z) ):
                if z == lb: raise IndexError('z coordinate lies on the mesh boundary, z={0}, bounding solid: {1}'.format(z, self.__b.get_key()))
                lb += self.__z[i]
                if z < lb: 
                    res = i
                    break
        return res                

    def set_value_by_coord(self, val, z, cs='rel'):
        """Set value to the mesh element, specified by its z coordinate, relative or absolute.
        
        The value set to the mesh element, which covers the given coordinate."""
        k = self.element_index(z[-1], cs)
        self.__v[k] = val

    def set_value_by_index(self, val, k):
        """Set value to mesh element specified by its index.

        Index is an integer. Counting starts from zero."""
        self.__v[k] = val

    def set_values_by_function(self, f, cs='rel'):
        """Set values of the mesh by function f(z): z -> f.
        
        Value of each mesh element is set to f(z), where z is
        coordinate of the mesh element's center."""
        v = []
        for xyz in self.element_coords(cs):
            v.append( f(xyz[-1]) )
        self.__v = v
        return

    def clear(self):
        """Set grid so that the mesh has only one element and set the value to 0.""" 
        ###  self.set_values(0.)
        ###  self.set_grid()
        self.__z = [1.]
        self.__v = [0.]

    def set_values(self, val, cs='rel'):
        """Set values of the mesh.

        Accepted types of val are:

        - a list or a tuple. Must have the same number of elements as the 
          list returned by the get_grid() method.

        - a mapping (function) used to calculate value at each mesh element center.
          The meaning of the mapping's argument can be set by the method's optional 
          argument cs, its meaning see in element_coord() method.

        - another instance of the zmesh class. In this case, grid and values of this 
          instance are copied to self. This is equal to :

            self.update(othr)

        - if not one of the above, transformed to the list [val]*len(self.get_grid())

        """
        if isinstance(val, list) or isinstance(val, tuple):
            if len(self.__z) == len(val):
                self.__v = list(val[:])
            else:
                raise IndexError('Wron number of elements in ', val)
        elif hasattr(val, '__call__'):
            # val is a function.
            self.set_values_by_function(val, cs)
        elif isinstance(val, zmesh):
            self.update(val)
        else:
            # assume val is the value to be set to all mesh elements.
            self.__v = [val] * len(self.__z)
        return

    def mean(self):
        r = 0.
        for (d, v) in zip(self.__z, self.__v):
            r += d*v
        return r

    def get_max(self, func=None):
        """
        Returns (Vmax, i) tuple, where Vmax is the maximal value, and i --its index.

        When func is given, maximum is searched among func(vi).
        """
        i = 0
        if func is not None:
            v = map(func, self.__v)
        else:
            v = self.__v[:]

        vm = max(v)
        im = v.index(vm)
        coord = self.element_coord(im, 'abs')
        return (vm, coord)

    def get_value_by_coord(self, xyz, cs='rel'):
        """Returns the value of mesh element, specified by the xyz coordinate. 
        
        The value of the mesh element covering point with axial coordinate z is
        returned."""
        bnd = self.boundary_coords(cs)
        z = xyz[-1]

        __v = self.values()

        if z in bnd:
            # z lies on the boundary. return mean of the two adjacent elements.
            k = bnd.index(z)
            v = (__v[k-1] + __v[k] ) * 0.5
        elif bnd[0] < z < bnd[-1]:
            # z is in the range of zmesh
            k = self.element_index(z, cs)
            v = __v[k]
        else:
            # z is outside zmesh. 
            v = 0.
        return v

    def get_value_by_index(self, k):
        """Returns the value of mesh element speficied by its index"""
        return self.values()[k] # values() to ensure that prec is taken into account
        # return self.__v[k]

    def values(self):
        """Returns the list of values in the order described in method set_values()"""
        if self.__p ==  0.:
            return self.__v[:]
        else:
            return map(lambda v: _my_round(v, self.__p), self.__v)

    def items(self, key_type='index', cs='rel'):
        """Returns a list of tuples (k, val) in the order described in method
        set_values().

        If key_type is 'index' (defalut), k is the mesh element index. 
        If key_type is 'coord', k is the mesh
        center's coordinates, k = (x,y,z). In this case one can additionally
        specify coordinate system, 'rel' or 'abs'"""
        r = []
        for k in range(len(self.__z)):
            if key_type == 'index': key = k
            if key_type == 'coord': key = self.element_coord( k, cs )
            r.append( (key, self.values()[k]))
        return r

    def get_solid(self):
        """Returns the reference solid.  """
        return self.__b


    def get_box(self, k, cs='rel'):
        return self.get_solid(k, cs)

    def get_cylinder(self, k, cs='rel'):
        return self.get_solid(k, cs)

    def crop(self, othr):
        """put to self data from othr, so that mesh elements coincide."""
        raise UserWarning('Deprecated method. Use update()')
        self.update(othr)
        return

    def adjust_grid(self, Nmax, dVmin, alpha=1./3.):
        """
        Changes the grid by inserting new mesh elements between elements with maximal dV,
        and by combining elements with dV less than dVmin.

        """
        while len(self.__v) < Nmax:
            # find mesh elements with max difference dV
            dVmax = 0
            for (i, V) in enumerate( zip(self.__v[1:], self.__v[:-1]) ):
                dV = abs(V[0] - V[1])
                if dV > dVmax:
                    imax = i
                    dVmax = dV
            # if dVmax is greater than dVmin, replace 3 adjacent mesh elements with 3:
            if dVmax > dVmin:
                # new mesh
                dz = self.__b[imax] + self.__b[imax+1]
                beta = self.__b[imax] / self.__b[imax+1]
                bnew = self.__b[:]
                bnew.insert(imax+1, alpha*dz)
                bnew[imax+2] = dz*(1.- alpha)/(1. - beta)
                bnew[imax] = dz - bnew[imax+1] - bnew[imax+2]
                # new values for the new mesh elememnts:
                return NotImplemented

    def interpolate(self, z, cs='rel'):
        """
        Returns interpolated value at coordinate z.

        >>> m = zmesh(solids.Box())
        >>> m.set_grid([1]*5)
        >>> m.set_values([1, 2, 3, 4, 5])
        >>> for (x,y,z) in m.element_coords('1'):
        ...     print z, m.interpolate(z, '1')
        ...
        >>> for z in m.boundary_coords('1'):
        ...     print z, m.interpolate(z, '1')
        ...


        """
        if cs == '1':
            pass
        else:
            # put here transform to the '1' cs
            raise NotImplementedError('interpolate not implemented for cs ', cs)

        # linear interpolation:
        i = self.element_index(z, '1')
        (x,y,zc) = self.element_coord(i, '1')
        if z <= zc:
            # interpolate between i-1 and i element:
            (x,y,z1) = self.element_coord(i-1, '1')
            z2 = zc
            y1 = self.__v[i-1]
            y2 = self.__v[i]
        else:
            # interpolate between i and i+1 element:
            z1 = zc
            (x,y,z2) = self.element_coord(i, '1')
            y1 = self.__v[i]
            y2 = self.__v[i+1]
        # parameters of the linear interpolation y = az + b
        # raise ValueError(y1, y2, z1, z2)
        if z1 == z2:
            a = 0.
        else:
            a = (y1 - y2)/(z1 - z2)
        b = 0.5*(y1 + y2 - a*(z1 + z2))
        return (a*z + b)

    def integral(self, A=None, B=None, cs='rel'):
        """
        Returns integral from A to B of the piecewise-constant function.

        cs defines the meaning of A and B. Can be 'rel', 'abs' and '1'.

        >>> m = zmesh(solids.Box(Z=4.))
        >>> m.integral(-0.5, 0.5, '1')
        0.0

        >>> m.set_grid([1]*4)
        >>> m.set_values([1, 2, 3, 4])
        >>> Zlst = [-4.] + map(float, m.boundary_coords('rel')) + map(lambda x: x[2], m.element_coords('rel')) + [4.]
        >>> Zlst.sort()
        >>> print Zlst
        >>> for A in Zlst:
        ...     for B in Zlst:
        ...         print '    {0:7.3f} {1:7.3f}   {2:9.5f}'.format(A, B, m.integral(A, B, 'rel'))
        ...

        >>> m.integral(cs='1')
        >>> m.integral(cs='rel')
        >>> m.integral(cs='abs')

        """
        # process None cases for A and B:
        if A is None:
            # correspondent to the element's lowest z
            A = float(self.boundary_coords(cs)[0])
        if B is None:
            # corresponds to the element's highest z
            B = float(self.boundary_coords(cs)[-1])

        # check that A <= B:
        if A > B:
            A, B = B, A
            direction = -1.
        else:
            direction = 1.
        # we work internaly in the '1' coordinate system.
        if cs == '1':
            zA = A
            zB = B
            pass
        elif cs == 'rel':
            ah = self.__b.Z  # absolute height
            zA = A/ah
            zB = B/ah
        elif cs == 'abs':
            ah = self.__b.Z          # absolute height
            ap = self.__b.abspos().z # absolute position
            zA = (A - ap) / ah
            zB = (B - ap) / ah
        else:
            raise ValueError('Unknown coordinate system ', cs)

        # extended partition
        z = map(float, self.boundary_coords(cs='1'))
        z = z + [max(zB, 0.5) + 1.]
        v = [0.*self.__v[0]] + self.__v + [0.*self.__v[-1]] # multiply zero by one element of __v is to preserve the type.

        # find indices where zA and zB lie:
        iA = 0  # iA: zA in z[iA-1] -- z[iA]
        for zi in z:
            if zi >= zA:
                break
            else:
                iA += 1
        iB = 0  # iB: zB in z[iB-1] -- z[iB]
        for zi in z:
            if zi >= zB:
                break
            else:
                iB += 1
        # print
        # print
        # print '-'*80
        # print zA, zB
        # print iA, iB
        # print (' '*1 + '{:10} '*len(v)).format(*v)
        # print (' '*7 + '{:10} '*len(z)).format(*z)

        if iA == iB:
            res = (zB - zA) * v[iA]
        else:
            res = (z[iA] - zA) * v[iA]
            for i in range(iA+1, iB):
                # print i, z[i-1], z[i], v[i]
                res += (z[i] - z[i-1]) * v[i]
            res += (zB - z[iB-1]) * v[iB]
        # print '-'*80 
        return res * direction * self.__b.Z

    def __mul__(self, othr):
        """
        Multiply by another zmesh object or by scalar.

        >>> z1 = zmesh(solids.Box())
        >>> z1.set_grid([1]*5)
        >>> z1.set_values(range(5))

        >>> z2 = 2.0 * z1
        >>> print z2.values()

        >>> z3 = z2 * z1
        >>> print z3.values()

        >>> z3 = 3.0 + z1
        >>> print z3.values()

        >>> z3 = z3 + z1
        >>> print z3.values()


        """
        operation = lambda x, y: x*y
        if isinstance(othr, zmesh):
            if self.__b.extension('z') != othr.__b.extension('z'):
                raise ValueError('Zmesh boundaries on different axial levels.')
            else:
                # operand 1
                op1 = self.copy()

                # operand 2
                op2 = othr.copy()

                # common_grid changes the state of its operands. THerefore use
                # here op1 and op2 and not original self and othr
                op1.unify(op2)
                op1.set_values(map(operation, op1.__v, op2.__v))
                return op1
        else:
            op1 = self.copy()
            op1.set_values(map(operation, self.__v, [othr]*len(self.__v)))
            return op1

    def __rmul__(self, othr):
        return self * othr

    def __div__(self, othr):
        """
        Divide by another zmesh object or by scalar.

        """
        operation = lambda x, y: x/y
        if isinstance(othr, zmesh):
            if self.__b.extension('z') != othr.__b.extension('z'):
                raise ValueError('Zmesh boundaries on different axial levels.')
            else:
                # operand 1
                op1 = self.copy()

                # operand 2
                op2 = othr.copy()

                # common_grid changes the state of its operands. THerefore use
                # here op1 and op2 and not original self and othr
                op1.unify(op2)
                op1.set_values(map(operation, op1.__v, op2.__v))
                return op1
        else:
            op1 = self.copy()
            op1.set_values(map(operation, self.__v, [othr]*len(self.__v)))
            return op1

    def __add__(self, othr):
        operation = lambda x, y: x+y
        if isinstance(othr, zmesh):
            if self.__b.extension('z') != othr.__b.extension('z'):
                print self.__b.get_key(), self.__b.extension('z')
                print othr.__b.get_key(), othr.__b.extension('z')
                raise ValueError('Zmesh boundaries on different axial levels.')
            else:
                # operand 1
                op1 = self.copy()

                # operand 2
                op2 = othr.copy()

                # common_grid changes the state of its operands. THerefore use
                # here op1 and op2 and not original self and othr
                op1.unify(op2)
                op1.set_values(map(operation, op1.__v, op2.__v))
                return op1
        else:
            op1 = self.copy()
            op1.set_values(map(operation, self.__v, [othr]*len(self.__v)))
            return op1

    def __radd__(self, othr):
        return self + othr

    def __sub__(self, othr):
        operation = lambda x, y: x-y
        if isinstance(othr, zmesh):
            if self.__b.extension('z') != othr.__b.extension('z'):
                raise ValueError('Zmesh boundaries on different axial levels.')
            else:
                # operand 1
                op1 = self.copy()

                # operand 2
                op2 = othr.copy()

                # common_grid changes the state of its operands. THerefore use
                # here op1 and op2 and not original self and othr
                op1.unify(op2)
                op1.set_values(map(operation, op1.__v, op2.__v))
                return op1
        else:
            op1 = self.copy()
            op1.set_values(map(operation, self.__v, [othr]*len(self.__v)))
            return op1

    def __rsub__(self, othr):
        return -(self - othr)

    def __neg__(self):
        res = self.copy()
        res.set_values(map(lambda x: -x, self.__v))
        return res

    def __str__(self):
        """
        Pseudo-graphics representation of the mesh:

        AZ1        AZ2        AZ3        AZ4      ...         AZN
        |   rdz1   |   rdz2   |   rdz3   |   rdz4   |   ...   |
        |   val1   |   val2   |   val3   |   val4   |   ...   |

       where rdzi -- i-th relative delta z, vali -- i-th value, AZi -- absolute i-th boundary coordinate.
        """
        f_d = '{0}'
        f_v = '{0}'
        f_Z = '{0}'

        len_MAX = 10

        delim = '|'
        margin = ' '*4

        zl = self.boundary_coords('abs')
        dl = self.__z[:]
        vl = self.__v[:]

        l1 = '' # first line
        l2 = '' # second line
        l3 = '' # third line
        while dl:
            d = f_d.format(dl.pop(0))
            v = f_v.format(vl.pop(0))
            z = f_Z.format(zl.pop(0))
            len_d = len(d)
            len_v = len(v)
            len_z = len(z)
            len_2 = max(len_d, len_v)
            l1 += z + ' '*len_2 + margin
            l2 += delim + ' '*(len_z-1) + d + ' '*(len_2 - len_d) + margin
            l3 += delim + ' '*(len_z-1) + v + ' '*(len_2 - len_v) + margin
        l2 += delim
        l3 += delim
        l1 += f_Z.format(zl.pop(0))
        return '\n'.join([l2, l3, l1])


    def unify(self, othr, log=False):
        """
        Changes self and othr so that their mesh boundaries coincide.
        """

        # find region where meshes intersect:
        z1min, z1max = self.__b.extension('z')
        z2min, z2max = othr.__b.extension('z')

        if z1min > z2max or z2min > z1max:
            # there is no intersection. Nothing to do.
            return

        if (z1min, z1max) == (z2min, z2max) and self.__z == othr.__z:
            # grids are equal. Nothing to do
            return

        # each mesh is divided to three parts: below intersection, intersection and above intersection.
        l1_l = []   # (l)ower part
        v1_l = []
        l1_m = self.get_grid(False)  # (m)iddle part
        v1_m = self.__v[:]
        l1_u = []   # (u)pper part
        v1_u = []
        l2_l = []
        v2_l = []
        l2_m = othr.get_grid(False)
        v2_m = othr.__v[:]
        l2_u = []
        v2_u = []

        MO = min(self.MINIMAL_OFFSET, othr.MINIMAL_OFFSET)

        if not _are_close(z1min, z2min, abs_err=self.MINIMAL_OFFSET):
            if z1min > z2min:
                l2_l, v2_l, l2_m, v2_m = split_list(l2_m, v2_m, z1min - z2min, MO)
            else:
                l1_l, v1_l, l1_m, v1_m = split_list(l1_m, v1_m, z2min - z1min, MO)
            if log:
                print 'after zmin comparison:'
                print 'l1_l, l1_m, l1_u: ', l1_l, l1_m, l1_u
                print 'l2_l, l2_m, l2_u: ', l2_l, l2_m, l2_u

        if not _are_close(z1max, z2max, abs_err=self.MINIMAL_OFFSET):
            if z1max > z2max:
                l1_m, v1_m, l1_u, v1_u = split_list(l1_m, v1_m, sum(l2_m), MO)
            else:
                l2_m, v2_m, l2_u, v2_u = split_list(l2_m, v2_m, sum(l1_m), MO)
            if log:
                print 'after zmax comparison:'
                print 'l1_l, l1_m, l1_u: ', l1_l, l1_m, l1_u
                print 'l2_l, l2_m, l2_u: ', l2_l, l2_m, l2_u

        if log:
            print 'after zmin and zmax comparison:'
            print 'l1_l, l1_m, l1_u: ', l1_l, l1_m, l1_u
            print 'l2_l, l2_m, l2_u: ', l2_l, l2_m, l2_u
        # find common grid of the intersection part:
        lc_m, v1_m, v2_m = common_grid(l1_m, v1_m, l2_m, v2_m, min(self.MINIMAL_OFFSET, othr.MINIMAL_OFFSET))
        if log:
            print 'lc_m: ', lc_m

        # put new grids to mesh instances:
        self.__z = l1_l + lc_m + l1_u
        self.__v = v1_l + v1_m + v1_u
        othr.__z = l2_l + lc_m + l2_u
        othr.__v = v2_l + v2_m + v2_u
        self._normalize_grid()
        othr._normalize_grid()
        return

    def _normalize_grid(self):
        s = sum(self.__z)
        self.__z = map( lambda d: d/s, self.__z)
        return

    def update(self, othr, log=False):
        # find region where meshes intersect:
        z1min, z1max = self.__b.extension('z')
        z2min, z2max = othr.__b.extension('z')
        if log:
            print 'z1min, z1max: ', z1min, z1max
            print 'z2min, z2max: ', z2min, z2max

        if z1min >= z2max or z2min >= z1max:
            # there is no intersection. Self remains unchanged.
            return

        if (z1min, z1max) == (z2min, z2max) and self.__z == othr.__z:
            # grids are equal. Simply put values from othr to self:
            self.__v = othr.__v[:]
            return

        # self is divided to three parts: below othr, intersection with othr and above othr.
        l_l = []   # (l)ower part
        v_l = []
        l_m = self.get_grid(False)  # (m)iddle part
        v_m = self.__v[:]
        l_u = []   # (u)pper part
        v_u = []
        # grid of othr:
        l2 = othr.get_grid(False)
        v2 = othr.__v[:]

        MO = min(self.MINIMAL_OFFSET, othr.MINIMAL_OFFSET)

        if not _are_close(z1min, z2min, abs_err=self.MINIMAL_OFFSET):
            if z1min < z2min:
                l_l, v_l, l_m, v_m = split_list(l_m, v_m, z2min - z1min, MO)
                z1min = z2min
            else:
                l2, v2 = split_list(l2, v2, z1min - z2min, MO)[2:]
                z2min = z1min
            if log:
                print 'after zmin comparison:'
                print 'l_l, l_m, l_u: ', l_l, l_m, l_u
                print 'v_l, v_m, v_u: ', v_l, v_m, v_u
                print 'l2, v2: ', l2, v2

        if not _are_close(z1max, z2max, abs_err=self.MINIMAL_OFFSET):
            if z1max > z2max:
                l_m, v_m, l_u, v_u = split_list(l_m, v_m, z2max - z2min, MO)
            else:
                l2, v2 = split_list(l2, v2, z1max - z2min, MO)[:2]
            if log:
                print 'after zmax comparison:'
                print 'l_l, l_m, l_u: ', l_l, l_m, l_u
                print 'v_l, v_m, v_u: ', v_l, v_m, v_u
                print 'l2, v2: ', l2, v2

        if log:
            print 'after zmin and zmax comparison:'
            print 'l_l, l_m, l_u: ', l_l, l_m, l_u
            print 'v_l, v_m, v_u: ', v_l, v_m, v_u
            print 'l2, v2: ', l2, v2

        self.__z = l_l + l2 + l_u
        self.__v = v_l + v2 + v_u
        self._normalize_grid()
        return


def split_list(l, v, z, MINIMAL_OFFSET):
    assert len(l) == len(v)
    assert z > 0.
    assert len( filter(lambda d: d < 0., l) ) == 0 # all elements of l are non-negative 
    l1 = []
    l2 = l[:]
    v1 = []
    v2 = v[:]
    while z > 0.:
        d = l2[0]
        if _are_close(d, z, abs_err=MINIMAL_OFFSET):
            l1.append(d)
            l2.pop(0)
            v1.append(v2.pop(0))
            break 
        elif d > z:
            l1.append(z)
            l2[0] -= z
            v1.append(v2[0])
            break
        else:
            l1.append(d)
            l2.pop(0)
            z -= d
            v1.append(v2.pop(0))
    return l1, v1, l2, v2

def common_grid(l1, v1, l2, v2, MINIMAL_OFFSET, log=False):
    """
    Assuming that sum(l1) = sum(l2)
    """
    assert _are_close(sum(l1), sum(l2), abs_err=MINIMAL_OFFSET)
    assert len(l1) == len(v1)
    assert len(l2) == len(v2)
    nl = []
    nv1 = []
    nv2 = []
    l1 = l1[:]
    l2 = l2[:]
    v1 = v1[:]
    v2 = v2[:]
    while l1 or l2:
        if log:
            print
            print l1
            print l2
        d1 = l1[0]
        d2 = l2[0]
        if _are_close(d1, d2, abs_err=MINIMAL_OFFSET):
            nl.append(d1)
            l1.pop(0)
            l2.pop(0)
            nv1.append(v1.pop(0))
            nv2.append(v2.pop(0))
        elif d1 < d2:
            nl.append(d1)
            l1.pop(0)
            l2[0] -= d1
            nv1.append(v1.pop(0))
            nv2.append(v2[0])
        else:
            nl.append(d2)
            l1[0] -= d2
            l2.pop(0)
            nv1.append(v1[0])
            nv2.append(v2.pop(0))
    return (nl, nv1, nv2)
            


if __name__ == '__main__':
    import doctest
    doctest.testmod()

