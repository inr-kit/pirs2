from pirs.solids import Box, Cylinder

b = Box(X=3, Y=3)

c = Cylinder(R=0.4)

b.grid.x = 1
b.grid.y = 1

for i in [0, 1]:
    for j in [0, 1]:
        cc = c.copy_tree()
        b.grid.insert((i, j, 0), cc)
        cc.material = 'm{}{}'.format(i,j)

from pirs.tools.plots import colormap
colormap(b, filename='ex3_1.pdf')

b.grid.center()
colormap(b, filename='ex3_2.pdf')

