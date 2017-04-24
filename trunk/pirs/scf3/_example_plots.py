from pirs.tools.plots.plot_shapely import ShapelyToAxis
from shapely.geometry import Point
from shapely.affinity import rotate

p1 = Point((0, 0))
p2 = Point((1, 1))

ax = ShapelyToAxis(p1, axis=None, color='red', label='p1', pointsize=30)
ShapelyToAxis(p2, axis=ax, color='green', pointsize=20)
ax.get_figure().savefig('example_plot1.pdf')

l1 = Point((0.5, 0.5)).buffer(1.1, resolution=2).boundary
l2 = Point((0.5, 0.7)).buffer(1.1, resolution=2).boundary

ShapelyToAxis(l1, axis=ax, color='blue', indices='iv', order='iv', label='l1')
ShapelyToAxis(l2, axis=ax, color='blue', indices='', order='i', label='l2')
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 2)
ax.get_figure().savefig('example_plot2.pdf')

pl1 = Point((0.5, 0.5)).buffer(0.6, resolution=3)
pl2 = Point((0.3, 0.5)).buffer(0.6, resolution=3)

ShapelyToAxis(pl1, axis=ax, color='lime', indices='vb', order='ibv', label='pl1')
ShapelyToAxis(pl2, axis=ax, color='grey', indices='', order='i', label='pl2')
ax.get_figure().savefig('example_plot3.pdf')

mp = rotate(pl1.symmetric_difference(pl2), angle=90)
ShapelyToAxis(mp, axis=ax, color='magenta', indices='', order='ib', label='sd')
ax.get_figure().savefig('example_plot4.pdf')


