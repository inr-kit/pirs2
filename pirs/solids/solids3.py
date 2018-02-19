#!/bin/env python.my
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


"""
Extension of the positions.PositionedTree class to implement methods to define
intersection with other tree elements.

Based on the solids2.py module. THe difference is that in solids2.py I tried to
reinvent API, and here I only re-implement the API of existing solids (defined in
solids.py module).

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at
from .positions import PositionedTree 
from .zmesh_nodecimal import zmesh
from .intersections import isect

class BaseSolid(PositionedTree):
    """
    Prototype class, common to all solids. Some methods, which implementation
    depend on the solid's type, must be implemented later.

    System variables are defined here. They need properties xmin xmax... zmax, which
    depend on the solid class.

    """
    def __init__(self, **kwargs):
        super(BaseSolid, self).__init__()
        # system variables
        self.__heat = None #zmesh(self)
        self.__temp = None #zmesh(self)
        self.__dens = None #zmesh(self)

        #: Solid's name. This attribute not
        #: used by PIRS.
        self.name = None # placeholder for something.  

        self.__mat = 0 #  this takes less memory as string 'void'

        self._no_interior = False

        self.__stype = kwargs.get('__stype', None)  # for particular classes

        self.setp(**kwargs)
        return

    def __var(self, name):
        if name == 'heat':
            return self.__heat
        if name == 'dens':
            return self.__dens
        if name == 'temp':
            return self.__temp

    get_var = __var

    @property
    def material(self):
        """
        Material name. Any immutable, e.g. integer or string.
        """
        return self.__mat

    @material.setter
    def material(self, value):
        self.__mat = value

    @property
    def heat(self):
        """
        Heat axial distribution.
        """
        if self.__heat is None:
            self.__heat = zmesh(self)
        return self.__heat

    @property
    def temp(self):
        """Temperature axial distribution.
        """
        if self.__temp is None:
            self.__temp = zmesh(self)
        return self.__temp

    @property
    def dens(self):
        """Density axial distribution.
        """
        if self.__dens is None:
            self.__dens = zmesh(self)
        return self.__dens

    @heat.setter
    def heat(self, value):
        self.__heat = value

    @temp.setter
    def temp(self, value):
        self.__temp = value

    @dens.setter
    def dens(self, value):
        self.__dens = value

    def has_var(self, name):
        """
        Return True, if axial distribution name (can be 'temp', 'heat' or 'dens')
        is defined for the solid.
        """
        return bool(self.__var(name))

    def get_value_by_index(self, var, i):
        """
        Returns ``i``-th value in the axial distribution specified by ``var``.

        If axial distribution is not defined for the solid yet, return default value.
        """

        mesh = self.__var(var)
        if mesh:
            return mesh.get_value_by_index(i)
        else:
            if var == 'temp':
                return 293.15
            elif var == 'dens':
                return 1.0e-4
            else:
                return 0.

    def get_value_by_coord(self, var, xyz, cs='rel'):
        """
        Returns value of axial distribution specified by ``var`` at position given by the ``xyz`` tuple.

        Optional argument ``cs`` specifies whether ``xyz`` given in absolute (``'abs'``) or relative (``'rel'``) coordinate system.
        """
        mesh = self.__var(var)
        if mesh:
            return mesh.get_value_by_coord(xyz, cs)
        else:
            if var == 'temp':
                return 293.15
            elif var == 'dens':
                return 1.0e-4
            else:
                return 0.

    def is_constant(self, var):
        """
        Checks if the axial distribution ``var`` is constant.
        """
        mesh = self.__var(var)
        if mesh:
            return mesh.is_constant()
        else:
            return True

    def heats(self):
        """
        Iterator. Yeilds child elements with heat axial distribution, recursively.
        """
        for v in self.values(True):
            if v.__heat is not None:
                yield v
        
    def temps(self):
        """
        Iterator. Yeilds child elements with temperature axial distribution defined, recursively.
        """
        for v in self.values():
            if v.__temp is not None:
                yield v
        
    def denss(self):
        """
        Iterator. Yeilds child elements with density axial distribution defined, recursively.
        """
        for v in self.values():
            if v.__dens is not None:
                yield v

    @property
    def stype(self):
        """
        Returns type of the solid.
        """
        return self.__stype

    def common_zmesh(self, own=False):
        """
        Returns an instance of the ``Mesh()`` class, which axial boundaries is the union
        of axial boundaries of all meshes of the solid itself and all its children.
        """
        # grid of the own state variables:
        cmesh = zmesh(self)
        for zm in filter(None, [self.__temp, self.__dens, self.__heat]):
            cmesh.unify(zm.copy())
        if own:
            return cmesh
        
        # children grids:
        for c in self.children: #### .values():
            ccm = c.common_zmesh()
            cmesh.unify(ccm)
        return cmesh

    def max(self, param='heat', filter_=lambda x: True):
        """
        Returns a tuple (v, key) where v is the maximal value of parameter param
        found in the solid itself and its children. Searched only elements that 
        pass the filter_ functions, i.e if filter_(element) returns True.
        """
        if filter_(self) and self.has_var(param): 
            mesh = self.__var(param)
            vmax = max(mesh.values())
            kmax = self.get_key()
        else:
            # do not check the element self, check their children only
            kmax = None
            vmax = None


        for c in self.children: #### .values():
            vc, kc = c.max(param, filter_)
            if kc is not None:
                if kmax is None or vc > vmax:
                    vmax = vc
                    kmax = kc

        return (vmax, kmax)


    def is_visible(self):
        """
        Checks if the solid is seen from its parent(s), and is not completely
        covered by the younger siblings. Only in this case the element and its
        interior can be "seen" in the model. Otherwise, it can be
        removed from the model tree, without actually changing the model.
        
        Note that the element can also be covered by its child. In this case,
        however, its children (at least one that covers) are still visible 
        and cannot be removed.
        """
        if self.hiding_parent() is None and self.covering_sibling() is None:
            return True
        else:
            return False

    def hiding_parent(self):
        """
        Returns the container that completely hides the solid. If there are no
        such parent, returns None.
        
        """
        for p in self.get_parents():
            if not self.intersect(p): return p
        return None

    def covering_sibling(self):
        """
        Returns the younger sibling of the solid or the younger sibling of the
        solid's parent(s) that covers coimpletely the solid. If there are no
        such siblings, returns None.

        """
        # own younger siblings:
        slist = self.get_siblings()[1]
        slist.reverse()
        for s in slist:
            if self.lies_in(s): return s
        # parent younger siblings:            
        for p in self.get_parents():
            slist = p.get_siblings()[1]
            slist.reverse()
            for ye in slist:
                if self.lies_in(ye): return ye
        return None    

    def remove_invisible(self):
        """
        Removes all invisible children of the element recursively.

        The element itself remains in the model even if its is_visible() method
        returns False.
        
        """
        # remove invisible direct children:
        for c in self.children[:]: #### .values():
            if not c.is_visible():
                c.withdraw()
        # for the remaining direct children call the method recursively:
        for c in self.children[:]: #### .values():
            c.remove_invisible()
        return

    def intersect(self, othr):
        """
        Returns True if self positioned at self.abspos() intersects (i.e. has common points)
        with othr positioned at othr.abspos().
        """
        # often self and othr are siblings. In this case it is not necessary to
        # call abspos to get their relative position.
        if self.parent is othr.parent and self.ijk == othr.ijk:
            rpos = self.pos - othr.pos
        else:
            rpos = self.abspos() - othr.abspos()

        return isect(self.intersection_argument, othr.intersection_argument, rpos)

    def Zrange(self, cs='abs'):
        """
        Returns tuple of floats (Zmin, Zmax) -- range of self in z coordinate.
        """
        print 'Zrange is depricated'
        if cs == 'abs':
            z0 = self.abspos(coordinate='z')#  .z
        else:
            z0 = self.pos.z
        dz = self.Z*0.5
        return (z0 - dz, z0 + dz)

    # extension method is the generalization of Zrange. use it whenewer possible.
    # This generalization is used in lies_in method.
    def extension(self, a, s='abs'):
        """
        Returns tuple (min, max) representing extension of the solid along axis a.

        Argument a can be 'x', 'y' or 'z'.

        Optional argument s specifies the coordinate system. 'abs' means the
        gloabal coordinate system (with respect to the root of self), any other
        means the local element's coordinate system.

        """
        if s is 'abs':
            ref = self.abspos(coordinate=a)###   [a]
        else:
            ref = 0. # self.pos[a]
        ###   dim2 = getattr(self, a.upper()) * 0.5
        if a == 'x':
            dim = self.X
        elif a == 'y':
            dim = self.Y
        elif a == 'z':
            dim = self.Z
        dim2 = dim * 0.5
        return (ref-dim2, ref+dim2)

    def lies_in(self, othr):
        """
        Returns True, if self lies completely inside othr.
        """
        # Solid s1 of type T1 lies completely in another solid s2 of type T2,
        # if and only if s2.circumscribed(s1) lies completely in s2.
        circ = othr.circumscribed(self)
        circ.pos = self.abspos()
        # compare extensions of the circumscribed container and othr
        # in every axis:
        for a in ['x', 'y', 'z']:
            rc = circ.extension(a, 'abs')
            ro = othr.extension(a, 'abs')
            if rc[0] < ro[0] or ro[1] < rc[1]:
                return False
        return True

    def circumscribed(self, s, adjust_position=True):
        """
        Returns a new instance of the class self.__class__ that circumscribes s.
        """
        c = self.__class__()
        c.circumscribe(s, adjust_position)
        return c

    def get_radius(self, inscribed=True):
        """
        Returns radius of circumscribed sphere. Deprecated, use circumscribe method.
        """
        print 'Deprecated method get_radius'
        raise NotImplementedError
        if not inscribed:
            return Sphere().circumscribed(self).R
        else:
            raise NotImplementedError('Inscribed radius not implemented')

    def __eq__(self, othr):
        if self is othr:
            return True

        if not isinstance(othr, BaseSolid):
            return False

        # compare types:
        if self.stype != othr.stype:
            #print 'difference in types '
            return False
        # compare materials:
        if self.material != othr.material:
            #print 'difference in materials'
            return False

        # compare number of children:
        if len(self.children) != len(othr.children):
            return False
        # compare local positions
        if self.pos != othr.pos:
            #print 'difference in local position'
            return False
        if self.ijk != othr.ijk:
            return False
        # compare dimensions
        for a in 'xyz':
            if self.extension(a, 'rel') != othr.extension(a, 'rel'):
                #print 'difference in dimensions along ', a
                return False
        # compare zmeshes:
        if self.__heat != othr.__heat:
            #print 'difference in heat'
            return False
        if self.__dens != othr.__dens:
            #print 'difference in dens'
            return False
        if self.__temp != othr.__temp:
            #print 'difference in temp'
            return False

        # compare interiors:
        for (sc, oc) in zip(self.children, othr.children):
            if not sc == oc:
                return False
        return True

    def __ne__(self, othr):
        return not self == othr

    def lattice_elements(self):
        """
        Returns list of boxes that represent lattice elements of the solid.

        Returned values are tuples of the form (ijk, itype, Box()), where
        ijk is (i,j,k), itype is the type
        """
        # list of unique lattice elements. It always has an empty lattice element.
        unique = []
        Imin, Imax = self.grid.extension('x')
        Jmin, Jmax = self.grid.extension('y')
        Kmin, Kmax = self.grid.extension('z')

        pos = self.abspos()
        gor = pos + self.grid.origin
        cp0 = gor * 0. # used later

        leb = Box(X=self.grid.x, Y=self.grid.y, Z=self.grid.z)
        leb.pos = gor
        leb.material = self.material
        unique.append(leb)
        leb._no_interior = self._no_interior

        # sort children by their grid indices:
        ddd = {}
        for c in self.children:
            if c.i is None:
                p0 = c.pos
                x, X = c.extension('x', 'rel')
                y, Y = c.extension('y', 'rel')
                z, Z = c.extension('z', 'rel')

                i, j, k = self.grid.index(p0.x+x, p0.y+y, p0.z+z)
                I, J, K = self.grid.index(p0.x+X, p0.y+Y, p0.z+Z)

                for ii in range(i, I+1):
                    for jj in range(j, J+1):
                        for kk in range(k, K+1):
                            ijk = (ii, jj, kk)
                            lst = ddd.get(ijk, [])
                            if not lst:
                                ddd[ijk] = lst
                            lst.append(c)
            else:
                lst = ddd.get(c.ijk, [])
                if not lst:
                    ddd[c.ijk] = lst
                lst.append(c)
        
        for k in range(Kmin, Kmax+1):
            for j in range(Jmin, Jmax+1):
                for i in range(Imin, Imax+1):
                    chl = ddd.get((i,j,k), [])
                    if chl:
                        leb = Box(X=self.grid.x, Y=self.grid.y, Z=self.grid.z)
                        leb._no_interior = self._no_interior
                        pijk = self.grid.position(i,j,k)
                        leb.pos = pos + pijk
                        visible_interior = True
                        covering_child = None
                        for ch in chl:
                                chnew = leb.insert(ch.copy_tree()) # note, this resets indices i,j,k of the chnew.
                                if ch.i is None:
                                    chnew.pos += -pijk
                                if leb.lies_in(chnew):
                                    # if ch completely covers leb, previously inserted elements can be withdrawn.
                                    visible_interior = False
                                    covering_child = chnew
                                    for c in leb.children[:-1]: #### .values()[:-1]:
                                        c.withdraw()
                        if visible_interior:
                            leb.material = self.material
                            if self.__dens:
                                leb.dens.update(self.dens)
                            if self.__temp:
                                leb.temp.update(self.temp)
                            if self.__heat:
                                leb.heat.update(self.heat)

                            # remove unnecassary zmesh elements for lattice elements
                            # in the upper and lower layers:
                            if k in [Kmin, Kmax]:
                                for zmesh in filter(None, [leb.__dens, leb.__temp, leb.__heat]):
                                    if len(zmesh.get_grid()) == 2:
                                        zmesh.simplify()
                            chpos = cp0
                        else:
                            # simplify leb structure in the way that leb
                            # is replaced with its covering child
                            covering_child.withdraw()
                            for c in leb.children[:]:
                                covering_child.insert(c)
                                c.pos = c.pos - covering_child.pos
                            leb = covering_child
                            chpos = covering_child.pos.copy()
                        leb.pos = gor + chpos
                        # check if it is unique
                        try:
                            itype = unique.index(leb)
                            #print 'existing element with index ', itype
                        except ValueError:
                            itype = len(unique)
                            unique.append(leb)
                            #print 'new element to unique '
                    else:
                        # there are no children in leb (i,j,k).
                        itype = 0
                    yield ((i,j,k), unique[itype], itype)
                                
    def copy_node(self):
        #print self.__class__.__name__, ' BaseSolid copy_node'
        new = super(BaseSolid, self).copy_node()
        if self.__heat:
            new.__heat = self.__heat.copy(new)
        if self.__temp:
            new.__temp = self.__temp.copy(new)
        if self.__dens:
            new.__dens = self.__dens.copy(new)
        new.name = self.name
        new.material = self.material
        new.__stype = self.__stype
        return new

    def layers(self, temp=True, dens=True, heat=True):
        """
        Returns iterator with elements describing each layer.

        Each returned element is a tuple (Zmin, Zmax, values, children, (is_first, is_last))
        """
        ml = []
        if temp:
            if self.__temp:
                ml.append(self.__temp.copy())
            else:
                tdef = zmesh(self)
                tdef.set_values(293.15)
                ml.append(tdef)
        if dens:
            if self.__dens:
                ml.append(self.__dens.copy())
            else:
                ddef = zmesh(self)
                ddef.set_values(1.0e-3)
                ml.append(ddef)
        if heat:
            if self.__heat:
                ml.append(self.__heat.copy())
            else:
                hdef = zmesh(self)
                hdef.set_values(0.0)
                ml.append(hdef)
        if len(ml) == 0:
            raise ValueError('No zmesh attributes given')

        # z coordinates of the unified grid:
        mll = filter(None, ml)
        if len(mll) == 0:
            zl = self.extension('z', 'abs')
        else:
            um = mll[0]
            for m in mll[1:]:
                um.unify(m)
            zl = um.boundary_coords('abs')
        ll = len(zl)

        # z coordinates of children:
        cz = []
        for c in self.children:
            cz.append(c.extension('z', 'abs'))

        for i in range(ll-1):
            # axial coordinates of the layer
            z1, z2 = zl[i:i+2] 

            # list of values:
            vl = []
            for m in ml:
                if m is None:
                    vl.append(0.)
                else:
                    vl.append(m.get_value_by_index(i))

            # list of children that can intersect the layer:
            cl = []
            for (c, (czmin, czmax)) in zip(self.children, cz):
                if czmin < z2 and czmax > z1:
                    cl.append(c)

            # set mark for the first and last layers:
            isf = (i == 0)     # is first?
            isl = (i == ll-2)  # is last?
            yield (z1, z2, vl, cl, (isf, isl))




class Sphere(BaseSolid):
    """
    A sphere, which radius is defined by the attribute ``R``.
    """
    # for p in __mro__:
    #     __doc__ += p.__doc__ # attempt to save parent's docstrings.
    def __init__(self, **kwargs):
        super(Sphere, self).__init__(__stype='sphere')
        self.R = 1. # sphere radius
        
        self.setp(**kwargs)
        return

    @property
    def X(self):
        """Sphere's dimension along axis X."""
        return self.R*2.
    @property
    def Y(self):
        """Sphere's dimension along axis Y."""
        return self.R*2.
    @property
    def Z(self):
        """Sphere's dimension along axis Z."""
        return self.R*2.

    @property
    def intersection_argument(self):
        return ('sphere', self.R)

    def circumscribe(self, s, adjust_position=True):
        """
        Changes inplace parameters of the sphere, so that it circumscribes solid s.
        """
        if isinstance(s, Cylinder):
            self.R = (s.R**2. + (s.Z/2.)**2.)**0.5
        elif isinstance(s, Sphere):
            self.R = s.R
        elif isinstance(s, Box):
            self.R = (self.X**2. + self.Y**2. + s.Z**2.)**0.5 * 0.5
        else:
            raise NotImplementedError('Cannot find parameters of circumscribed sphere for ', s.__class__.__name__)
        if adjust_position:
            self.pos = self.pos - self.abspos() + s.abspos()
        return

    def copy_node(self):
        #print self.__class__.__name__, ' Sphere copy_node'
        new = super(Sphere, self).copy_node()
        new.R = self.R
        return new


