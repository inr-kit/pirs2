from pirs.tools import dump
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

from hscf3 import si
from hmcnp5 import mi

mi.wp.prefix = 'cm_'
si.wp.prefix = 'cs_'

I = 0
while I < 5:
    # mcnp run
    mi.gm = si.gm.copy_tree()
    mr = mi.run('R', tasks=3)
    # relaxed power
    for (em, es) in zip(mr.heats(), si.gm.heats()):
        h = 0.5 *em.heat + 0.5 * es.heat
        es.heat.update(h)
    # scf run
    si.run('R')
    # store results
    dump('{}_coupling.dump'.format(I), 
         Keff = mi.keff(),
         mr = mr,
         sr = si.gm,
         I = I)

    I += 1

    dtmax = 0
    dtpos = None
    for (em, es) in zip(mr.heats(), si.gm.heats()):
        dt = em.temp - es.temp
        for v in dt.values():
            v = abs(v)
            if dtmax < v:
                dtmax = v
                dtpos = em.abspos()
    print 'Iteration {}, Keff={}'.format(I, mi.keff())
    print 'dTmax {} at {}'.format(dtmax, dtpos)



