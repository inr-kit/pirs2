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

Interface for box container with rods inserted into the grid.
"""
from math import pi
pi4 = pi/4.
pi2 = pi/2.

from .convertors import rod2material, isheated
from ...scf2.input import Input
from ...scf2.output import read_pl_rod
from ...scf2.material import RodMaterialCollection
from ...solids import Box

_Tkelvin = 273.15 

class Model(Input):
    def __init__(self, gm=None):
        self.__gm = gm # general model
        self.__mdict = {} # dictionary for material names.
        self.__mc = RodMaterialCollection() # collection of rod materials 

        # some parameters for convenience
        self.exit_pressure = None # exit_pressure
        self.__pd = 0 # pressure_drop
        self.inlet_temperature = None # inlet_temperature

        self.__ifr = None # inlet_flow_rate
        self.__imf = None # inlet_mass_flux

        self.__tp = None # total_power
        self.__ahf = None # average_heat_flux

        super(Model, self).__init__()
        return

    

    def clear(self):
        """
        Clears only tables, filled by _process_model.
        """
        self.find('rod_number', 'material_type')[0].clear()
        self.find('material', 'property', 'fuel_conductivity')[0].clear()
        self.find('material', 'fuel_diameter')[0].clear()
        self.find('material', 'property', 'clad_conductivity')[0].clear()
        self.find('material', 'clad_thickness')[0].clear()
        self.find('t', 'axial_cell_number', 'rod_number', 'power_map')[0].clear()
        self.find('t', 'cell_number', 'cell_length')[0].clear()
        self.find('channel_number', 'channel_area')[0].clear()
        self.find('t', 'channel', 'max_40_x_')[0].clear()
        self.find('t', 'rod', 'max_6_x')[0].clear()

    @property
    def pressure_drop(self):
        """
        Pressure drop.

        If specified, it also changes switch ``set_driving_pressure_condition``.
        """
        return self.__pd

    @pressure_drop.setter
    def pressure_drop(self, v):
        self.__pd = v

    @property
    def inlet_flow_rate(self):
        """
        Inlet flow rate.

        By setting this property, the ``inlet_mass_flux`` property is set to 0.
        """
        return self.__ifr

    @inlet_flow_rate.setter
    def inlet_flow_rate(self, v):
        self.__ifr = v
        self.__imf = 0

    @property
    def inlet_mass_flux(self):
        """
        Inlet mass flux.

        By setting this property, the ``inlet_flow_rate`` property is set to 0.
        """
        return self.__imf

    @inlet_mass_flux.setter
    def inlet_mass_flux(self, v):
        self.__imf = v
        self.__ifr = 0

    @property
    def total_power(self):
        """
        Total power.

        By setting this property, the ``average_heat_flux`` property is set to 0.
        """
        return self.__tp

    @total_power.setter
    def total_power(self, v):
        self.__tp = v
        self.__ahf = 0.

    @property
    def average_heat_flux(self):
        """
        Average heat flux.

        By setting this property, the ``total_power`` property is set to 0.
        """
        return self.__ahf

    @average_heat_flux.setter
    def average_heat_flux(self, v):
        self.__ahf = v
        self.__tp = 0.

    @property
    def gm(self):
        return self.__gm

    @gm.setter
    def gm(self, value):
        self.__gm = value

    @property
    def materials(self):
        """
        Dictionary for correspondence bentween material names and rod materials.
        """
        return self.__mdict

    def _process_rods(self):
        """
        Prepares rod data.
        """
        gm = self.__gm

        gm.remove_by_criteria(name=-1)


        r_props = {} # dict (i,j): list of rod properties.
        r_ordered = []
        for r in gm.children:
            if None not in r.ijk:
                ij = r.ijk[:2]
                l = r_props.get(ij, [])
                if not l:
                    # get rod mateiral and its index:
                    m = rod2material(r, self.__mdict) # rod's material
                    if m:
                        # can be treates as a rod.
                        # only first rod having i,j will be taken into account.
                        l.append( isheated(r) ) # flag heated/notheated rod.
                        l.append(r)   # rod itself,
                        l.append([])  # list for rod-channel connections. Will be filled later, in channel loop.

                        l.append(self.__mc.index(m)) # rod material index
                        r_props[ij] = l
                        r_ordered.append(l)
            else:
                print 'element skipped\n', r.str_tree(['id()', 'name', 'ijk'])
        self.__rodsd = r_props
        self.__rodsl = r_ordered

        # put data to tables.
        t = self.find('rod_number', 'material_type')[0]
        t.clear()
        for Nr, r in enumerate(r_ordered, 1):
            x, y, z = r[1].abspos().car
            t.rows.append([Nr, r[3], r[1].R*2*1e-2, 0.1, x, y])

        tf1 = self.find('material', 'property', 'fuel_conductivity')[0]
        tf2 = self.find('material', 'fuel_diameter')[0]
        tc1 = self.find('material', 'property', 'clad_conductivity')[0]
        tc2 = self.find('material', 'clad_thickness')[0]
        for t in [tf1, tf2, tc1, tc2]:
            t.clear()

        for Nm, m in self.__mc.items():
            tf1.rows.append([Nm, m.fp, m.fc, m.fsh, m.fD, m.fe, m.fte])
            tf2.rows.append([Nm, m.fd, m.fir, m.ftd, m.fop, m.fr])

            tc1.rows.append([Nm, m.cp, m.cc, m.csh, m.cd, m.ce, m.cte])
            tc2.rows.append([Nm, m.ct, m.gc, m.fg, m.mg, m.cr, m.fgp, m.fgv])


    def _process_heats(self):
        # axial height
        v = self.find('v', 'total_axial_length')[0]
        v.value = self.__gm.Z * 1e-2

        # common grid for SCF axial grid:
        cmesh = self.__gm.common_zmesh(own=True)
        for r in self.__rodsl:
            if r[0]:
                cmesh.unify(r[0])
        for r in self.__rodsl:
            if r[0]:
                cmesh.unify(r[0])

        self.__cmesh = cmesh # needed to put SCF results back to the model.

        v = self.find('v', 'number_of_axial_nodes')[0]
        v.value = len(cmesh.get_grid())
        t = self.find('t', 'axial_cell_number', 'rod_number', 'power_map')[0]
        t.clear()
        zlst = cmesh.element_coords('abs')
        Nr = 1
        for r in self.__rodsl:
            Nz = 1
            for z in zlst:
                if r[0]:
                    h = r[0].get_value_by_coord(z, 'abs')
                else:
                    h = 0.
                # h can be of uncertainties class
                if hasattr(h, 'nominal_value'): 
                    t.rows.append([Nz, Nr, h.nominal_value])
                else:
                    t.rows.append([Nz, Nr, h])
                Nz += 1
            Nr += 1

        t = self.find('t', 'cell_number', 'cell_length')[0]
        t.clear()
        for Nz, dz in enumerate(cmesh.get_grid(), 1):
            t.rows.append([Nz, dz* self.__gm.Z*1e-2])
            
            
    def _process_channels(self):
        """
        Assumes that each grid element has rod and only rods are in the container.
        """
        gm = self.__gm
        r_props = self.__rodsd

        ### Imin, Imax, Jmin, Jmax, Kmin, Kmax = gm.grid.extension()
        # Imin, Imax, ... should be defined not by the container grid properties only, but also
        # by the rods inserted into the container's grid. For example, there can be row(s) and
        # column(s) of grid element around the bundle without rods.
        r = self.__rodsl[0][1]
        Imin = r.ijk[0] 
        Jmin = r.ijk[1]
        Kmin = r.ijk[2]
        Imax = Imin
        Jmax = Jmin
        Kmax = Kmin
        for r in gm.children:
            if None not in r.ijk:
                i, j, k = r.ijk
                if Imin > i: Imin = i
                if Imax < i: Imax = i
                if Jmin > j: Jmin = j
                if Jmax < j: Jmax = j
                if Kmin > k: Kmin = k
                if Kmax < k: Kmax = k

        Xmin, Xmax = gm.extension('x', 'rel')
        Ymin, Ymax = gm.extension('y', 'rel')

        pll = gm.grid.position(Imin, Jmin, Kmin) # position of the lower left rod
        pur = gm.grid.position(Imax, Jmax, Kmax) # position of the upper right rod

        gx = gm.grid.x
        gy = gm.grid.y
        gxl = pll.x - Xmin # width of the channels in the left column
        gxr = Xmax - pur.x # width of the channels in the right column
        gyl = pll.y - Ymin # height of the channels in the lower row
        gyu = Ymax - pur.y # height of the channels in the upper row

        a0 = gx * gy # internal channel area
        a1 = gxl * gy      # left column channels area
        a2 = gxr * gy      # right column channels area
        a3 = gx * gyl      # lower row channels area
        a4 = gx * gyu      # upper row channels area

        ch_props = {}
        ch_ordered = []
        Nc = 1 # counter to enumerate the channels.
        #NEW
        print 'J:', Jmin-1, Jmax
        print 'I:', Imin-1, Imax
        for j in range(Jmin-1, Jmax+1):
            for i in range(Imin-1, Imax+1):
                print 'channel ', Nc, (i, j)
                ind_r = (i+1, j) # right neighbour index
                ind_u = (i, j+1) # upper neighbour index
                # distance and gap to the right neighbour
                if i == Imin-1:
                    dst_r = (gxl + gx)*0.5
                    gap_u = gxl
                    dx = gxl
                    print 'left column'
                elif i == Imax-1:
                    dst_r = (gx + gxr)*0.5
                    gap_u = gx
                    dx = gx
                    print 'pre-right column'
                elif i == Imax:
                    gap_u = gxr
                    dx = gxr
                    print 'right column'
                else:
                    dst_r = gx
                    gap_u = gx
                    dx = gx
                    print 'middle column'
                # distance to the upper neighbour
                if j == Jmin-1:
                    dst_u = (gyl + gy)*0.5
                    gap_r = gyl
                    dy = gyl
                    print 'lower row'
                elif j == Jmax-1:
                    dst_u = (gy + gyu)*0.5
                    gap_r = gy
                    dy = gy
                    print 'pre-upper row'
                elif j == Jmax:
                    gap_r = gyu
                    dy = gyu
                    print 'upper row'
                else:
                    dst_u = gy
                    gap_r = gy
                    dy = gy
                    print 'middle row'
                # adjacent rods and how they affect gaps:
                arods = {}
                if i < Imax and j < Jmax:
                    arods[2] = r_props[(i+1, j+1)]
                    arods[2][2].append((Nc, 0.25))
                    gap_u = gap_u - arods[2][1].R
                    gap_r = gap_r - arods[2][1].R
                if j >= Jmin and i < Imax:
                    arods[0] = r_props[(i+1, j)]
                    arods[0][2].append((Nc, 0.25))
                    gap_r = gap_r - arods[0][1].R
                if i >= Imin and j < Jmax:
                    arods[1] = r_props[(i, j+1)]
                    arods[1][2].append((Nc, 0.25))
                    gap_u = gap_u - arods[1][1].R
                if i >= Imin and j >= Jmin:
                    arods[3] = r_props[(i, j)]
                    arods[3][2].append((Nc, 0.25))
                print 'rods: ', sorted(arods.keys())
                # channel area, perimeters
                ra = 0.
                wp = 0.
                hp = 0.
                for r in arods.values():
                    rR = r[1].R
                    ra += rR**2.
                    wp += rR
                    # if r[0]: hp += rR 
                    hp += rR
                area = dx*dy - pi4*ra
                wp *= pi2 
                hp *= pi2
                # list of adjacent channels:
                nbrs = []
                if i < Imax:
                    nbrs.append((ind_r, gap_r, dst_r))
                if j < Jmax:
                    nbrs.append((ind_u, gap_u, dst_u))

                ch_props[(i,j)] = (Nc, area, wp, hp, nbrs)
                ch_ordered.append((i,j))
                Nc += 1
                        
        #NEW
        ## ## for j in range(Jmin-1, Jmax+1):
        ## ##     for i in range(Imin-1, Imax+1):
        ## ##         nbrs = [] # list of neighbours with bigger Nc
        ## ##         if (i, j) == (Imin-1, Jmin-1):
        ## ##             # this is the lower left channel
        ## ##             r = r_props[(Imin, Jmin)]
        ## ##             rR = r[1].R
        ## ##             area = gxl*gyl - pi4*rR**2
        ## ##             wp = pi2*rR
        ## ##             if r[0]:
        ## ##                 hp = wp
        ## ##             else:
        ## ##                 hp = 0.
        ## ##             # right neighbour:
        ## ##             gap_r = gyl - rR
        ## ##             dst_r = (gxl + gx)*0.5 
        ## ##             ind_r = (i+1, j)
        ## ##             # upper neighbour:
        ## ##             gap_u = gxl - rR
        ## ##             dst_u = (gyl + gy)*0.5
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_r, gap_r, dst_r), (ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             r[2].append((Nc, 0.25))
        ## ##         elif (i, j) == (Imin-1, Jmax):
        ## ##             # the upper left channel
        ## ##             r = r_props[(Imin, j)]
        ## ##             rR = r[1].R
        ## ##             area = gxl*gyu - pi4*rR**2
        ## ##             wp = pi2*rR
        ## ##             if r[0]:
        ## ##                 hp = wp
        ## ##             else:
        ## ##                 hp = 0.
        ## ##             # right neighbour:
        ## ##             gap_r = gyu - rR
        ## ##             dst_r = (gxl + gx)*0.5 
        ## ##             ind_r = (i+1, j)
        ## ##             nbrs = [(ind_r, gap_r, dst_r)]
        ## ##             # rod-channel connections:
        ## ##             r[2].append((Nc, 0.25))
        ## ##         elif (i, j) == (Imax, Jmin-1):
        ## ##             # the lower right channel
        ## ##             r = r_props[(i, Jmin)]
        ## ##             rR = r[1].R
        ## ##             area = gxr*gyl - pi4*rR**2
        ## ##             wp = pi2*rR
        ## ##             if r[0]:
        ## ##                 hp = wp
        ## ##             else:
        ## ##                 hp = 0.
        ## ##             # upper neighbour:
        ## ##             gap_u = gxr - rR
        ## ##             dst_u = (gyl + gy)*0.5
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             r[2].append((Nc, 0.25))
        ## ##         elif (i, j) == (Imax, Jmax):
        ## ##             # the upper right channel
        ## ##             r = r_props[(i, j)]
        ## ##             rR = r[1].R
        ## ##             area = gxr*gyu - pi4*rR**2
        ## ##             wp = pi2*rR
        ## ##             if r[0]:
        ## ##                 hp = wp
        ## ##             else:
        ## ##                 hp = 0.
        ## ##             nbrs = []
        ## ##             # rod-channel connections:
        ## ##             r[2].append((Nc, 0.25))
        ## ##         elif i == Imin-1:
        ## ##             # the left column channels
        ## ##             a = a1
        ## ##             rl = r_props[(Imin,   j)]
        ## ##             ru = r_props[(Imin, j+1)]
        ## ##             area = a - pi4*(rl[1].R**2 + ru[1].R**2)
        ## ##             wp = 0.
        ## ##             hp = 0.
        ## ##             for r in (rl, ru):
        ## ##                 rR = r[1].R
        ## ##                 wp += rR
        ## ##                 if r[0]:
        ## ##                     hp += rR
        ## ##             wp *= pi2
        ## ##             hp *= pi2
        ## ##             # right neighbour:
        ## ##             gap_r = gy - rl[1].R - ru[1].R
        ## ##             dst_r = (gxl + gx)*0.5 
        ## ##             ind_r = (i+1, j)
        ## ##             # upper neighbour:
        ## ##             gap_u = gxl - ru[1].R
        ## ##             dst_u = gy
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_r, gap_r, dst_r), (ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             rl[2].append((Nc, 0.25))
        ## ##             ru[2].append((Nc, 0.25))
        ## ##         elif i == Imax:
        ## ##             # the right column channels
        ## ##             a = a2
        ## ##             rl = r_props[(Imax,   j)]
        ## ##             ru = r_props[(Imax, j+1)]
        ## ##             area = a - pi4*(rl[1].R**2 + ru[1].R**2)
        ## ##             wp = 0.
        ## ##             hp = 0.
        ## ##             for r in (rl, ru):
        ## ##                 rR = r[1].R
        ## ##                 wp += rR
        ## ##                 if r[0]:
        ## ##                     hp += rR
        ## ##             wp *= pi2
        ## ##             hp *= pi2
        ## ##             # upper neighbour:
        ## ##             gap_u = gxr - ru[1].R
        ## ##             dst_u = gy
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             rl[2].append((Nc, 0.25))
        ## ##             ru[2].append((Nc, 0.25))
        ## ##         elif j == Jmin-1:
        ## ##             # the lower row channels
        ## ##             a = a3
        ## ##             rl = r_props[(  i, Jmin)]
        ## ##             rr = r_props[(i+1, Jmin)]
        ## ##             area = a - pi4*(rl[1].R**2 + rr[1].R**2)
        ## ##             wp = 0.
        ## ##             hp = 0.
        ## ##             for r in (rl, rr):
        ## ##                 rR = r[1].R
        ## ##                 wp += rR
        ## ##                 if r[0]:
        ## ##                     hp += rR
        ## ##             wp *= pi2
        ## ##             hp *= pi2
        ## ##             # right neighbour:
        ## ##             gap_r = gyl - rr[1].R
        ## ##             dst_r = gx 
        ## ##             ind_r = (i+1, j)
        ## ##             # upper neighbour:
        ## ##             gap_u = gx - rl[1].R - rr[1].R
        ## ##             dst_u = gy
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_r, gap_r, dst_r), (ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             rl[2].append((Nc, 0.25))
        ## ##             rr[2].append((Nc, 0.25))
        ## ##         elif j == Jmax:
        ## ##             # the upper row channels
        ## ##             a = a4
        ## ##             rl = r_props[(  i, Jmax)]
        ## ##             rr = r_props[(i+1, Jmax)]
        ## ##             area = a - pi4*(rl[1].R**2 + rr[1].R**2)
        ## ##             wp = 0.
        ## ##             hp = 0.
        ## ##             for r in (rl, rr):
        ## ##                 rR = r[1].R
        ## ##                 wp += rR
        ## ##                 if r[0]:
        ## ##                     hp += rR
        ## ##             wp *= pi2
        ## ##             hp *= pi2
        ## ##             # right neighbour:
        ## ##             gap_r = gyu - rr[1].R
        ## ##             dst_r = gx 
        ## ##             ind_r = (i+1, j)
        ## ##             nbrs = [(ind_r, gap_r, dst_r)]
        ## ##             # rod-channel connections:
        ## ##             rl[2].append((Nc, 0.25))
        ## ##             rr[2].append((Nc, 0.25))
        ## ##         else:
        ## ##             # internal channels
        ## ##             r1 = r_props[(  i,  j)]      # lower left rod
        ## ##             r2 = r_props[(i+1,  j)]      # lower right
        ## ##             r3 = r_props[(  i,j+1)]      # upper left
        ## ##             r4 = r_props[(i+1,j+1)]      # upper right rod

        ## ##             area = a0 - pi4*(r1[1].R**2 + r2[1].R**2 + r3[1].R**2 + r4[1].R**2)

        ## ##             wp = 0.
        ## ##             hp = 0.
        ## ##             for r in (r1, r2, r3, r4):
        ## ##                 rR = r[1].R
        ## ##                 wp += rR
        ## ##                 if r[0]:
        ## ##                     hp += rR
        ## ##             wp *= pi2
        ## ##             hp *= pi2
        ## ##             # right neighbour:
        ## ##             gap_r = gy - r2[1].R - r4[1].R
        ## ##             dst_r = gx 
        ## ##             ind_r = (i+1, j)
        ## ##             # upper neighbour:
        ## ##             gap_u = gx - r3[1].R - r4[1].R
        ## ##             dst_u = gy
        ## ##             ind_u = (i, j+1)
        ## ##             nbrs = [(ind_r, gap_r, dst_r), (ind_u, gap_u, dst_u)]
        ## ##             # rod-channel connections:
        ## ##             r1[2].append((Nc, 0.25))
        ## ##             r2[2].append((Nc, 0.25))
        ## ##             r3[2].append((Nc, 0.25))
        ## ##             r4[2].append((Nc, 0.25))


        ## ##         ch_props[(i,j)] = (Nc, area, wp, hp, nbrs)
        ## ##         ch_ordered.append( (i,j) )
        ## ##         Nc += 1
        # put data to SCF tables
        t1 = self.find('channel_number', 'channel_area')[0]
        t2 = self.find('t', 'channel', 'max_40_x_')[0]
        t1.clear()
        t2.clear()
        for ij in ch_ordered:
            Nc, area, wp, hp, nbrs = ch_props[ij]
            t1.rows.append([Nc, area*1e-4, wp*1e-2, hp*1e-2, 1.1, 1.2])

            t2row = []
            for ijn, gap, dst in nbrs:
                Nn = ch_props[ijn][0] # index of the neighbour channel
                t2row.extend( [Nn, gap*1e-2, dst*1e-2] )
            t2.rows.append([Nc] + t2row)

        tr = self.find('t', 'rod', 'max_6_x')[0]
        tr.clear()
        for Nr, r in enumerate(self.__rodsl, 1):
            row = []
            for Nc, f in r[2]:
                row.extend( [Nc, f] )
            if row:
                tr.rows.append([Nr] + row)

    def _process_params(self):
        if self.exit_pressure is not None:
            self.find('v', 'exit_pressure')[0].value = self.exit_pressure

        if self.inlet_temperature is not None:
            self.find('inlet_temperature')[0].value = self.inlet_temperature

        if self.__pd is not None:
            s, v = self.find('pressure_drop')
            v.value = self.__pd
            if self.__pd > 0:
                s.state = 'pressure_condition'
            else:
                s.state = 'pure_flow'

        if self.__imf is not None:
            self.find('inlet_mass_flux')[0].value = self.__imf
        if self.__ifr is not None:
            self.find('inlet_flow_rate')[0].value = self.__ifr

        if self.__tp is not None:
            self.find('total_power')[0].value = self.__tp
        if self.__ahf is not None:
            self.find('average_heat_flux')[0].value = self.__ahf

    def _process_model(self):
        self._process_rods()
        self._process_heats()
        self._process_channels()
        self._process_params()

    def __str__(self):
        self._process_model()
        return super(Model, self).__str__()

    def run(self, mode, outp='r'):
        """
        Optional argument outp specifies what results, rod or channel
        will be put to the output model. Can be 'r' or 'c'.

        """

        if mode in 'rR':
            super(Model, self).run(mode)

            if mode == 'R':
                # SCF was actually run. Read output data
                self._get_rod_results()
                return self.__gm# .copy_tree()
            else:
                return self.__gm

        else:
            raise ValueError('Unknown mode {}'.format(mode))

            
    def _get_rod_results(self):
        """
        Read rod results and insert them into the model.
        """
        cb = Box()
        cb.name = -1 # this means that this box contains SCF results.
        cb.X = self.__gm.grid.x
        cb.Y = self.__gm.grid.y
        cb.Z = self.__gm.Z
        cb.material = self.__gm.material
        cb.dens.set_grid(self.__cmesh.get_grid())
        cb.temp.set_grid(self.__cmesh.get_grid())
        cb.dens.prec = self.__gm.dens.prec
        cb.temp.prec = self.__gm.temp.prec

        for Nr, table in read_pl_rod(self.wp.pl_rod.exfile):
            # coolant box -- container for coolant results
            b = cb.copy_tree()     # box for coolant properties 
            r = self.__rodsl[Nr-1] # rod
            self.__gm.grid.insert(r[1].ijk, b, 0) # must be inserted 'before' the rod.
            Tcool = []
            Dcool = []
            Tfuel = []
            for row in table:
                Tfc = row[5] + _Tkelvin # fuel centerline temperature
                Tfs = row[4] + _Tkelvin # fuel surface temperature
                Tf = 0.3 * Tfc  +  0.7 * Tfs

                Tcl = row[1] + _Tkelvin # coolant temperature
                rcl = row[6] * 1e-3     # coolant density

                Tcool.append(Tcl)
                Dcool.append(rcl)
                Tfuel.append(Tf)
            b.temp.set_values(Tcool)
            b.dens.set_values(Dcool)
            if r[0]:
                fuel = r[0].get_solid()
                fuel.temp.set_values(0) # to let grid change
                fuel.temp.set_grid(self.__cmesh.get_grid())
                fuel.temp.set_values(Tfuel)
            
            



                


