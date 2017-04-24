from pirs import McnpInterface
from geom3 import cnt

mi = McnpInterface(cnt)

if __name__ == '__main__':
    mi.wp.prefix = 'm1_'
    mi.run('P')
