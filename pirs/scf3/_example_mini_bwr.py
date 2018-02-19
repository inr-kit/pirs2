from model import Bundle, Rod, Relation
from pirs.tools.plots.plot_shapely import ShapelyToAxis 
from random import uniform

# dimensions:
pp = 2. # pin pitch
rr = 0.9 # pin radius
Np = 3 # number of pin rows and columns in the assembly

# assembly bundle
a = Bundle.box(ll=(0,0), ur=(pp*(Np-1), pp*(Np-1)), r=1.3*rr) 
a.wt =1.
a.color = 'blue'

# channel
ch = Bundle.box(ll=(1, 1), ur=(3.1, 3.0), r=0.1)
ch.color = 'green'
ch.wt = 0.2
rc = Relation()
rc.x = 0
rc.y = 0
a.interior.append((ch, rc))


# insert fuel pins into the assembly
Imin = -1
Imax = 1
for i in range(Imin, Np+Imax):
    x = pp * i
    for j in range(Imin, Np+Imax):
        if (i, j) != (-10, -10):
            y = pp * j
            r = Relation()
            r.x = x  + uniform(-0.1*rr, 0.1*rr)
            r.y = y  + uniform(-0.1*rr, 0.1*rr)
            p = Rod()   
            p.radius = 0.3 + 0.05*i + 0.15*j 
            p.color = 'red'
            a.interior.append((p, r))



plt = a.plot(order='ioptc')
plt.get_figure().savefig('mini_bwr.pdf')

for (e, r, s, c) in a.visible_interior():
    print e, r, c

ax = None
Nch = 0
for ch in a.own_subchannels():
    ax = ShapelyToAxis(ch, axis=ax, order='b', label=(Nch, ch.area))
    Nch += 1
ax.get_figure().savefig('mini_bwr_channels.pdf')
