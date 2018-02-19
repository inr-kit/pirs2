from pirs.solids import Cylinder
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

from pin_model import model as cell

"""
IFBA fuel pin.  Copy of standard pin, with layer of ifba added.
"""
# data from table 6, p.8:
r1 = 0.3951
r2 = 0.3991

# geometry: copy of pin
ifba_pin = cell.get_child('clad').copy_tree()
# add layer of ifba to the 'gap' element:
gap = ifba_pin.get_child('gap')
ifba = gap.insert(Cylinder(R=r2, Z=gap.Z, material='ifba'), 0)
ifba.name = 'ifba'

ifba.dens.set_values(1.69)






