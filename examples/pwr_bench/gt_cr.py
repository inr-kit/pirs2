from pirs.solids import Cylinder
from pin_model import ah 

"""
Guide tube and control rod models.
"""

# data from table 6, p.8:
r1 = 0.5624
r2 = 0.6032

tube = Cylinder(R=r2, Z=ah, material='zirc')
watr = tube.insert(Cylinder(R=r1, Z=ah, material='water'))
watr.name = 'wchan'

watr.temp.set_values(580)
watr.dens.set_values(0.71187)

tube.temp.set_values(580)
tube.dens.set_values(6.504)

# water channels
chan = tube.copy_tree()

# let's model an absorber rod in the tube:
absrod = watr.insert(Cylinder(R=r1*0.9, Z=ah, material='ifba', pos.Z=ah*0.7)
absrod.name = 'absorber rod'


