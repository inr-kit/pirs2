from tramat import Mixture

print 'nMix', Mixture.nMix

m = Mixture(92235)
m2 = Mixture(m)
m3 = Mixture(m, 1, 1001, 2)

print 'nMix', Mixture.nMix

fe = Mixture('Fe')
h1 = Mixture(1001)


for f in ['C2H5OH', 'Al2O3', 'Fe2O3', 'C4B', 'HeHF', 'Fe', 'U']:
    print f
    mix = Mixture(f, names={'Fe':fe, 'H':h1})
    print mix.report()
    for n, c in mix.elements().items():
        print n, c


print 'nMix', Mixture.nMix



