from sys import argv

from pirs.tools import Plotter
from pirs.tools import load

from pin_model import fuel_key

# Setup plotting 
ppp = Plotter()
ppp.figsize=(8, 16)
# MCNP results
ppp.add_line(0, 0, fuel_key, 'heat',  0, fmt='.y', label='$p_{__i}$')
# Relaxed heat
ppp.add_line(0, 1, fuel_key, 'heat', -3, fmt='.k', label='$P_{__i}$')
# TH result of fuel temp
ppp.add_line(1, 1, fuel_key, 'temp', -3, fmt='.k', label='$T_{f,__i}$')
# TH result for water temp
ppp.add_line(2, 1, ('scf_c0'), 'temp', -3, fmt='.k', label='$T_{w,__i}$')
# TH result for water density
ppp.add_line(3, 1, ('scf_c0'), 'dens', -3, fmt='.k', label=r'$\rho_{w,__i}$')
ppp.ylim[0] = (0, 1)
ppp.ylabel[0] = 'relative heat'
ppp.ylabel[1] = 'fuel temperature, K'
ppp.ylabel[2] = 'water temperature, K'
ppp.ylabel[3] = 'water density, g/cm3'
ppp.xlabel[3] = 'z coordinate, cm'

for f in argv[1:]:
    print 'printing from ', f
    d = load(f)
    Ic = d['Ic']
    kcode = d['kcode']
    sres = d['scf_result']
    mres = d['mcnp_result']
    Rm = d['relaxed']

    fig = ppp.figure(mres, sres)
    fig.suptitle('Iteration {0} kcode {1} {2} {3}'.format(Ic, kcode.Nh, kcode.Ncs, kcode.Nct))
    fig.savefig(f + '.pdf')

# Take Keff from the last dump and plot:
Keff = d['Keff'][2:]
Kerr = d['Kerr'][2:]
import matplotlib.pyplot as plt
a = plt.figure(figsize=(8, 16)).add_subplot(111)
a.errorbar(range(1, len(Keff)+1), Keff, Kerr, fmt='o')
a.get_figure().savefig(f + 'keff.pdf')


