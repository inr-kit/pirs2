#!/bin/env python
"""
Script provides a command line interface to the TSP python package.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from sys import argv
from os import path
from tsp import pre_pro

def main():
    msg = """
(P)ython (P)re(P)rocessor: script from the tsp Python package. Abbreviation
"tsp" means (T)ext with (S)nippets (P)reprocessor.

Usage:

> {} template [snippet]

where `template' is a text file containing python snippets.  Snippets are
evaluated/executed and the snippet code is replaced with the result of
evaluation/execution. The resulting file is saved to `template.res'.

When optional `snippet` is given, it is evaluated or executed before the
snippets in `template`.
""".format(path.basename(argv[0]))

    if len(argv) < 2 or not path.exists(argv[1]):
        print msg
    else:
        if len(argv) == 3:
            preamb = argv[2]
        else:
            preamb = None
        pre_pro(fname=argv[1], level='main', preamb = preamb)

if __name__ == '__main__':
    main()
