u4_f = 1.215
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

u4_c = 0.1771

u5_f = 1.219
u5_c = 0.9519e-1

u8_f = 0.2998
u8_c = 0.7019e-1

print 'u5: ', u5_f/(u5_f+u5_c)
print 'u8: ', u8_f/(u8_f+u8_c)

from pirs.mcnp import Material
u = Material('U')
a4 = u.how_much(1, 92234).v
a5 = u.how_much(1, 92235).v
a8 = u.how_much(1, 92238).v
print a5, a8
print u.report()

kinf = (a4*u4_f + a5*u5_f + a8*u8_f) / (a4*(u4_f + u4_c) + a5*(u5_f + u5_c) + a8*(u8_f + u8_c))
print kinf
