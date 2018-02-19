from model import Bundle, Rod, Relation
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


# dimensions:
pp = 2. # pin pitch
r = 0.9 # pin radius
Np = 10 # number of pin rows and columns in the assembly

points_on_walls = False # True


# assembly bundle
a = Bundle.box(ll=(0,0), ur=(pp*(Np-1), pp*(Np-1)), r=1.3*r) 
a.wt =1.
a.color = 'blue'

# channel
ch = Bundle.box(ll=(0, 0), ur=(2*pp, 3*pp), r=0.8*r)
ch.color = 'green'
ch.wt = 0.2
rc = Relation()
rc.x = 5*pp
rc.y = 3*pp
a.interior.append((ch, rc))

# fuel pin master model
p = Rod()   
p.radius = r
p.color = 'red'

# insert fuel pins into the assembly
chsh = a.shapely([0])
if points_on_walls:
    Imin = 0
    Imax = 0
else:
    Imin = -1
    Imax = 1
for i in range(Imin, Np+Imax):
    x = pp * i
    for j in range(Imin, Np+Imax):
        y = pp * j
        r = Relation()
        r.x = x
        r.y = y
        a.interior.append((p, r))
        if points_on_walls:
            psh = a.shapely([-1])
            if psh.intersects(chsh):
                # if pin intersects with the channel, 
                # remove it:
                a.interior.pop(-1)

# for fun, insert one pin into the channel:
ch.interior.append((p, Relation(pp, 1.5*pp)))

# define triangulation points at channel and assembly walls:
if points_on_walls:
    a.vertices.extend(a.iwall.points(Np-2, 'LineS'))
    ow = ch.owall(0,0)
    # rc.vertices.extend(ow.points([1, 2, 1, 2, 1, 1, 1, 1], 'segments'))
    rc.vertices.extend(ow.points([1, 2, 1, 2], 'LineS'))
    rc.vertices.extend(ow.points(1, 'arcs'))

ch.vertices.extend(ch.iwall.points(2, 'lines'))



plt = a.plot(order='ioptc')
plt.get_figure().savefig('bwr.pdf')

ch.plot(axis=plt, x=rc.x, y=rc.y, order='ioptc')
plt.get_figure().savefig('bwr_chan.pdf')
