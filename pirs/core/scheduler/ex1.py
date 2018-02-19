# Distribute work among available processors
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

from mpi4py.futures import MPIPoolExecutor
from pirs.core.scheduler import WorkPlace, InputFile
import random

N = 100
lst = list(range(N))


def job(n):
    w = WorkPlace()
    w.prefix = 'wp_for_job'
    i = InputFile()
    i.basename = 'start.sh'
    i.string = 'echo {}; date; sleep {}s; date'.format(n, random.randint(1, 30))
    i.cmd = './start.sh &> log.txt'
    i.executable = True
    w.files.append(i)
    w.prepare()
    out = w.run()
    return n, out

if __name__ == '__main__':
    with MPIPoolExecutor() as executor:
        print 'Im here'
        outs = executor.map(job, lst)
        print outs
