from pin_scf import SI, thp, Na, Np, cflow
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

from assembly_model import rod_keys, Nx, Ny

# 1

# change keys, specifying rod elements
# in the general model:
SI.keys['rods'] = rod_keys

# 2

# adjust total power:
SI.total_power = thp / Na # / Np * Nx*Ny 

# adjust flow rate:
SI.inlet_flow_rate = cflow / Na #  / Np * Nx*Ny



if __name__ == '__main__':
    from assembly_model import model
    SI.gm = model
    SI.keys['coolant'] = ''
    SI.run('R')

