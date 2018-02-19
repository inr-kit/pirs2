from pirs.core.tramat import Mixture
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


m1 = Mixture(1001)   # mixture conatins only H-1
m2 = Mixture('He')   # mixture of He nuclide with nat. abund.
# Mixture does not accept string representation of a nuclide:
# m2 = Mixture('He-4') # will cause an error

m3 = Mixture(m1, (0.1, 1), m2, (0.9, 1))  # 0.1 mole of m1 and 0.9 moles of m2
m4 = Mixture(m1, (0.1, 2), m2, (0.9, 2))  # 0.1 g of m1 and 0.9 g of m2
m5 = Mixture(m1, (0.1, 1), m2, (0.9, 2))  # 0.1 mole of m1 and 0.9 g of m2.

m1.dens = 1.0  # g/cm3
m6 = Mixture(m1, (0.1, 3), m2, (0.9, 1))  # 0.1 cm3 of m1 and 0.9 moles of m2

for m in [m1, m2, m3, m4, m5, m6]:
    print m.report()
    print '='*30
