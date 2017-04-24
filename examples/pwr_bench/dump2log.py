import sys
from datetime import datetime
from pirs.tools import load
from pirs.solids.functions import max_diff, max_err

Nht = 0 #: total number of histories (active) 

ff = lambda e: e.name == 'fuel'
fc = lambda e: e.name == -1

tprev = None
sprev = None
if __name__ == '__main__':
    print '{0:>3s} {1:>9s} {2:>17s} {3:>9s} {4:>7s} {5:>10s}'.format('I', 'Alpha', 'Keff', 'dHmax', 'Nh', 'Ntot'),
    print '{0:12s}'.format('Krlx'),
    print '{0:36s}'.format('relaxed_heat'),
    print '{0:36s}'.format('relaxed_Tf'),
    print '{0:36s}'.format('relaxed_Tc'),
    print '{0:36s}'.format('relaxed_Rho_c')

    first_dump = True
    for dfile in sys.argv[1:]:
        dmp = load(dfile)
        SI = dmp['SI']
        MI = dmp['MI']
        Keff = dmp['Keff']
        Kerr = dmp['Kerr']
        Krel = dmp['Krel']
        tstamp = dmp['_timestamp']
        a = dmp['a']

        t = datetime.strptime(tstamp, '%Y-%m-%d %H:%M:%S')


        s_m = SI.gm
        m_m = MI.gm
        if first_dump:
            f1k = None
            c1k = None
            for e in s_m.values():
                if f1k is None and e.name == 'fuel':
                    f1k = e.get_key()
                if c1k is None and e.name == -1:
                    c1k = e.get_key()
                if f1k and c1k:
                    break
            izmid = len(s_m.get_child(f1k).heat.get_grid())/2

            first_dump = False
            s_p = s_m    # SI.gm of the previous iteration.

        # parameters of the MCNP run:
        heat, herr, hkey, hxyz = max_err(m_m, 'heat', filter_=ff)
        print '{0:4s} {1:9.6f}'.format(dfile[-8:-5], a), 
        print '{0:7.5f}+-{1:7.5f}'.format(Keff[-1], Kerr[-1]),
        print '{0:8.4f}%'.format(herr*100), 
        Nht += MI.kcode.Nh * (MI.kcode.Nct - MI.kcode.Ncs)
        print '{0:7d} {1:10d}'.format(MI.kcode.Nh, Nht),

        f1 = s_m.get_child(f1k)
        c1 = s_m.get_child(c1k)

        f1.temp.prec = 0
        c1.temp.prec = 0

        ftemp = f1.temp.values()
        fheat = f1.heat.values()
        Iheat = f1.heat.integral(cs='abs')

        ctemp = c1.temp.values()
        cdens = c1.dens.values()

        # relaxed values for Keff:
        print '|{0:8.5f}'.format(Krel[-1]),
        print '|{0:12.4e}'.format(Iheat),

        # Tf convergence: Max diff between iterations
        if not first_dump:
            t1, t2, dt, key, iz = max_diff(s_m, s_p, 'temp', norm=abs, filter_=ff)
            print '|{} {}-{}, key {} iz {}|'.format(t1-t2, t1, t2, key, iz)

        # relaxed temp, temp, dens:
        for var in [fheat, ftemp, ctemp, cdens]:
            print '  |',
            for i in [0, izmid, -1]:
                print ' {0:9.3e}'.format(var[i]),


        print tstamp,

        if tprev is not None:
            dt = t - tprev
            s = dt.microseconds/1e6 + dt.seconds + dt.days*24*3600
            N = MI.kcode.Nh
            print '{0:9.1f}'.format(s),
            if sprev is not None:
                tau = (s - sprev) / (N - Nprev)
                t0 = (s + sprev - tau*(N + Nprev))/2.
                print tau, t0,
            sprev = s
            Nprev = N
            tprev = t
        print
        tprev = t
        s_p = s_m



