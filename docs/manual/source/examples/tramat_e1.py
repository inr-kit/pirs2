from pirs.core.tramat import Nuclide

n1 = Nuclide((2, 4, 0)) # tuple (Z, A, I)
n2 = Nuclide('He-4')    # string
n3 = Nuclide('Ag-110m') # string for isomer
n4 = Nuclide(2004)      # ZAID integer
n5 = Nuclide(n4)        # copy of n4.

for n in [n1, n2, n3, n4, n5]:
    print repr(n), n.name, n.ZAID, n.M()

