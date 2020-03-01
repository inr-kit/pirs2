import logging, sys
from autologging import TRACE
logging.basicConfig(level=TRACE, stream=sys.stdout, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')


from pirs.mcnp import Material



# Check constructors
m = Material(1001)         # from int ZAID
m = Material('Al')         # Element name
m = Material('U3Si2')      # Chemical formula
m2 = Material(m)           # bypass single Material argument
assert m is m2

m = Material(1001, 1, 1002, 1)  # Amounts as integers
