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

from pin_model import rod_key
from rod_models import pin_r3 

# 1

# create interface
SI = ScfInterface()# version='2.5')


# model elements to be considered as
# coolant container and rods:
### SI.keys['rods'].append(rod_key)
### SI.keys['coolant'] = ''

# 2

# TH specifications, Table 2, p.5
thp = 3565e6    # Core thermal power, W
Na = 193        # number of assemblies
Np = 264        # number of pins
Tin = 560.      # inlet temperature, K
cflow = 15849.4 * 1e3 # core flow, g/sec
Pin = 15.5e6    # inlet pressure 
Pin = 15.45e6   # while this is the exit pressure

### SI.inlet_temperature = Tin
### SI.total_power = thp / Na / Np       # average pin power
### SI.inlet_flow_rate = cflow / Na / Np # assuming no bypass
### SI.exit_pressure = Pin               # SCF accepts exit pressure 
# thi.pressure_drop = 0.02e6 

# 3

# SCF calculation control parameter
###   SI.calcon.get_variable('max_of_axial_flow_iterations').value = 1000
###   SI.corr.get_variable('roughness').value = 1e-5 # has no influence
###   SI.specpar.get_variable('rod_diameter').value = pin_r3*2 
###   SI.gsww.get_variable('rod_diameter').value = pin_r3*2 
###   SI.rodlayout.get_variable('number_of_fuel_nodes').value = 10 
###   SI.calcon.get_variable('axial_flow_convergence').value = 1e-5
###   SI.calcon.get_variable('boundary_pressure_convergence').value = 1e-5
###   SI.calcon.get_variable('lateral_flow_damping').value = -1.0
###   SI.calcon.get_variable('axial_flow_damping').value = -0.5
###   SI.calcon.get_variable('sor_acceleration').value = 1.9
###   
###   SI.latr.get_switch('set_constant_mixing_coefficient').state = 0
###   
###   # 4
###   
###   # Material names correspondence between general model and SCF
###   SI.materials['uo2'] = 'benpwr' # TH correlations for fuel from OECD benchmark
###   SI.materials['mox1'] = 'benpwr'
###   SI.materials['mox2'] = 'benpwr'
###   SI.materials['mox3'] = 'benpwr'
###   # SI.materials['uo2'] = 'uo2'
###   SI.materials['zirc'] = 'zircaloy'
###   
###   SI.materials['ifba'] = SI.materials['uo2']


