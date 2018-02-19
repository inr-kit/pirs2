from geom1 import cnt
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


for v in cnt.values(True):
    v.temp.set_values(300.)

cnt.dens.set_values(1.0)
cnt.children[0].dens.set_values(5.0)
cnt.children[1].dens.set_values(5.0)

f1 = cnt.get_child((0,0))
f2 = cnt.get_child((1,0))

f1.temp.set_grid([1, 3, 1])
f1.temp.set_values([280, 320, 293])

f2.temp.set_grid([1, 2, 1])
f2.temp.set_values([275, 314, 293])

f1.dens.set_values(10.)
f2.dens.set_values(10.)

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    pd = colormap(cnt, plane={'y':0}, var='dens', aspect='auto')
    pt = colormap(cnt, plane={'y':0}, var='temp', aspect='auto')
    pd.get_figure().savefig('geom2_d.pdf')
    pt.get_figure().savefig('geom2_t.pdf')

