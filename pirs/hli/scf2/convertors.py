# default rod materials:
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

from ...scf2.material import RodMaterial
defr = RodMaterial()
deff = RodMaterial()
defg = RodMaterial()

def _default_material():
    res = RodMaterial()
    res.fd = -1
    res.ct = -1
    return res


def rod2material(rod, mdict):
    """
    Analyses structure of the rod and returns description of SCF rod material.

    Possible structures of the rod:

        * Clad -- gap -- fuel. 
          All are coaxial cylinders of the same height. In this case, clad.material defines clad TH propoerties,
          gap.material defines nothing and fuel.material defines fuel TH properties. Clad_thickness is defined as
          difference between clad and gap radii, fuel_diameter is defined from the fuel radius. 

    """


    # all children of rod:
    vals = list(rod.values())

    # check the model
    invalid = [] 
    if rod.stype != 'cylinder':
        invalid.append('not cylinder')
    mc = mdict.get(rod.material)# , _default_material())
    if mc is None:
        mc = _default_material()
        # invalid.append('SCF material for rod material {} not given'.format(repr(rod.material)))
    for v in vals:
        if v.pos.car != (0,0,0):
            invalid.append('not coaxial')
        if v.stype != 'cylinder':
            invalid.append('not all cylinders')
        if v.Z != rod.Z:
            invalid.append('different heights')
    if invalid:
        print 'rod2material returns None with message\n---\n{}\n---\nRod is:\n{}'.format(', '.join(invalid), rod)
        return None
        # raise ValueError('Invalid rod model: {}'.format(invalid))

    mc = mc.copy()
    if len(vals) == 0:
        # rod is clad only
        if mc.fd < 0:
            mc.fd = rod.R * 2 * 1e-2 * 0.9
        if mc.ct < 0:
            mc.ct = rod.R     * 1e-2 * 0.1  * 0.99
    elif len(vals) == 1:
        # rod is clad-fuel, without gap
        fuel = vals[0]
        mf = mdict.get(fuel.material) #, _default_material())
        if mf:
            mc.update(mf)# , 'fuel')
        # geometry
        if mc.fd < 0:
            mc.fd = fuel.R * 2. * 1e-2
        if mc.ct < 0:
            mc.ct = (rod.R - fuel.R)*1e-2 * 0.99
    elif len(vals) > 1:
        # case when rod is a clad-gap-fuel.
        gap = vals[0]
        fuel = vals[1]
        mf = mdict.get(fuel.material)# , _default_material()) # fuel-related properties
        mg = mdict.get(gap.material)# , _default_material())  # gap-related properties
        if mf:
            mc.update(mf, 'fuel')
        if mg:
            mc.update(mg, 'gap')
        # geometrical parameters are taken from the model:
        if mc.fd < 0:
            mc.fd = fuel.R * 2. * 1e-2 # fuel_diameter
        if mc.ct < 0:
            mc.ct = (rod.R - gap.R)*1e-2     # clad_thickness

    gap = rod.R*1e-2 - mc.ct - mc.fd*0.5
    if gap == 0:
        print 'WARNING: zero gap for rod', rod.ijk, rod.material
        for v in vals:
            print v.material
    return mc

def isheated(rod):
    """
    Returns the non-zero heat attribute of the rod internals. If there is no
    such attribute, returns None.
    """
    for v in rod.values(True):
        if v.has_var('heat') and v.heat.values() != [0.]:
            return v.heat
    return None


