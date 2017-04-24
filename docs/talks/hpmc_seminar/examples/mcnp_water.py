from pirs.mcnp import Material

m1 = Material(('H', 2, 1),
              ('O', 1, 1))
m1.sdict[8018] = 8016
m1.thermal = 'lwtr'

m1.T = 300
print m1.card()

m1.T = 450
print m1.card()
