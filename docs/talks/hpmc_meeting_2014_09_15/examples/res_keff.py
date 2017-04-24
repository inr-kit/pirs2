from pirs.tools import load
from pirs.tools.plots import MeshPlotter

dmp = load('results/b_iteration_058.dump')

kkk = MeshPlotter()
kkk.figsize=(8,4)
kkk.add_line(0, 0, (), 'temp',  0, fmt='.k', label='$k_{eff}$')
kkk.xlabel[0] = 'Iteration index'
kkk.ylabel[0] = '$k_{eff}$'

Keff = dmp['Keff'][2:]
Kerr = dmp['Kerr'][2:]
fig = kkk.figure([range(1, len(Keff)+1), Keff, Kerr])
fig.savefig('res_keff.pdf')
