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

Function to extract SCF-relevant parts of general model.
"""

import time

def find_fuel(r):
    """
    find fuel element in rod r and return it, or None.

    TODO: use ckeys of interface2

    """
    for c in r.values():
        if c.local_key == 'fuel':
            return c
    return None
        

def scf_standard_model(gm, keys, log=True):
    """
    gm -- general model, usualy ScfInterface.__gm
    keys -- dictionary with keys, usualy, ScfInterface.keys

    Returns: 
        sm -- the standard model 
        skeys -- dictioary like keys but corresponds to sm.

    SM must fulfill the following requirements:

        * All fuel elements must have the same lower and upper z coordinate,

        * All elements must have the same layer boundaries.

    """

    if log:
        t1 = time.time()

    # standard model consists only of the coolant container and rods.
    #  elements of the original model:
    ocoolant = gm.get_child(keys['coolant'])
    orods = [] 
    for key in keys['rods']:
        r = gm.get_child(key)
        orods.append(r)
    if log:
        t2 = time.time()
        print 'orods generated ', t2-t1
        t1 = t2

    #  sm = ocoolant.copy_node()
    #  sm.pos = ocoolant.abspos()  # elements in the general model and standard model have the same abs.positions.

    #  if log:
    #      t2 = time.time()
    #      print 'sm created ', t2-t1
    #      t1 = t2

    #  # insert copy of rods to the standard model:
    #  fuels = [] # list of fuel elements in the standard model
    #  for r in orods:
    #      rcopy = sm.insert(r.local_key, r.copy_tree())
    #      # ensure that rods in the standard model have the same position as in the
    #      # original model:
    #      rcopy.pos = r.abspos() - sm.pos 
    #      rcopy.ijk = (None, None, None)
    #      fuels.append(find_fuel(rcopy))

    #  if log:
    #      t2 = time.time()
    #      print 'fuels generated ', t2-t1
    #      t1 = t2

    # ----------------------------------------------------------------------------------------------
    # another way to create sm:
    gm2 = gm.copy_tree()
    ccl = gm2.get_child(keys['coolant'])

    # rods local keys
    rod_lkeys = []
    for key in keys['rods']:
        k = None
        if isinstance(key, str):
            k = key
        elif isinstance(key, tuple):
            k = key[-1]
        else:
            raise ValueError('Rod key of unsupported type', key)
        rod_lkeys.append(k)
    all_lkeys = ccl.children_keys #### ()
    rem_lkeys = set(all_lkeys) - set(rod_lkeys)
    fuels = []
    while rem_lkeys:
        ccl.remove(rem_lkeys.pop())
    # check that all rods are in sm2 and generate list of fuel keys:
    for key in keys['rods']:
        r = gm2.get_child(key)
        f = find_fuel(r)
        if f is not None:
            fuels.append(f)
    sm = ccl

    # ----------------------------------------------------------------------------------------------


    # Check that all fuel elements are of the same height and 
    # have the same z coordinate:
    z = fuels[0].abspos().z
    Z = fuels[0].Z
    for f in fuels[1:]:
        if f.abspos().z != z:
            raise ValueError('There are fuel elements positioned at different z.')
        if f.Z != Z:
            raise ValueError('There are fuel elements of different height.')
    # currently, only a model with uncutted fuel elements can be processed:
    czmin, czmax = sm.extension('z')
    for f in fuels:
        fzmin, fzmax = f.extension('z')
        for p in f.get_parents():
            pzmin, pzmax = p.extension('z')
            if fzmin < pzmin or fzmax > pzmax:
                raise ValueError('Fuel element {0} cutted by its parent {1}'.format(f.get_key(), p.get_key()))
    if log:
        t2 = time.time()
        print 'fuel elements checked ', t2-t1
        t1 = t2

    # calculate the common mesh: 
    log_flag = False
    sm.temp.unify(sm.dens, log_flag)
    for f in fuels:
        for mesh in [f.temp, f.dens, f.heat]:
            sm.temp.unify(mesh, log_flag)
    # put the common mesh to all elements:
    sm.temp.unify(sm.dens, log_flag)
    for f in fuels:
        for mesh in [f.temp, f.dens]:
            sm.temp.unify(mesh, log_flag)
    if log:
        t2 = time.time()
        print 'common mesh generated ', t2-t1
        t1 = t2

    # save fuel keys:
    # new dictionary with element keys. Additionally, it has keys for fuel elements.
    skeys = {}
    skeys['coolant'] = sm.get_key()
    rkeys = []
    for r in sm.children: #### .values():
        rkeys.append(r.get_key())
    fkeys = []
    for f in fuels:
        fkeys.append(f.get_key())

    skeys['rods'] = rkeys
    skeys['fuels'] = fkeys

    if log:
        t2 = time.time()
        print 'Standardized model created. ', t2-t1

    return (sm, skeys)
        


