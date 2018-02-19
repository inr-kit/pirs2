from pirs.mcnp import Material
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


u = Material((92235,  4, 2), (92238, 96, 2))
p = Material((94239, 90, 2), (94240, 10, 2))
o = Material(8016)

uox = u + 2*o
pox = p + 2*o

mox = Material((uox, 1), (pox, 1))
print mox.report()

def of(m):
    a1 = m.how_much(1, ZAID=[92235, 94239])
    a2 = m.how_much(1, Z=[92, 94])
    return a1 / a2 - 0.10

mox.tune(of, [uox, pox])
print mox.report()
print mox.how_much(1, ZAID=[92235, 94239])
print mox.how_much(1, Z=[92, 94])
