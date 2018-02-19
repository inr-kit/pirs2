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


b = Box(X=3, Y=3)

c = Cylinder(R=0.4)

b.grid.x = 1
b.grid.y = 1

for i in [0, 1]:
    for j in [0, 1]:
        cc = c.copy_tree()
        b.grid.insert((i, j, 0), cc)
        cc.material = 'm{}{}'.format(i,j)

from pirs.tools.plots import colormap
colormap(b, filename='ex3_1.pdf')

b.grid.center()
colormap(b, filename='ex3_2.pdf')

