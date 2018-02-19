
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

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from ... import mcnp
from ...solids import Sphere, Box, Cylinder

def solid2surface(solid, refl=''):
    """
    Returns an instance of the mcnp.surfaces.Surface class correspondent to the
    solid.

    >>> for s in [Box(), Cylinder()]:
    ...     print solid2surface(s)
    ...
    {} rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5
    {} rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0

    """
    x0, y0, z0 = solid.abspos().car  # center's absolute coordinates
    if isinstance(solid, Box):
        Xmin, Xmax = solid.extension('x')
        Ymin, Ymax = solid.extension('y')
        Zmin, Zmax = solid.extension('z')
        s = mcnp.Surface(type='rpp', plst=[Xmin, Xmax, Ymin, Ymax, Zmin, Zmax], cmnt=solid.name, refl=refl )
    elif isinstance(solid, Cylinder):
        # solid is a cylinder
        if solid.as_macrobody:
            Zmin, Zmax = solid.extension('z')
            s = mcnp.Surface(type='rcc', plst=[x0, y0, Zmin, 0, 0, solid.Z, solid.R], cmnt=solid.name, refl=refl)
        else:
            s = mcnp.Surface(type='c/z', plst=[x0, y0, solid.R], cmnt=solid.name, refl=refl)
    else:
        # solis is a sphere
        s = mcnp.Surface(type='s', plst=[x0, y0, z0, solid.R], cmnt=solid.name, refl=refl)
    return s

def solid2volume_(solid, refl=''):
    """
    The volume() method of the Surface class returns a volume defined through
    simple surfaces. It is better to use MB, if possible.
    """
    return mcnp.Volume(1, solid2surface(solid, refl))



def zmesh2volumes(zmesh, Zmin, Zmax, children=[]):
    """
    Returns a list of volumes correspondent to the axial mesh zmesh. The lower
    and upper volumes are bounded by the Zmin and Zmax, respectively.

    >>> zmesh = Box().dens
    >>> zmesh.set_grid([1]*4)
    >>> for v in zmesh2volumes(zmesh, -100, 100):
    ...     print v
    ...
    {} pz  -100.0 -{} pz  -0.25
    {} pz  -0.25 -{} pz  0.0
    {} pz  0.0 -{} pz  0.25
    {} pz  0.25 -{} pz  100.0

    Children can be taken into account:
    >>> for v in zmesh2volumes(zmesh, -100, 100, [Box(), Cylinder()]):
    ...     print v
    {} pz  -100.0 -{} pz  -0.25 {} rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5 {} rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
    {} pz  -0.25 -{} pz  0.0 {} rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5 {} rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
    {} pz  0.0 -{} pz  0.25 {} rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5 {} rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
    {} pz  0.25 -{} pz  100.0 {} rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5 {} rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0

    """
    res = []
    # z list for the mesh
    zlst = zmesh.boundary_coords('abs')
    zlst[0] = Zmin
    zlst[-1] = Zmax
    #vlst = map( lambda x: mcnp.surfaces.Surface('pz {0}'.format(x)).volume(), zlst)
    vlst = map( lambda x: mcnp.surfaces.Surface(type='pz', plst=[x]).volume(), zlst)
    # z ranges for the children
    zran = map( lambda x: x.Zrange('abs'), children)
    for (v1, v2, z1, z2) in zip(vlst[:-1], vlst[1:], zlst[:-1], zlst[1:]):
        res.append( v1 & (-v2) )
        # check if children can intersect:
        for (c, zr) in zip(children, zran):
            if zr[1] <= z1 or zr[0] >= z2:
                pass
            else:
                res[-1] = res[-1] & mcnp.surfaces.Volume(1, solid2surface(c))
    return res

