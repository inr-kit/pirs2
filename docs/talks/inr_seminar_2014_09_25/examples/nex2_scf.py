from pirs import ScfInterface
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

from pirs.scf2 import RodMaterial
from ex2_geom import b

c = b.children[0]
g = c.children[0]
f = g.children[0]
c.Z = f.Z
g.Z = f.Z
b.Z = f.Z

b.grid.insert( (0,0,0), c)
b.grid.x = b.X
b.grid.y = b.Y
b.grid.z = b.Z
c.pos *= 0.

print c.ijk
print b

i = ScfInterface(b)
i.exit_pressure = 15.45e6 # Pa
i.inlet_temperature = 560 - 273.15 # C
i.inlet_flow_rate = 0.28 # g/s
i.total_power = 6e4     # W

# rod T/H parameters
cld = RodMaterial()
cld.gc = 1e2
uox = RodMaterial()
uox.gc = 1e4
uox.fp = 'benpwr'
i.materials['steel'] = cld
i.materials['fuel'] = uox

if __name__ == '__main__':
    f.heat.set_grid([1]*10)
    f.heat.set_values(1.)
    i.run('R')
    from pirs.tools.plots import colormap
    colormap(b, {'z':0}, filename='ex2sz.pdf')
    colormap(b, {'x':0}, filename='ex2sx.pdf', aspect='auto')

    colormap(b, {'x':0}, filename='ex2sh.pdf', aspect='auto', var='heat')
    colormap(b, {'x':0}, filename='ex2st.pdf', aspect='auto', var='temp')
    colormap(b, {'x':0}, filename='ex2sd.pdf', aspect='auto', var='dens')


