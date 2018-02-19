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

dmp = load('results/b_iteration_058.dump')

kkk = MeshPlotter()
kkk.figsize=(8,4)
kkk.add_line(0, 0, (), 'temp',  0, fmt='.k', label='$k_{eff}$')
kkk.xlabel[0] = 'Iteration index'
kkk.ylabel[0] = '$k_{eff}$'

Keff = dmp['Keff'][2:]
Kerr = dmp['Kerr'][2:]
fig = kkk.figure([range(1, len(Keff)+1), Keff, Kerr])
fig.savefig('res_keff.pdf')
