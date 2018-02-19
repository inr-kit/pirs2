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

Compute Keff as function of coolant density.
"""
from a_model import a as model
from a_mcnp import MI

m1 = model
m2 = model.copy_tree()

MI.kcode.Nh = 100000
MI.kcode.Nct = 1000
MI.kcode.Ncs = 100

for d in [0.6, 0.7, 0.8]:
    m = model.copy_tree()
    for e in m.values(True):
        if e.material == 'bwater':
            e.dens.set_values(d)
    MI.gm = m
    MI.run('r')


