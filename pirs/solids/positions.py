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

Add positioning to the Tree elements.
"""
from math import ceil, copysign
from ..core.trageom import Vector3
from ..core.trageom.vector import _are_close
from .tree import Tree

class RGrid(object):
    def __init__(self, container, x=1, y=1, z=1, origin=(0, 0, 0)):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__o = Vector3(origin)
        self.__c = container   # link to the solid containing the grid.
        return

    def copy(self, container):
        new = self.__class__(container, self.x, self.y, self.z, self.__o.car)
        return new

    @property
    def x(self):
        """
        Grid pitch along x axis.
        """
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @property
    def y(self):
        """
        Grid pitch along y axis.
        """
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = val

    @property
    def z(self):
        """
        Grid pitch along z axis.
        """
        return self.__z

    @z.setter
    def z(self, val):
        self.__z = val

    @property
    def container(self):
        """
        Link to the solid containing the grid.
        """
        return self.__c

    def position(self, i, j, k, coordinate=None):
        """
        Returns position of element ijk with respect to the grid's container.
        """
        if coordinate is None:
            return self.__o + Vector3((self.x*i, self.y*j, self.z*k))
        else:
            if coordinate == 'x':
                return self.__o.x + self.x*i
            elif coordinate == 'y':
                return self.__o.y + self.y*j
            elif coordinate == 'z':
                return self.__o.z + self.z*k
            else:
                raise NotImplementedError('coordinate {} not implemented'.format(coordinate))

    def index(self, x, y, z):
        """
        Returns index i,j,k of the element containing point p (with respect to the grid's container)

        index(x=5, y=7, z=8) # returns tuple (i, j, k)


        """
        ox, oy, oz = self.__o.car

        res = []
        for (o , a, d) in ((ox, x, self.x), (oy, y, self.y), (oz, z, self.z)):
            l = a - o
            N = copysign(ceil(abs(l)/d - 0.5), l)
            res.append(int(N))

        return res 

        # return NotImplementedError

    @property
    def origin(self):
        """
        Position of the grid's central element (0,0,0) with respect to the container.
        """
        return self.__o

    @origin.setter
    def origin(self, value):
        self.__o = value # TODO: check type of value.

    def set_origin(self, (i, j, k), (x, y, z)):
        """
        Sets the grid origin so that the grid element (i,j,k) has position (x, y, z) 
        with respect to the grid's container.
        """
        self.__o.x = x - i*self.x
        self.__o.y = y - j*self.y
        self.__o.z = z - k*self.z

    def __eq__(self, othr):
        if self is othr:
            return True
        else:
            return (self.x == othr.x and
                    self.y == othr.y and
                    self.z == othr.z and
                    self.__o == othr.__o)

    def __ne__(self, othr):
        return not self == othr

    def __str__(self):
        return 'grid x={0} y={1} z={2} origin={3}'.format(self.x, self.y, self.z, self.__o.car)

    def __getitem__(self, index):
        """
        Returns grid dimension along axis specifyed by the character attribute 'index'.
            
        This syntax is similar to Vector3 class.
        """
        if index == 'x':
            return self.x
        elif index == 'y':
            return self.y
        elif index == 'z':
            return self.z
        else:
            raise IndexError('Unsupported index ', index)

    def extension(self, a=None):
        """
        Returns tuple (Imin, Imax) of minimal and maximal grid element indices
        in the direction along axis a.

        The argument a can be 'x', 'y' or 'z'.

        UPD: the default a is None; in this case the tuple (Imin,
        Imax, Jmin, Jmax, Kmin, Kmax) is returned.

        """
        if a is None:
            ii = self.extension('x')
            jj = self.extension('y')
            kk = self.extension('z')
            return ii + jj + kk
        else:
            step = self[a]
            orig = self.origin[a]
            amin, amax = self.__c.extension(a, 'rel')

            # float values:
            fmax = (amax - orig - 0.5*step)/step 
            fmin = (orig - amin - 0.5*step)/step 
            # check if they are close to integers:
            Nmax = ceil(fmax) - 1.
            if _are_close(fmax, Nmax):
                imax = int(Nmax)
            else:
                imax = int(Nmax) + 1
            Nmin = ceil(fmin) - 1.
            if _are_close(fmin, Nmin):
                imin = int(Nmin)
            else:
                imin = int(Nmin) + 1
            imin = -imin
            return (imin, imax)

    def __extension(self, a):
        dx = self[a]
        dx2 = dx/2.
        x, X = self.__c.extension(a, 'rel')
        o = self.origin[a]

        n = -int(ceil((o - dx2 - x)/dx))
        N = int(ceil((X - o - dx2)/dx))

        return (n, N)

    def used(self):
        """
        Returns True if at least one of the grid container's local children has not None i,j,k attributes.
        """
        for e in self.__c.children: #### .values():
            if e.indexed():
                return True
        return False

    def elements(self):
        """
        Iterates over index-positioned elements.
        """
        for e in self.__c.children:
            if e.indexed():
                yield e

    def center(self, log=False):
        """
        Positions the central element of the grid so that the box circumscribing all inserted grid elements is centered
        with repsect to the container.
        """
        elst = list(self.elements())
        if len(elst) > 0:
            Imin, Jmin, Kmin = elst.pop(0).ijk
            Imax, Jmax, Kmax = Imin, Jmin, Kmin
        else:
            # there are no index-positioned elements.
            return

        for e in elst:
            if Imin > e.i: Imin = e.i
            if Imax < e.i: Imax = e.i
            if Jmin > e.j: Jmin = e.j
            if Jmax < e.j: Jmax = e.j
            if Kmin > e.k: Kmin = e.k
            if Kmax < e.k: Kmax = e.k

        if log:
            print 'Imin: ', Imin
            print 'Imax: ', Imax
            print 'Jmin: ', Jmin
            print 'Jmax: ', Jmax
            print 'Kmin: ', Kmin
            print 'Kmax: ', Kmax

        self.origin.x = -(Imin + Imax)/2. * self.x
        self.origin.y = -(Jmin + Jmax)/2. * self.y
        self.origin.z = -(Kmin + Kmax)/2. * self.z
        return

    def insert(self, ijk, element, i=None):
        """
        Inserts element into the grid's container and specifies for the inserted element
        that it should be positioned with respect to the ijk-th grid element.
        """
        self.__c.insert(element, i)
        element.i, element.j, element.k = map(int, ijk)
        return element

    def _append(self, ijk, element):
        self.__c._append(element)
        element.i, element.j, element.k = map(int, ijk)

    def boundaries(self, d='x'):
        """
        Returns coordinates of boundaries in direction d with respect to the grid's container.
        """
        dmin, dmax = self.__c.extension(d, 'rel')
        b = [dmin]
        Imin, Imax = self.extension(d)
        if d == 'x':
            # along x axis.
            o = self.__o.x
            dd = self.x
        elif d == 'y':
            # along y axis.
            o = self.__o.y
            dd = self.y
        elif d == 'z':
            # along z axis.
            o = self.__o.z
            dd = self.z
        else:
            raise ValueError('Unsupported value of d ', d)

        for i in range(Imin, Imax):
            x = o + dd*i + dd*0.5
            b.append(x)
        b.append(dmax)
        return b


            
class PositionedTree(Tree):
    def __init__(self, **kwargs):
        super(PositionedTree, self).__init__()
        self.__pos = Vector3((0,0,0))           # position of element with respect to its parent
        self.__grd = None ### RGrid(self)                # grid parameters, used to position children
        self.__i = None                           # indices used to position element in the grid of its parent.
        self.__j = None
        self.__k = None

        self.setp(**kwargs)

        ## self.__abspos = None # variable to store computed abspos(). See compile() method
        return

    @property
    def i(self):
        """Index to position solid in the parent's grid along x axis.
        """
        return self.__i

    @i.setter
    def i(self, value):
        self.__i = value

    @property
    def j(self):
        """Index to position solid in the parent's grid along x axis.
        """
        return self.__j

    @j.setter
    def j(self, value):
        self.__j = value

    @property
    def k(self):
        """Index to position solid in the parent's grid along x axis.
        """
        return self.__k

    @k.setter
    def k(self, value):
        self.__k = value

    @property
    def pos(self):
        """
        Position of the element with respect to its parent. By default at the origin.
        """
        return self.__pos

    @pos.setter
    def pos(self, value):
        if isinstance(value, Vector3):
            self.__pos = value
        else:
            raise TypeError

    @property
    def ijk(self):
        """
        Tuple with element indices spcifying the parent's grid element where the element
        is positioned.
        """
        return (self.i, self.j, self.k)

    @ijk.setter
    def ijk(self, value):
        self.i, self.j, self.k = value
        return

    @property
    def grid(self):
        """
        Grid description. Its parameters are used to compute absolute position
        of children, if they have other than None i,j,k attributes.
        """
        if self.__grd is None:
            self.__grd = RGrid(self)
        return self.__grd

    def indexed(self):
        """
        Returns Ture if self is positioned using the indices i, j and k.
        """
        return (not (self.i, self.j, self.k) == (None, None, None))

    def abspos(self, cs='abs', coordinate=None):
        """
        Returns absolute position of the element with respect to the tree's
        root.

        Optional argument cs (by default 'abs') specifies the coordinate
        system. Can be 'abs', 'rel', or an instance of the PositionedTree
        class. In the latter case, it must be a direct or indirect parent of
        self; the returned position is with respect to this parent.

        Optional argument coordinate defines the coordinate's name returned by
        the method. By default, coordinate is None and the vector itself is
        returned. If coordinate is one of 'x', 'y', 'z', 'r', etc. (the
        complete list of variables see in the description of the Vector3
        class), the correspondent coordinate is returned.

        """
        if cs == 'abs':
            ref = self.root
        elif cs == 'rel':
            ref = self
        elif isinstance(cs, PositionedTree):
            ref = cs
        else:
            raise TypeError('Unsupported type {} or value of cs: {}'.format(cs.__class__.__name__, repr(cs)))

        if ref is self or self.parent is None: 
            if coordinate is None:
                pp = Vector3((0,0,0))
            else:
                pp = 0.
        else:
            pp = self.parent.abspos(cs=ref, coordinate=coordinate)
            if self.parent is not None and self.indexed():
                pp += self.parent.__grd.position(self.i, self.j, self.k, coordinate)
        ###  res = pp + self.pos
        if coordinate is None:
            return pp + self.pos 
        elif coordinate == 'x':
            return pp + self.pos.x
        elif coordinate == 'y':
            return pp + self.pos.y
        elif coordinate == 'z':
            return pp + self.pos.z
        else:
            raise ValueError("Unknown value of the 'coordinate' argument: ", coordinate)

    def copy_node(self):
        new = self.__class__()
        new.__pos = self.__pos.copy()
        if self.__grd is not None:
            new.__grd = self.__grd.copy(new)
        return new

    def copy_tree(self):
        new = self.copy_node()
        for c in self.children:
            newc = c.copy_tree()

            new._append(newc)
            newc.i = c.i
            newc.j = c.j
            newc.k = c.k
        return new


        
