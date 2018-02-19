from geom_scf import b
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


# 1

import hpmc

s = hpmc.ScfInterface(b)
s.keys['rods'].append((0,))

s.inlet_temperature = 560.
s.total_power = 3.5e6 / 200/200.
s.inlet_flow_rate = 1.6e7 / 200 / 200.
s.exit_pressure = 15.5e6

s.run('R')

