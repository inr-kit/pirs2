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


c = Surface('rcc 0 0 0   0 0 10  4')

# mapping surface -> ID
l = []
for f in c.facets():
    l.append(f.a1[1])
m = lambda s: l.index(s) + 1

# macrobody exterior defined by simple surfaces
v = c.volume(m)
print ' c cells'
print '1 0 ',  v, ' $ cylinder exterior'
print '2 0 ', -v, ' $ cylinder interior'

print ''
print 'c surfaces:'
for s in l:
    print str(s).format(m(s))
