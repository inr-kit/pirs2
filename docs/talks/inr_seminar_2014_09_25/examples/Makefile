
EXpy=$(wildcard ex*.py)
EXout=$(EXpy:.py=.out)

all: $(EXout)

%.out: %.py
	python $< > $@

.PHONY: clean

clean: 
	-rm *.out *.png *.pdf 
	-rm -rf mcnp?
