
# EXpy=ex1.py ex2.py tramat_e1.py tramat_e2.py tramat_e3.py mcnp.mat_e1.py mcnp.mat_e2.py mcnp.sur1.py mcnp.vol1.py mcnp.vol2.py mcnp.cell1.py trageom.py sched_wp1.py sched_if1.py sol1.py sol2.py sol3.py
EXpy=$(wildcard *.py)
EXout=$(EXpy:.py=.out)

all: $(EXout)

%.out: %.py
	python $< > $@

.PHONY: clean

clean: 
	-rm *.out *.png 
	-rm -rf wp?
