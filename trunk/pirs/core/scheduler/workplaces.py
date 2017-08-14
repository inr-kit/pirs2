# -*- coding: utf-8 -*-

"""
Try to create several workplaces with MPI processes.

Important is to use non-mpi version of MCNP.
"""

from pirs.core.scheduler import WorkPlace, InputFile
try:
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
except:
    rank = 0

if rank == 0 or rank > 0:
    w = WorkPlace()
    w.prefix = 'wp_by_rank{}'.format(rank)

    # MCNP input file
    i1 = InputFile()
    i1.basename = 'inp'
    i1.string = """ c MCNP input file
1 0 -1 imp:n=1
2 0  1 imp:n=0

1 so 10

sdef pos 0 0 0
nps 100000000
prdmp j j 1
print

    """

    i2 = InputFile()
    i2.basename = 'start.sh'
    i2.string = """#!/bin/bash
    ls -l
    pwd
    module li
    echo $SHELL
    which mcnp5
    mcnp5 inp = inp

    """
    i2.cmd = './start.sh  &> log.txt'
    i2.executable = True
    w.files.append(i1)
    w.files.append(i2)
    w.prepare()
    print w.lcd
    out = w.run(files=['mctal'])
    print rank, out
