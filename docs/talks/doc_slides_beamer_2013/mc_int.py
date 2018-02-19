from hpmc import McnpInterface
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

from mcnp import Material

m = McnpInterface(b)

u = Material((92235, 0.5, 2),
             (92238, 95.5, 2))

o = Material('O')
h = Material('H')

f = u + 2*o
w = h*2 + o
w.thermal = 'lwtr'


f.sdict[8018] = 8016
w.sdict[8018] = 8016

m.materials['fuel'] = f
m.materials['water'] = w

m.bc['radial'] = '*'

m.adc.append('ksrc 0 0 0')
m.adc.append('kcode 500 1. 20 100')

m.run('P')

r = m.run('R')