def zmesh2mtally(zmesh):
    """
    Returns an instance of the mcnp.MeshTally class correspondent to the 
    zmesh that describes the fission heat.
    """
    mt = mcnp.MeshTally()
    mt.ttype = 7
    ref = zmesh.get_solid() # reference solid for the mesh.
    mt.cmt = ' heat in {0}'.format( ref.get_key() )
    if isinstance(ref, Cylinder):
        mt.geom = 'cyl'
        x,y,z = ref.abspos().car
        mt.origin = (x, y, z - ref.Z/2)
        mt.axs = (0, 0, 1)
        mt.imesh[0] = ref.R
        mt.jmesh.pop()
        zlst = zmesh.boundary_coords('abs')
        for z in map(lambda x: x-zlst[0], zlst[1:]):
            mt.jmesh.append(z)
    elif isinstance(ref, Box):
        mt.geom = 'xyz'
        x, y, z = ref.abspos().car
        mt.origin = (x - ref.X/2., y - ref.Y/2., z - ref.Z/2.)
        mt.imesh[0] = x + ref.X/2.
        mt.jmesh[0] = y + ref.Y/2.
        mt.kmesh.pop()
        for z in zmesh.boundary_coords('abs')[1:]:
            mt.kmesh.append(z)
    else:
        raise NotImplementedError('Cannot convert to mesh tally zmesh with reference of type ', ref.__class__.__name__)
    return mt

def grid2tally(container, rod):
    """
    Returns an instance of the mcnp.MeshTally class that decribes rods
    in the grid of solid.

    Rods must satisfy certain consditions and must be inserted into a grid.
    """
    mt = mcnp.MeshTally()
    mt.ttype = 7
    mt.cmt = 'heat in the grid elements of the element {0}'.format(container.get_key())
    mt.geom = 'xyZ'
    z, Z = container.extension('z')

    x, y = container.abspos().car[:2]
    xlst = container.grid.boundaries('x')
    ylst = container.grid.boundaries('y')

    mt.origin = (xlst.pop(0) + x, ylst.pop(0) + y, z)
    mt.imesh[0] = xlst.pop(0) + x 
    while xlst:
        mt.imesh.append(xlst.pop(0) + x)
    mt.jmesh[0] = ylst.pop(0) + y
    while ylst:
        mt.jmesh.append(ylst.pop(0) + y)
    # i, I = container.grid.extension('x')
    # j, J = container.grid.extension('y')
    # mt.iints[0] = I - i + 1
    # mt.jints[0] = J - j + 1
    mt.kmesh.pop()
    for z in rod.heat.boundary_coords('abs')[1:]:
        mt.kmesh.append(z)
    return mt


def base_element2volume(solid):
    """
    Returns an instance of mcnp.Volume() class representing the base element of
    the solid's grid.
    """
    g = solid.grid # short name of the grid
    be = Box()
    be.pos = solid.abspos() + g.origin
    be.X = g.x
    be.Y = g.y
    be.Z = g.z
    # check if axial boundaries are needed:
    bz, bZ = be.extension('z')
    cz, cZ = solid.extension('z')
    if bz <= cz and cZ <= bZ:
        c = Box()
        c.X = be.X*2
        c.Y = be.Y*2
        c.Z = be.Z
        c.pos = be.pos
        be.pos *= 0
        c.insert(be)
    return solid2volume(be)

