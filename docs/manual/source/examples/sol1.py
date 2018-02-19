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

b = Box()
b.X = 3
b.Y = 4
b.Z = 5
b.material = 'm1'

c1 = Cylinder()
c1.R = 1
c1.Z = 4
c1.material = 'm2'

b.insert(c1)

c2 = c1.copy_tree()
c2.material = 'm3'
c2.R = 0.8 
c2.pos.x = 0.8
c2.pos.y = 0.6

b.insert(c2)


colormap(b, filename='sol1z.png')
colormap(b, plane={'x':0}, filename='sol1x.png')

