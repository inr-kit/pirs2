from pirs.mcnp import Material
# depleted u, mass fractions
ud = Material((92235,  0.2, 2),
              (92238, 99.8, 2))
# simplified o for oxide
o = Material(8016)
# pu  
pu = Material((94239, 93.6, 2),
              (94240,  5.9, 2),
              (94241,  0.4, 2),
              (94242,  0.1, 2))
# oxides and mox
ux = Material((ud, 1), (o, 2))
px = Material((pu, 1), (o, 2))
mox = Material((ux, 0.5), (px, 0.5))
print mox.report()
# objective function
def obj(mix):
    a1 = mix.how_much(2, ZAID=[92235, 94239, 94241, 94243])
    a2 = mix.how_much(2, Z=[92, 94])
    return a1/a2 - 0.025
mox.tune(obj, [ux, px]) 
print mox.report()
