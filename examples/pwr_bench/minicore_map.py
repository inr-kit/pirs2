# This model uses the fact that there is no additional space
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

# between assemblies. Thus, the bundle of NxM assemblies can
# be represented as a single assembly with 17*N x 17*M lattice.

# create common map of pins. There are two kinds of
# pins: UOX and MOX.
from assembly_map import str2dict, map_string4, map_string2 
u_map = map_string2
m_map = map_string4


c_map = []
lu = u_map.splitlines()
lm = m_map.splitlines()
for (l1, l2) in zip(lu, lm): 
    c_map.append(l2 + l1 + l2)
for l1 in lu:
    c_map.append(l1 + l1 + l1)
for (l1, l2) in zip(lu, lm):
    c_map.append(l1 + l2 + l1)
c_map = '\n'.join(c_map)
print c_map
map_dict = str2dict(c_map)
print 'map dictionary is prepared'

from minicore_map2 import m as map_dict

