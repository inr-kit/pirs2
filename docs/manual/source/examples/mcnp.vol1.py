from pirs.mcnp import Volume
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


v1 = Volume(1, 'a')  
v2 = Volume(1, 'b')
v3 = Volume(-1, 'c')

# new volume as intersection and union
r = v1 & v2 | v3

# string representation of volume
print ' r: ', r
print '-r:', -r

# surface definition substitution
s = {}
s['a'] = 1
s['b'] = 2
s['c'] = 3

print ' r: ',  r.copy(s)
print '-r: ', -r.copy(s)


