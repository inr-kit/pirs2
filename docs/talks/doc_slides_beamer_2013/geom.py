from hpmc import Box, Cylinder
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


b = Box(X=1.2, Y=1.2, Z=110)
c = Cylinder(R=0.5, Z=100)
b.insert(0, c)

b.material = 'water'
c.material = 'fuel'

b.dens.set_grid([1, 1])
b.dens.set_values(1.)

c.temp.set_grid([1]*3)
b.temp.set_values([300, 500, 350])

c.heat.set_grid([1]*10)


