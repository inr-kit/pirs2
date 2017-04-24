"""
Functions to prepare existing data sets for temerature interpolation of thermal
data by mixing.

The mixing of nuclides with different suffices cannot be used directly if
thermal data are applied, since the same s(a,b) data is used for all nuclides
with particular ZAIDS.

One needs to have two sets of cross-sections both for thermal and fast data to
mix temperature.

The following example does not work (in thermal region, only one temperature is used)::

    m1   1001.31c  0.5  1001.32c 0.5
    mt1  lwtr01.31t                  $ thermal data for 1001

The next example works, but requires cross-section files for "artificial" nuclide with ZAID
1004 (for example)::

    m1  1001.31c 0.5   1004.32c 0.5
    mt1     lwtr01.31t               $ thermal data for 1001, at temperature for 1001.31c
            lwt401.31t               $ thermal data for 1004, at temperature for 1004.32c

Thermal data on the mt card are specified without fractions. Thus, to simulate
the same temperature for fast and thermal data, one needs that the existing
fast and thermal cross-sections are prepared at the same temperatures.

Currently, this is NOT the case for the jeff31 data: thermal data for h in
water are prepared for 293, 323, 373, 423, 473, ..., K while the fast data are
for 300, 400, 500, ... K.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

def prepare(xsdir):
    return NotImplemented

