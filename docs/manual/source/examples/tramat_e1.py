from pirs.core.tramat import Nuclide
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


n1 = Nuclide((2, 4, 0)) # tuple (Z, A, I)
n2 = Nuclide('He-4')    # string
n3 = Nuclide('Ag-110m') # string for isomer
n4 = Nuclide(2004)      # ZAID integer
n5 = Nuclide(n4)        # copy of n4.

for n in [n1, n2, n3, n4, n5]:
    print repr(n), n.name, n.ZAID, n.M()

