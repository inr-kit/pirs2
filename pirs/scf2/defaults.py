"""
Default values for PWR model.
"""

def pwr_pin(model):
    g = model['initialisation']
    g['title'].value = 'Default data for PWR pin'

    g = model['properties']
    g['set_water'].state = 'set_water'

    g = model['correlations']
    g['bowring'].state = 'bowring'
    g['void_armand'].state = 'void_armand'
    g['friction_armand'].state = 'friction_armand'
    g['friction_blasius'].state = 'friction_blasius'
    g['set_heat_transfer'].state = 'dittus'
    g['set_chf_'].state = 'barnett'
    g['set_shape_'].state = 'chf_none'
    g['set_simple_fuel'].state = 'set_simple_fuel'
    p, e, c = g.find('blasius_laminar_')
    p.value = 64.0
    e.value = -1.0
    c.value = 0.
    p, e, c = g.find('blasius_turbulent_')
    p.value = 0.316
    e.value = -0.25
    c.value = 0.
    g['roughness'].value = 1.e-5
    p, re, pe, c = g.find('dittus_boelter_')
    p.value = 0.023
    re.value = 0.8
    pe.value = 0.4
    c.value = 0.

    g = model['rod_layout']
    g['number_of_fuel_nodes'].value = 10
    g['set_radial_dir'].state = 'set_radial_dir'

    model['grid_spacer_']['set_grid_spacer'].state = 'set_grid_spacer'

    g = model['calculation_control']
    g['bicgstab'].state = 'bicgstab'
    g['set_buoyancy'].state = 0
    g['axial_flow_conv'].value = 1e-7
    g['axial_flow_damp'].value = -0.5
    g['boundary_pressure_conv'].value = 1e-7
    g['lateral_flow_damp'].value = -1.0
    g['sor_acc'].value = 1.9

    g = model['lateral_transport']
    g.find('v', 'constant_mix')[0].value = 0.005
    g['set_constant_mix'].state = 'set_constant'
    g['set_equal_mass'].state = 'set_equal_mass'
    g['crossflow_resistance_coef'].value = 0.75
    g['lateral_conduction_factor'].value = 0.0

    g = model['operating_conditions']
    g['split_first'].state = 'split_first'
    g['set_pure_flow'].state = 'set_pure_flow'
    g['set_transient_flow'].state = 'rate_factor'
    g.find('v', 'inlet_boron_concentration')[0].value = 0.
    g['inlet_boron_conc'].value = 0.

    model.find('power_map_time')[0].rows.append([0])
    model.find('v', 'heat_fraction_moderator')[0].value = 0.




