from pirs.solids import Box
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

from pirs.mcnp import Material
from pirs import McnpInterface

# GEOMETRY 
b = Box(material='m1')
b.dens.set_values(18.8)

# MCNP-SPECIFIC DATA
i = McnpInterface(b)
i.materials['m1'] = Material('U')  # material
i.bc['axial'] = '*'               # b.c.
i.bc['radial'] = '*'
i.adc.append('ksrc 0 0 0')        # kcode source
i.adc.append('kcode 100 1 30 100')

if __name__ == '__main__':
    # RUN MCNP
    i.run('R')                # start MCNP 
    print 'K-inf:', i.keff()  # print Keff
