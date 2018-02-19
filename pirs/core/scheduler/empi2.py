from mpi4py import MPI
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

import time
import random

c = MPI.COMM_WORLD
s = c.Get_size()
r = c.Get_rank()

lst = list(range(10))
if r == 0:
    ps = set()
    while lst:
        rr = c.recv()
        print '1Got message from', rr
        c.send(lst.pop(0), rr)
        ps.add(rr)
    # send finalization messages
    while ps:
        rr = c.recv()
        print '2Got message from', rr, ps
        c.send(None, rr)
        ps.remove(rr)
else:
    f = open('out{}.txt'.format(r), 'w')
    n = -1
    while n is not None:
        c.send(r, 0)
        n = c.recv(source=0)
        w = random.randint(1, 5)
        time.sleep(w)
        print >> f, 'Processing {} for {}s on {}'.format(n, w, r)
    f.close()

MPI.Finalize()
