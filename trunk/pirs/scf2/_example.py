"""
Using the InputData class, describe two rods with 6 channels.

            
              dx1              dx2                 dx3
        ---------------------------------------------------|
        |            |                      |              |
        |                                 _____            |
  dy2   |    c1      |        c2         /     \     c3    |
        |           ____                /       \          |
        |          /    \              |         |         |
        |         |      |             |         |         |
        |- - - - -|  r1  |- - - - - - -|   r2    |- - - - -|
        |         |      |             |         |         |
        |          \____/              |         |         |
        |    c4               c5        \       /    c6    |
  dy1   |            |                   \_____/           |
        |                                   |              |
        |            |                                     |
        |--------------------------------------------------|
     

Vertically, rods r1 and r2, each have two zones. Rod 1 consists of zone 1 and 2,
rod 2 -- of zones 3 and 4.

  Zt    ----------------------------------------------------
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |    mat4  |        |
        |         |       |            |          |        |
        |         |  mat2 |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |----------|        |   z2
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
  z1    |         |-------|            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |  mat1 |            |    mat3  |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        |         |       |            |          |        |
        ----------------------------------------------------

mat1 and mat2: uo2, zirc
mat3 and mat4: MOX, ss316


Operating conditions are given by Tin for each channel, and Pin and Pout pressures.
     
"""
from math import pi

from input import Input
from output import read_output

scf = Input()

scf['initialisation'][0].value = 'two rods, six channels. Water'

scf['properties'][0].state = 'water'

grp = scf['correlations']
grp[0].state = 'bowring'
grp[1].state = 'armand'
grp[2].state = 'armand'
grp[3].state = 'blasius'
grp[4].state = 'dittus'
grp[5].state = 'barnett'
grp[6].state = 'none'
grp[7].state = 'simple'
grp.set_variables('blasius_', 64, -1, 0, 0.316, -0.25, 0)
grp.set_variables('dittus_boelter_', 0.023, 0.8, 0.4, 0.)

# this is necessary, Uwe says (for mixing model)
scf['special_parameters'].set_variables('rod_diameter', 9.5e-3)

# channel layout
dx1, dx2, dx3 = 0.00635, 0.0096, 0.00635
dy1, dy2 = 0.00635, 0.00635
r1, r2 = 0.0095/2, 0.0095/2
t = scf['channel_layout'][0]
t.rows.append([1, dx1*dy2 - pi*r1**2/4., pi*r1/2., pi*r1/2., dx1/2., dy1+dy2/2.])
t.rows.append([2, dx2*dy2 - pi*(r1**2 + r2**2)/4., pi*(r1+r2)/2, pi*(r1+r2)/2, dx1+dx2/2., dy1+dy2/2.])
t.rows.append([3, dx3*dy2 - pi*r2**2/4., pi*r2/2., pi*r2/2., dx1+dx2+dx3/2., dy1+dy2/2])
t.rows.append([4, dx1*dy1 - pi*r1**2/4., pi*r1/2., pi*r1/2., dx1/2., dy2/2.])
t.rows.append([5, dx2*dy1 - pi*(r1**2 + r2**2)/4., pi*(r1+r2)/2, pi*(r1+r2)/2, dx1+dx2/2., dy2/2.])
t.rows.append([6, dx3*dy1 - pi*r2**2/4., pi*r2/2., pi*r2/2., dx1+dx2+dx3/2., dy2/2])
t = scf['channel_layout'][1]
t.rows.append([1, 2, dy2-r1, (dx1+dx2)/2., 4, dx1-r1, (dy1+dy2)/2.])
t.rows.append([2, 3, dy2-r2, (dx2+dx3)/2., 5, dx2-r1-r2, (dy1+dy2)/2.])
t.rows.append([3, 6, dx3-r2, (dy1+dy2)/2.])
t.rows.append([4, 5, dy1-r1, (dx1+dx2)/2.])
t.rows.append([5, 6, dy1-r2, (dx2+dx3)/2.])
t.rows.append([6, 0, 0, 0])

# rod layout
dc = 0.00064  # clad thickness
dg = 0.0005 # gap thickness
grp = scf['rod_layout']
grp[0].state = -1
grp[1].state = 'dir'
grp[2].value = 6
grp[3].value = 100.

t = grp.find('rod_number', 'material_type', 'outer_diameter')[0]
t.rows.append([1, 1, r1*2, 1., dx1, dy1])
t.rows.append([2, 2, r2*2, 1., dx1+dx2, dy1])
t = grp.find('rod', 'max_6_x_(channel')[0]
t.rows.append([1, 1, 0.25, 2, 0.25, 4, 0.25, 5, 0.25])
t.rows.append([2, 2, 0.25, 3, 0.25, 5, 0.25, 6, 0.25])

