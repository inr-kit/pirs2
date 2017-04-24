from math import pi, sin
import time

from . import workplace

class ScfVariable(object):
    """
    Class to represent a SCF variable.

    Attributes:

        name: string name of the SCF variable,
        value: value of the SCF variable.
    """
    def __init__(self, name='var_name', value='var_value'):
        self.name = name
        self.value = value

        self.active = True
        return

    def clear(self):
        """
        Does nothing.
        """
        return

    def __str__(self):
        # FIXME add quotes to self.value, if necessary.
        #       Both quotes, ' and " are allowable in input.txt.
        #       Note that SCF treats in correct way both cases 
        #       (checked for the title):
        #       title = ' title of the problem is "name" '
        #       title = " title of the problem is 'name' "
        res = '{0} = {1}'.format(self.name, self.value)
        if not self.active:
            res = '! ' + res
        return res


class ScfTable(object):
    """
    SCF table has column names. External files not implemented.

    >>> t = ScfTable(['col_1', 'col_2', 'col_3'])
    >>> t.rows.append([0, 1, 5])
    >>> t.rows.append([1, 1, 4])
    >>> t.rows.append([2, 1, 3])
    >>> t.rows.append([3, 1, 2])

    >>> t[0]
    [0, 1, 5]
    >>> t['col_3']
    [5, 4, 3, 2]
    >>> t[0, 2]
    5

    >>> print t

    A special case: number of columns is less than the number of row elements.
    This case appears, for example, when representing the second table of the
    channel_layout group. In this case one has to specify explicitly the
    maximal number of columns, while if there are less entries in particular
    row, its string must end with zeroes or with the '/' character.

    >>> t = ScfTable()
    >>> t.columns.append('channel')
    >>> t.columns.append('max_40_x_(neighbour+gap+distance)')
    >>> t.rows.append([1, 2, 1., 1.])
    >>> t.rows.append([2, 3, 1., 1.])
    >>> t.NCmax = 19
    >>> print t


    """
    def __init__(self, columns=[]):
        self.__c = columns[:]  # column names.
        self.__r = []          # list with rows. Each element -- a list of table entries.
        self.__n = None        # max. number of columns.

    def __getitem__(self, key):
        if isinstance(key, int):
            # only one index given. Assume it is row's index,
            # return the whole row
            return self.__r[key]
        elif isinstance(key, tuple):
            # tuple is given. Assume this is (row, column) indices.
            i, j = key
            return self.__r[i][j]
        elif key in self.__c:
            # key is the name of the column. Return the whole column
            j = self.__c.index(key)
            return map(lambda x: x[j], self.__r)
        else:
            raise TypeError('Unsupported index type or value', i)

    @property
    def rows(self):
        """
        List of the rows.

        Each element of the list is a list of table entries.
        """
        return self.__r

    @property
    def columns(self):
        """
        List of the column names.
        """
        return self.__c

    def clear(self):
        """
        Removes all table's data.

        Does not change the column names and the number of columns!
        """
        self.__r = []


    @property
    def NCmax(self):
        """
        Maximal number of columns. 
        
        By default, it is set to None. In this case, the number of columns in
        the table is defined by the actually specified colmun names and by the
        actual table data.
        
        NCmax can be set manually. In this case, only this amount of column
        names and row elements is printed out.

        If a row contains less than NCmax elements, the corresponding string
        ends with the '/' character. Missing column names are replaced with
        empty string, '', so that they are not seen in the print-out.
        """
        if self.__n is None:
            NC1 = len(self.__c)
            NC2 = max( [0] + map(len, self.__r) )
            NCmax = max(NC1, NC2)
            return NCmax
        else:
            return self.__n

    @NCmax.setter
    def NCmax(self, value):
        self.__n = int(value)
        return

    def __str__(self):
        # prepare column names
        NCmax = self.NCmax
        Ncol = len(self.__c)
        if NCmax >= Ncol:
            cols = self.__c + ['']*(NCmax - Ncol)
        else:
            cols = self.__c[:NCmax]

        # prepare rows
        rows = []
        for r in self.__r:
            Nrow = len(r)
            if NCmax > Nrow:
                row = r[:] + ['/'] + ['']*(NCmax - Nrow - 1)
            elif NCmax == Nrow:
                row = r[:]
            else:
                row = r[:NCmax]
            rows.append(row)

        res = []
        res.append('file = this_file')

        # find columns width
        wmax = map(len, cols)
        for r in rows:
            w = map(lambda x: len(str(x)), r)
            wmax = map(max, zip(wmax, w))

        # format string
        f = map(lambda (i,x): '{{{0}:>{1}}}'.format(i,x), enumerate(wmax))
        f = '   '.join(f)

        # table head
        res.append(f.format(*cols))
        # table data
        for r in rows:
            res.append(f.format(*r))
        # end table with !, otherwise the end is not detected.
        res.append('!')

        return '\n'.join(res)






class ScfSwitch(object):
    """
    Each state must have name.

    Order of states, when written out, must be well defined.

    >>> ss = ScfSwitch()
    >>> ss.cn = 'set_subcooled_void_'
    >>> ss.add('levy')
    >>> ss.add('zuber')
    >>> ss.add('unal')
    >>> ss.add('bowring')
    >>> ss.add('none')
    >>> ss.state      # by default, the first state
    0
    >>> ss.state = 3  # state index to be turned on.
    >>> ss.state      # returns the current state switch
    3
    >>> print ss      # returns string for input.txt.
    set_subcooled_void_levy = off
    set_subcooled_void_zuber = off
    set_subcooled_void_unal = off
    set_subcooled_void_bowring = on
    set_subcooled_void_none = off
    <BLANKLINE>
    >>> ss.state = 'unal' # one can use state names as well.
    >>> print ss
    set_subcooled_void_levy = off
    set_subcooled_void_zuber = off
    set_subcooled_void_unal = on
    set_subcooled_void_bowring = off
    set_subcooled_void_none = off
    <BLANKLINE>
    """
    def __init__(self):
        self.__n = []
        self.__s = None

        self.cn = '' # states common name.
        self.active = True
        return

    def add(self, state_name):
        if self.__n == []:
            # when first state name is added, turn this state on.
            self.__s = 0
        self.__n.append(state_name)
        return

    def clear(self):
        """
        Resets the switch state to the default position. 
        
        Does not change the switch options!
        """
        self.state = 0

    @property
    def states(self):
        """
        List of the switch names. To append see add() method.
        """
        return map(lambda n: self.cn + n, self.__n)

    @property
    def state(self):
        """
        Current state of the switch.
        """
        return self.__s

    @state.setter
    def state(self, value):
        if value in self.__n:
            self.__s = self.__n.index(value)
        elif value is None:
            # this turns off all states, i.e. all states become 'off' value.
            self.__s = None
        else:
            i = int(value)
            e = self.__n[i] # to check that i is in the range.
            self.__s = i
        return

    def __str__(self):
        vals = ['off'] * len(self.__n)
        if self.__s is not None:
            # self.__s is the index.
            vals[self.__s] = 'on'

        res = []
        if not self.active:
            prefix = '! '
        else:
            prefix = ''
        for (n, v) in zip(self.states, vals):
            var = ScfVariable(n, v)
            res.append(prefix + str(var))
        res.append('')
        return '\n'.join(res)


