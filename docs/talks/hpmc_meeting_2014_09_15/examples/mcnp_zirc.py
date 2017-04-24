from pirs.mcnp import Material
# zircaloy-2, Table 5, p.7
zr = Material(('Zr', 98.23), 
              ('Sn', 1.50),
              ('Fe', 0.12), 
              ('Cr', 0.10),
              ('N',  0.05)) 

print zr.card()
