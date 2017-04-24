# This model uses the fact that there is no additional space
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

