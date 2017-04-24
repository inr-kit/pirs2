from hpmc import Box, Cylinder

b = Box(X=1.2, Y=1.2, Z=110)
c = Cylinder(R=0.5, Z=100)
g = Cylinder(R=0.4, Z=100)
f = Cylinder(R=0.3, Z=100)
b.insert(0, c)
c.insert(1, g)
g.insert(2, f)


b.material = 'water'
c.material = 'steel'
f.material = 'fuel'

b.dens.set_grid([1, 1])
b.dens.set_values(1.)

c.temp.set_grid([1]*3)
c.temp.set_values([300, 500, 350])

f.heat.set_grid([1]*10)
f.heat.set_values(1.)


