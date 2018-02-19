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
The module defines functions to chek if solids (boxes, cylinders, shperes)
intersect or not.

Functions called isect_?() check intersection of two solids of the same type.
Functions called isect_?_? check intersection of two solids of different type.

All function assume that solids are open (do not contain their boundary
surfaces). Therefore, two just touching solids do not intersect.

For any two types a and b, functions isect_a_b and isect_b_a are the same. Thus,
only one of them is actually implemented.

There is a wrapper function, isect() that can take two forms in arbitrary order.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from ..core.trageom import Vector3
from ..core.trageom.vector import _are_close


def isect_c(c1, c2, p):
    """
    Returns True if cylinders c1 and c2 intersect, when c2 is positioned at p
    with respect to c1.     

    Arguments c1 and c2 must be tuples (R, Z) specifying the cylinder's radius
    and height. p must be an instance of the trageom.Vector3 class.
    """

    r1,z1 = c1
    r2,z2 = c2
    if abs( p.z ) < z1/2. + z2/2.:
        # if projections of two cylinders onto the z-axis intesect, check
        # whether their circles intersect.
        if p.r < r1 + r2:
            # z projections intersect. If projections onto xy plane do not,
            # cylinders do not intersect.
            return True
    return False

def isect_b(b1, b2, p):
    """
    Returns True if box b1 intersects box b2 positioned at p with respect to
    b1. 
    
    Arguments b1 and b2 must be tuples (X,Y,Z) specifying dimenstions of the
    boxes. p must be an instance of the trageom.Vector3 class.

    """
    X1, Y1, Z1 = b1
    X2, Y2, Z2 = b2

    px2 = abs(p.x)*2.
    X12 = X1 + X2
    if  px2 < X12 and not _are_close(px2, X12):
        py2 = abs(p.y)*2.
        Y12 = Y1 + Y2
        if  py2 < Y12 and not _are_close(py2, Y12):
            pz2 = abs(p.z)*2.
            Z12 = Z1 + Z2
            if  pz2 < Z12 and not _are_close(pz2, Z12):
                return True
    return False  

def isect_s(r1, r2, p):
    """
    Returns True if sphere with radius r1 intersects sphere r2 positioned at p
    with respect to r1.     

    Arguments r1 and r2 must be convertable to float, p must be of the 
    trageom.Vector3() class.

    """
    return p.R < r1 + r2


def isect_c_b(c, b, p):
    """
    Returns True if cylinder c intersects box b positioned at p with respect to
    c.
    
    Argument c is a tuple (R,Z) specifying the radius and height of the
    cylinder, b is a tuple (X, Y, Z) with the box dimensions. p must be an
    instance of the trageom.Vector3 class.

    """
    cR, cZ = c
    bX, bY, bZ = b
    if abs( p.z ) < (cZ + bZ)/2.:
        # z-projections intersect.
        py = abs(p.y)
        bY = bY*0.5
        if py < bY + cR:
            # y-projections intersect. 
            if py < bY:
                # box intersect the x-axis. cR can be used as the X dimension
                # of the cylinder.
                cX = cR
            else:
                # box does not intersect the x-axis. The X dimension of the
                # cylinder must be computed.
                #
                # In this case, there must be a non-empty section of the cylinder
                # with the plane build on one of the box facets perpendicular to
                # the y-axis. The form of this section is a (flat) rectangle, which
                # Z dimension is equal to cylinder's Z dimension, and X dimension
                # depends on the cylinder's radius, box Y dimension and the
                # y-coordinate of their relative position.
                cX = (cR**2.  -  (py - bY)**2)**0.5
            if abs(p.x) < bX*0.5 + cX:
                return True
    return False                        

def isect_c_s(c, s, p):
    """
    Returns True if cylinder c intersects sphere s positioned at p with respect
    to c. 
    
    Argument c is a tuple (R, Z) specifying the cylinder's radius and height,
    and s must be the radius of the sphere. p must be an instance of the
    trageom.Vector3 class.

    """
    # if projections of cylinder and sphere onto the z-axis intesect, calculate
    # the radius of the circle( which is intersection of cylinder's top/bottom
    # planes with the sphere) and search futher
    pz = abs(p.z)
    cZ = c[1] * 0.5
    if pz < cZ + s:
        # z projections of cylinder and sphere intersect
        if pz <= cZ:  sR = s
        else       :  sR = (s**2. - (pz - cZ)**2.)**0.5
        if p.r < c[0] + sR:
            return True
    return False

def isect_b_s(b, r, p):
    """
    Returns True if box b intersects sphere r positioned at p with respect to
    b.
    
    Argument b is a tuple (X,Y,Z) with box dimensions, and r is the sphere's
    radius. p must be an instance of the trageom.Vector3 class.

    """
    # if projections of box and sphere onto one of axes intesect, search futher.
    pz = abs(p.z)
    bZ = b[2]*0.5
    if pz < bZ + r:
        # if projections of box and sphere onto z intersect, find radius of the
        # circle (intersection of the sphere with one of the box facets
        # perpendicular to z axis) and chek next projections.
        if pz <= bZ:   sR = r
        else       :   sR = (r**2. - (pz - bZ)**2.)**0.5
        py = abs(p.y)
        bY = b[1]*0.5
        if py < bY + sR:
            # if projections onto y axis of the box and circle intersect, check
            # x axis projection
            if py <= bY:   pass
            else       :   sR = (sR**2. - (py - bY)**2.)**0.5
            if abs(p.x) < b[0]*0.5 + sR:
                return True
    return False

def isect(f1, f2, p):
    """
    Wrapper for the above functions.

    f1 and f2 are tuples (form_type, P), where form_type is a string 'box', 'cylinder' or 'sphere' and P is the
    correspondent tuple of the parameters. 

        isect(('box', (X,Y,Z)), ('box',(X,Y,Z)), p)
        isect(('box', (X,Y,Z)), ('sphere', R), p)

    """
    # shorter names:
    n1, v1 = f1
    n2, v2 = f2
    b = 'box'
    s = 'sphere'
    c = 'cylinder'

    if (n1, n2) == (c, c):
        return isect_c(v1, v2, p)
    if (n1, n2) == (c, b):
        return isect_c_b(v1, v2, p)
    if (n1, n2) == (b, c):
        return isect_c_b(v2, v1, p)
    if (n1, n2) == (c, s):
        return isect_c_s(v1, v2, p)
    if (n1, n2) == (s, c):
        return isect_c_s(v2, v1, p)

    if (n1, n2) == (b, b):
        return isect_b(v1, v2, p)
    if (n1, n2) == (b, s):
        return isect_b_s(v1, v2, p)
    if (n1, n2) == (s, b):
        return isect_b_s(v2, v1, p)

    if (n1, n2) == (s, s):
        return isect_s(v1, v2, p)

    return NotImplementedError('Intersection not implemented for types ', (n1, n2))

    if 'box' in tset:
        if 'cylinder' in tset:
            return
