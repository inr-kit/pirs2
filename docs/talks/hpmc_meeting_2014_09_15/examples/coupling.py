from pirs.tools import dump
from hscf3 import si
from hmcnp5 import mi

mi.wp.prefix = 'cm_'
si.wp.prefix = 'cs_'

I = 0
while I < 5:
    # mcnp run
    mi.gm = si.gm.copy_tree()
    mr = mi.run('R', tasks=3)
    # relaxed power
    for (em, es) in zip(mr.heats(), si.gm.heats()):
        h = 0.5 *em.heat + 0.5 * es.heat
        es.heat.update(h)
    # scf run
    si.run('R')
    # store results
    dump('{}_coupling.dump'.format(I), 
         Keff = mi.keff(),
         mr = mr,
         sr = si.gm,
         I = I)

    I += 1

    dtmax = 0
    dtpos = None
    for (em, es) in zip(mr.heats(), si.gm.heats()):
        dt = em.temp - es.temp
        for v in dt.values():
            v = abs(v)
            if dtmax < v:
                dtmax = v
                dtpos = em.abspos()
    print 'Iteration {}, Keff={}'.format(I, mi.keff())
    print 'dTmax {} at {}'.format(dtmax, dtpos)



