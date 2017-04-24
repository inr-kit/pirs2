from hmcnp1 import mi
from mcnp_water import m1 as w
from mcnp_zirc import zr
from mcnp_mox import mox

mi.materials['water'] = w
mi.materials['fuel'] = mox
mi.materials['steel'] = zr
mi.materials['zirc'] = zr

if __name__ == '__main__':
    mi.wp.prefix = 'm2_'
    mi.run('P')
