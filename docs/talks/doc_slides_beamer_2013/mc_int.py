from hpmc import McnpInterface
from mcnp import Material

m = McnpInterface(b)

u = Material((92235, 0.5, 2),
             (92238, 95.5, 2))

o = Material('O')
h = Material('H')

f = u + 2*o
w = h*2 + o
w.thermal = 'lwtr'


f.sdict[8018] = 8016
w.sdict[8018] = 8016

m.materials['fuel'] = f
m.materials['water'] = w

m.bc['radial'] = '*'

m.adc.append('ksrc 0 0 0')
m.adc.append('kcode 500 1. 20 100')

m.run('P')

r = m.run('R')
