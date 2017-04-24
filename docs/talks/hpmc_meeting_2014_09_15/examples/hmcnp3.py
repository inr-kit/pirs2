from hmcnp2 import mi

mi.bc['radial'] = '*'
mi.bc['axial'] = ''

if __name__ == '__main__':
    mi.wp.prefix = 'm3_'
    mi.run('P')

