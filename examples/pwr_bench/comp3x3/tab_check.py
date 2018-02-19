"""
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

Checks table resutls for the benchmark.
"""
import sys

for dname in sys.argv[1:]:
    with open(dname, 'r') as tfile:
        IJKset = set()
        Imin = None
        Imax = None
        Jmin = None
        Jmax = None
        Kmin = None
        Kmax = None
        Ws = 0.
        for l in tfile:
            t = l.split()
            i, j, k = map(int, t[:3])
            Tf, Tc, Rc, Hf = map(float, t[3:])

            if Imin is None or Imin > i:
                Imin = i
            if Imax is None or Imax < i:
                Imax = i
            if Jmin is None or Jmin > j:
                Jmin = j
            if Jmax is None or Jmax < j:
                Jmax = j
            if Kmin is None or Kmin > k:
                Kmin = k
            if Kmax is None or Kmax < k:
                Kmax = k

            IJKset.add((i,j,k))
            Ws += Hf

        for i in range(Imax+1-Imin):
            for j in range(Jmax+1-Imin):
                for k in range(Kmax+1-Kmin):
                    if (i,j,k) not in IJKset:
                        print 'no data for ', i, j, k

        print 'Ws {0:14.6e}'.format(Ws)

