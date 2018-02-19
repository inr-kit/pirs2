from pirs.mcnp import Material, Surface, Cell, Model
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


c1 = Cell()

# Cell 1 
c1.mat = Material('Fe')
c1.rho = -10.
c1.vol = Surface('so 8.0').volume()
c1.opt['imp:n'] = 1

# Cell 2
c2 = Cell()
c2.vol = -c1.vol

# direct use of cells
print c1.card()
print c2.card()

# cells in a model
m = Model()
m.cells.append(c1)
m.cells.append(c2)

for c in m.cards():
    print c

