from pirs.mcnp import Material

u = Material((92235,  4, 2), (92238, 96, 2))
p = Material((94239, 90, 2), (94240, 10, 2))
o = Material(8016)

uox = u + 2*o
pox = p + 2*o

mox = Material((uox, 1), (pox, 1))
print mox.report()

def of(m):
    a1 = m.how_much(1, ZAID=[92235, 94239])
    a2 = m.how_much(1, Z=[92, 94])
    return a1 / a2 - 0.10

mox.tune(of, [uox, pox])
print mox.report()
print mox.how_much(1, ZAID=[92235, 94239])
print mox.how_much(1, Z=[92, 94])
