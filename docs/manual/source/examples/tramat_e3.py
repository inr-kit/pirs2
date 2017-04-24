from pirs.core.tramat import Mixture

h1 = Mixture('H')
he = Mixture('He')

m1 = h1 + he
m2 = 2*h1
m3 = 2*h1 + 3*he
m4 = 2*m1 + 3*m2

m1.name = 'm1'
m2.name = 'm2'
m3.name = 'm3'
m4.name = 'm4'

for m in [m1, m2, m3, m4]:
    print m.report()
    print '='*30

