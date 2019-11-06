# A script to test the pirs.core.tramat.Mixer with autologging

import logging, sys
from autologging import TRACE
logging.basicConfig(level=TRACE, stream=sys.stdout, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')

from pirs.core.tramat import Mixture, Nuclide

m1 = Mixture(92235, (1, 1), 92238, (1, 1))
m1.name = 'Umix'
print 'm1 created'

print m1.report()

m2 = Mixture('Al')
print m2.report()

