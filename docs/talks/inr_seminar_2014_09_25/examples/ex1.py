from pirs.solids import Box
from pirs.mcnp import Material
from pirs import McnpInterface

# GEOMETRY 
b = Box(material='m1')
b.dens.set_values(18.8)

# MCNP-SPECIFIC DATA
i = McnpInterface(b)
i.materials['m1'] = Material('U')  # material
i.bc['axial'] = '*'               # b.c.
i.bc['radial'] = '*'
i.adc.append('ksrc 0 0 0')        # kcode source
i.adc.append('kcode 100 1 30 100')

if __name__ == '__main__':
    # RUN MCNP
    i.run('R')                # start MCNP 
    print 'K-inf:', i.keff()  # print Keff
