from pirs.solids import Box, Cylinder
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


cnt = Box(X=2.53, Y=2.53, Z=365, material = 'water')
r = Cylinder(R=0.4583, Z=365, material = 'steel')
f = Cylinder(R=0.3951, Z=365, material = 'fuel')

r.insert(f)
cnt.insert(r)

r2 = cnt.insert(r.copy_tree())
r2.pos.x = 0.8 
r2.pos.y = 0.8

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    pz = colormap(cnt, plane={'z':0})
    px = colormap(cnt, plane={'x':0}, aspect='auto')
    py = colormap(cnt, plane={'y':0}, aspect='auto')
    pz.get_figure().savefig('geom1_pz.pdf')
    px.get_figure().savefig('geom1_px.pdf')
    py.get_figure().savefig('geom1_py.pdf')

