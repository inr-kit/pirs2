from pin_scf import SI, thp, Na, Np, cflow
from assembly_model import rod_keys, Nx, Ny

# 1

# change keys, specifying rod elements
# in the general model:
SI.keys['rods'] = rod_keys

# 2

# adjust total power:
SI.total_power = thp / Na # / Np * Nx*Ny 

# adjust flow rate:
SI.inlet_flow_rate = cflow / Na #  / Np * Nx*Ny



if __name__ == '__main__':
    from assembly_model import model
    SI.gm = model
    SI.keys['coolant'] = ''
    SI.run('R')

