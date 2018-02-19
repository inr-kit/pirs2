from pirs.tools import Plotter
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

from pirs.tools import load

# prepare plotter
plt = Plotter()
# for my results
plt.add_line(0, 0, '', 'temp', 0,           fmt='.g', label='$T_T$') # results for rod (1,1)
plt.add_line(1, 1, '', 'temp', 0, sharey=0, fmt='.g', label='$T_T$') # results for rod (51,1)
plt.add_line(2, 2, '', 'temp', 0,           fmt='.g', label='$T_T$') # results for rod (1,35)
plt.add_line(3, 3, '', 'temp', 0, sharey=2, fmt='.g', label='$T_T$') # results for rod (51,35)
# for alex results
plt.add_line(0, 4, '', 'temp', 0, fmt='.b', label='$T_I$') # results for rod (1,1)
plt.add_line(1, 5, '', 'temp', 0, fmt='.b', label='$T_I$') # results for rod (51,1)
plt.add_line(2, 6, '', 'temp', 0, fmt='.b', label='$T_I$') # results for rod (1,35)
plt.add_line(3, 7, '', 'temp', 0, fmt='.b', label='$T_I$') # results for rod (51,35)


# get my results:
d = load('n_iteration_017.dump')
sres = d['scf_result']
print 'dump read'
apins = {}
for c in sres.children.values():
    index = -1
    if c.ijk == (1-2, 1-2, 0):
        index = 0
    elif c.ijk == (51-2, 1-2, 0):
        index = 1
    elif c.ijk == (1-2, 35-2, 0):
        index = 2
    elif c.ijk == (51-2, 35-2, 0):
        index = 3
    if index in [0, 1, 2, 3]:
        for cc in c.values():
            if cc.local_key == 'fuel':
                apins[index] = cc.withdraw()
print 'apins found'

# get alex results:
data = {}
data[0] = []
data[1] = []
data[2] = []
data[3] = []
with open('anton_tmp.dat', 'r') as f:
    for l in f:
        for (i, v) in enumerate(l.split()[1:]):
            data[i].append(float(v))
ipins = {}
for (index, pin) in apins.items():
    ipin = pin.copy_tree()
    ipin.temp.clear()
    ipin.temp.set_grid([1]*20)
    ipin.temp.set_values(data[index])
    ipins[index] = ipin
print 'ipins found'

fig = plt.figure(apins[0], apins[1], apins[2], apins[3],
                 ipins[0], ipins[1], ipins[2], ipins[3])
for (i, label) in [(0, 'pin 1,1'), (1, 'pin 51,1'), (2, 'pin 1,35'), (3, 'pin 51,35')]:
    ax = plt.axdict[i]
    ax.text(1, 1, label, horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes)
print 'figure generated'

fig.savefig('minicore_comparison.pdf')


        
