
from pin_scf import SI, thp, Na, cflow
from minicore_model import rod_keys, Nax, Nay

# 1

# change keys, specifying rod elements
# in the general model:
SI.keys['rods'] = rod_keys
print 'SI.keys:', SI.keys.keys()

# there is new mox materials: 
SI.materials['mox1'] = 'benpwr'
SI.materials['mox2'] = 'benpwr'
SI.materials['mox3'] = 'benpwr'

# 2

# adjust total power:
SI.total_power = thp / Na *Nax*Nay 

# adjust flow rate:
SI.inlet_flow_rate = cflow / Na * Nax*Nay


if __name__ == '__main__':
    from minicore_model import minicore
    SI.gm = minicore
    SI.keys['coolant'] = ''
    SI.run('r')

