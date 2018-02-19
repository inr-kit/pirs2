from tramat import Mixture
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


print 'nMix', Mixture.nMix

m = Mixture(92235)
m2 = Mixture(m)
m3 = Mixture(m, 1, 1001, 2)

print 'nMix', Mixture.nMix

fe = Mixture('Fe')
h1 = Mixture(1001)


for f in ['C2H5OH', 'Al2O3', 'Fe2O3', 'C4B', 'HeHF', 'Fe', 'U']:
    print f
    mix = Mixture(f, names={'Fe':fe, 'H':h1})
    print mix.report()
    for n, c in mix.elements().items():
        print n, c


print 'nMix', Mixture.nMix



