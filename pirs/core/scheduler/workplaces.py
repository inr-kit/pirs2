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
    size = comm.Get_size()
    name = MPI.Get_processor_name()
    mess = 'Hello from process {} / {} on {}'.format(rank, size, name)
except Exception as e:
    comm = None
    raise e

if comm is not None:

    w = WorkPlace()
    w.prefix = 'wp_by_rank{}'.format(rank)

    # MCNP input file
    i1 = InputFile()
    i1.basename = 'inp'
    i1.exfile = "inp_"

    i2 = InputFile()
    i2.basename = 'start.sh'
    i2.string = """#!/bin/bash
    ls -l
    pwd
    . $PROJECT/mcnp/modules5
    module li
    echo $SHELL
    date
    which mcnp5.seq
    mcnp5.seq inp = inp
    date

    """
    i2.cmd = './start.sh  &> log.txt'
    i2.executable = True
    w.files.append(i1)
    w.files.append(i2)
    w.prepare()
    comm.Barrier()
    print mess, w.lcd, i2.cmd
    comm.Barrier()
    out = w.run(files=['mctal'])
    print out
    comm.Barrier()
