#!/bin/env python.my

"""
The script generates python representation of awr masses from xsdir. The awr
values are read from xsdir and printed out in the form of python dictionary.

This script relies on the py4mcnp package, which is not part of tramat.

End-users of tramat do not need this script, since the masses from xsdir are
already in the data_masses.py module
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import os
from py4mcnp.files import xsdir

xf = xsdir('xsdir')
print 'awr = {'
klist = xf.awr.keys()
klist.sort()
for k in klist:
    print '   {0:6d} : {1:11.6f},'.format(k, xf.awr[k])
print '      }'
print