def solid2volume(solid, refl=''):
    """
    Tries to take into account parents of solid.
    """
    if solid.parent is not None:
        if isinstance(solid, Box):
            if isinstance(solid.parent, Box):
                px, pX = solid.parent.extension('x', 'abs')
                py, pY = solid.parent.extension('y', 'abs')
                pz, pZ = solid.parent.extension('z', 'abs')
                sx, sX = solid.extension('x', 'abs')
                sy, sY = solid.extension('y', 'abs')
                sz, sZ = solid.extension('z', 'abs')
                # sx += solid.pos.x
                # sX += solid.pos.x
                # sy += solid.pos.y
                # sY += solid.pos.y
                # sz += solid.pos.z
                # sZ += solid.pos.z
                # print 'solid2volume extensions: '
                # print sx, px, sX, pX
                # print sy, py, sY, pY
                # print sz, pz, sZ, pZ
                vols = []
                if sX < pX:
                    s = mcnp.Surface(type='px', plst = [sX], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if sx > px:
                    s = mcnp.Surface(type='px', plst = [sx], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if sY < pY:
                    s = mcnp.Surface(type='py', plst = [sY], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if sy > py:
                    s = mcnp.Surface(type='py', plst = [sy], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if sZ < pZ:
                    s = mcnp.Surface(type='pz', plst = [sZ], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if sz > pz:
                    s = mcnp.Surface(type='pz', plst = [sz], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if vols:
                    v = mcnp.Volume(0)
                    while vols:
                        v = v | vols.pop(0)
                        # print 'soid2volume: i', v, solid.local_key, solid.parent.local_key
                else:
                    v = -mcnp.Volume(0)
                # print 'soid2volume: r', v, solid.local_key, solid.parent.local_key
                return v
            elif isinstance(solid.parent, Cylinder):
                dx = solid.X/2.
                dy = solid.Y/2.
                pxy = (solid.pos.x - dx, solid.pos.y - dy) # left  lower corner
                pxY = (solid.pos.x - dx, solid.pos.y + dy) # left  upper corner
                pXY = (solid.pos.x + dx, solid.pos.y + dy) # right upper corner
                pXy = (solid.pos.x + dx, solid.pos.y - dy) # right lower corner
                
                r2 = solid.parent.R**2
                bxy = pxy[0]**2 + pxy[1]**2 < r2
                bxY = pxY[0]**2 + pxY[1]**2 < r2
                bXY = pXY[0]**2 + pXY[1]**2 < r2
                bXy = pXy[0]**2 + pXy[1]**2 < r2

                pz, pZ = solid.parent.extension('z', 'abs')
                sx, sX = solid.extension('x', 'abs')
                sy, sY = solid.extension('y', 'abs')
                sz, sZ = solid.extension('z', 'abs')

                vols = []
                if bXY or bXy:
                    s = mcnp.Surface(type='px', plst = [sX], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if bxy or bxY:
                    s = mcnp.Surface(type='px', plst = [sx], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if bxY or bXY:
                    s = mcnp.Surface(type='py', plst = [sY], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if bxy or bXy:
                    s = mcnp.Surface(type='py', plst = [sy], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if sZ < pZ:
                    s = mcnp.Surface(type='pz', plst = [sZ], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if sz > pz:
                    s = mcnp.Surface(type='pz', plst = [sz], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                    
                if vols:
                    v = mcnp.Volume(0)
                    while vols:
                        v = v | vols.pop(0)
                        # print 'soid2volume: i', v, solid.local_key, solid.parent.local_key
                else:
                    v = -mcnp.Volume(0)
                # print 'soid2volume: r', v, solid.local_key, solid.parent.local_key
                return v
        elif isinstance(solid, Cylinder):
            if isinstance(solid.parent, Box):
                px, pX = solid.parent.extension('x', 'abs')
                py, pY = solid.parent.extension('y', 'abs')
                pz, pZ = solid.parent.extension('z', 'abs')
                sx, sX = solid.extension('x', 'abs')
                sy, sY = solid.extension('y', 'abs')
                sz, sZ = solid.extension('z', 'abs')
                x0, y0, z0 = solid.abspos().car
                vols = []
                if sx < pX and px < sX and sy < pY and py < sY:
                    s = mcnp.Surface(type='c/z', plst = [x0, y0, solid.R], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                if sz > pz:
                    s = mcnp.Surface(type='pz', plst = [sz], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if sZ < pZ:
                    s = mcnp.Surface(type='pz', plst = [sZ], refl=refl)
                    vols.append(mcnp.Volume(1, s))

                if vols:
                    v = mcnp.Volume(0)
                    while vols:
                        v = v | vols.pop(0)
                else:
                    v = -mcnp.Volume(0)
                # print 'soid2volume: r', v, solid.local_key, solid.parent.local_key
                return v
            elif isinstance(solid.parent, Cylinder):

                pz, pZ = solid.parent.extension('z', 'abs')
                sz, sZ = solid.extension('z', 'abs')

                vols = []
                if solid.pos.r < solid.R + solid.parent.R:
                    s = mcnp.Surface(type='c/z', plst = solid.abspos().car[:2] + (solid.R,), refl = refl)
                    vols.append(mcnp.Volume(1, s))
                if sz > pz:
                    s = mcnp.Surface(type='pz', plst = [sz], refl=refl)
                    vols.append(mcnp.Volume(-1, s))
                if sZ < pZ:
                    s = mcnp.Surface(type='pz', plst = [sZ], refl=refl)
                    vols.append(mcnp.Volume(1, s))
                    
                if vols:
                    v = mcnp.Volume(0)
                    while vols:
                        v = v | vols.pop(0)
                else:
                    v = -mcnp.Volume(0)
                return v
    return mcnp.Volume(1, solid2surface(solid, refl))






