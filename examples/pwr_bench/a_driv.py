from a_mcnp import MI
from a_scf import si as SI

print 'Initial models'
print MI.gm.str_tree(['id()', 'name'])
print SI.gm.str_tree(['id()', 'name'])


sres = SI.run('R')
print 'result of the 1-st SCF run:'
print sres.str_tree(['id()', 'name'])


MI.gm = sres
MI.run('r')
print 'MI.gm after the first MCNP run'
print MI.gm.str_tree(['id()', 'name'])


sres = SI.run('R')
print 'result of the 2-nd SCF run'
print sres.str_tree(['id()', 'name'])



MI.gm = sres
MI.run('r')
print 'MI.gm after the 3-rd run'
print MI.gm.str_tree(['id()', 'name'])

