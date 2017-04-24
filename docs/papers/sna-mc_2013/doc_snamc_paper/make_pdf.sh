#!/bin/bash -l

# use vim to change latex file.

texfile="_build/latex/SNA-MC2013_travleev_paper.tex"

cp $texfile $texfile.orig

vim -X -E $texfile <<-"EOF"
    /\\title{Latex-title}
    .,+6 del
    /phantomsection
    :del
    %s/\\subsection/\\subsubsection/g
    %s/\\section/\\subsection/g
    %s/\\chapter/\\section/g
    :update
    :quit
EOF


sleep 2

# force the use of custom sphinx.sty:
cp _static/sphinx.sty _build/latex/.;

cd _build/latex/;
make ;
bibtex   SNA-MC2013_travleev_paper;
pdflatex SNA-MC2013_travleev_paper;
pdflatex SNA-MC2013_travleev_paper;
evince SNA-MC2013_travleev_paper.pdf &
wait

cp SNA-MC2013_travleev_paper.pdf ~/work/kithome/.


