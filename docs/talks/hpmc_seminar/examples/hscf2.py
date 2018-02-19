from hscf1 import si
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


# set boundary conditions
si.find('total_power')[0].value = 7e4*4 # W 
si.find('average_heat_flux')[0].value = 0.0
si.find('inlet_temperature')[0].value = 280 # C
si.find('inlet_flow_rate')[0].value = 0.28*4 # g/sec 
si.find('inlet_mass_flux')[0].value = 0.
si.find('set_driving_pressure_condition')[0].state = 'set_pure_flow_condition'
si.find('exit_pressure')[0].value = 15.45e6 # Pa 
si.find('v', 'pressure_drop')[0].value = 0. 
si.find('inlet_boron_concentration')[0].value = 0. 
si.find('heat_fraction_moderator')[0].value = 0. 

si.find('number_of_fuel_nodes')[0].value = 10

# variables:
si.find('blasius_laminar_prefactor')[0].value = 64.0
si.find('blasius_laminar_reynolds_exponent')[0].value = -1.0 
si.find('blasius_laminar_constant')[0].value = 0 

si.find('blasius_turbulent_prefactor')[0].value = 0.316 
si.find('blasius_turbulent_reynolds_exponent')[0].value = -0.25 
si.find('blasius_turbulent_constant')[0].value = 0 

si.find('dittus_boelter_prefactor')[0].value = 0.023 
si.find('dittus_boelter_reynolds_exponent')[0].value = 0.8 
si.find('dittus_boelter_prandtl_exponent')[0].value = 0.4 
si.find('dittus_boelter_constant')[0].value = 0. 

si.find('set_buoyancy')[0].state = 0

si.find('power_map_time')[0].rows.append([0])

# set switches 
active = ['set_water',
          'set_subcooled_void_bowring',
          'set_boiling_void_armand_mod',
          'set_two_phase_friction_armand',
          'set_turbulent_friction_blasius', 
          'set_heat_transfer_dittus_boelter',
          'set_chf_barnett+b&w',
          'set_shape_chf_none',
          'set_simple_fuel_cladding_gap',
          'set_radial_dir',
          'set_bicgstab_iteration',
          'set_grid_spacer',
          'set_flow_split_first_axial',
          'set_transient_flow_rate_factor',
          'set_constant_mixing_coefficient',
          'set_equal_mass_exchange',
          ]
for sw in active:
    si.find('s', sw)[0].state = sw 

if __name__ == '__main__':
    si.wp.prefix = 's2_'
    si.run('r')
