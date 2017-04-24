
# Number of assembly rows and columns
Nax = 1
Nay = 1

Np = 17

Npx = Nax*Np
Npy = Nay*Np

from minicore_map import map_dict


from rod_models import ap, ah, pp
from pirs.solids import Box
from rod_models import uox, mox1, mox2, mox3, waba, tube, chan, ifba 

###   # take mox fractions from MCNP materials:
###   from pin_mcnp import moxlist
###   r = moxlist[0].recipe()
###   ux = r[0][0] # uox ingridiend
###   px = r[1][0] # puox ingridiend
###   moxfrac = []
###   for m in moxlist:
###       gux = m.how_much(2, ux)
###       gpx = m.how_much(2, px)
###       f = gpx/(gux + gpx) 
###       moxfrac.append(f)

minicore = Box(Z=ah)
minicore.X = Nax * ap
minicore.Y = Nay * ap
minicore.material = 'bwater'
minicore.temp.set_values(560.)
minicore.dens.set_values(0.8)

minicore.grid.x = pp
minicore.grid.y = pp
minicore.grid.z = minicore.Z

print 'minicore variable is created'

# prepare all rods
rods = []
fmt = ' {},{}'
for j in range(Npy):
    for i in range(Npx):
        rtype = map_dict[(i,j)]
        if rtype == 'u':
            key = 'uox'
            rod = uox.copy_tree()
            rod.pu_fraction = 0.
        elif rtype == 'm1':
            key = 'mox1'
            rod = mox1.copy_tree()
            rod.pu_fraction = moxfrac[0] 
        elif rtype == 'm2':
            key = 'mox2'
            rod = mox2.copy_tree()
            rod.pu_fraction = moxfrac[1] 
        elif rtype == 'm3':
            key = 'mox3'
            rod = mox3.copy_tree()
            rod.pu_fraction = moxfrac[2] 
        elif rtype == 'i':
            key = 'ifba'
            rod = ifba.copy_tree()
        elif rtype == 'g':
            key = 'tube'
            rod = tube.copy_tree()
        elif rtype == 'c':
            key = 'chan'
            rod = chan.copy_tree()
        elif rtype == 'w':
            key = 'waba'
            rod = waba.copy_tree()
        else:
            raise ValueError('Unknown rod type, ', repr(rtype))
        key = key + fmt.format(i,j)
        rod.name = key
        rods.append(rod)
print 'rods are created'

# insert rods to the minicore.
rod_keys = []
for j in range(Npy):
    for i in range(Npx):
        rod = rods.pop(0)
        minicore.grid.insert((i-1,j-1,0), rod)
        rod_keys.append(rod.get_key())
print 'rods are inserted'

minicore.grid.center()


