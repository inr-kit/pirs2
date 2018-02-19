"""
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

Test interpolation of cross sections by comparing
axial power profile.

Model -- one PWR pin with mox fuel.
"""
from pirs.solids import Box
from pirs.tools import dump

from rod_models import mox3
from pin_mcnp import MI

b = Box(Z=mox3.Z, X=1.26, Y=1.26)
b.material = 'bwater'
b.dens.set_grid([1, 1, 1])
b.dens.set_values([0.77, 0.74, 0.77])
b.insert(mox3)
f = mox3.children[0]
f.heat.set_grid([1]*10)

b.temp.set_values(600)
mox3.temp.set_values(600)

MI.gm = b

MI.kcode.Nh = 800000
MI.kcode.Nct = 4000
MI.kcode.Ncs = 3000

MI.adc[0] = 'prdmp j {0} 1'.format(MI.kcode.Nct/4)

ksrc = 'ksrc '
for c in f.heat.element_coords('abs'):
    ksrc += ' {0} {1} {2}'.format(*c)
MI.adc[1] = ksrc    

# mesh for shannon entrophy
MI.adc.append('HSRC 2 -{0} {0}  2 -{0} {0}  30 -{1} {1}'.format(b.X/2., b.Z/2.))

MI.wp.prefix = 'jnter'
# MI.wp.exe = 'mpirun ' + MI.wp.exe
Ntasks = 4 


f.temp.set_values(900)
MI.run('R', tasks=Ntasks)
dump('jnter09.dump', r=MI.gm)

MI.xsdir.read(MI.xsdir.datapath + '/xsd900') # xsdir without xs for 900 K
MI.run('R', tasks=Ntasks)
dump('jnter09i.dump', r=MI.gm)

exit()

f.temp.set_values(800)
MI.run('R', tasks=Ntasks)
dump('jnter08.dump', r=MI.gm)

f.temp.set_values(1000)
MI.run('R', tasks=Ntasks)
dump('jnter10.dump', r=MI.gm)


