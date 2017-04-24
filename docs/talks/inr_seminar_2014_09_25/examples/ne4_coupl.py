from model import a
from mncp_data import MI  # McnpInterface
from scf_data import SI   # ScfInteface

# assign geometry with MCNP interface
MI.gm = a
# start MCNP
b = MI.run('R')

# assign ScfInterface model containing MCNP results
SI.gm = b
c = SI.run('R')