t = grp.find('material', 'property', 'fuel_conductivity')[0]
# fuel properties
t.rows.append([1, 'uo2'])
t.rows.append([2, 'uo2_puo2'])
t.rows.append([3, 'uo2'])
t.rows.append([4, 'uo2_puo2'])
t = grp.find('material', 'fuel_diameter')[0]
t.rows.append([1, (r1-dc-dg)*2, 0, 1, 0, 3e-6])
t.rows.append([2, (r1-dc-dg)*2, 0, 1, 0.3, 3e-6]) 
t.rows.append([3, (r1-dc-dg)*2, 0, 1, 0.3, 3e-6]) 
t.rows.append([4, (r1-dc-dg)*2, 0, 1, 0.3, 3e-6]) 
# clad properties
t = grp.find('material', 'property', 'clad_conductivity')[0]
t.rows.append([1, 'zircaloy'])
t.rows.append([2, 'ss316'])
t.rows.append([3, 'zircaloy'])
t.rows.append([4, 'ss316'])
t = grp.find('material', 'clad_thickness')[0]
t.rows.append([1, dc, 5e3, 'off', 'on', 1e-6, 5e5, 1e-3])
t.rows.append([2, dc, 5e3, 'off', 'on', 1e-6, 5e5, 1e-3])
t.rows.append([3, dc, 5e3, 'off', 'on', 1e-6, 5e5, 1e-3])
t.rows.append([4, dc, 5e3, 'off', 'on', 1e-6, 5e5, 1e-3])
# rods axial configuration
Zt = 4.
z1 = 2.
z2 = 3.
tables = grp.find('configuration_type')
tables[0].rows.append([1, 2])
tables[0].rows.append([2, 2])
tables[1].rows.append([1, 1, z1/Zt, 1])
tables[1].rows.append([1, 2, Zt/Zt, 2])
tables[1].rows.append([2, 1, z2/Zt, 3])
tables[1].rows.append([2, 2, Zt/Zt, 4])
# burnup
t = grp.find('rod_number', 'burnup')[0]
t.rows.append([0, 0, 0])
t.rows.append([0, 1, 0])
# gap gas
grp.find('molar_fraction_he')[0].rows.append([1, 1.] + [0.]*5)
grp.find('molar_fraction_he')[0].rows.append([2, 1.] + [0.]*5)

# calculation control
grp = scf['calculation_control']
Nz = 30
grp[0].state = 'bicgstab'
grp[1].state = 'incompress'
grp[2].state = -1
grp[3].state = 0
# grp[4].state = 0 this is critical flux iterations. Do not need it here.
grp.set_variables('_temperature_change', 100, 100, 100)
grp['total_axial_length'].value = Zt
z = map(lambda x: x*Zt/Nz, range(0, Nz+1)) + [z1, z2]
z = list(set(z))
z.sort()
dz = map(lambda z1, z2: z2-z1, z[:-1], z[1:])
grp['number_of_axial_nodes'].value = len(dz) 
t = grp.find('cell_length')[0]
for (i, dd) in enumerate(dz):
    t.rows.append([i+1, dd])


# spacer grids
# model 3 spacer grids, located at
sgz = [0.2, 0.4, 0.75]
# each grid leads to the loss coefficient sgc
sgc = 0.1
grp = scf['grid_spacer_wire_wrap']
grp[0].state = 'spacer'
grp[1].value = 1
t = grp.find('loss_coefficient')[0]
for z in sgz:
    t.rows.append([0, z, sgc])

grp = scf['lateral_transport']
grp[0].state = 'rosehart'
grp[1].state = 'mass'
grp['lateral_conduction'].value = 0.

# Operation conditions:
Pout = 1.5e7  # exit pressure
dP = 7.8e1  # pressure drop
Tin = [281, 282, 283, 284, 285, 286] # Tin for each channel
Wtot = 60e3 # total power
pmap1 = map(lambda x: 1. + 0.01*x, range(len(dz)))
pmap2 = map(lambda x: 2. + 0.01*x, range(len(dz)))
grp = scf['operating_conditions']
grp[0].state = 'split'
grp[1].state = 'pure'
grp[2].state = 'factor'
grp.set_variables('', Pout, Tin[0], 0., 0.4, 0, Wtot, 0, dP, 0)
# tables = grp['channel_number'] 
# for (i, T) in enumerate(Tin, 1):
#     tables[0].rows.append([i, T])
grp['power_map_time'].rows.append([0])
t = grp.find('axial_cell_number', 'power_map')[0]
for (Ir, pmap) in enumerate([pmap1, pmap2], 1):
    for (Ic, p) in enumerate(pmap, 1):
        t.rows.append([Ic, Ir, p])


# start the code:
scf.run('R')

# read output:
(rr, cc) = read_output(scf.wp.output.exfile)
print rr[0]

