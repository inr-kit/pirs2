#!/bin/bash -l

# generate standard tex:
make clean;
make latex;

# use vim to change latex file.
texfile="build/latex/tsp.tex"

if [[ -f $texfile ]]; then

cp $texfile $texfile.orig

vim -n -e $texfile <<-"EOF"
    %s/|//g
    %s/OriginalVerbatim/Verbatim/g
    %s/\\hline//g
    :update
    :quit
EOF

cd build/latex/;
make ;
bibtex tsp;
pdflatex tsp;
pdflatex tsp;
pdflatex tsp;

evince tsp.pdf &
wait

fi

