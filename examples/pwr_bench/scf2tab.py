"""
Reads scf output and generates table for benchmark.

The reason -- to get fuel temperatures as specified by SCF, not average used in MCNP.
"""
import sys
from pirs.scf2.output import read_pl_rod, read_output

CK = 273.15

for n in sys.argv[1:]:
    res = open(n + '.dat', 'w')

    orods, channels = read_output(n + '/output.txt')
    prods = list(read_pl_rod(n + '/pl_rod_+0.000E+00.txt'))

    for i in range(51):
        for j in range(51):
            Nr = i + j*51
            orod = orods[Nr]
            Nrr, prod = prods[Nr]

            Tfac = orod.column('tfuave')

            for k in range(20):
                t = prod[k]

                print>>res, '{0:5d}{1:5d}{2:5d}'.format(i, j, k),
                Tfa = Tfac[k] + CK # Tf average by SCF
                Tfi = t[4] + CK # surface fuel temperature
                Tfc = t[5] + CK # centerline fuel temperature

                Tfb = 0.3*Tfc + 0.7*Tfi # Tf average by Rowand

                Tcl = t[1] + CK # coolant temperature
                Rcl = t[6] *1e-3 # coolant density

                for v in [Tfb, Tcl, Rcl]:
                    print>>res, '{0:17.12f}'.format(v),
                if k == 0:
                    print>>res, '# ', Nr, Nrr, orod.number
                else:
                    print>>res


