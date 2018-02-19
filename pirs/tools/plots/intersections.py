from shapely.geometry import Point, Polygon
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


def ssect(solid, plane, var=None):
    """
    Returns description of the intersection of solid with the plane in terms,
    independent on matplotlib or shapely. Later, this description can be used
    to construct correspondent objects.

    Returned tuple is ('shape_name', p1, p2, ... pN) where 'shape_name' is a
    string 'circle', 'rect' and p1, ... pN -- parameters of the shape.

    """

    d, v = plane.items()[0]
    p = solid.abspos()

    vmin, vmax = solid.extension(d, 'abs')
    if vmin <= v <= vmax:
        # plane intersects the solid.
        if solid.stype == 'cylinder':
            if d == 'z':
                # cylinder cutted with horizontal plane
                x, y, z = p.car[:]
                shape = ('ci', x, y, solid.R)
            elif d in 'xy':
                # cylinder cutted with vertical plane 
                h = solid.Z # rectangle's height
                if d is 'y':
                    w = 2 * (solid.R**2 - (p.y - v)**2)**0.5
                    x = p.x - w*0.5 
                else:
                    w = 2 * (solid.R**2 - (p.x - v)**2)**0.5
                    x = p.y - w*0.5 
                y = p.z - solid.Z/2.
                shape = ('re', x, y, w, h)
            else:
                raise ValueError('Unknown axis {}'.format(d))
        elif solid.stype == 'box':
            if d == 'z':
                h = solid.Y
                w = solid.X
                x = p.x - solid.X*0.5
                y = p.y - solid.Y*0.5
            else:
                h = solid.Z
                y = p.z - solid.Z*0.5
                if d == 'y':
                    w = solid.X
                    x = p.x - w*0.5
                elif d == 'x':
                    w = solid.Y
                    x = p.y - w*0.5
                else:
                    raise ValueError('Unknown axis {}'.format(d))
            shape = ('re', x, y, w, h)
        else:
            raise NotImplementedError('Intersection with {} not implemented yet'.format(solid.stype))
        # add data about variable
        if var is not None:
            if d == 'z':
                # only one value:
                v = solid.get_value_by_coord(var, (0,0,p.z), 'abs')
                vl = [v]
                zl = [] 
            else:
                # add all zmesh values.
                if solid.has_var(var):
                    mesh = getattr(solid, var)
                    zl = mesh.boundary_coords('abs')
                    vl = mesh.values()
                else:
                    v = solid.get_value_by_coord(var, (0,0,0), 'abs')
                    vl = [v]
                    zl = []
            return shape, zl, vl
        else:
            return shape
    else:
        # plane does not intersect the solid.
        if var is None:
            return ()
        else:
            return (), (), ()

def toshapely(shape):
    """
    Transforms meta-description to shapely object.
    """
    if shape[0] == 're':
        x0, y0, w, h = shape[1:]
        x1 = x0 + w
        y1 = y0 + h
        res = Polygon([(x0,y0), (x1,y0), (x1,y1), (x0,y1), (x0,y0)])
    elif shape[0] == 'ci':
        x, y, R = shape[1:]
        res = Point((x, y)).buffer(R, resolution=16)
    else:
        raise TypeError('Unknown section type {}'.format(repr(shape[0])))
    return res

def extensions(shape):
    if shape[0] == 're':
        x, y, w, h = shape[1:]
        res = (x, y, x+w, y+h)
    elif shape[0] == 'ci':
        x, y, R = shape[1:]
        res = (x-R, y-R, x+R, y+R)
    else:
        raise TypeError('Unknown section type {}'.format(repr(shape[0])))
    return res

