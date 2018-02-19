
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

from pin_scf import SI, thp, Na, cflow
from minicore_model import rod_keys, Nax, Nay

# 1

# change keys, specifying rod elements
# in the general model:
SI.keys['rods'] = rod_keys
print 'SI.keys:', SI.keys.keys()

# there is new mox materials: 
SI.materials['mox1'] = 'benpwr'
SI.materials['mox2'] = 'benpwr'
SI.materials['mox3'] = 'benpwr'

# 2

# adjust total power:
SI.total_power = thp / Na *Nax*Nay 

# adjust flow rate:
SI.inlet_flow_rate = cflow / Na * Nax*Nay


if __name__ == '__main__':
    from minicore_model import minicore
    SI.gm = minicore
    SI.keys['coolant'] = ''
    SI.run('r')

