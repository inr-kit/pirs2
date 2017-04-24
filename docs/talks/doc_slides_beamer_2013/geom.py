from hpmc import Box, Cylinder

b = Box(X=1.2, Y=1.2, Z=110)
c = Cylinder(R=0.5, Z=100)
b.insert(0, c)

b.material = 'water'
c.material = 'fuel'

b.dens.set_grid([1, 1])
b.dens.set_values(1.)

c.temp.set_grid([1]*3)
b.temp.set_values([300, 500, 350])

c.heat.set_grid([1]*10)


