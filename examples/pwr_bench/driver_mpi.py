# import section
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sys import argv
import gc
from datetime import datetime
import time
import argparse
from myplatform import node

from pirs.tools import dump, load

# filenames
dump_suffix = 'iteration_{0:03d}.dump'


# process command line argument
parser = argparse.ArgumentParser('Driver for coupled calculations.')
parser.add_argument('key', help='Prefix (new run) or existing dump file (continue run).')
parser.add_argument('--Nh', help='Number of histories in 1-st iteration of a new run.', type=int, dest='Nh', default=None)
parser.add_argument('--Nz', help='Number of axial layers for a new run.', type=int, dest='Nz', default=None)
parser.add_argument('--dTf', help='Discretization for Tfuel, K', type=float, dest='dTf', default=None)
parser.add_argument('--dTc', help='Discretization for Tcool, K', type=float, dest='dTc', default=None)
parser.add_argument('--uxsdir', help='Update xsdir for continue run.', dest='uxsdir', action='store_true')
args = parser.parse_args()
print args


if '.dump' in args.key:
    # args.key is the dump file. Read it and continue calculations.
    print 'loading data from {0}'.format(args.key)
    dmp = load(args.key)
    Ic = dmp['Ic']
    s1 = dmp['s1']
    Ss = dmp['Ss']
    MI = dmp['MI']
    SI = dmp['SI']
    Keff = dmp['Keff']
    Kerr = dmp['Kerr']
    Krel = dmp['Krel']
    dTf = dmp['dTf']
    dTc = dmp['dTc']
    # prefix = dmp['prefix']
    prefix = args.key[0:-len(dump_suffix.format(0))]
    SI.wp.prefix = prefix + 'scf_'
    MI.wp.prefix = prefix + 'mcnp_'

    if args.uxsdir:
        from pirs.mcnp.xsdir import XSDIRFILE
        MI.xsdir.read(XSDIRFILE)

else:
    # first argument is not a dump file. Then, it is just string that defines the case name.
    prefix = args.key + '_' 
    if prefix[0] in 'pqr':
        exit()
        from pin_model import model
        from pin_scf import SI
        from pin_mcnp import MI
    elif prefix[0] in 'abcde':
        # import description of the assembly
        from a_model import a as model
        from a_mcnp import MI
        from a_scf import si as SI
    elif prefix[0] in 'mno':
        exit()
        # import description of the minicore
        from minicore_model import minicore as model
        from minicore_scf import SI
        from minicore_mcnp import MI

    SI.wp.prefix = prefix + 'scf_'
    MI.wp.prefix = prefix + 'mcnp_'

    # command line parameters only for the initial start
    if args.Nh is not None: MI.kcode.Nh = args.Nh
    if args.Nz is not None: Nz = args.Nz


    s1 = MI.kcode.Nct * MI.kcode.Nh # total number of histories in iteration.
    Ss = 0 # cumulative number of neutron histories
    Ic = 0 # iteration counter

    # store MCNP input for initial state:
    MI.gm = model
    MI.run('r')

    # SCF run to get initial temperature distribution
    SI.gm = model
    for e in SI.gm.values():
        if e.name == 'fuel':
            e.heat.clear()
            e.heat.set_grid([1.]*Nz)
            e.heat.set_values(1.0)
    SI.run('R')

    dump(prefix + 'init.dump', SI=SI)

    # 'initial' values for Keff and std.dev.  To simplify comparison 
    # to "previous" at the first iteration.
    Keff = [1.]
    Kerr = [1.]
    Krel = [0.] # for relaxed Keff

    dTf = 10.
    dTc = 1.0


if 'ic2' in node:
    Ntasks = 16
    if 'mpirun' not in MI.wp.exe:
        MI.wp.exe = 'mpirun ' + MI.wp.exe
elif 'hc3' in node:
    Ntasks = 8
    if 'mpirun' not in MI.wp.exe:
        MI.wp.exe = 'mpirun ' + MI.wp.exe
elif 'inr' in node:
    Ntasks = 4

# command line parameters for start and continuation:
if args.dTf is not None: dTf = args.dTf
if args.dTc is not None: dTc = args.dTc

print MI.wp.prefix, args.key, prefix
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
        dump(prefix + dump_suffix.format(Ic),
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



