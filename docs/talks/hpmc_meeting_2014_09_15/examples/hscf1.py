from pirs import ScfInterface
from hmcnp5 import mi

si = ScfInterface(mi.gm)

if __name__ == '__main__':
    si.wp.prefix = 's1_'
    si.run('r')
