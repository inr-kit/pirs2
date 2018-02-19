from pirs.core.trageom import Vector3, pi2, pi
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


v1 = Vector3(car=(1, 0, 0))   # x, y, z
v2 = Vector3(cyl=(1, 0, 1))   # r, theta, z
v3 = Vector3(sph=(1, 0, 0))   # R, theta, phi

print 'rotate v1:'
print v1.car
v1.t += pi2
print v1.car

print 'stretch v2 2 times:'
print v2.car
v2.R *= 2.
print v2.car

print 'flip v3:'
print v3.car
v3.p = pi 
print v3.car
