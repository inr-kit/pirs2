from pirs.core.tramat.mixer import Mixture, Amount, Nuclide

m = Mixture(1001)

assert m.how_much(1) == m.amount(1)
assert m.how_much(2) == m.amount(2)

m = Mixture(
        1001, (1, 1),
        1002, (1, 1),
        1003, (1, 1))

assert m.how_much(1) == Amount(3, 1)
assert m.how_much(1, 1001) == Amount(1, 1)

i1 = Mixture(1001)
i2 = Mixture(1002)
i3 = Mixture(1003)
i1.dens = 1.0
i2.dens = 2.0
i3.dens = 3.0

m = Mixture(
        i1, (1, 3),
        i2, (1, 3),
        i3, (1, 3))

assert m.how_much(3, i1) == Amount(1, 3)
assert m.how_much(3) == Amount(3, 3)
assert m.how_much(3, i2, i3) == Amount(2, 3)


