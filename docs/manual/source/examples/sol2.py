from pirs.solids import Box, Cylinder
from pirs.tools.plots import colormap

# pin model
pin = Cylinder(R=0.45, Z=100, material='clad')
pin.insert(Cylinder(R=0.4, Z=pin.Z-5, material='fuel'))

# assembly box
a = Box(X=5, Y=7, Z=pin.Z+10, material='water')
a.grid.x = 1
a.grid.y = 1.1
a.grid.z = a.Z

# insert pins
for i in range(5):
    for j in range(6):
        a.grid.insert((i,j,0), pin.copy_tree())

# center grid with respect to solid
a.grid.center()

colormap(a, filename='sol2z.png')
colormap(a, plane={'x':0}, filename='sol2x.png', aspect='auto')




