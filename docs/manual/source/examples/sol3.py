from pirs.solids import Cylinder
from pirs.tools.plots import colormap

c = Cylinder(Z=2)

# heat
c.heat.set_grid([1, 2, 1])
c.heat.set_values([0.1, 0.2, 0.3])

# temperature
c.temp.set_grid([1]*20)
c.temp.set_values(lambda z: 300 + 100*z)

# density
c.dens.set_grid([1]*5)
c.dens.set_values(1.)

colormap(c, var='heat', plane={'x':0}, filename='sol3h.png')
colormap(c, var='temp', plane={'x':0}, filename='sol3t.png')
colormap(c, var='dens', plane={'x':0}, filename='sol3d.png')



