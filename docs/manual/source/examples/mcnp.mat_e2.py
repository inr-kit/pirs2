from pirs.mcnp import Material

h = Material('H')
o = Material('O')

h2o = 2*h + o

# thermal data
h2o.thermal = 'lwtr'

# nuclide substitution
h2o.sdict[8018] = 8016

for t in [300, 350, 400]:
    h2o.T = t
    print h2o.card()
