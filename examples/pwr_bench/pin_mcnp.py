from pirs import McnpInterface
import pirs.mcnp as mcnp

# 1

# material compositions
water = mcnp.Material((1001, 2), (8016, 1))
water.thermal = 'lw'
water.name = 'Water'
bc = 1.20e-3 #: specs in benchmark

# boron = mcnp.Material((5010, 0.2, 2), (5011, 0.8, 2)) # actually, B-10 content is 19.9 %, number fraction
boron = mcnp.Material('B')
bwater = mcnp.Material((water, 1-bc, 2), 
                      (boron, bc, 2))
bwater.thermal = 'lw'
bwater.name = 'Coolant with {0} wt.% of nat.boron'.format(bc*100)


# 2

zirc = mcnp.Material(('Zr', 98.23), 
                     ('Sn', 1.50),
                     ('Fe', 0.12), 
                     ('Cr', 0.10),
                     ('N',  0.05)) # zircaloy-2, Table 5, p.7
zirc.name = 'Zircaloy'

# 3

u = mcnp.Material((92235,  4.2, 2),
                  (92238, 95.8, 2)) # mass fractions

ud = mcnp.Material((92235,  0.2, 2), # depleted uranium
                   (92238, 99.8, 2)) # mass fractions

o = mcnp.Material(8016)
# uo2 = 1*u + 2*o # 1*u (one mole of u) is not equal to u (that is defined above as 4.2 g and 95.8 g)!
uo2 = mcnp.Material((u, 1), (o, 2))
uo2.name = 'UOX'

# mox material:
pu = mcnp.Material((94239, 93.6, 2),
                   (94240,  5.9, 2),
                   (94241,  0.4, 2),
                   (94242,  0.1, 2))

# there are 3 mox materials differing by Pu-fissile fraction.
ux = mcnp.Material((ud, 1), (o, 2))
px = mcnp.Material((pu, 1), (o, 2))
moxlist = []
moxfrac = [] # fraction of Pu
for f in [2.5, 3.0, 4.5]:
    # mox = mcnp.Material((pu, 0.5), (ud, 0.5), (o, 2))
    mox = mcnp.Material((ux, 0.5), (px, 0.5))
    mox.name = 'MOX with {0} of fissile Pu'.format(f)
    def objective(mix, target=f*0.01):
        a1 = mix.how_much(2, ZAID=[94239, 94241, 94243])
        a2   = mix.how_much(2, Z=[92,94])
        return a1/a2 - target
    mox.tune(objective, [ux, px])
    moxlist.append(mox)

    # compute Pu fraction in MOX:
    a1 = mox.how_much(2, Z=[92])
    a2 = mox.how_much(2, Z=[94])
    moxfrac.append(a2/(a2+a1))

ifba = mcnp.Material(('Zr', 1), (boron, 2))
ifba.name = 'IFBA'

al2o3 = mcnp.Material(('Al', 2), (o, 3))
b4c = mcnp.Material((boron, 4), (6000, 1)) 
waba = mcnp.Material((al2o3, 90, 2), (b4c, 10, 2))
waba.name = 'WABA'


# 4

# substitution rules for isotopes not in xsdir:
water.sdict[8018] = 8016
bwater.sdict[8018] = 8016
uo2.sdict[8018] = 8016
o.sdict[8018] = 8016

swater = bwater.copy()
swater.name = 'Stagnant coolant'

# 5

# MCNP interface
MI = McnpInterface()

# correspondence of the material names and material compositions:
MI.materials['water'] = water
MI.materials['bwater'] = bwater # borated water
MI.materials['swater'] = swater # stagnant water
MI.materials['zirc'] = zirc
MI.materials['uo2'] = uo2
# MI.materials['mox'] = mox
MI.materials['mox1'] = moxlist[0]
MI.materials['mox2'] = moxlist[1]
MI.materials['mox3'] = moxlist[2]
MI.materials['oxygen'] = o
MI.materials['ifba'] = ifba
MI.materials['waba'] = waba

# reflective bc on the lateral facets:
MI.bc['radial'] = '*'

# kcode parameters:
MI.kcode.Nh = 2000     # histories per cycle
MI.kcode.Ncs = 10      # inactive cycles
MI.kcode.Nct =  50     # total cycles
MI.kcode.active = True
# additional data card to specify kcode source for the first run only:
MI.adc.append('ksrc  0 0 -150  0 0 0  0 0 150') 

# 6

# Save MCNP results using uncertainties package:
MI.tallyCollection.use_uncertainties = True

if __name__ == '__main__':
    fs = '{0:>6d}{1}    {2:20.14e}'

    uo2.dens = 10.21
    zirc.dens = 6.504
    water.dens = 1.0
    bwater.dens = 1.0
    waba.dens = 3.5635
    ifba.dens = 1.69
    for mox in moxlist:
        mox.dens = 10.41

    for m in [zirc, water, bwater, ifba, waba, uo2] + moxlist:
        m = m.expanded()
        m.remove_duplicates()
        m.normalize(1)
        m.isotope_format_string = fs

        print 'c'
        print m.card(suffixes=False).replace('{0:<}', '##')

    # report weight fractions of boron:
    print boron.report()
