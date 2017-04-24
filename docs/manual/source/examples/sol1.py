from pirs.solids import Box, Cylinder
from pirs.tools.plots import colormap

b = Box()
b.X = 3
b.Y = 4
b.Z = 5
b.material = 'm1'

c1 = Cylinder()
c1.R = 1
c1.Z = 4
c1.material = 'm2'

b.insert(c1)

c2 = c1.copy_tree()
c2.material = 'm3'
c2.R = 0.8 
c2.pos.x = 0.8
c2.pos.y = 0.6

b.insert(c2)


colormap(b, filename='sol1z.png')
colormap(b, plane={'x':0}, filename='sol1x.png')

