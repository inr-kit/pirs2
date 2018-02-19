from hmcnp3 import mi
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

# additional cell cards
mi.acc.append('c commented cell card')

# additional surface cards
mi.asc.append('c commented surface card')

# additional data cards
ksrc = 'ksrc '
for v in mi.gm.values(True):
    if v.material == 'fuel':
        x, y, z = v.abspos().car
        ksrc += '  {0} {1} {2}'.format(x, y, z-v.Z*0.49)
        ksrc += '  {0} {1} {2}'.format(x, y, z)
        ksrc += '  {0} {1} {2}'.format(x, y, z+v.Z*0.49)
mi.adc.append(ksrc)

# kcode card
mi.kcode.active = True # otherwise commented
mi.kcode.Nh = 1000 # histories per cycle
mi.kcode.Ncs = 20 # cycles to skip
mi.kcode.Nct = 100 # total num of cycles

if __name__ == '__main__':
    mi.wp.prefix = 'm4_'
    mi.run('P')

