#!/bin/bash

#PBS -l select=1:ncpus=5:mpiprocs=5
#PBS -l walltime=00:05:00
#PBS -A FUA11_MCHIFI
#PBS -q xfuadebug


echo "Hello Marconi!"
echo "PBS_JOBNAME       $PBS_JOBNAME"
echo "PBS_ENVIRONMENT   $PBS_ENVIRONMENT"
echo "PBS_JOBID         $PBS_JOBID"
echo "PBS_QUEUE         $PBS_QUEUE"
echo "PBS_O_WORKDIR     $PBS_O_WORKDIR"
echo "PBS_O_HOME        $PBS_O_HOME"
echo "PBS_O_QUEUE       $PBS_O_QUEUE"
echo "PBS_O_LOGNAME     $PBS_O_LOGNAME"
echo "PBS_O_SHELL       $PBS_O_SHELL"
echo "PBS_O_HOST        $PBS_O_HOST"
echo "PBS_O_MAIL        $PBS_O_MAIL"
echo "PBS_O_PATH        $PBS_O_PATH"
echo "PBS_O_NODEFILE    $PBS_O_NODEFILE"
echo "Goodbye marconi!"


module load python/2.7.12                
module load intel/pe-xe-2017--binary     
module load intelmpi/2017--binary        
module load mkl/2017--binary             
module load numpy/1.11.2--python--2.7.12 
module load mpi4py/2.0.0--python--2.7.12 

mpirun python workplaces.py 

