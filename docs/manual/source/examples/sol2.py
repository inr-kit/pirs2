from pirs.solids import Box, Cylinder
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

from pirs.tools.plots import colormap

# pin model
pin = Cylinder(R=0.45, Z=100, material='clad')
pin.insert(Cylinder(R=0.4, Z=pin.Z-5, material='fuel'))

# assembly box
a = Box(X=5, Y=7, Z=pin.Z+10, material='water')
a.grid.x = 1
a.grid.y = 1.1
a.grid.z = a.Z

# insert pins
for i in range(5):
    for j in range(6):
        a.grid.insert((i,j,0), pin.copy_tree())

# center grid with respect to solid
a.grid.center()

colormap(a, filename='sol2z.png')
colormap(a, plane={'x':0}, filename='sol2x.png', aspect='auto')




