# see http://stackoverflow.com/questions/12343428/latex-reference-and-makefile

.DELETE_ON_ERROR:

.PHONY: examples

command = pdflatex -shell-escape
maintex = $(wildcard main*.tex)

main.pdf: scheme_wrapper.pdf $(maintex) examples
	$(command) main 
	while grep 'Rerun to get ' main.log; do $(command) main ; done

scheme_wrapper.pdf: scheme.tex scheme_wrapper.tex
	$(command) scheme_wrapper 
	while grep 'Rerun to get ' scheme_wrapper.log; do $(command) scheme_wrapper ; done

examples:
	$(MAKE) -C examples

clean:
	-rm *.aux
	-rm *.log
	-rm *.nav
	-rm *.out
	-rm *.pdf
	-rm *.snm
	-rm *.toc
	-rm *.vrb
	-rm *.pyg

clean-examples:
	$(MAKE) -C examples clean
