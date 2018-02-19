from mpi4py import MPI
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
