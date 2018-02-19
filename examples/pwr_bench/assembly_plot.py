from sys import argv
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


# for plotting without x tunneling
from matplotlib import use
# use('Cairo.pdf')
use('cairo')
from pirs.tools.plots import MeshPlotter as Plotter
from pirs.tools import load


if len(argv) < 2:
    print """
    Script is used to plot axial distributions of temperature and power in 
    one pin, specified in the command line arguments:

    > python assembly_plot.py   Nx   Ny     *.dump

    Where Nx and Ny are pin indices followed by dump files.
    """
    exit()

argvc = argv[1:]
        
try:
    Nx = int(argvc[0])
    argvc.pop(0)
except ValueError:
    Nx = 0
try:
    Ny = int(argvc[0])
    argvc.pop(0)
except ValueError:
    Ny = Nx
print 'FIgures will be plotted for Nx, Ny = ({}, {})'.format(Nx, Ny)

if argvc[-1] == 'noplot':
    # only text file will be printed.
    doplot = False
    argvc.pop()
else:
    doplot = True


# Setup plotting  later
ppp = None


for f in argvc:
    if '.dump' in f:
        print 'printing from ', f
        d = load(f)
        Ic = d['Ic']
        kcode = d['kcode']
        sres = d['scf_result']
        mres = d['mcnp_result']
        Rm = d['relaxed']

        prefix = f[:-5]
        if doplot:
            if ppp is None:

                # first, get the proper compound key for the fuel pin to be plotted:
                for c in sres.children:
                    if c.ijk == (Nx, Ny, 0):
                        for cc in c.values():
                            if cc.local_key == 'fuel':
                                fuel_key = cc.get_key()
                                break
                        else:
                            raise ValueError('element {} found by indices ({}, {}), has no fuel inside. Specify other indices.'.format(c.get_key(), Nx, Ny))
                        print 'Figures will be plotted for the model element {}'.format(fuel_key)
                        break

                # Setup plotting 
                ppp = Plotter()
                ppp.figsize=(8, 8)
                # MCNP results
                ppp.add_line(0, 0, fuel_key, 'heat',  0, fmt='.y', label='$p_{__i}$')
                # Relaxed heat
                ppp.add_line(0, 1, fuel_key, 'heat', -1, fmt='.k', label='$P_{__i}$')
                # TH result of fuel temp
                ppp.add_line(1, 1, fuel_key, 'temp', -1, fmt='.k', label='$T_{f,__i}$')
                ppp.ylabel[0] = 'relative heat'
                ppp.ylabel[1] = 'fuel temperature, K'
                ppp.xlabel[1] = 'z coordinate, cm'

                

            fig = ppp.figure(mres, sres)
            fig.suptitle('Iteration {0}, {1}'.format(Ic, fuel_key[0]))

            fig.savefig(prefix + '_{0}_{1}.pdf'.format(Nx, Ny))

        # save power and temperature axial profiles to a text file:
        for (PI, PJ) in [(1,1), (51,51), (1,51), (51,1), (18,18), (34,34), (18,34), (34,18)]:
            for c in sres.children:
                if c.ijk == (PI-2, PJ-2, 0):
                    for cc in c.values():
                        if cc.local_key == 'fuel':
                            fuel = cc
                            break
            print 'printinfg txt file for ', (PI, PJ), fuel.get_key()
            hfmt = '{:>11s}'
            vfmt = '{:>11.4f}'
            for (mesh, name) in [(fuel.temp, 'temp'), (fuel.heat, 'heat')]:
                mesh.prec = 0.
                zl = mesh.boundary_coords('abs')
                zlmin = zl[:-1]
                zlmax = zl[1:]
                vl = mesh.items('coord', 'abs')
                with open(prefix + name + '_{0}_{1}.txt'.format(PI, PJ), 'w') as ftxt:
                    ftxt.write((hfmt*5).format('Xmid', 'Ymid', 'Zmid', 'Zmin', 'Zmax'))
                    ftxt.write('{:>13s}\n'.format(name))
                    for (zmin, zmax, (mid, v)) in zip(zlmin, zlmax, vl):
                        xmid, ymid, zmid = mid
                        print xmid, ymid, zmid, zmin, zmax, v
                        ftxt.write((vfmt*5).format(xmid, ymid, zmid, zmin, zmax))
                        if not isinstance(v, float):
                            v = v.nominal_value
                        ftxt.write('{:>13.5e}\n'.format(v))
    else:
        print 'warning command line argument {} is not a dump file, skipping it.'.format(repr(f))

if doplot:
    kkk = Plotter()
    kkk.figsize=(8,4)
    kkk.add_line(0, 0, fuel_key, 'temp',  0, fmt='.k', label='$k_{eff}$')
    kkk.xlabel[0] = 'Iteration index'
    kkk.ylabel[0] = '$k_{eff}$'

    Keff = d['Keff'][2:]
    Kerr = d['Kerr'][2:]
    fig = kkk.figure([range(1, len(Keff)+1), Keff, Kerr])
    fig.savefig(prefix + '_keff.pdf')

