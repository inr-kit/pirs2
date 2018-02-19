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

from pirs.tools.plots import colormap

c = Cylinder(Z=2)

# heat
c.heat.set_grid([1, 2, 1])
c.heat.set_values([0.1, 0.2, 0.3])

# temperature
c.temp.set_grid([1]*20)
c.temp.set_values(lambda z: 300 + 100*z)

# density
c.dens.set_grid([1]*5)
c.dens.set_values(1.)

colormap(c, var='heat', plane={'x':0}, filename='sol3h.png')
colormap(c, var='temp', plane={'x':0}, filename='sol3t.png')
colormap(c, var='dens', plane={'x':0}, filename='sol3d.png')



