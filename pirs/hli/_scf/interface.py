"""
SCF interface
"""

from ...solids import Box

from . import tables
from . import convertors
from . import standard_model

from ... import scf

import os
from math import pi
import time

#     Terminology used below:
#         
#         pin: 
#             clad
#             gap
#             pellets (fuel)
#             gas plena
#             plugs
# 
#         rod: common term for pin and pin with zero power
# 
#         channel:
#             all coolant region between rods, note that this differs from the
#             SCF term 'channel', where it means one particular part of the
#             coolant area between rods and bundle boundary.
# 
#         bundle:
#             rods,


class ScfInterface(scf.model.Model):
    """
    To define the SCF's geometry, one needs to specify bundle boundaries and rods.

    The bundle boundary is a general model element (GME) containing coolant
    (see definition below) and rods. Rods can be inserted into the bundle
    boundary GME, or into the coolant GME.

    Each rod must be GME of the Cylinder class. If it has children, they must
    be cylinders coaxial with the rod's cylinder.  If a rod (or its child) has
    nonzero heat attribute it is considered as a pin. 

    If a rod itself has a non-zero heat attribute, it is considered as a pin with 
    zero clad and gap thickness (will SCF fail in this case?).

    If a rod's child has a non-zero heat attribute, this child considered as pellets.

    """
    def __init__(self, gm=None, version='2.3', **kwargs):
        self.__gm = None # link to the general model
        self.__pm = None # process model with extra solids for channels
        super(ScfInterface, self).__init__( version=version, **kwargs )

        self.keys = { 'coolant': '', 'rods': [], 'water-boxes': [] }
        self.materials = { 'zirc': 'zircaloy', 'uo2': 'uo2' }
        self.wrapped = False

        if gm is not None:
            self.gm = gm
        return

    @property
    def gm(self):
        """
        Link to the general model. 
        """
        return self.__gm

    @gm.setter
    def gm(self, value):
        self.__gm = value

    @property
    def keys(self):
        """
        Compound keys for accessing coolant and rods in the general model.

        They are represented as a map with the following associations:

        coolant:     a compound key by which to access the coolant (must be a Box)
        rods:        a list of compound keys by which to access the individual rods
                     (must be Cylinders)
        water-boxes: a list of compound keys by which to access water boxes (must be
                     Boxes)

        By default, coolant is an empty string, which means that the model's root
        will be used as a coolant.

        """
        return self.__keys

    @keys.setter
    def keys(self, value):
        self.__keys = value

    @property
    def materials(self):
        """
        Dictionary to define the actual meaning of the  material names used in
        the general model.  Keys are strings with material names from the
        general model, values are strings describing valid SCF input materials.

        """
        return self.__mdict

    @materials.setter
    def materials(self, v):
        self.__mdict = v

    @property
    def wrapped(self):
        """
        Set this to True if the coolant box is surrounded by a wrapper material
        and the wetted area of channels near the border of the grid needs to be
        increased accordingly.

        """
        return self.__wrapped

    @wrapped.setter
    def wrapped(self, v):
        self.__wrapped = v

    def __str__(self):
        self._process_model()
        return super(ScfInterface, self).__str__()

    def _process_model(self, log=True):
        """
        This processes a general model that can be converted to a SCF standard
        model with the following properties:

        For rods:
        - must have the same radius
        - must be arranged in a rectangular grid without gaps (missing rods)
        - must have equal fuel length & axial layering
        - must be accessible as children of the general model using the
          compound keys given in self.keys['rods']
        
        For coolant:
        - the axial area that is shared with the rods must have the same axial
          layering
        - axial height above or below the endpoints of fuel elements will not
          be modeled by SCF

        The standard model will contain additional Box elements representing
        coolant channels. These will cover the coolant box completely and
        share the same axial layering. Each rod will be adjacent to four such
        channels. They can be accessed using compound keys of the form
        'scf_c{}' with {} being an index from 0 to n-1.

        Each rod must have the following structure

            - self.keys['rods'][i] ~= cladding (cylinder)
                - 'gap' (cylinder)
                    - 'fuel' ~= fuel pellets (cylinder)

        """
        if log:
            t1 = time.time()
            TFORMAT = '_process_model(): {} {}'

        # in SCF interface use "standard model" that contains only SCF-relevant parts:
        # future conversion of GM to SM (standardized):
        sm, skeys = standard_model.scf_standard_model(self.__gm, self.keys)
        # save standard model and keys for read_output
        self.__sm = sm
        self.__skeys = skeys

        if log:
            t2 = time.time()
            print TFORMAT.format('standard_model called', t2-t1)
            t1 = t2

        tab = tables.calculate_tables(sm, skeys['coolant'], skeys['rods'], skeys['fuels'],
                self.materials, self.wrapped)
        if log:
            t2 = time.time()
            print TFORMAT.format('call tables.calculate_tables()', t2-t1)
            t1 = t2

        # common z mesh for SCF model taken from first fuel:
        first_fuel = sm.get_child(skeys['fuels'][0])
        zgrid = first_fuel.temp.get_grid()
        zlen = float(first_fuel.Z) / 100.0
        self.__rod_mapping = tab['rod-mapping']

        # create new channel boxes:
        nr = len(sm.children) # number of children berofe inserting channel boxes
        nc = 0 # counter for channel boxes
        for (crow,box) in zip(tab['channel-positions'], tab['channel-boxes']):
            box.X = 100*box.X
            box.Y = 100*box.Y
            box.Z = sm.Z
            box.material = sm.material
            i = crow[0] - 1
            box.pos.x = 100*crow[4]
            box.pos.y = 100*crow[5]

            sm.insert("scf_c{0}".format(i), box)
            #print 'scf_c{0}: pos={1} abspos={2}, dimensions: {3} {4} {5}'.format(i, box.pos, box.abspos(), box.X, box.Y, box.Z)
            nc += 1
            # sm.shift_child("scf_c{0}".format(i), 0)

        # shift channel boxes before rods:
        sm.shift_children(nr, nc, 0)

        #print 'new order in sm:'
        #for c in sm.children:
        #    print c.local_key
        #print '-'*10

        # hack: specify that sm lattice elements are completely filled
        sm.scf_interface_lattice_filled = True
        sm._no_interior = True

        if log:
            t2 = time.time()
            print TFORMAT.format('new channel boxes created', t2-t1)
            t1 = t2



        # -------------- title -----------------------------------------------------
        self.init.clear()
        self.init.get_variable('title').value = 'created by pirs.hpmc.ScfInterface()'

        # -------------- channel layout --------------------------------------------
        # channel areas and perimeters
        ch_layout = self.layout.get_table('channel_number', 'channel_area',
                'wetted_perimeter', 'heated_perimeter', 'x_position', 'y_position')
        ch_layout.clear()
        ch_layout.rows.extend(tab['channel-positions'])

        # table 2 (channel neighbors)
        ch_neighbours = self.layout.get_table('channel',
                'max_40_x_(neighbour+gap+distance)')
        ch_neighbours.clear()
        ch_neighbours.rows.extend(tab['channel-neighbours'])

        # ------------ axial heat dist ------------------------------------------------
        # axial heat flux table, global, not needed
        heatflux = self.heat.get_table('relative_axial_location', 'relative_heat_flux')
        heatflux.clear()
        heatflux.rows.append([0, 0])
        heatflux.rows.append([1, 0])

        # -------------- rod layout ------------------------------------------------
        # table 3 (rod layout)
        if self.version == '2.5':
            row_name = 'outer_diameter'
        else:
            row_name = 'outer_diamter'

        rod_layout = self.rodlayout.get_table('rod_number', 'material_type',
                row_name, 'power_fraction', 'x_position', 'y_position')
        rod_layout.clear()
        rod_layout.rows.extend(tab['rod-positions'])

        # neighbouring channels
        rod_neighbour = self.rodlayout.get_table('rod', 'max_6_x_(channel+fraction)')
        rod_neighbour.clear()
        rod_neighbour.rows.extend(tab['rod-neighbours'])

        # material properties
        rod_mats = self.rodlayout.get_table('material', 'property', 'fuel_conductivity',
                'fuel_specific_heat', 'fuel_density', 'fuel_emissivity',
                'fuel_thermal_expansion')
        rod_mats.clear()
        rod_mats.rows.extend(tab['fuel-materials-1'])

        rod_props = self.rodlayout.get_table('material', 'fuel_diameter',
                'fuel_inner_radius', 'fraction_of_theoretical_density',
                'fraction_of_puo2', 'fuel_roughness')
        rod_props.clear()
        rod_props.rows.extend(tab['fuel-materials-2'])

        clad_mats = self.rodlayout.get_table('material', 'property', 'clad_conductivity',
                'clad_specific_heat', 'clad_density', 'clad_emissivity',
                'clad_thermal_expansion')
        clad_mats.clear()
        clad_mats.rows.extend(tab['cladding-materials-1'])

        clad_props = self.rodlayout.get_table('material', 'clad_thickness',
                'gap_conductance', 'fill_gap', 'model_gap', 'clad_roughness',
                'fill_gas_pressure', 'fill_gas_volume')
        clad_props.clear()
        clad_props.rows.extend(tab['cladding-materials-2'])

        # -------------- operating conditions --------------------------------------

        # this is handled in the scf package:
        # boundary conditions, these parameters need to be set by the user:
        # * exit pressure
        # * inlet temp
        # * total power
        #
        # additionally one of
        # * pressure drop    -> driving pressure condition
        # * inlet flow rate  \_ pure flow condition
        # * inlet mass flux  /

        # mass flow rate calculated based on first cell
        massflow = self.opcon.get_switch('set_flow_split_first_axial')
        massflow.state = 'set_flow_split_first_axial'

        # initial power map
        pmap_time = self.opcon.get_table('power_map_time')
        pmap_time.clear()
        pmap_time.rows.append([0])

        pmap = self.opcon.get_table('axial_cell_number', 'rod_number', 'power_map')
        pmap.clear()
        pmap.rows.extend(tab['power-map'])

        # -------------- calculation control  --------------------------------------
        # steady state
        self.calcon.get_variable('start_time').value = 0.0
        self.calcon.get_variable('stop_time').value = 0.0
        self.calcon.get_variable('time_step').value = 0.00
        self.calcon.get_variable('print_timestep_every').value = 1000


        # overridden by cell length table below
        self.calcon.get_variable('total_axial_length').value = zlen
        self.calcon.get_variable('number_of_axial_nodes').value = len(zgrid)

        # set mode heights and try the new scf.model methods
        table = self.calcon.get_table('cell_number', 'cell_length')
        table.clear()
        for(i, dz) in enumerate(zgrid, 1):
            table.rows.append([i, float(dz)*zlen])

        # -------------- special parameters  --------------------------------------
        # docu says: only needed for Rehme correlation of triangular rod arrays
        self.specpar.get_variable('rod_diameter').value = tab['rod-diameter']

        if log:
            t2 = time.time()
            print TFORMAT.format('ends', t2-t1)
            t1 = t2

        return 

    def run(self, mode='r', **kwargs):
        #self._process_model()
        super(ScfInterface, self).run(mode, **kwargs) # scf started here

        if mode.isupper():
            # SCF was actually run. Read results.
            nm = self.read_output()
        else:
            # otherwise, return a copy of the input model.
            nm = self.__gm.copy_tree()
        return nm

    def read_output(self):
        print 'read_output started'
        out = self.wp.output.exfile

        if not os.access(out, os.R_OK):
            raise ValueError('No output produced, failed to execute scf.')

        (rs, cs) = scf.read_output(out)
        print 'output.read_output completed with {} rs and {} cs elements'.format(len(rs), len(cs))

        # SCF results are first saved to the sm, and then (see below) copied to
        # the returned general model:
        sm = self.__sm
        skeys = self.__skeys

        coolant      = sm.get_child(skeys['coolant'])
        first_fuel   = sm.get_child(skeys['fuels'][0])
        fuel_bound   = first_fuel.temp.boundary_coords('abs')
        # r_low  = fuel_bound[0]  # lowest  z coordinate of fuel elements
        # r_high = fuel_bound[-1] # highest z coordinate of fuel elements
        # c_low  = None #     idx of coolant grid cell that represents lowest  rod grid cell
        # c_high = None # 1 + idx of coolant grid cell that represents highest rod grid cell
        # for (i, c) in enumerate(coolant.temp.boundary_coords('abs')):
        #     if c_low is None and c >= r_low:
        #         c_low = i
        #     if c_high is None and c >= r_high:
        #         c_high = i

        c_low  = coolant.temp.element_index(first_fuel.temp.element_coord( 0, 'abs')[-1], cs='abs')
        c_high = coolant.temp.element_index(first_fuel.temp.element_coord(-1, 'abs')[-1], cs='abs')
        c_high += 1

        for (i, r) in enumerate(cs[:-1]):             # last cs is the average values.
            T = r.column('temperature')
            D = r.column('density')
            # convert C -> K and kg/m^3 -> g/cm^3:
            T = map(lambda x: x + 273.15, T)
            D = map(lambda x: x * 1e-3,   D)

            # SCF prints out values on axial layer boundary. We need
            # mean values in a layer:
            Tc = map(convertors.mean, T[1:], T[:-1])
            Dc = map(convertors.mean, D[1:], D[:-1])

            # sm allready has proper axial grid. Use it for channel box:
            cbox = sm.get_child('scf_c{0}'.format(i))
            cbox.temp.update(sm.temp)
            cbox.dens.update(sm.dens)
            # for i in range(c_low, c_high):
            #     cbox.temp.set_value_by_index(Tc[i-c_low], i)
            #     cbox.dens.set_value_by_index(Dc[i-c_low], i)

            Told = cbox.temp.values()
            Dold = cbox.dens.values()
            Tnew = Told[0:c_low] + Tc + Told[c_high:]
            Dnew = Dold[0:c_low] + Dc + Dold[c_high:]
            cbox.temp.set_values( Tnew )
            cbox.dens.set_values( Dnew )

            # Take care of extra coolant below and above fuel.
            # Don't use mean values here, but boundary values:
            if c_low > 0: # have coolant below lower end of fuel
                cbox.temp.set_value_by_index(T[0], c_low - 1)
                cbox.dens.set_value_by_index(D[0], c_low - 1)

            if c_high < len(cbox.temp.get_grid()): # have coolant above upper end of fuel
                cbox.temp.set_value_by_index(T[-1], c_high)
                cbox.dens.set_value_by_index(D[-1], c_high)
            #print 'scf results to {}, pos={}, dimensions: {} {} {}'.format(cbox.get_key(), cbox.pos, cbox.X, cbox.Y, cbox.Z)
            #print cbox.temp
            #print cbox.dens
        print 'loop over cs completed'


        # put fuel temperature
        for (rkey, r) in zip(skeys['rods'], rs):
            rod = sm.get_child(rkey)
            f = standard_model.find_fuel(rod)
            if f is not None:
                # print 'put fuel temperature to ', f.get_key()
                T = r.column('tfuave')
                # Results for rods are given for axial layers, thus no mean
                # is needed as for channel rods.
                f.temp.set_values(T)
                f.temp += 273.15
                # print f.temp

        # Copy results from standard model to the general model:
        gm = self.__gm.copy_tree()
        cl = gm.get_child(self.keys['coolant'])
        # copy channel boxes:
        nr = len(cl.children)
        nc = 0
        for e in sm.children[:]: #### .values():
            if isinstance(e.local_key, str) and e.local_key.startswith('scf_c'):
                cl.insert(e.local_key, e)
                # cl.shift_child(e.local_key, 0)
                e.temp.prec = sm.temp.prec
                e.dens.prec = sm.dens.prec
                #print '{} moved to output model'.format(e.local_key)
                nc += 1
        cl.shift_children(nr, nc, 0)
        #print 'new order in cl:'
        #for c in cl.children:
        #    print c.local_key
        #print '-'*10

        cl.scf_interface_lattice_filled = True
        cl._no_interior = True

        # copy fuel temperature distributions:
        for fkey in skeys['fuels']:
            if fkey[-2] == 'gap':
                rkey = fkey[:-2]
            else:
                rkey = fkey[:-1]

            fuel_g = standard_model.find_fuel(gm.get_child(rkey))  # fuel element of result model
            fuel_s = sm.get_child(fkey)
            fuel_g.temp.update(fuel_s.temp)

        return gm

    def _read_output(self):
        """
        Put rod-centered channels.
        """
        print 'read_output started'
        out = self.wp.output.exfile.replace('output.txt', 'pl_rod_+0.000E+00.txt')

        if not os.access(out, os.R_OK):
            raise ValueError('No output produced, failed to execute scf.')

        data  = list(scf.output.read_pl_rod(out))
        print 'output.read_pl_rod completed with {} elements'.format(len(data))

        # SCF results are first saved to the sm, and then (see below) copied to
        # the returned general model:
        sm = self.__sm
        skeys = self.__skeys

        coolant      = sm.get_child(skeys['coolant'])
        first_fuel   = sm.get_child(skeys['fuels'][0])

        # Master model for rod-centered channel box:
        dzl = [] # list of axial heights
        zmin = rs[0].column('Zmin')
        zmax = rs[0].column('Zmax')
        for (z1, z2) in zip(zmin, zmax):
            dzl.append(z2-z1)
        cbox = Box(X=coolant.grid.x, Y=coolant.grid.y, Z=first_fuel.Z)
        cbox.pos = first_fuel.pos.copy()
        cbox.material = coolant.material
        cbox.dens.set_grid(dzl)
        cbox.temp.set_grid(dzl)

        nr = len(sm.children)
        nc = 0
        for (rkey, r) in zip(skeys['rods'], rs):
            rod = sm.get_child(rkey)
            f = standard_model.find_fuel(rod)
            if f is not None:
                # print 'put fuel temperature to ', f.get_key()
                T = r.column('tfuave')
                # Results for rods are given for axial layers, thus no mean
                # is needed as for channel rods.
                f.temp.set_values(T)
                f.temp += 273.15
                # print f.temp
            cb = cbox.copy_tree()
            sm.insert('scf_c{}'.format(nc), cb, rod.ijk)

            # SCF-computed values:
            T = r.column('tfluid')
            cb.temp.set_values
            nc += 1

