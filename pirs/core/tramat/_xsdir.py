#!/bin/env python.my
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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

