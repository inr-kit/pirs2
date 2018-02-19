from pirs.mcnp import Surface
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


s1 = Surface('px 1.0 $ a plane')
s2 = Surface('* pz 5.1')

s3 = Surface(type='c/z', plst=[0, 0, 6], cmnt='cylinder at z axis')
s4 = Surface('rcc 0 0 0  0 0 5  3')

#surface cards
for s in [s1, s2, s3, s4]:
    print s.card()

