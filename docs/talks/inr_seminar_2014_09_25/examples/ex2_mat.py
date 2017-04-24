from pirs.mcnp import Material

# water 
h = Material('H')
o = Material('O')

w = 2*h + o
print w.report()

w.thermal = 'lwtr'
w.T = 450
w.sdict[8018] = 8016
print w.card(comments=False)

# Zircaloy
s = Material( ('Zr', 98.23, 1),
              ('Sn', 1.50,  1),
              ('Fe', 0.12,  1))
