from pirs.mcnp import Material, Surface, Cell, Model

c1 = Cell()

# Cell 1 
c1.mat = Material('Fe')
c1.rho = -10.
c1.vol = Surface('so 8.0').volume()
c1.opt['imp:n'] = 1

# Cell 2
c2 = Cell()
c2.vol = -c1.vol

# direct use of cells
print c1.card()
print c2.card()

# cells in a model
m = Model()
m.cells.append(c1)
m.cells.append(c2)

for c in m.cards():
    print c

