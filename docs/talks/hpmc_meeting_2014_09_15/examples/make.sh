#!/bin/bash


geom=" geom1 geom2 geom3"
mcnp=" mcnp_water mcnp_zirc mcnp_mox"
hmcn=" hmcnp1 hmcnp2 hmcnp3 hmcnp4 hmcnp5"
hscf=" hscf1 hscf2 hscf3"

if [ $# == 0 ]; then
    scripts=${geom}${mcnp}${hmcn}${hscf};
        rm geom*.pdf
        rm -rf m?_?
        rm hmcn*.pdf
        rm -rf s?_?
        rm hscf*.pdf
else
    if [ $1 == 'geom' ]; then
        scripts=$geom
        rm geom*.pdf
    fi;
    if [ $1 == 'mcnp' ]; then
        scripts=$mcnp
    fi;
    if [ $1 == 'hmcn' ]; then
        scripts=$hmcn
        rm -rf m?_?
        rm hmcn*.pdf
    fi;
    if [ $1 == 'hscf' ]; then
        scripts=$hscf
        rm -rf s?_?
        rm hscf*.pdf
    fi;
fi;


for s in $scripts; do
    echo $s;
    python ${s}.py > ${s}.log;
done

