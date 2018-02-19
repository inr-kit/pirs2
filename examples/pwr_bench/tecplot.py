def read_tecplot(fname):
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

    data = {}
    with open(fname, 'r') as f:
        for l in f:
            entries = l.split()
            i, j, k = map(int, entries[:3])
            v = float(entries[3])

            data[(i,j,k)] = v
    return data


if __name__ == '__main__':
    d = read_tecplot('TFUEL_AI.dat')
    for ijk in ((1, 1, 10), (51, 1, 10), (1, 51, 10), (51, 51, 10), (4, 4, 10)):
        print ijk, d[ijk]

    


