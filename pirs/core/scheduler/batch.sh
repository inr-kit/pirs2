#!/bin/bash

#PBS -l select=1:ncpus=5:mpiprocs=5
#PBS -l walltime=00:05:00
#PBS -A FUA11_MCHIFI
#PBS -q xfuadebug

cd $PBS_O_WORKDIR

module load python/2.7.12                
module load intel/pe-xe-2017--binary     
module load intelmpi/2017--binary        
module load mkl/2017--binary             
module load numpy/1.11.2--python--2.7.12 
module load mpi4py/2.0.0--python--2.7.12 

mpirun python workplaces.py 

