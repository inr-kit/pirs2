# ----------------------------------------------------------------------------------

from pirs.solids import Box
from rod_models import pp, ah, ap
from rod_models import ifba as pin

w = Box(X=pp, Y=pp, Z=ah + 2*ap)  # water box
w.material = 'water'

w.dens.set_values(1)
w.temp.set_values(580.) 

w.insert(pin)


# needed in SCF interface:
fuel_key = ('pin', 'gap', 'fuel') 
rod_key = pin.get_key()

# unify names
model = w


