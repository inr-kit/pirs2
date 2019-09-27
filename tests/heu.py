# Create composition of the 'meat', using specs

from pirs.mcnp import Material

# Assume that the enrichment process works equally for U-5 and U-4. Under this
# assumption the content of U4 and U5 will have the same ratio in all
# enrichments. Equations describing isotopic composition of U:
#
#   n5 / n4 = 0.7200 / 0.0055 == gamma                          (1)
#
#   n5 / (n4 + n5 + n8) = x (this is the u5 enrichment)         (2)
#
#   n4 + n5 + n8 = 1.0     (n4, n5 and n8 are molar fractions)  (3)
#
#
# From the above equations:
#          n5 = x
#          n4 = n5 / gamma     = x / gamma
#          n8 = 1.0 - n5 - n4  = 1.0 - x(gamma + 1)/gamma


x = 0.93
g = 0.72 / 0.0055

u93 = Material(
      92235, (x, 1),
      92234, (x/g, 1),
      92238, (1.0 - x*(g + 1)/g, 1))
al = Material('Al')
si = Material('Si')

u93.name = 'U93'
al.name = 'Al'
si.name = 'Si'

usi = Material(
        u93, (3, 1),
        si,  (2, 1))
usi.dens = 12.2
al.dens = 2.7

meat1 = Material(
            usi, (0.27, 3),
            al,  (1.00, 3))
meat2 = Material(
            usi, (0.14, 3),
            al,  (1.00, 3))
meat1.name = 'meat1'
meat2.name = 'meat2'

for m in (u93, al, si, usi, meat1, meat2):
    print(m.report())

for m in (meat1, meat2):
    ug = m.how_much(2, u93)
    vv = m.cc()
    print(m.name, ug, vv, ug/vv)