class ScfGroup(list):
    """
    A list of objects (switches, variables, etc.) with the name.
    """
    def __init__(self, name='group_name'):
        super(ScfGroup, self).__init__()
        self.name = name
        return

    def clear(self):
        """
        Calls clear method of each element in the group
        """
        for e in self:
            e.clear()

    def get_table(self, *columns):
        """
        Returns the first table of the group having columns
        """
        s = set(columns)
        for e in self:
            if hasattr(e, 'columns') and set(e.columns).issuperset(s):
                return e
        else:
            raise ValueError('Group has no table with columns ', columns)

    def get_variable(self, name):
        """
        Returns the first variable (actually, any object having attribute 'name') of the group with the specified name.
        """
        for e in self:
            if hasattr(e, 'name') and name == e.name:
                return e
        else:
            raise ValueError('Group has no Variable with name ', name)

    def get_switch(self, name):
        """
        Returns the first switch of the group having state name specified in the argument. 
        """
        for e in self:
            if hasattr(e, 'states') and name in e.states:
                return e
        else:
            raise ValueError('Group has no switch with state name ', name)


    def __str__(self):
        res = ['&{0}'.format(self.name)]
        for e in self:
            res.append(str(e))
        return '\n'.join(res)

class InputData(object):
    """
    O-O representation of all keywords, tables and switches of the SCF input file.

    InputData is an ordered set (list, tuple, orderedDict) of ScfGroups.
    """
    def __init__(self, version='2.3'):
        # self.groups = 

        # initialize attributes
        self.clear_initialization()
        self.clear_properties()
        self.clear_correlations()
        self.clear_special_parameters()
        self.clear_axial_heat_flux()
        self.clear_channel_layout()
        self.clear_thermal_connection()
        self.clear_channel_area_variation()
        self.clear_gap_spacing_variation()
        self.clear_rod_layout()
        self.clear_calculation_control()
        self.clear_grid_spacer_wire_wrap()
        self.clear_lateral_transport()
        self.clear_operating_conditions()
        self.clear_output_display()
        return

    def clear_initialization(self):
        """
        Clear all input data in the initialization group.
        """
        self.initialization = ScfGroup('initialisation')
        self.init.append(ScfVariable('title', "'Title of the problem'"))

        # Properties
        self.prop = ScfGroup('properties')
        s = ScfSwitch()
        s.cn = 'set_'
        s.add('water')
        s.add('lead_bismuth')
        s.add('lead')
        s.add('sodium')
        s.add('helium')
        s.add('air')
        self.prop.append(s)

        # Correlations
        self.corr = ScfGroup('correlations')
        s = ScfSwitch()
        s.cn = 'set_subcooled_void_'
        s.add('levy')
        s.add('saha_zuber')
        s.add('unal')
        s.add('bowring')
        s.add('none')
        s.state = 3
        self.corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_boiling_void_'
        s.add('homogeneous')
        s.add('armand_mod')
        s.add('smith')
        s.add('chexal_lellouche')
        s.state = 1
        self.corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_two_phase_friction_'
        s.add('homogeneous')
        s.add('armand')
        s.add('lockhart')
        s.state = 1
        self.corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_turbulent_friction_'
        s.add('blasius')
        s.add('rehme_wire')
        s.add('rehme_grid')
        s.add('churchill')
        s.state = 0
        self.corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_heat_transfer_'
        s.add('dittus_boelter')
        s.add('gnielinski')
        s.add('subbotin')
        s.state = 0
        self.corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_chf_'
        s.add('barnett+b&w')
        s.add('biasi')
        s.add('okb')
        s.add('w3')
        s.add('levitan')
        s.add('epri')
        s.state = 0
        self.corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_shape_chf_'
        s.add('none')
        s.add('cobra4i')
        s.add('tong')
        s.add('w3')
        s.add('smolin')
        s.state = 0
        self.corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_'
        s.add('simple_fuel_cladding_gap')
        s.add('transuranus_urgap_fuel_cladding_gap')
        s.add('vver1000_benchmark_fuel_cladding_gap')
        s.state = 0
        self.corr.append(s)

        self.corr.append(ScfVariable('blasius_laminar_prefactor', 64.0))
        self.corr.append(ScfVariable('blasius_laminar_reynolds_exponent', -1.0))
        self.corr.append(ScfVariable('blasius_laminar_constant', 0.0))
        self.corr.append(ScfVariable('blasius_turbulent_prefactor', 0.316))
        self.corr.append(ScfVariable('blasius_turbulent_reynolds_exponent', -0.25))
        self.corr.append(ScfVariable('blasius_turbulent_constant', 0.0))
        self.corr.append(ScfVariable('roughness', 3e-6))
        self.corr.append(ScfVariable('dittus_boelter_prefactor', 0.023))
        self.corr.append(ScfVariable('dittus_boelter_reynolds_exponent', 0.8))
        self.corr.append(ScfVariable('dittus_boelter_prandtl_exponent', 0.4))
        self.corr.append(ScfVariable('dittus_boelter_constant', 0.0))
        self.corr.append(ScfVariable('chf_multiplier', 1.0e10))

        # special parameters
        self.specpar = ScfGroup('special_parameters')
        self.specpar.append(ScfVariable('rod_pitch', 0.))
        self.specpar.append(ScfVariable('rod_diameter', 8.5e-3))
        self.specpar.append(ScfVariable('wire_wrap_pitch', 0.))
        self.specpar.append(ScfVariable('wire_wrap_diameter', 0.))
        self.specpar.append(ScfVariable('perimeter_ratio', 0.))

        # axial heat flux
        self.heat = ScfGroup('axial_heat_flux')
        t = ScfTable(['relative_axial_location', 'relative_heat_flux'])
        t.rows.append([0., 1.])
        t.rows.append([1., 1.])
        self.heat.append(t)

        # channel layout. By default, two rods with axially-independent
        # properties are modelled.
        # 
        #  __________________
        # | 1 |    2    | 3  |
        # |   _         _    |
        # |_ /1\ _ _ _ /2\ _ |
        # |  \_/       \_/   |
        # | 4 |    5    |  6 |
        # |__________________|
                                    
        
        self.layout = ScfGroup('channel_layout')
        t1 = ScfTable()
        t1.columns.append('channel_number')
        t1.columns.append('channel_area')
        t1.columns.append('wetted_perimeter')
        t1.columns.append('heated_perimeter')
        t1.columns.append('x_position')
        t1.columns.append('y_position')

        pa = pi*r**2   # pin area
        a1 = (p/2.)**2 - pa/4.  # area 1
        a2 = (p**2)/2. - pa/2.  # area 2
        hp1 = pi*r/2.
        hp2 = pi*r
        wp1 = p + hp1
        wp2 = p + hp2
        t1.rows.append([1, a1, wp1, hp1,   -p/4.,  p/4.])  # coordinates assume that pin 1 at the origin.
        t1.rows.append([2, a2, wp2, hp2,    p/2.,  p/4.])
        t1.rows.append([3, a1, wp1, hp1,  p*1.25,  p/4.])
        t1.rows.append([4, a1, wp1, hp1,   -p/4., -p/4.])  # coordinates assume that pin 1 at the origin.
        t1.rows.append([5, a2, wp2, hp2,    p/2., -p/4.])
        t1.rows.append([6, a1, wp1, hp1,  p*1.25, -p/4.])

        t2 = ScfTable()
        t2.columns.append('channel')
        t2.columns.append('max_40_x_(neighbour+gap+distance)')
        t2.NCmax = 19
        g1 = p/2. - r
        g2 = p - 2*r
        d1 = 3./4.*p
        d2 = p/2.
        t2.rows.append([1, 2, g1, d1, 4, g1, d2])
        t2.rows.append([2, 3, g1, d1, 5, g2, d2])
        t2.rows.append([3, 6, g1, d2])
        t2.rows.append([4, 5, g1, d1])
        t2.rows.append([5, 6, g1, d1])
        t2.rows.append([6, 0, 0., 0.]) # FIXME is it needed inSCF?

        self.layout.append(t1)
        self.layout.append(t2)

        # thermal connection
        self.thcon = ScfGroup('thermal_connection')
        t = ScfTable()
        t.columns.append('connection_number')
        t.columns.append('rho_cp_thickness')
        t.columns.append('wall_width')
        t.columns.append('first_channel')
        t.columns.append('resistance')
        t.columns.append('second_channel')
        t.columns.append('resistance')
        self.thcon.append(t)

        # channel area variation
        self.areavar = ScfGroup('channel_area_variation')
        v = ScfVariable('gradual_insertion_iterations', 1)  
        t = ScfTable()
        t.columns.append('channel_number')
        t.columns.append('axial_location')
        t.columns.append('channel_area')
        t.columns.append('wetted_perimeter')
        t.columns.append('heated_perimeter')
        self.areavar.append(v)
        self.areavar.append(t)

        # gap spacing variation
        self.gapvar = ScfGroup('gap_spacing_variation')
        t = ScfTable()
        t.columns.append('gap_number')
        t.columns.append('axial_location')
        t.columns.append('gap_spacing')
        self.gapvar.append(t)

        # rod layout
        self.rodlayout = ScfGroup('rod_layout')
        s1 = ScfSwitch()
        s1.add('set_burnup_by_transient')
        s1.state = None

        s2 = ScfSwitch()
        s2.add('set_axial_conduction')
        s2.state = None

        s3 = ScfSwitch()
        s3.add('set_radial_twigl')
        s3.add('set_radial_sor')
        s3.add('set_radial_dir')
        s3.state = 2

        v1 = ScfVariable('number_of_fuel_nodes', 6)                     # radial nodes for pellets
        v2 = ScfVariable('minimum_fuel_cladding_gap_conductance', 500.)

        t1 = ScfTable()
        t1.columns.append('rod_number')
        t1.columns.append('material_type')
        t1.columns.append('outer_diamter')
        t1.columns.append('power_fraction')
        t1.columns.append('x_position')
        t1.columns.append('y_position')
        t1.rows.append([1, 1, 2*r, 1., 0., 0.])
        t1.rows.append([2, 1, 2*r, 1.,  p, 0.])

        t2 = ScfTable()
        t2.NCmax = 12
        t2.columns.append('rod')
        t2.columns.append('max_6_x_(channel+fraction)')
        t2.rows.append([1, 1, 0.25, 2, 0.25, 4, 0.25, 5, 0.25])
        t2.rows.append([2, 2, 0.25, 3, 0.25, 5, 0.25, 6, 0.25])

        t3 = ScfTable()
        t3.columns.append('material')
        t3.columns.append('property')
        t3.columns.append('fuel_conductivity')
        t3.columns.append('fuel_specific_heat')
        t3.columns.append('fuel_density')
        t3.columns.append('fuel_emissivity')
        t3.columns.append('fuel_thermal_expansion')
        t3.NCmax = 7
        t3.rows.append([1, 'uo2', 0, 0, 0, 0, 0])

        t4 = ScfTable()
        t4.columns.append('material')
        t4.columns.append('fuel_diameter')
        t4.columns.append('fuel_inner_radius')
        t4.columns.append('fraction_of_theoretical_density')
        t4.columns.append('fraction_of_puo2')
        t4.columns.append('fuel_roughness')
        t4.rows.append([1, 2*(r - ct - gt), 0., 1., 0, 3e-6])

        t5 = ScfTable()
        t5.columns.append('material')
        t5.columns.append('property')
        t5.columns.append('clad_conductivity')
        t5.columns.append('clad_specific_heat')
        t5.columns.append('clad_density')
        t5.columns.append('clad_emissivity')
        t5.columns.append('clad_thermal_expansion')
        t5.NCmax = 7
        t5.rows.append([1, 'zircaloy', 0, 0, 0, 0, 0])

        t6 = ScfTable()
        t6.columns.append('material')
        t6.columns.append('clad_thickness')
        t6.columns.append('gap_conductance')
        t6.columns.append('fill_gap')
        t6.columns.append('model_gap')
        t6.columns.append('clad_roughness')
        t6.columns.append('fill_gas_pressure')
        t6.columns.append('fill_gas_volume')
        t6.rows.append([1, ct, 0., 'off', 'on', 1e-6, 5e5, r**2*pi*0.2]) # about 20 cm plena

        t7 = ScfTable()
        t7.columns.append('configuration_type')
        t7.columns.append('number_of_zones')

        t8 = ScfTable()
        t8.columns.append('configuration_type')
        t8.columns.append('zone_number')
        t8.columns.append('zone_end_relative_axial_location')
        t8.columns.append('material')

        t9 = ScfTable()
        t9.columns.append('rod_number')
        t9.columns.append('relative_axial_location')
        t9.columns.append('burnup')
        t9.rows.append([0, 0., 0.])  # rod 0 means all rods.
        t9.rows.append([0, 1., 0.])

        t10 = ScfTable()
        t10.columns.append('rod_number')
        t10.columns.append('molar_fraction_he')
        t10.columns.append('molar_fraction_xe')
        t10.columns.append('molar_fraction_ar')
        t10.columns.append('molar_fraction_kr')
        t10.columns.append('molar_fraction_h')
        t10.columns.append('molar_fraction_n')
        
        self.rodlayout.append(s1)
        self.rodlayout.append(s2)
        self.rodlayout.append(s3)
        self.rodlayout.append(v1)
        self.rodlayout.append(v2)
        self.rodlayout.append(t1)
        self.rodlayout.append(t2)
        self.rodlayout.append(t3)
        self.rodlayout.append(t4)
        self.rodlayout.append(t5)
        self.rodlayout.append(t6)
        self.rodlayout.append(t7)
        self.rodlayout.append(t8)
        self.rodlayout.append(t9)
        self.rodlayout.append(t10)

        # calculation control
        self.calcon = ScfGroup('calculation_control')

        s1 = ScfSwitch()
        s1.add('set_sor_iteration')
        s1.add('set_gauss_elimination')
        s1.state = 1

        s2 = ScfSwitch()
        s2.add('set_full_equations')
        s2.add('set_incompressible')
        s2.add('set_thermal_transient')

        s3 = ScfSwitch()
        s3.add('set_boron_transport')
        s3.state = None

        s4 = ScfSwitch()
        s4.add('set_buoyancy')

        s5 = ScfSwitch()
        s5.add('set_critical_power_iteration')
        s5.state = None

        v1 = ScfVariable('start_time', 0.)
        v2 = ScfVariable('stop_time', 0.)
        v3 = ScfVariable('time_step', 0.)
        v4 = ScfVariable('number_of_time_steps', 0)
        v5 = ScfVariable('maximum_cladding_temperature_change', 100.)
        v6 = ScfVariable('maximum_central_fuel_temperature_change', 100.)
        v7 = ScfVariable('maximum_coolant_temperature_change', 100.)
        v8 = ScfVariable('maximum_void_change', 1.)
        v10 = ScfVariable('print_timestep_every', 0)

        v11 = ScfVariable('total_axial_length', Hz)
        v12 = ScfVariable('number_of_axial_nodes', Nz)

        v13 = ScfVariable('print_axial_level_every', 1)

        v14 = ScfVariable('sor_convergence', 1.0e-6)
        v15 = ScfVariable('axial_flow_convergence', 1.0e-4)

        v16 = ScfVariable('boundary_pressure_convergence', 1.0e-3)
        
        v17 = ScfVariable('channel_orientation', 0.0)
        
        v18 = ScfVariable('lateral_flow_damping', 0.7)
        v19 = ScfVariable('axial_flow_damping', 0.7)
        v20 = ScfVariable('pressure_damping', -1.0)
        v21 = ScfVariable('sor_acceleration', 1.0)
        
        v22 = ScfVariable('max_of_axial_flow_iterations', 100)
        v23 = ScfVariable('min_of_axial_flow_iterations', 10)
        v24 = ScfVariable('max_of_sor_iterations', 9999)
        v25 = ScfVariable('min_of_sor_iterations', 5)

        t1 = ScfTable()
        t1.columns.append('time')
        t1.columns.append('time_step_size')

        t2 = ScfTable()
        t2.columns.append('cell_number')
        t2.columns.append('cell_length')

        self.calcon.append(s1)
        self.calcon.append(s2)
        self.calcon.append(s3)
        self.calcon.append(s4)
        self.calcon.append(s5)

        for v in [v1, v2, v3, v4, v5, v6, v7, v8, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25]:
            self.calcon.append(v)

        self.calcon.append(t1)
        self.calcon.append(t2)

        # Grid spacer and wire wraps
        self.gsww = ScfGroup('grid_spacer_wire_wrap')

        s1 = ScfSwitch()
        s1.add('set_wire_wrap')
        s1.add('set_grid_spacer')
        s1.add('set_both')
        s1.state = 1 # cannot be None if there are more than 1 element in the group. Turn off the grids in the correlations by not choosing the rehme* option. 

        v1 = ScfVariable('gradual_insertion_iterations', 1)
        v2 = ScfVariable('rod_diameter', 0.0)
        v3 = ScfVariable('wire_wrap_pitch', 0.0)
        v4 = ScfVariable('wire_wrap_thickness', 0.0)

        t1 = ScfTable()
        t1.columns.append('gap_number')
        t1.columns.append('effective_length')
        t1.columns.append('relative_crossing')
        t1.columns.append('relative_crossing')

        t2 = ScfTable()
        t2.columns.append('channel_number')
        t2.columns.append('number_of_wire_wraps')

        t3 = ScfTable()
        t3.columns.append('channel_number')
        t3.columns.append('relative_axial_location')
        t3.columns.append('loss_coefficient')

        t4 = ScfTable()
        t4.columns.append('gap_number')
        t4.columns.append('relative_axial_location')
        t4.columns.append('cross_flow_fraction')

        self.gsww.append(s1)
        self.gsww.append(v1)
        self.gsww.append(v2)
        self.gsww.append(v3)
        self.gsww.append(v4)
        self.gsww.append(t1)
        self.gsww.append(t2)
        self.gsww.append(t3)
        self.gsww.append(t4)

        # lateral transport
        self.latr = ScfGroup('lateral_transport')

        s1 = ScfSwitch()
        s1.add('set_constant_mixing_coefficient')
        s1.add('set_rogers_tahir_rectangular')
        s1.add('set_rogers_tahir_triangular')
        s1.add('set_rogers_rosehart')
        s1.state = 3

        s2 = ScfSwitch()
        s2.add('set_equal_mass_exchange')
        s2.add('set_equal_volume_exchange')


        v1 = ScfVariable('constant_mixing_coefficient', 0.)
        v2 = ScfVariable('void_drift_coefficient', 1.4)
        v3 = ScfVariable('crossflow_resistance_coefficient', 0.5)
        v4 = ScfVariable('lateral_conduction_factor', 0.)

        self.latr.append(s1)
        self.latr.append(s2)
        self.latr.append(v1)
        self.latr.append(v2)
        self.latr.append(v3)
        self.latr.append(v4)

        # operating conditions
        self.opcon = ScfGroup('operating_conditions')

        s1 = ScfSwitch()
        s1.add('set_uniform_inlet_flux')
        s1.add('set_flow_split_first_axial')
        s1.add('set_flow_rate_fraction')
        s1.add('set_flux_fraction')
        s1.add('set_flow_rate')
        s1.add('set_flux')
        s1.state = 1

        s2 = ScfSwitch()
        s2.add('set_pure_flow_condition')
        s2.add('set_unified_pressure_drop')
        s2.add('set_driving_pressure_condition')

        s3 = ScfSwitch()
        s3.add('set_transient_flow_rate_factor')
        s3.add('set_transient_flow_rate')
        s3.add('set_transient_flux')

        v1 = ScfVariable('exit_pressure', 15.5e6)           # Pa
        v2 = ScfVariable('inlet_temperature', 580-273.15)   # deg C
        v3 = ScfVariable('inlet_boron_concentration', 0.0)
        v4 = ScfVariable('inlet_flow_rate', 0.361)          # kg/s
        v5 = ScfVariable('inlet_mass_flux', 0.0)
        v6 = ScfVariable('total_power', 3e4)                # J/s
        v7 = ScfVariable('average_heat_flux', 0.0)
        v8 = ScfVariable('pressure_drop', 0.0)
        v9 = ScfVariable('heat_fraction_moderator', 0.0)

        t1 = ScfTable()
        t1.columns.append('channel_number')
        t1.columns.append('inlet_temperature')

        t2 = ScfTable()
        t2.columns.append('channel_number')
        t2.columns.append('inlet_flow')

        t3 = ScfTable()
        t3.columns.append('time')
        t3.columns.append('exit_pressure')

        t4 = ScfTable()
        t4.columns.append('time')
        t4.columns.append('inlet_temperature')

        t5 = ScfTable()
        t5.columns.append('channel_number')
        t5.columns.append('time')
        t5.columns.append('inlet_temperature')

        t6 = ScfTable()
        t6.columns.append('time')
        t6.columns.append('inlet_boron_concentration')

        t7 = ScfTable()
        t7.columns.append('channel_number')
        t7.columns.append('time')
        t7.columns.append('inlet_boron_concentration')

        t8 = ScfTable()
        t8.columns.append('time')
        t8.columns.append('inlet_flow')

        t9 = ScfTable()
        t9.columns.append('channel_number')
        t9.columns.append('time')
        t9.columns.append('inlet_flow')

        t10 = ScfTable()
        t10.columns.append('time')
        t10.columns.append('heat_flux_factor')

        t11 = ScfTable()
        t11.columns.append('power_map_time')

        t12 = ScfTable()
        t12.columns.append('axial_cell_number')
        t12.columns.append('rod_number')
        t12.columns.append('power_map')
        # cosine heat flux for both pins.
        dZ = Hz / Nz
        for i_r in [1, 2]:
            for i_c in range(Nz):
                t12.rows.append([i_c+1, i_r, sin((i_c + 0.5)/Nz * pi)])

        for s in [s1, s2, s3]:
            self.opcon.append(s)

        for v in [v1, v2, v3, v4, v5, v6, v7, v8, v9]:
            self.opcon.append(v)

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]:
            self.opcon.append(t)

        # output display
        self.odisp = ScfGroup('output_display')

        v = ScfVariable('delta_time', 1e6)

        t1 = ScfTable()
        t1.columns.append('channel_number')

        t2 = ScfTable()
        t2.columns.append('rod_number')

        t3 = ScfTable()
        t3.columns.append('gap_number')

        t4 = ScfTable()
        t4.columns.append('axial_location')
        t4.columns.append('channel_or_rod_number')
        t4.columns.append('variable')

        self.odisp.append(v)
        self.odisp.append(t1)
        self.odisp.append(t2)
        self.odisp.append(t3)
        self.odisp.append(t4)


