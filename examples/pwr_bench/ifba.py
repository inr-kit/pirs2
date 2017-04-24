from pirs.solids import Cylinder
from pin_model import model as cell

"""
IFBA fuel pin.  Copy of standard pin, with layer of ifba added.
"""
# data from table 6, p.8:
r1 = 0.3951
r2 = 0.3991

# geometry: copy of pin
ifba_pin = cell.get_child('clad').copy_tree()
# add layer of ifba to the 'gap' element:
gap = ifba_pin.get_child('gap')
ifba = gap.insert(Cylinder(R=r2, Z=gap.Z, material='ifba'), 0)
ifba.name = 'ifba'

ifba.dens.set_values(1.69)






