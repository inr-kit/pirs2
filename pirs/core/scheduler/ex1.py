# Distribute work among available processors
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