class Model(object):
    """
    SCF model

    This is rather an InputFile, since it does not provide convenient interface
    to define a calculational model.

    >>> sm = Model()
    >>> print sm

    """
    def __init__(self, version='2.3'):
        self.__version = version
        # workplace
        self.__wp = workplace.ScfWorkPlace()

        # Some parameters used in the default input file:
        # input data to compute area and perimeters:
        p = 1.26      *1e-2  # [m], pin pitch
        r = 0.9166/2. *1e-2  # [m], pin outer radius
        # data for the default rod geometry:
        gt = 0.03 *1e-2 # [m], gap thickness
        ct = 0.05 *1e-2 # [m], clad thickness
        # axial mesh for calculation
        Nz = 10    # number of axial nodes
        Hz = 3.6576 # [m], rod height


        # Initialisation        
        self.__init = ScfGroup('initialisation')
        self.__init.append(ScfVariable('title', "'Title of the problem'"))

        # Properties
        self.__prop = ScfGroup('properties')
        s = ScfSwitch()
        s.cn = 'set_'
        s.add('water')
        s.add('lead_bismuth')
        s.add('lead')
        s.add('sodium')
        s.add('helium')
        s.add('air')
        self.__prop.append(s)

        # Correlations
        self.__corr = ScfGroup('correlations')
        s = ScfSwitch()
        s.cn = 'set_subcooled_void_'
        s.add('levy')
        s.add('saha_zuber')
        s.add('unal')
        s.add('bowring')
        s.add('none')
        s.state = 3
        self.__corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_boiling_void_'
        s.add('homogeneous')
        s.add('armand_mod')
        s.add('smith')
        s.add('chexal_lellouche')
        s.state = 1
        self.__corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_two_phase_friction_'
        s.add('homogeneous')
        s.add('armand')
        s.add('lockhart')
        s.state = 1
        self.__corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_turbulent_friction_'
        s.add('blasius')
        s.add('rehme_wire')
        s.add('rehme_grid')
        s.add('churchill')
        s.state = 0
        self.__corr.append(s)

        s = ScfSwitch()
        s.cn = 'set_heat_transfer_'
        s.add('dittus_boelter')
        s.add('gnielinski')
        s.add('subbotin')
        s.state = 0
        self.__corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_chf_'
        s.add('barnett+b&w')
        s.add('biasi')
        s.add('okb')
        s.add('w3')
        s.add('levitan')
        s.add('epri')
        s.state = 0
        self.__corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_shape_chf_'
        s.add('none')
        s.add('cobra4i')
        s.add('tong')
        s.add('w3')
        s.add('smolin')
        s.state = 0
        self.__corr.append(s)
        
        s = ScfSwitch()
        s.cn = 'set_'
        s.add('simple_fuel_cladding_gap')
        s.add('transuranus_urgap_fuel_cladding_gap')
        s.add('vver1000_benchmark_fuel_cladding_gap')
        s.state = 0
        self.__corr.append(s)

        self.__corr.append(ScfVariable('blasius_laminar_prefactor', 64.0))
        self.__corr.append(ScfVariable('blasius_laminar_reynolds_exponent', -1.0))
        self.__corr.append(ScfVariable('blasius_laminar_constant', 0.0))
        self.__corr.append(ScfVariable('blasius_turbulent_prefactor', 0.316))
        self.__corr.append(ScfVariable('blasius_turbulent_reynolds_exponent', -0.25))
        self.__corr.append(ScfVariable('blasius_turbulent_constant', 0.0))
        self.__corr.append(ScfVariable('roughness', 3e-6))
        self.__corr.append(ScfVariable('dittus_boelter_prefactor', 0.023))
        self.__corr.append(ScfVariable('dittus_boelter_reynolds_exponent', 0.8))
        self.__corr.append(ScfVariable('dittus_boelter_prandtl_exponent', 0.4))
        self.__corr.append(ScfVariable('dittus_boelter_constant', 0.0))
        if version == '2.5':
            self.__corr.append(ScfVariable('effective_emissivity', 0.0))

        self.__corr.append(ScfVariable('chf_multiplier', 1.0e10))

        # special parameters
        self.__specpar = ScfGroup('special_parameters')
        self.__specpar.append(ScfVariable('rod_pitch', 0.))
        self.__specpar.append(ScfVariable('rod_diameter', 8.5e-3))
        self.__specpar.append(ScfVariable('wire_wrap_pitch', 0.))
        self.__specpar.append(ScfVariable('wire_wrap_diameter', 0.))
        self.__specpar.append(ScfVariable('perimeter_ratio', 0.))

        # axial heat flux
        self.__heat = ScfGroup('axial_heat_flux')
        t = ScfTable(['relative_axial_location', 'relative_heat_flux'])
        t.rows.append([0., 1.])
        t.rows.append([1., 1.])
        self.__heat.append(t)

        # channel layout. By default, two rods with axially-independent
        # properties are modelled.
        # 
        #  __________________
        # | 1 |    2    | 3  |
        # |   _         _    |
        # |_ /1\ _ _ _ /2\ _ |
        # |  \_/       \_/   |
        # | 4 |    5    |  6 |
        # |__________________|
                                    
        
        self.__layout = ScfGroup('channel_layout')
        t1 = ScfTable()
        t1.columns.append('channel_number')
        t1.columns.append('channel_area')
        t1.columns.append('wetted_perimeter')
        t1.columns.append('heated_perimeter')
        t1.columns.append('x_position')
        t1.columns.append('y_position')

        pa = pi*r**2   # pin area
        a1 = (p/2.)**2 - pa/4.  # area 1
        a2 = (p**2)/2. - pa/2.  # area 2
        hp1 = pi*r/2.
        hp2 = pi*r
        wp1 = p + hp1
        wp2 = p + hp2
        t1.rows.append([1, a1, wp1, hp1,   -p/4.,  p/4.])  # coordinates assume that pin 1 at the origin.
        t1.rows.append([2, a2, wp2, hp2,    p/2.,  p/4.])
        t1.rows.append([3, a1, wp1, hp1,  p*1.25,  p/4.])
        t1.rows.append([4, a1, wp1, hp1,   -p/4., -p/4.])  # coordinates assume that pin 1 at the origin.
        t1.rows.append([5, a2, wp2, hp2,    p/2., -p/4.])
        t1.rows.append([6, a1, wp1, hp1,  p*1.25, -p/4.])

        t2 = ScfTable()
        t2.columns.append('channel')
        t2.columns.append('max_40_x_(neighbour+gap+distance)')
        t2.NCmax = 19
        g1 = p/2. - r
        g2 = p - 2*r
        d1 = 3./4.*p
        d2 = p/2.
        t2.rows.append([1, 2, g1, d1, 4, g1, d2])
        t2.rows.append([2, 3, g1, d1, 5, g2, d2])
        t2.rows.append([3, 6, g1, d2])
        t2.rows.append([4, 5, g1, d1])
        t2.rows.append([5, 6, g1, d1])
        t2.rows.append([6, 0, 0., 0.]) # FIXME is it needed inSCF?

        self.__layout.append(t1)
        self.__layout.append(t2)

        # thermal connection
        self.__thcon = ScfGroup('thermal_connection')
        t = ScfTable()
        t.columns.append('connection_number')
        t.columns.append('rho_cp_thickness')
        t.columns.append('wall_width')
        t.columns.append('first_channel')
        t.columns.append('resistance')
        t.columns.append('second_channel')
        t.columns.append('resistance')
        self.__thcon.append(t)

        # channel area variation
        self.__areavar = ScfGroup('channel_area_variation')
        v = ScfVariable('gradual_insertion_iterations', 1)  
        t = ScfTable()
        t.columns.append('channel_number')
        t.columns.append('axial_location')
        t.columns.append('channel_area')
        t.columns.append('wetted_perimeter')
        t.columns.append('heated_perimeter')
        self.__areavar.append(v)
        self.__areavar.append(t)

        # gap spacing variation
        self.__gapvar = ScfGroup('gap_spacing_variation')
        t = ScfTable()
        t.columns.append('gap_number')
        t.columns.append('axial_location')
        t.columns.append('gap_spacing')
        self.__gapvar.append(t)

        # rod layout
        self.__rodlayout = ScfGroup('rod_layout')
        s1 = ScfSwitch()
        s1.add('set_burnup_by_transient')
        s1.state = None

        s2 = ScfSwitch()
        s2.add('set_axial_conduction')
        s2.state = None

        s3 = ScfSwitch()
        s3.add('set_radial_twigl')
        s3.add('set_radial_sor')
        s3.add('set_radial_dir')
        s3.state = 2

        v1 = ScfVariable('number_of_fuel_nodes', 6)                     # radial nodes for pellets
        v2 = ScfVariable('minimum_fuel_cladding_gap_conductance', 500.)

        t1 = ScfTable()
        t1.columns.append('rod_number')
        t1.columns.append('material_type')
        if version == '2.5':
            t1.columns.append('outer_diameter')
        else:
            t1.columns.append('outer_diamter')
        t1.columns.append('power_fraction')
        t1.columns.append('x_position')
        t1.columns.append('y_position')
        t1.rows.append([1, 1, 2*r, 1., 0., 0.])
        t1.rows.append([2, 1, 2*r, 1.,  p, 0.])

        t2 = ScfTable()
        t2.NCmax = 12
        t2.columns.append('rod')
        t2.columns.append('max_6_x_(channel+fraction)')
        t2.rows.append([1, 1, 0.25, 2, 0.25, 4, 0.25, 5, 0.25])
        t2.rows.append([2, 2, 0.25, 3, 0.25, 5, 0.25, 6, 0.25])

        t3 = ScfTable()
        t3.columns.append('material')
        t3.columns.append('property')
        t3.columns.append('fuel_conductivity')
        t3.columns.append('fuel_specific_heat')
        t3.columns.append('fuel_density')
        t3.columns.append('fuel_emissivity')
        t3.columns.append('fuel_thermal_expansion')
        t3.NCmax = 7
        t3.rows.append([1, 'uo2', 0, 0, 0, 0, 0])

        t4 = ScfTable()
        t4.columns.append('material')
        t4.columns.append('fuel_diameter')
        t4.columns.append('fuel_inner_radius')
        t4.columns.append('fraction_of_theoretical_density')
        t4.columns.append('fraction_of_puo2')
        t4.columns.append('fuel_roughness')
        t4.rows.append([1, 2*(r - ct - gt), 0., 1., 0, 3e-6])

        t5 = ScfTable()
        t5.columns.append('material')
        t5.columns.append('property')
        t5.columns.append('clad_conductivity')
        t5.columns.append('clad_specific_heat')
        t5.columns.append('clad_density')
        t5.columns.append('clad_emissivity')
        t5.columns.append('clad_thermal_expansion')
        t5.NCmax = 7
        t5.rows.append([1, 'zircaloy', 0, 0, 0, 0, 0])

        t6 = ScfTable()
        t6.columns.append('material')
        t6.columns.append('clad_thickness')
        t6.columns.append('gap_conductance')
        t6.columns.append('fill_gap')
        t6.columns.append('model_gap')
        t6.columns.append('clad_roughness')
        t6.columns.append('fill_gas_pressure')
        t6.columns.append('fill_gas_volume')
        t6.rows.append([1, ct, 0., 'off', 'on', 1e-6, 5e5, r**2*pi*0.2]) # about 20 cm plena

        t7 = ScfTable()
        t7.columns.append('configuration_type')
        t7.columns.append('number_of_zones')

        t8 = ScfTable()
        t8.columns.append('configuration_type')
        t8.columns.append('zone_number')
        t8.columns.append('zone_end_relative_axial_location')
        t8.columns.append('material')

        t9 = ScfTable()
        t9.columns.append('rod_number')
        t9.columns.append('relative_axial_location')
        t9.columns.append('burnup')
        t9.rows.append([0, 0., 0.])  # rod 0 means all rods.
        t9.rows.append([0, 1., 0.])

        t10 = ScfTable()
        t10.columns.append('rod_number')
        t10.columns.append('molar_fraction_he')
        t10.columns.append('molar_fraction_xe')
        t10.columns.append('molar_fraction_ar')
        t10.columns.append('molar_fraction_kr')
        t10.columns.append('molar_fraction_h')
        t10.columns.append('molar_fraction_n')
        
        self.__rodlayout.append(s1)
        self.__rodlayout.append(s2)
        self.__rodlayout.append(s3)
        self.__rodlayout.append(v1)
        self.__rodlayout.append(v2)
        self.__rodlayout.append(t1)
        self.__rodlayout.append(t2)
        self.__rodlayout.append(t3)
        self.__rodlayout.append(t4)
        self.__rodlayout.append(t5)
        self.__rodlayout.append(t6)
        self.__rodlayout.append(t7)
        self.__rodlayout.append(t8)
        self.__rodlayout.append(t9)
        self.__rodlayout.append(t10)

        # calculation control
        self.__calcon = ScfGroup('calculation_control')

        s1 = ScfSwitch()
        s1.add('set_sor_iteration')
        s1.add('set_gauss_elimination')
        if version == '2.5':
            s1.add('set_bicgstab_iteration')
            s1.state = 2

        s2 = ScfSwitch()
        s2.add('set_full_equations')
        s2.add('set_incompressible')
        s2.add('set_thermal_transient')
        if version == '2.5':
            s2.active = False

        s3 = ScfSwitch()
        s3.add('set_boron_transport')
        s3.state = None

        s4 = ScfSwitch()
        s4.add('set_buoyancy')

        s5 = ScfSwitch()
        s5.add('set_critical_power_iteration')
        s5.state = None

        v1 = ScfVariable('start_time', 0.)
        v2 = ScfVariable('stop_time', 0.)
        v3 = ScfVariable('time_step', 0.)
        v4 = ScfVariable('number_of_time_steps', 0)
        v5 = ScfVariable('maximum_cladding_temperature_change', 100.)
        v6 = ScfVariable('maximum_central_fuel_temperature_change', 100.)
        v7 = ScfVariable('maximum_coolant_temperature_change', 100.)
        v8 = ScfVariable('maximum_void_change', 1.)
        v10 = ScfVariable('print_timestep_every', 0)

        v11 = ScfVariable('total_axial_length', Hz)
        v12 = ScfVariable('number_of_axial_nodes', Nz)

        v13 = ScfVariable('print_axial_level_every', 1)

        v14 = ScfVariable('sor_convergence', 1.0e-6)
        if version == '2.5':
            v14.active = False

        v15 = ScfVariable('axial_flow_convergence', 1.0e-4)

        v16 = ScfVariable('boundary_pressure_convergence', 1.0e-3)
        
        v17 = ScfVariable('channel_orientation', 0.0)
        
        v18 = ScfVariable('lateral_flow_damping', 0.7)
        v19 = ScfVariable('axial_flow_damping', 0.7)
        v20 = ScfVariable('pressure_damping', -1.0)
        if version == '2.5':
            v20.active = False
        v21 = ScfVariable('sor_acceleration', 1.0)
        
        v22 = ScfVariable('max_of_axial_flow_iterations', 100)
        v23 = ScfVariable('min_of_axial_flow_iterations', 10)
        v24 = ScfVariable('max_of_sor_iterations', 9999)
        v25 = ScfVariable('min_of_sor_iterations', 5)
        if version == '2.5':
            v24.active = False
            v25.active = False

        t1 = ScfTable()
        t1.columns.append('time')
        t1.columns.append('time_step_size')

        t2 = ScfTable()
        t2.columns.append('cell_number')
        t2.columns.append('cell_length')

        self.__calcon.append(s1)
        self.__calcon.append(s2)
        self.__calcon.append(s3)
        self.__calcon.append(s4)
        self.__calcon.append(s5)

        for v in [v1, v2, v3, v4, v5, v6, v7, v8, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25]:
            self.__calcon.append(v)

        self.__calcon.append(t1)
        self.__calcon.append(t2)

        # Grid spacer and wire wraps
        self.__gsww = ScfGroup('grid_spacer_wire_wrap')

        s1 = ScfSwitch()
        s1.add('set_wire_wrap')
        s1.add('set_grid_spacer')
        s1.add('set_both')
        s1.state = 1 # cannot be None if there are more than 1 element in the group. Turn off the grids in the correlations by not choosing the rehme* option. 

        v1 = ScfVariable('gradual_insertion_iterations', 1)
        v2 = ScfVariable('rod_diameter', 0.0)
        v3 = ScfVariable('wire_wrap_pitch', 0.0)
        v4 = ScfVariable('wire_wrap_thickness', 0.0)

        t1 = ScfTable()
        t1.columns.append('gap_number')
        t1.columns.append('effective_length')
        t1.columns.append('relative_crossing')
        t1.columns.append('relative_crossing')

        t2 = ScfTable()
        t2.columns.append('channel_number')
        t2.columns.append('number_of_wire_wraps')

        t3 = ScfTable()
        t3.columns.append('channel_number')
        t3.columns.append('relative_axial_location')
        t3.columns.append('loss_coefficient')

        t4 = ScfTable()
        t4.columns.append('gap_number')
        t4.columns.append('relative_axial_location')
        t4.columns.append('cross_flow_fraction')

        self.__gsww.append(s1)
        self.__gsww.append(v1)
        self.__gsww.append(v2)
        self.__gsww.append(v3)
        self.__gsww.append(v4)
        self.__gsww.append(t1)
        self.__gsww.append(t2)
        self.__gsww.append(t3)
        self.__gsww.append(t4)

        # lateral transport
        self.__latr = ScfGroup('lateral_transport')

        s1 = ScfSwitch()
        s1.add('set_constant_mixing_coefficient')
        s1.add('set_rogers_tahir_rectangular')
        s1.add('set_rogers_tahir_triangular')
        s1.add('set_rogers_rosehart')
        s1.state = 3

        s2 = ScfSwitch()
        s2.add('set_equal_mass_exchange')
        s2.add('set_equal_volume_exchange')


        v1 = ScfVariable('constant_mixing_coefficient', 0.)
        v2 = ScfVariable('void_drift_coefficient', 1.4)
        v3 = ScfVariable('crossflow_resistance_coefficient', 0.5)
        v4 = ScfVariable('lateral_conduction_factor', 0.)

        self.__latr.append(s1)
        self.__latr.append(s2)
        self.__latr.append(v1)
        self.__latr.append(v2)
        self.__latr.append(v3)
        self.__latr.append(v4)

        # operating conditions
        self.__opcon = ScfGroup('operating_conditions')

        s1 = ScfSwitch()
        s1.add('set_uniform_inlet_flux')
        s1.add('set_flow_split_first_axial')
        s1.add('set_flow_rate_fraction')
        s1.add('set_flux_fraction')
        s1.add('set_flow_rate')
        s1.add('set_flux')
        s1.state = 1

        s2 = ScfSwitch()
        s2.add('set_pure_flow_condition')
        s2.add('set_unified_pressure_drop')
        s2.add('set_driving_pressure_condition')

        s3 = ScfSwitch()
        s3.add('set_transient_flow_rate_factor')
        s3.add('set_transient_flow_rate')
        s3.add('set_transient_flux')

        v1 = ScfVariable('exit_pressure', 15.5e6)           # Pa
        v2 = ScfVariable('inlet_temperature', 580-273.15)   # deg C
        v3 = ScfVariable('inlet_boron_concentration', 0.0)
        v4 = ScfVariable('inlet_flow_rate', 0.361)          # kg/s
        v5 = ScfVariable('inlet_mass_flux', 0.0)
        v6 = ScfVariable('total_power', 3e4)                # J/s
        v7 = ScfVariable('average_heat_flux', 0.0)
        v8 = ScfVariable('pressure_drop', 0.0)
        v9 = ScfVariable('heat_fraction_moderator', 0.0)

        t1 = ScfTable()
        t1.columns.append('channel_number')
        t1.columns.append('inlet_temperature')

        t2 = ScfTable()
        t2.columns.append('channel_number')
        t2.columns.append('inlet_flow')

        t3 = ScfTable()
        t3.columns.append('time')
        t3.columns.append('exit_pressure')

        t4 = ScfTable()
        t4.columns.append('time')
        t4.columns.append('inlet_temperature')

        t5 = ScfTable()
        t5.columns.append('channel_number')
        t5.columns.append('time')
        t5.columns.append('inlet_temperature')

        t6 = ScfTable()
        t6.columns.append('time')
        t6.columns.append('inlet_boron_concentration')

        t7 = ScfTable()
        t7.columns.append('channel_number')
        t7.columns.append('time')
        t7.columns.append('inlet_boron_concentration')

        t8 = ScfTable()
        t8.columns.append('time')
        t8.columns.append('inlet_flow')

        t9 = ScfTable()
        t9.columns.append('channel_number')
        t9.columns.append('time')
        t9.columns.append('inlet_flow')

        t10 = ScfTable()
        t10.columns.append('time')
        t10.columns.append('heat_flux_factor')

        t11 = ScfTable()
        t11.columns.append('power_map_time')

        t12 = ScfTable()
        t12.columns.append('axial_cell_number')
        t12.columns.append('rod_number')
        t12.columns.append('power_map')
        # cosine heat flux for both pins.
        dZ = Hz / Nz
        for i_r in [1, 2]:
            for i_c in range(Nz):
                t12.rows.append([i_c+1, i_r, sin((i_c + 0.5)/Nz * pi)])

        for s in [s1, s2, s3]:
            self.__opcon.append(s)

        for v in [v1, v2, v3, v4, v5, v6, v7, v8, v9]:
            self.__opcon.append(v)

        for t in [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]:
            self.__opcon.append(t)

        if version == '2.5':
            self.__pointk = ScfGroup('pointkinetics')
            v1 = ScfVariable('set_pointkinetics_power', 'off')
            v2 = ScfVariable('pointkinetics_max_time_step', 1e-5)
            v3 = ScfVariable('prompt_neutron_lifetime', 2.0e-5)
            v4 = ScfVariable('power_weighting_exponent', 2.0)
            v5 = ScfVariable('fraction_delayed_neutrons_group_1', 0.000266)
            v6 = ScfVariable('fraction_delayed_neutrons_group_2', 0.001491)
            v7 = ScfVariable('fraction_delayed_neutrons_group_3', 0.001316)
            v8 = ScfVariable('fraction_delayed_neutrons_group_4', 0.002849)
            v9 = ScfVariable('fraction_delayed_neutrons_group_5', 0.000896)
            v10= ScfVariable('fraction_delayed_neutrons_group_6', 0.000182)
            v11 = ScfVariable('decay_constant_group_1', 0.0127)
            v12 = ScfVariable('decay_constant_group_2', 0.0317)
            v13 = ScfVariable('decay_constant_group_3', 0.1150)
            v14 = ScfVariable('decay_constant_group_4', 0.3110)
            v15 = ScfVariable('decay_constant_group_5', 1.4000)
            v16 = ScfVariable('decay_constant_group_6', 3.8700)

            v17 = ScfVariable('doppler_coefficient', -2.8e-5)
            v18 = ScfVariable('coolant_temperature_coefficient', -9.85e-5)
            v19 = ScfVariable('void_coefficient', -0.12345)
            v20 = ScfVariable('boron_coefficient', -0.2e-5)

            self.__pointk.append(v1)
            self.__pointk.append(v2)
            self.__pointk.append(v3)
            self.__pointk.append(v4)
            self.__pointk.append(v5)
            self.__pointk.append(v6)
            self.__pointk.append(v7)
            self.__pointk.append(v8)
            self.__pointk.append(v9)
            self.__pointk.append(v10)
            self.__pointk.append(v11)
            self.__pointk.append(v12)
            self.__pointk.append(v13)
            self.__pointk.append(v14)
            self.__pointk.append(v15)
            self.__pointk.append(v16)
            self.__pointk.append(v17)
            self.__pointk.append(v18)
            self.__pointk.append(v19)
            self.__pointk.append(v20)

        # output display
        self.__odisp = ScfGroup('output_display')

        v = ScfVariable('delta_time', 1e6)

        t1 = ScfTable()
        t1.columns.append('channel_number')

        t2 = ScfTable()
        t2.columns.append('rod_number')

        t3 = ScfTable()
        t3.columns.append('gap_number')

        t4 = ScfTable()
        t4.columns.append('axial_location')
        t4.columns.append('channel_or_rod_number')
        t4.columns.append('variable')

        self.__odisp.append(v)
        self.__odisp.append(t1)
        self.__odisp.append(t2)
        self.__odisp.append(t3)
        self.__odisp.append(t4)

    @property
    def total_power(self):
        """
        Total power, J/s. 
        
        Goes to the operating_conditions block
        """
        return self.__opcon.get_variable('total_power').value

    @total_power.setter
    def total_power(self, value):
        self.__opcon.get_variable('total_power').value = value
        return

    @property
    def inlet_temperature(self):
        """
        Inlet temperature, K. 
        
        Currently, does not support time dependence.
        """
        # convert Celsius to Kelvin for user
        return self.__opcon.get_variable('inlet_temperature').value + 273.15

    @inlet_temperature.setter
    def inlet_temperature(self, value):
        # convert Kelvin to Celsius for SCF
        self.__opcon.get_variable('inlet_temperature').value = value - 273.15
        return

    @property
    def exit_pressure(self):
        """
        Exit pressure, Pa.
        """
        return self.__opcon.get_variable('exit_pressure').value

    @exit_pressure.setter
    def exit_pressure(self, value):
        self.__opcon.get_variable('exit_pressure').value = value
        return

    @property
    def pressure_drop(self):
        """
        Pressure drop (exit pressure - inlet pressure), Pa.
        """
        return self.__opcon.get_variable('pressure_drop').value

    @pressure_drop.setter
    def pressure_drop(self, value):
        self.__opcon.get_variable('pressure_drop').value = value
        self.__opcon.get_switch('set_driving_pressure_condition').state = 'set_driving_pressure_condition'
        return

    @property
    def inlet_flow_rate(self):
        """
        Mass flow rate, g/s.
        """
        # convert kg/s to g/s for user
        return self.__opcon.get_variable('inlet_flow_rate').value * 1e3

    @inlet_flow_rate.setter
    def inlet_flow_rate(self, value):
        # convert g/s to kg/s for SCF
        self.__opcon.get_variable('inlet_flow_rate').value = value / 1e3
        self.__opcon.get_variable('inlet_mass_flux').value = 0.0 # mutually exclusive
        self.__opcon.get_switch('set_driving_pressure_condition').state = 'set_pure_flow_condition'
        return

    @property
    def inlet_mass_flux(self):
        """
        Mass flux, g/(cm^2 s).
        """
        # convert kg/(m^2 s) to g/(cm^2 s) for user
        return self.__opcon.get_variable('inlet_mass_flux').value / 1e1

    @inlet_mass_flux.setter
    def inlet_mass_flux(self, value):
        # convert g/(cm^2 s) to kg/(m^2 s) for SCF
        self.__opcon.get_variable('inlet_mass_flux').value = value * 1e1
        self.__opcon.get_variable('inlet_flow_rate').value = 0.0 # mutually exclusive
        self.__opcon.get_switch('set_driving_pressure_condition').state = 'set_pure_flow_condition'

    def clear(self):
        """
        """
        return NotImplemented

    @property
    def wp(self):
        """
        Instance of the ScfWorkPlace() class. 
        
        Prepares working directory for SCF and starts the code.
        """
        return self.__wp

    @property
    def init(self):
        """
        The 'initialization' group.
        """
        return self.__init

    @property
    def prop(self):
        """
        The 'properties' group.
        """
        return self.__prop

    @property
    def corr(self):
        """
        The 'correlations' group.
        """
        return self.__corr

    @property
    def specpar(self):
        """
        The 'special_parameters' group.
        """
        return self.__specpar

    @property
    def heat(self):
        """
        The 'axial_heat_flux' group.
        """
        return self.__heat

    @property
    def layout(self):
        """
        The 'channel_layout' group.
        """
        return self.__layout

    @property
    def thcon(self):
        """
        The 'thermal_connection' group.
        """
        return self.__thcon

    @property
    def areavar(self):
        """
        The 'channel_area_variation' group.
        """
        return self.__areavar

    @property
    def gapvar(self):
        """
        The 'gap_spacing_variation' group.
        """
        return self.__gapvar

    @property
    def rodlayout(self):
        """
        The 'rod_layout' group.
        """
        return self.__rodlayout

    @property
    def calcon(self):
        """
        The 'calculation_control' group.
        """
        return self.__calcon

    @property
    def gsww(self):
        """
        The 'grid_spacer_wire_wrap' group.
        """
        return self.__gsww

    @property
    def latr(self):
        """
        The 'lateral_transport' group.
        """
        return self.__latr

    @property
    def opcon(self):
        """
        The 'operating_conditions' group.
        """
        return self.__opcon

    @property
    def pointk(self):
        """
        The 'pointkinetics' group
        """
        if self.__version == '2.5':
            return self.__pointk
        else:
            raise TypeError

    @property
    def odisp(self):
        """
        The 'output_display' group.
        """
        return self.__odisp


    # FIXME provide safe method to copy workplace
    @wp.setter
    def wp(self, value):
        self.__wp = value

    def run(self, mode='r', **kwargs):
        """
        Prepares content of the input file and starts SCF job.
        """
        t1 = time.time()
        self.__wp.input.string = str(self)
        t2 = time.time()
        self.process_model_time = t2 -t1
        self.wp.run(mode, **kwargs)
        self.run_time = time.time() - t2

    @property
    def version(self):
        return self.__version

    def __str__(self):
        res = []

        res.append(str(self.__init))
        res.append(str(self.__prop))
        res.append(str(self.__corr))
        res.append(str(self.__specpar))
        res.append(str(self.__heat))
        res.append(str(self.__layout))
        res.append(str(self.__thcon))
        res.append(str(self.__areavar))
        res.append(str(self.__gapvar))
        res.append(str(self.__rodlayout))
        res.append(str(self.__calcon))
        res.append(str(self.__gsww))
        res.append(str(self.__latr))
        res.append(str(self.__opcon))
        if self.__version == '2.5':
            res.append(str(self.__pointk))
        res.append(str(self.__odisp))

        res.append('end')

        return '\n\n'.join(res)




if __name__ == '__main__':
    import doctest
    doctest.testmod()

    m = Model()
    m.run('R')

