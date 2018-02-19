# ----------------------------------------------------------------------------------
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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