class Cylinder(BaseSolid):
    """
    A finite-height cylinder with the axis parallel to the z axis.
    Cylinder geometry is defined by attributes ``R`` and ``Z``.
    """
    def __init__(self, **kwargs):
        super(Cylinder, self).__init__(__stype='cylinder')
        self.Z = 1.
        self.R = 1.
        # work around to simplify mcnp input:
        self.as_macrobody = True
        self.clad_thickness = None # set it to some value (in SCF units) instead of actual modelling of the gap.
        self.pu_fraction = 0.

        self.setp(**kwargs)
        return

    @property
    def X(self):
        """Cylinder's dimension along X axis."""
        return self.R*2.
    @property
    def Y(self):
        """Cylinder's dimension along Y axis."""
        return self.R*2.

    @property
    def intersection_argument(self):
        return ('cylinder', (self.R, self.Z))

    def circumscribe(self, s, adjust_position=True):
        """
        Change inplace properties of the cylinder so that it circumscribes solid s.
        """
        if isinstance(s, Cylinder):
            self.R = s.R
            self.Z = s.Z
        elif isinstance(s, Sphere):
            self.R = s.R
            self.Z = s.Z
        elif isinstance(s, Box):
            self.R = (s.X**2. + s.Y**2.)**0.5 * 0.5
            self.Z = self.Z
        else:
            raise NotImplementedError('Cannot find parameters of circumscribed cylinder for ', s.__class__.__name__)
        if adjust_position:
            self.pos = self.pos - self.abspos() + s.abspos()
        return

    def copy_node(self):
        #print self.__class__.__name__, ' Cylinder copy_node'
        new = super(Cylinder, self).copy_node()
        new.R = self.R
        new.Z = self.Z
        new.clad_thickness = self.clad_thickness
        new.pu_fraction = self.pu_fraction
        return new




class Box(BaseSolid):
    """
    A box with facets perpendicular to the axes.

    Box geometry is defined by three atributes, ``X``, ``Y`` and ``Z``, 
    which represent box dimensions. 
    """
    def __init__(self, **kwargs):
        super(Box, self).__init__(__stype='box')

        #: Box dimension along x axis
        self.X = 1.

        #: Box dimension along y axis
        self.Y = 1.

        #: Box dimension along z axis
        self.Z = 1.
        self.setp(**kwargs)
        return

    @property
    def R(self):
        """ Radius of circumscribed sphere."""
        return (self.X**2. + self.Y**2. + self.Z**2.)**0.5 * 0.5

    @property
    def intersection_argument(self):
        return ('box', (self.X, self.Y, self.Z))

    def circumscribe(self, s, adjust_position=True):
        """
        Changes inplace properties of the box, so it circumscribes solid s.
        """
        self.X = s.X
        self.Y = s.Y
        self.Z = s.Z
        if adjust_position:
            self.pos = self.pos - self.abspos() + s.abspos()
        return

    def copy_node(self):
        #print self.__class__.__name__, ' Box copy_node'
        new = super(Box, self).copy_node()
        new.X = self.X
        new.Y = self.Y
        new.Z = self.Z
        return new



