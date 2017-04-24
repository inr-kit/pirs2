"""
Compute Keff as function of coolant density.
"""
from a_model import a as model
from a_mcnp import MI

m1 = model
m2 = model.copy_tree()

MI.kcode.Nh = 100000
MI.kcode.Nct = 1000
MI.kcode.Ncs = 100

for d in [0.6, 0.7, 0.8]:
    m = model.copy_tree()
    for e in m.values(True):
        if e.material == 'bwater':
            e.dens.set_values(d)
    MI.gm = m
    MI.run('r')


