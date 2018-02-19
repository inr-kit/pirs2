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


h1 = Mixture('H')
he = Mixture('He')

m1 = h1 + he
m2 = 2*h1
m3 = 2*h1 + 3*he
m4 = 2*m1 + 3*m2

m1.name = 'm1'
m2.name = 'm2'
m3.name = 'm3'
m4.name = 'm4'

for m in [m1, m2, m3, m4]:
    print m.report()
    print '='*30

