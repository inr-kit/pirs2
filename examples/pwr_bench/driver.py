# import section
from sys import argv
import gc
from datetime import datetime
import time
from myplatform import node

from pirs.tools import dump, load


# process command line argument
if '.dump' in argv[1]:
    # argv[1] is the dump file. Read it and continue calculations.
    print 'loading data from {0}'.format(argv[1])
    dmp = load(argv[1])
    Ic = dmp['Ic']
    s1 = dmp['s1']
    Ss = dmp['Ss']
    MI = dmp['MI']
    SI = dmp['SI']
    Keff = dmp['Keff']
    Kerr = dmp['Kerr']
    Krel = dmp['Krel']
    prefix = dmp['prefix']
    dTf = dmp['dTf']
    dTc = dmp['dTc']

else:
    # first argument is not a dump file. Then, it is just string that defines the case name.
    prefix = argv[1] + '_' 
    if argv[1][0] in 'pqr':
        exit()
        from pin_model import model
        from pin_scf import SI
        from pin_mcnp import MI
    elif argv[1][0] in 'abcde':
        # import description of the assembly
        from a_model import a as model
        from a_mcnp import MI
        from a_scf import si as SI
    elif argv[1][0] in 'mno':
        exit()
        # import description of the minicore
        from minicore_model import minicore as model
        from minicore_scf import SI
        from minicore_mcnp import MI

    SI.wp.prefix = prefix + 'scf_'
    MI.wp.prefix = prefix + 'mcnp_'

    # command line parameters only for the initial start
    if 'Nh' in argv:
        MI.kcode.Nh = int(argv[argv.index('Nh') + 1])
    Nz = 5
    if 'Nz' in argv:
        Nz = int(argv[argv.index('Nz') + 1])



    s1 = MI.kcode.Nct * MI.kcode.Nh # total number of histories in iteration.
    Ss = 0 # cumulative number of neutron histories
    Ic = 0 # iteration counter

    # SCF run to get initial temperature distribution
    SI.gm = model
    for e in SI.gm.values():
        if e.name == 'fuel':
            e.heat.clear()
            e.heat.set_grid([1.]*Nz)
            e.heat.set_values(1.0)
    SI.run('R')

    # 'initial' values for Keff and std.dev.  To simplify comparison 
    # to "previous" at the first iteration.
    Keff = [1.]
    Kerr = [1.]
    Krel = [0.] # for relaxed Keff

    dTf = 10.
    dTc = 1.0


if 'ic2' in node:
    Ntasks = 32
elif 'hc3' in node:
    Ntasks = 16
elif 'inr' in node:
    Ntasks = 3

# command line parameters for start and continuation:
if 'dTf' in argv:
    dTf = int(argv[argv.index('dTf') + 1])
if 'dTc' in argv:
    dTc = int(argv[argv.index('dTc') + 1])

# iterations
while True:

        if MI.wp.srctp.defined and 'ksrc' in MI.adc[-1]:
            # remove iksrc. Previous srctp will be used.
            MI.adc.pop()

        Ic += 1

        print
        print '----- Iteration {0} --- {1}'.format(Ic, datetime.now().strftime('%H:%M:%S'))

        # 4

        # ----------------------------------------------------------------------
        # MC-RUN
        # ----------------------------------------------------------------------
        # Compute new number of cycles
        s = 0.5*(s1 + (s1**2 + 4.*s1*Ss)**0.5)
        MI.kcode.Nh = int(s / MI.kcode.Nct)

        MI.gm = SI.gm.copy_tree()  

        # set Delta T for temperature representation.
        for e in MI.gm.temps():
            if   e.name == 'fuel': e.temp.prec = dTf
            elif e.name == -1:     e.temp.prec = dTc

        MI.run('R', tasks=Ntasks)

        # get Keff of last MCNP run and append it to Keff list:
        keff, err = MI.keff()
        Keff.append(keff)
        Kerr.append(err)

        # Do not propagate uncertainties to SCF 
        if MI.tallyCollection.use_uncertainties:
            nomvals = MI.gm.copy_tree()
            for e in nomvals.heats():
                e.heat.convert(lambda v: v.nominal_value)
        else:
            nomvals = MI.gm

        # ----------------------------------------------------------------------
        # Relaxation 
        # ----------------------------------------------------------------------
        Ss += s
        a = float(s)/float(Ss) # convert to float, otherwise s/Ss is allways zero.
        # relaxed heat for SCF
        for (se, me) in zip(SI.gm.heats(), nomvals.heats()):
            h = a*me.heat + (1.-a)*se.heat
            se.heat.update(h)
        # relaxed Keff:
        krel = a*keff + (1.-a)*Krel[-1]
        Krel.append(krel)

        # ----------------------------------------------------------------------
        # TH-RUN
        # ----------------------------------------------------------------------
        SI.run('R')


        # ----------------------------------------------------------------------
        # dump iteration results
        # ----------------------------------------------------------------------
        MI.clear()
        MI.wp.inp.string = ''
        SI.clear()
        SI.wp.input.string = ''
        dump(prefix + 'iteration_{0:03d}.dump'.format(Ic),
                dTf = dTf,
                dTc = dTc,
                Ic = Ic,
                s1 = s1,
                Ss = Ss,
                a = a,
                MI = MI,
                SI = SI,
                Keff = Keff,
                Kerr = Kerr,
                Krel = Krel,
                prefix = prefix
                )


        gc.collect()




