from geom_scf import b

# 1

import hpmc

s = hpmc.ScfInterface(b)
s.keys['rods'].append((0,))

s.inlet_temperature = 560.
s.total_power = 3.5e6 / 200/200.
s.inlet_flow_rate = 1.6e7 / 200 / 200.
s.exit_pressure = 15.5e6

s.run('R')

