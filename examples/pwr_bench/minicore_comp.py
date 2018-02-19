import sys
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


from pirs.tools import Plotter
from pirs.tools import load, dump
from pirs.solids import Box
from tecplot import read_tecplot

from minicore_model import minicore 

# get my results:
my = True
if my:
    Tres = minicore.copy_tree()
    with open('n_iteration_017_tfuel.txt', 'r') as f:
        for l1 in f:
            l2 = f.next()
            l3 = f.next()

            key = eval(l1)
            grid = eval(l2)
            temp = eval(l3)

            fuel = Tres.get_child(key)
            fuel.temp.set_grid(grid)
            fuel.temp.set_values(temp)

    if len(sys.argv) > 1 and sys.argv[1] == 'dump':
        dump('TFUEL_AT.dump', 
                scf_result = Tres,
                Keff = [-1.],
                Kerr = [-1.],
                Ic = 'Anton last iteration')
# get alex results:

his = True
if his:
    tecplot_file = 'TECPLOT_TFUEL.dat'
    d = read_tecplot(tecplot_file)
    Ires = minicore.copy_tree()
    for c in Ires.children:
        i, j = eval(c.local_key.split()[-1])
        i += 1
        j += 1
        for cc in c.children:
            if cc.local_key == 'fuel':
                vals = [d[(i,j,k)] for k in range(1, 21)]
                cc.temp.set_grid([1]*20)
                cc.temp.set_values(vals)
    # dump Alex's results as a general model to be used in 
    # plot_maps.py

    if len(sys.argv) > 1 and sys.argv[1] == 'dump':
        dump(tecplot_file + '.dump', 
                scf_result = Ires,
                Keff = [-1.],
                Kerr = [-1.],
                Ic = tecplot_file)
        exit()


if True:
    lrpairs = {}
    for (Ta, Ia) in zip(Tres.children, Ires.children):
        for (Tf, If)  in zip(Ta.children, Ia.children):
            if Tf.local_key == 'fuel':
                i, j, k = Ta.ijk
                i += 1
                j += 1
                if i <= 25:
                    # this is left pin
                    lrpairs[(i,j)] = [(Tf, If)]
                else:
                    lrpairs[(50-i,j)].append((Tf, If))
    print ' pairs found'


if True:
    plt1 = Plotter()
    plt1.add_line(0, 0, '', 'temp', 0, fmt='<g', label='T, left') 
    plt1.add_line(0, 1, '', 'temp', 0, fmt='<b', label='I, left') 
    plt1.add_line(0, 2, '', 'temp', 0, fmt='>g', label='T, right') 
    plt1.add_line(0, 3, '', 'temp', 0, fmt='>b', label='I, right') 
    plt1.ylabel[0] = 'Fuel temperature, K'
    plt1.xlabel[0] = 'Axial height, cm'
    plt1.ylim[0] = (600, 1300)

    plt2 = Plotter()
    plt2.add_line(0, 0, '', 'temp', 0, fmt='og', label='T') 
    plt2.add_line(0, 1, '', 'temp', 0, fmt='ob', label='I') 
    plt2.ylabel[0] = 'Fuel temperature, K'
    plt2.xlabel[0] = 'Axial height, cm'
    plt1.ylim[0] = (600, 1300)

    if len(sys.argv) > 1:
        direc = sys.argv[1]
        index = int(sys.argv[2])
        try:
            zlevel = float(sys.argv[3])
        except:
            zlevel = 0.
        # traverse data.
        tdI = {}
        tdT = {}
        for iii in range(51):
            tdI[iii] = 0.
            tdT[iii] = 0.

        if direc == 'i':
            odir = 'j'
        elif direc == 'j':
            odir = 'i'

    else:
        direc = None 

    for (key, value) in lrpairs.items():
        i, j = key
        if direc == 'i':
            toPlot = index == i
            io = j
        elif direc == 'j':
            toPlot = index == j
            io = i
        else:
            # plot all graphs
            toPlot = True

        if toPlot:
            args = value.pop(0)
            plt = plt2

            if value: 
                args += value.pop(0)
                plt = plt1

            fig = plt.figure(*args)
            ax = plt.axdict[0]

            ax.text(1, 1, args[0].parent.local_key, 
                     horizontalalignment='right', 
                     verticalalignment='bottom', 
                     transform=ax.transAxes)

            fig.savefig('minicore_comp_{:02d}_{:02d}.pdf'.format(i,j))
            fig.clf()

            if direc in 'ij':
                # append data to traverse:
                tdT[io] = args[0].temp.get_value_by_coord((0,0,zlevel), 'abs')
                tdI[io] = args[1].temp.get_value_by_coord((0,0,zlevel), 'abs')

                if direc == 'j' and len(args) == 4:
                    tdT[50-io] = args[2].temp.get_value_by_coord((0,0,zlevel), 'abs')
                    tdI[50-io] = args[3].temp.get_value_by_coord((0,0,zlevel), 'abs')

                print io, tdT[io], tdI[io]


    if direc in 'ij':
        # plot traverse along the direction direc.
        # at the specified height.
        plt = Plotter()
        plt.add_line(0, 0, '', 'temp', 0, fmt='og', label='T')
        plt.add_line(0, 1, '', 'temp', 0, fmt='ob', label='I')
        plt.ylabel[0] = 'Fuel temperature, K'
        plt.xlabel[0] = 'Index ' + odir 
        plt.ylim[0] = (600, 1300)

        xlst = range(0, len(tdT))
        elst = [0] * len(tdT)

        a1 = Box(X=1, Y=1, Z=51)
        a1.pos.z = 25
        a1.temp.set_grid([1]*51)
        a2 = a1.copy_tree()

        a0 = Box()
        a0.insert(1, a1)
        a0.insert(2, a2)

        tdT = map(lambda kv: kv[1], sorted(tdT.items()))
        tdI = map(lambda kv: kv[1], sorted(tdI.items()))

        for (tT, tI) in zip(tdT, tdI):
            print tT, tI

        print len(tdT), len(tdI)
        a1.temp.set_values(tdT)
        a2.temp.set_values(tdI)

        fig = plt.figure(a1, a2)
        plt.axdict[0].set_title('Traverse along {}={} at z {}'.format(direc, index, zlevel))
        fig.savefig('minicore_comp_{}{:02d}.pdf'.format(direc, index))

        # for 





        


        



