#!/usr/bin/env sh

Na=$(python -c "from a_model import Na;print Na")


if [ $# = 0 ]; then
    echo "parameters:  c t T Nz dTf dTc Nh"
fi

c=${1-a}
t=${2-1445}
T=${3-1455}
Nz=${4-5}
dTf=${5-10}
dTc=${6-1}
Nh=${7-10000}


host=${HOSTNAME:0:3}

case=${c}${host}_${Na}_${Nz}_${dTf}_${dTc}_${Nh}

submit="job_submit -t $t -T $T -o $case.out -e $case.err -J $case"

if [ "$host" = "ic2" ]; then
    submit="$submit -m 32000 -p 20/8 -c p -x+ "
elif [ "$host" = "hc3" ]; then
    submit="$submit -m 12000 -p 8/4  -c p -x+ "
else
    submit=""
fi

command="$submit python driver_mpi.py $case --Nh $Nh --Nz $Nz --dTf $dTf --dTc $dTc"

if [ $# = 0 ]; then 
    echo $command
else
    echo $command
    $command
fi


