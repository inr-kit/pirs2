u4_f = 1.215
u4_c = 0.1771

u5_f = 1.219
u5_c = 0.9519e-1

u8_f = 0.2998
u8_c = 0.7019e-1

print 'u5: ', u5_f/(u5_f+u5_c)
print 'u8: ', u8_f/(u8_f+u8_c)

from pirs.mcnp import Material
u = Material('U')
a4 = u.how_much(1, 92234).v
a5 = u.how_much(1, 92235).v
a8 = u.how_much(1, 92238).v
print a5, a8
print u.report()

kinf = (a4*u4_f + a5*u5_f + a8*u8_f) / (a4*(u4_f + u4_c) + a5*(u5_f + u5_c) + a8*(u8_f + u8_c))
print kinf
