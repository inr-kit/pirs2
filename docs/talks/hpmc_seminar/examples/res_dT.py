from pirs.tools import load
from pirs.tools.plots import MeshPlotter


kTf = MeshPlotter()
kTf.figsize=(8,4)
kTf.add_line(0, 0, (), 'temp',  0, fmt='.k', label='$\Delta T_f^{max}$')
kTf.ylabel[0] = '$\Delta T_f^{max}$'

kal = MeshPlotter()
kal.figsize=(8,4)
kal.add_line(0, 0, (), 'temp',  0, fmt='.k', label=r'$\alpha$')
kal.ylabel[0] = r'$\alpha$'

dt = []
x = []
dh = []
dhr = []
herr = []
Ss = []
for i in range(1, 56):
    print 'processing dump ' , i
    dmp = load('results/b_iteration_{0:03d}.dump'.format(i))
    sr = dmp['scf_result']
    mr = dmp['mcnp_result']
    ss = dmp['Ss']
    Ss.append(ss)
    dtmax = -1
    dhmax = -1
    for (se, me) in zip(sr.heats(), mr.heats()):
        dtl = (se.temp - me.temp).values()
        dhl = (se.heat - me.heat).values()
        for d, v in zip(dtl, se.temp.values()):
            d = abs(d/v)
            if d > dtmax:
                dtmax = d
        for d, v in zip(dhl, se.heat.values()):
            h = abs(d.nominal_value / v.nominal_value)
            if h > dhmax:
                dhmax = h
                dhmar = d.std_dev /v.nominal_value
    herrmax = -1
    for me in mr.heats():
        for h in me.heat.values():
            re = h.std_dev / h.nominal_value
            if re > herrmax:
                herrmax = re
    x.append(i)
    dt.append(dtmax)

    dh.append(dhmax)
    dhr.append(dhmar)
    herr.append(herrmax)

kTf.figure([x, dt, [0]*len(dt)]).savefig('res_dTf.pdf')

alpha = []
ssp = 0
for ss in Ss:
    s = ss - ssp
    alpha.append(s/ss)
    ssp = s

print x, alpha

kal.figure([x, alpha, [0]*len(alrpha)]).savefig('res_alpha.pdf')
