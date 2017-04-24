from .variables import ScfVariable, ScfTable, ScfSwitch, ScfGroup

def init(model):
    model.append(ScfGroup('initialisation'))
    model.append(ScfGroup('properties'))
    model.append(ScfGroup('correlations'))
    model.append(ScfGroup('special_parameters'))
    model.append(ScfGroup('axial_heat_flux'))
    model.append(ScfGroup('channel_layout'))
    model.append(ScfGroup('thermal_connection'))
    model.append(ScfGroup('channel_area_variation'))
    model.append(ScfGroup('gap_spacing_variation'))
    model.append(ScfGroup('rod_layout'))
    model.append(ScfGroup('calculation_control'))
    model.append(ScfGroup('grid_spacer_wire_wrap'))
    model.append(ScfGroup('lateral_transport'))
    model.append(ScfGroup('operating_conditions'))
    model.append(ScfGroup('pointkinetics'))
    model.append(ScfGroup('output_display'))

    # create variables, switches and tables:

    grp = model['initialisation']
    grp.append(ScfVariable('title', 'title of the problem'))

    grp = model['properties']
    grp.append(ScfSwitch('set_water', 
                         'set_lead_bismuth', 
                         'set_lead', 
                         'set_sodium', 
                         'set_helium', 
                         'set_air'))

    grp = model['correlations']
    grp.append(ScfSwitch('set_subcooled_void_levy',                        # switch-1
                         'set_subcooled_void_saha_zuber', 
                         'set_subcooled_void_unal', 
                         'set_subcooled_void_bowring', 
                         'set_subcooled_void_none'))
    grp.append(ScfSwitch('set_boiling_void_homogeneous',                   # switch-2
                         'set_boiling_void_armand_mod', 
                         'set_boiling_void_smith', 
                         'set_boiling_void_chexal_lellouche'))
    grp.append(ScfSwitch('set_two_phase_friction_homogeneous',              # switch-3
                         'set_two_phase_friction_armand',
                         'set_two_phase_friction_lockhart'
                         ))
    grp.append(ScfSwitch('set_turbulent_friction_blasius',                 # switch-4
                         'set_turbulent_friction_rehme_wire',
                         'set_turbulent_friction_rehme_grid',
                         'set_turbulent_friction_churchill'
                         ))
    grp.append(ScfSwitch('set_heat_transfer_dittus_boelter',                # switch-5
                         'set_heat_transfer_gnielinski',
                         'set_heat_transfer_subbotin'
                         ))
    grp.append(ScfSwitch('set_chf_barnett+b&w',                             # switch-6
                         'set_chf_biasi',
                         'set_chf_okb',
                         'set_chf_w3',
                         'set_chf_levitan',
                         'set_chf_epri'
                         ))
    grp.append(ScfSwitch('set_shape_chf_none',                              # switch-7
                         'set_shape_chf_cobra4i',
                         'set_shape_chf_tong',
                         'set_shape_chf_w3',
                         'set_shape_chf_smolin'
                         ))
    grp.append(ScfSwitch('set_simple_fuel_cladding_gap',                    # switch-8
                         'set_transuranus_urgap_fuel_cladding_gap',
                         'set_vver1000_benchmark_fuel_cladding_gap'
                         ))
    grp.append(ScfVariable('blasius_laminar_prefactor', ''))
    grp.append(ScfVariable('blasius_laminar_reynolds_exponent', ''))
    grp.append(ScfVariable('blasius_laminar_constant', ''))
    grp.append(ScfVariable('blasius_turbulent_prefactor', ''))
    grp.append(ScfVariable('blasius_turbulent_reynolds_exponent', ''))
    grp.append(ScfVariable('blasius_turbulent_constant', ''))
    grp.append(ScfVariable('roughness', 3e-6))
    grp.append(ScfVariable('dittus_boelter_prefactor', ''))
    grp.append(ScfVariable('dittus_boelter_reynolds_exponent', ''))
    grp.append(ScfVariable('dittus_boelter_prandtl_exponent', ''))
    grp.append(ScfVariable('dittus_boelter_constant', 0.))
    grp.append(ScfVariable('effective_emissivity', 0.))
    grp.append(ScfVariable('chf_multiplier', 1e10))

    grp = model['special_parameters']
    grp.append(ScfVariable('rod_pitch', 0.))
    grp.append(ScfVariable('rod_diameter', 0.))
    grp.append(ScfVariable('wire_wrap_pitch', 0.))
    grp.append(ScfVariable('wire_wrap_diameter', 0.))
    grp.append(ScfVariable('perimeter_ratio', 0.))

    grp = model['axial_heat_flux']
    # this table must contain at least two entries, even if actual
    # heat profile is define elsewhere
    grp.append(ScfTable('relative_axial_location', 'relative_heat_flux'))
    # grp[0].rows.append([0, 0])
    # grp[0].rows.append([1, 0])

    grp = model['channel_layout']
    grp.append(ScfTable('channel_number', 'channel_area', 'wetted_perimeter', 'heated_perimeter', 'x_position', 'y_position'))
    grp.append(ScfTable('channel', 'max_40_x_(neighbour+gap+distance)'))
    grp[-1].NCmax = 19

    grp = model['thermal_connection']
    grp.append(ScfTable('connection_number', 'rho_cp_thickness', 'wall_width', 'first_channel', 'resistance', 'second_channel', 'resistance'))

    grp = model['channel_area_variation']
    grp.append(ScfVariable('gradual_insertion_iterations', 1))
    grp.append(ScfTable('channel_number', 'axial_location', 'channel_area', 'wetted_perimeter', 'heated_perimeter'))

    grp = model['gap_spacing_variation']
    grp.append(ScfTable('gap_number', 'axial_location', 'gap_spacing'))

    grp = model['rod_layout']
    grp.append(ScfSwitch('set_burnup_by_transient'))
    grp.append(ScfSwitch('set_axial_conduction', 'set_radial_twigl', 'set_radial_sor', 'set_radial_dir'))
    grp.append(ScfVariable('number_of_fuel_nodes', 2))
    grp.append(ScfVariable('minimum_fuel_cladding_gap_conductance', 500.))
    grp.append(ScfTable('rod_number', 'material_type', 'outer_diameter', 'power_fraction', 'x_position', 'y_position'))
    grp.append(ScfTable('rod', 'max_6_x_(channel+fraction)'))
    grp[-1].NCmax = 12
    grp.append(ScfTable('material', 'property', 'fuel_conductivity', 'fuel_specific_heat', 'fuel_density', 'fuel_emissivity', 'fuel_thermal_expansion'))
    grp.append(ScfTable('material', 'fuel_diameter', 'fuel_inner_radius', 'fraction_of_theoretical_density', 'fraction_of_puo2', 'fuel_roughness'))
    grp.append(ScfTable('material', 'property', 'clad_conductivity', 'clad_specific_heat', 'clad_density', 'clad_emissivity', 'clad_thermal_expansion'))
    grp.append(ScfTable('material', 'clad_thickness', 'gap_conductance', 'fill_gap', 'model_gap', 'clad_roughness', 'fill_gas_pressure', 'fill_gas_volume'))
    grp.append(ScfTable('configuration_type', 'number_of_zones'))
    grp.append(ScfTable('configuration_type', 'zone_number', 'zone_end_relative_axial_location', 'material'))
    grp.append(ScfTable('rod_number', 'relative_axial_location', 'burnup'))
    grp.append(ScfTable('rod_number', 'molar_fraction_he', 'molar_fraction_xe', 'molar_fraction_ar', 'molar_fraction_kr', 'molar_fraction_h', 'molar_fraction_n'))

    grp = model['calculation_control']
    grp.append(ScfSwitch('set_sor_iteration', 'set_gauss_elimination', 'set_bicgstab_iteration'))
    # grp.append(ScfSwitch('set_full_equations', 'set_incompressible', 'set_thermal_transient'))
    grp.append(ScfSwitch('set_boron_transport'))
    grp.append(ScfSwitch('set_buoyancy'))
    grp.append(ScfSwitch('set_critical_power_iteration'))
    grp.append(ScfVariable('start_time', 0.))
    grp.append(ScfVariable('stop_time', 0.))
    grp.append(ScfVariable('time_step', 0.))
    grp.append(ScfVariable('number_of_time_steps', 0))
    grp.append(ScfVariable('maximum_cladding_temperature_change', 100.))
    grp.append(ScfVariable('maximum_central_fuel_temperature_change', 100.))
    grp.append(ScfVariable('maximum_coolant_temperature_change', 100.))
    grp.append(ScfVariable('maximum_void_change', 1.))
    grp.append(ScfVariable('print_timestep_every', 1000))
    grp.append(ScfVariable('total_axial_length', 1))
    grp.append(ScfVariable('number_of_axial_nodes', 1))
    grp.append(ScfVariable('print_axial_level_every', 1))
    # grp.append(ScfVariable('sor_convergence', 1e-6))
    grp.append(ScfVariable('axial_flow_convergence', 1e-4))
    grp.append(ScfVariable('boundary_pressure_convergence', 1e-3))
    grp.append(ScfVariable('channel_orientation', 0.))
    grp.append(ScfVariable('lateral_flow_damping', 0.7))
    grp.append(ScfVariable('axial_flow_damping', 0.7))
    # grp.append(ScfVariable('pressure_damping', -1.))
    grp.append(ScfVariable('sor_acceleration', 1.0))
    grp.append(ScfVariable('max_of_axial_flow_iterations', 500))
    grp.append(ScfVariable('min_of_axial_flow_iterations', 10))
    # grp.append(ScfVariable('max_of_sor_iterations', 9999))
    # grp.append(ScfVariable('min_of_sor_iterations', 5))
    grp.append(ScfTable('time', 'time_step_size'))
    grp.append(ScfTable('cell_number', 'cell_length'))

    grp = model['grid_spacer_wire_wrap']
    grp.append(ScfSwitch('set_wire_wrap', 'set_grid_spacer', 'set_both'))
    grp.append(ScfVariable('gradual_insertion_iterations', 1))
    grp.append(ScfVariable('rod_diameter', 0))
    grp.append(ScfVariable('wire_wrap_pitch', 0))
    grp.append(ScfVariable('wire_wrap_thickness', 0))
    grp.append(ScfTable('gap_number', 'effective_length', 'relative_crossing', 'relative_crossing'))
    grp.append(ScfTable('channel_number', 'number_of_wire_wraps'))
    grp.append(ScfTable('channel_number', 'relative_axial_location', 'loss_coefficient'))
    grp.append(ScfTable('gap_number', 'relative_axial_location', 'cross_flow_fraction'))

    grp = model['lateral_transport']
    grp.append(ScfSwitch('set_constant_mixing_coefficient', 
                         'set_rogers_tahir_rectangular', 
                         'set_rogers_tahir_triangular', 
                         'set_rogers_rosehart'))
    grp.append(ScfSwitch('set_equal_mass_exchange', 
                         'set_equal_volume_exchange'))
    grp.append(ScfVariable('constant_mixing_coefficient', 0.))
    grp.append(ScfVariable('void_drift_coefficient', 1.4))
    grp.append(ScfVariable('crossflow_resistance_coefficient', 0.5))
    grp.append(ScfVariable('lateral_conduction_factor', 1.0))

    grp = model['operating_conditions']
    grp.append(ScfSwitch('set_uniform_inlet_flux', 
                         'set_flow_split_first_axial', 
                         'set_flow_rate_fraction', 
                         'set_flux_fraction',
                         'set_flow_rate',
                         'set_flux'))
    grp.append(ScfSwitch('set_pure_flow_condition',
                         'set_unified_pressure_drop',
                         'set_driving_pressure_condition'))
    grp.append(ScfSwitch('set_transient_flow_rate_factor',
                         'set_transient_flow_rate',
                         'set_transient_flux'))
    grp.append(ScfVariable('exit_pressure', 1.))
    grp.append(ScfVariable('inlet_temperature'))
    grp.append(ScfVariable('inlet_boron_concentration'))
    grp.append(ScfVariable('inlet_flow_rate'))
    grp.append(ScfVariable('inlet_mass_flux'))
    grp.append(ScfVariable('total_power'))
    grp.append(ScfVariable('average_heat_flux'))
    grp.append(ScfVariable('pressure_drop'))
    grp.append(ScfVariable('heat_fraction_moderator'))
    grp.append(ScfTable('channel_number', 'inlet_temperature'))
    grp.append(ScfTable('channel_number', 'inlet_flow'))
    grp.append(ScfTable('time', 'exit_pressure'))
    grp.append(ScfTable('time', 'inlet_temperature'))
    grp.append(ScfTable('channel_number', 'time', 'inlet_temperature'))
    grp.append(ScfTable('time', 'inlet_boron_concentration'))
    grp.append(ScfTable('channel_number', 'time', 'inlet_boron_concentration'))
    grp.append(ScfTable('time', 'inlet_flow'))
    grp.append(ScfTable('channel_number', 'time', 'inlet_flow'))
    grp.append(ScfTable('time', 'heat_flux_factor'))
    grp.append(ScfTable('power_map_time'))
    grp.append(ScfTable('axial_cell_number', 'rod_number', 'power_map'))

    grp = model['pointkinetics']
    grp.append(ScfVariable('set_pointkinetics_power', 'off'))
    grp.append(ScfVariable('pointkinetics_max_time_step', 1e-05))
    grp.append(ScfVariable('prompt_neutron_lifetime', 2e-05))
    grp.append(ScfVariable('power_weighting_exponent', 2.0))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_1', 0.000266))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_2', 0.001491))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_3', 0.001316))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_4', 0.002849))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_5', 0.000896))
    grp.append(ScfVariable('fraction_delayed_neutrons_group_6', 0.000182))
    grp.append(ScfVariable('decay_constant_group_1', 0.0127))
    grp.append(ScfVariable('decay_constant_group_2', 0.0317))
    grp.append(ScfVariable('decay_constant_group_3', 0.115))
    grp.append(ScfVariable('decay_constant_group_4', 0.311))
    grp.append(ScfVariable('decay_constant_group_5', 1.4))
    grp.append(ScfVariable('decay_constant_group_6', 3.87))
    grp.append(ScfVariable('doppler_coefficient', -2.8e-05))
    grp.append(ScfVariable('coolant_temperature_coefficient', -9.85e-05))
    grp.append(ScfVariable('void_coefficient', -0.12345))
    grp.append(ScfVariable('boron_coefficient', -2e-06))

    grp = model['output_display']
    grp.append(ScfVariable('delta_time', 1e6))
    grp.append(ScfTable('channel_number'))
    grp.append(ScfTable('rod_number'))
    grp.append(ScfTable('gap_number'))
    grp.append(ScfTable('axial_location', 'channel_or_rod_number', 'variable'))
    return
