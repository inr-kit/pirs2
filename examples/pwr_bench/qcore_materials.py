from pirs.core.tramat import zai, Nuclide
from pirs.mcnp import Material

# list of nuclides to be taken into account
mcb_zaid = [
            # IFBA and WABA nuclides
            5010,
            5011,
            40000,
            6000,
            8016,
            13000,
            # fuel nuclides
            92234,
            92235,
            92236,
            92238,
            93237,
            94238,
            94239,
            94240,
            94241,
            94242,
            95241,
            95242,
            95243,
            96242,
            96243,
            96244,
            96245,
            42095,
            43099,
            44101,
            44103,
            47109,
            54135,
            55133,
            60143,
            60145,
            62147,
            62149,
            62150,
            62151,
            62152,
            63153,
            64155,
             8016]
mcb_zaid = [ # list of nuclides to exclude 
            51127,
            36095,
           ]
mcb_zai = map(zai, mcb_zaid)

# read files with number densities and compose materials
brnp = {}
mtrl = {}
labels = [ 'u42',
           'u45',
           'u42_ifba',
           'u45_ifba',
           'm40_25',
           'm40_30',
           'm40_45',
           'm43_25',
           'm43_30',
           'm43_50',
           'm40_waba',
           'm43_waba']

for label in labels:
    ff = 'mox_benchmark_data/nd_' + label + '.csv'
    # print 'reading ', ff 
    N = 0
    for l in open(ff, 'r'):
        row = l.split()
        if row[0] == 'Isotope':
            mtrl[(label, 'burnup')] = map(float, row[1:])
            for Nb in range(len(row)-1):
                mtrl[(label, Nb)] = []

        else:
            n = Nuclide(row[0])
            if n.ZAID not in mcb_zaid:
            # print row[0], n.ZAID
            # rz, ra, ri = zai(row[0])
            # if (rz, ra, ri) in mcb_zai:
                for Nb, nd in enumerate(map(float, row[1:])):
                    if nd > 0:
                        mtrl[(label, Nb)].append((n, nd))
                N += 1


    # print 'read {} nuclides'.format(N)

    

# construct materials:
mats = {}
fs = '{:>6d}.{}    {:21.15e}'
for ((label, b), recipe) in mtrl.items():
    # print label, b, len(recipe)
    if b != 'burnup':
        m = Material(*recipe)
        m.conc = m.moles().v * 1e24
        m.normalize(1)
        m.isotope_format_string = fs
        key = '{0}_{1}'.format(label, b)
        mats[key] = m
        m.name = key
        # substitute 40000 with natural composition of Zr:
        if 'ifba' in m.name:
            # m.sdict[40000] = Material('Zr')
            m.sdict[40000] = Material('Zr')
            print 'substitution rule for', m.name, m.sdict

        # substitutions for metastable isotopes:
        m.sdict[61548] = 61198
        m.sdict[47510] = 47160
        m.sdict[52527] = 52177
        m.sdict[52529] = 52179
        m.sdict[51000] = Material('Sb')

if __name__ == '__main__':
    dd = {}
    for key in sorted(mats.keys()):
        m = mats[key]
        for t in [580, 600]:
            m.T = t
            print m.card(suffixes=True).format('$ ' + key)
        ah = m.how_much(1, Z=[92,93,94,95])
        af = m.how_much(1, ZAID=[92235, 94239, 94241])
        if ah.v and af.v:
            dd[af/ah] = (key, m)
        print '-'*30

    for f in sorted(dd.keys()):
        key, m = dd[f]
        print f, key



