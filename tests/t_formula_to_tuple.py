import logging, sys
from autologging import TRACE
logging.basicConfig(level=TRACE, stream=sys.stdout, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')

from pirs.core.tramat.natural import formula_to_tuple

for f in 'H Al Al2O3 C2H5OH'.split():
    t = formula_to_tuple(f)
    print repr(f) 
    try:
        for tt in t:
            print '    ', repr(tt)
    except TypeError:
        print '    ', repr(t)


