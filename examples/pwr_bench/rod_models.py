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

Geometry of rods used in OECD NEA benchmark.
"""

# 1

# Dimensions form the benchmark
# www.oecd-nea.org/science/wprs/MOX-UOX-transients/benchmark_documents/
# specifications/mox_bench_spec.pdf

# Table 2, p.5:
ah = 365.76 # active height, cm
ap = 21.42  # assembly pitch, cm
pp = 1.26   # pin pitch, cm

# Table 6, p.8:
pin_r1 = 0.3951  # fuel pellets radius, cm
pin_r2 = 0.4010  # clad inner radius, cm
pin_r3 = 0.4583  # clad outer radius, cm

ifba_r1 = 0.3951
ifba_r2 = 0.3991
ifba_r3 = 0.4010
ifba_r4 = 0.4583

tube_r1 = 0.5624
tube_r2 = 0.6032

waba_r1 = 0.2858
waba_r2 = 0.3531
waba_r3 = 0.4039
waba_r4 = 0.4839

# 2

from pirs.solids import Cylinder
# from pin_mcnp import moxfrac

# 2a

# pin model -----------------------------------------------------------------------------
clad = Cylinder(R=pin_r3, Z=ah)
gap  = Cylinder(R=pin_r2, Z=ah)
fuel = Cylinder(R=pin_r1, Z=ah)
# do not model gap explicitly
# clad.insert('gap', gap)
clad.clad_thickness = (pin_r3 - pin_r2) * 1e-2 # SCF length unit is 1 m.
clad.pu_fraction = 0.
clad_dens_coeff = (pin_r3**2 - pin_r2**2) / (pin_r3**2 - pin_r1**2) 

# gap.insert('fuel', fuel)
clad.insert(fuel)
fuel.name = 'fuel'
fuel_key = fuel.get_key()

clad.material = 'zirc'
# gap.material = 'oxygen'
fuel.material = 'uo2'

clad.dens.set_values(6.504 * clad_dens_coeff)
clad.temp.set_values(600.)

# gap.dens.set_values(0.001)
# gap.temp.set_values(600.)

fuel.temp.set_values(1200)
fuel.dens.set_values(10.21)
fuel.heat.set_grid([1, 1, 2, 2, 3, 3, 3, 2, 2, 1, 1])
fuel.heat.set_values(0.5)

# precision for TH parameters in the MCNP model:
# fuel.temp.prec = 1. # all fuel temperatures are rounded to 10.

pin = clad.copy_tree()
pin.name = 'uox_pin'

# UOX pins -----------------------------------------------------------------------------
uox = pin.copy_tree()

# MOX pins -----------------------------------------------------------------------------
mox1 = pin.copy_tree()
mox2 = pin.copy_tree()
mox3 = pin.copy_tree()

mox1.get_child(fuel_key).material = 'mox1'
mox2.get_child(fuel_key).material = 'mox2'
mox3.get_child(fuel_key).material = 'mox3'

mox1.get_child(fuel_key).dens.set_values(10.41)
mox2.get_child(fuel_key).dens.set_values(10.41)
mox3.get_child(fuel_key).dens.set_values(10.41)
mox1.name = 'mox1_pin'
mox2.name = 'mox2_pin'
mox3.name = 'mox3_pin'



# 3

# ifba model 1: in SCF model, gap is from fuel to clad ----------------------------------
coat = Cylinder(R=ifba_r2, Z=ah, material='ifba')
coat.dens.set_values(1.69)
coat.temp.set_values(600.)

ifba = pin.copy_tree()
# gap = ifba.get_child('gap')

ifba.insert(coat, 0)
coat.name = 'coat'
ifba.name = 'ifba_pin'
ifba_fuel_key = ifba.children[1].get_key()
ifba_ab_key = coat.get_key()


# 4

# guide tube model ----------------------------------------------------------------------
tube = Cylinder(R=tube_r2, Z=ah, material='zirc')
tube.temp.set_values(600.)
tube.dens.set_values(6.504)

wch = Cylinder(R=tube_r1, Z=ah, material='swater') # water channel
wch.temp.set_values(580.)
wch.dens.set_values(0.71187)

tube.insert(wch)
tube.name = 'tube_rod'

# water channels -------------------------------------------------------------------------
chan = tube.copy_tree()
chan.name = 'chan_rod'

# WABA rods ------------------------------------------------------------------------------
waba = tube.copy_tree()
l1 = waba.insert(Cylinder(R=waba_r4, Z=ah, material='zirc'))
l2 = waba.insert(Cylinder(R=waba_r3, Z=ah, material='waba'))
l3 = waba.insert(Cylinder(R=waba_r2, Z=ah, material='zirc'))
l4 = waba.insert(Cylinder(R=waba_r1, Z=ah, material='swater'))

l1.temp.set_values(580.)
l2.temp.set_values(580.)
l3.temp.set_values(580.)
l4.temp.set_values(580.)

l1.dens.set_values(6.504)
l2.dens.set_values(3.5635)
l3.dens.set_values(6.504)
l4.dens.set_values(0.71187)

l1.name = 'waba_o_clad'
l2.name = 'waba'
l3.name = 'waba_i_clad'
l4.name = 'water'

waba.name = 'waba_rod'
waba_ab_key = l2.get_key()


# let's model an absorber rod in the tube:
# ar = wch.insert('absorber rod', Cylinder(R=tube_r1*0.9, Z=ah))
# ar.material = 'ifba'
# ar.pos.z = ah*0.7
# ar.dens.set_values(1.69)
# ar.temp.set_values(600.)






