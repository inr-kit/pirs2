from pirs.mcnp import Material
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

from pin_mcnp import MI, u, o 
from assembly_model import model


# Optionally, one can provide ksrc point
# for each fuel element:
ksrc = 'ksrc'
for e in model.values():
    if 'fuel' in e.get_key():
        x, y, z = e.abspos().car
        ksrc += '   {0} {1} {2}'.format(x, y, z)
MI.adc[-1] = ksrc

# 1

if __name__ == '__main__':
    MI.gm = model
    MI.run('P')

