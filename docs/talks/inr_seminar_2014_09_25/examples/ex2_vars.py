from ex2_geom import b
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


f = b.get_child((0, 0))

# fuel temperature axial profile
f.temp.set_grid([1, 1, 1])
f.temp.set_values(350)

# heat deposition axial profile
f.heat.set_grid([1, 1, 2, 3, 2, 1, 1])
f.heat.set_values([1, 2, 3, 4, 3, 2, 1])

# density axial profile in water
b.dens.set_grid([1, 1, 1])
b.dens.set_values([0.7, 0.65, 0.6])

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    colormap(b, {'x':0}, var='heat', filename='ex2t.pdf', aspect='auto')

