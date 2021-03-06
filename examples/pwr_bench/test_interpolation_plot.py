from pirs.tools import load
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

from pirs.tools.plots import MeshPlotter

r9 = load('jnter09.dump')['r']
r9i = load('jnter09i.dump')['r']

r9 = r9.get_child((0,0))
r9i = r9i.get_child((0,0))



g = MeshPlotter()


# heat
g.add_line(0, 0, (), 'heat', 0, color='r', label='900')
g.add_line(0, 1, (), 'heat', 0, color='k', label='900i')
# differences
g.add_line(1, 2,    (), 'heat', 0, color='k', label='900 - 900i')

# axial symmetry
g.add_line(2, 3,    (), 'heat', 0, color='r', label='900(z) - 900(-z)')
g.add_line(2, 4,    (), 'heat', 0, color='k', label='900i(z) - 900i(-z)')

# symmetrized difference
g.add_line(3, 5,    (), 'heat', 0, color='k', label='sym 900 - 900i')

# data for int. differences
di = r9.copy_tree()
di.heat = r9.heat - r9i.heat

# data for axial symmetry
a = []
for r in [r9, r9i]:
    rev = r.copy_tree()
    rev.heat.set_values(list(reversed(r.heat.values())))
    rev.heat = rev.heat - r.heat
    a.append(rev)

# data for symmetrized difference
b = []
for r in [r9, r9i]:
    rev = r.copy_tree()
    vals = list(rev.heat.values())
    sym = []
    for v1, v2 in zip(vals, reversed(vals)):
        sym.append((v1 + v2)*0.5)

    rev.heat.set_values(sym)
    b.append(rev)

b[0].heat = b[0].heat - b[1].heat

f = g.figure(r9, r9i, di, a[0], a[1], b[0])
f.savefig('test_inter.pdf')


