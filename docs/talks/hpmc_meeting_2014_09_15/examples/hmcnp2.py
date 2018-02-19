from hmcnp1 import mi
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

from mcnp_water import m1 as w
from mcnp_zirc import zr
from mcnp_mox import mox

mi.materials['water'] = w
mi.materials['fuel'] = mox
mi.materials['steel'] = zr
mi.materials['zirc'] = zr

if __name__ == '__main__':
    mi.wp.prefix = 'm2_'
    mi.run('P')
