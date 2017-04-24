from shapely.geometry import Point

from model import RPoly
from pirs.tools.plots.plot_shapely import ShapelyToAxis

        

p1 = Point((0,0)).buffer(1, resolution=5)
p2 = Point((0,5)).buffer(2, resolution=3)
p3 = Point((5,0))# .buffer(1, resolution=3)
p4 = Point((2,2))# .buffer(1, resolution=3)
p5 = Point((5,5))# .buffer(1, resolution=2)
p6 = Point((5,5)).buffer(3, resolution=2)

definition = [p6]# , p2, p1, p5, p3, p4]
w = RPoly(definition, -1)

ax = None
for p in definition:
    ax = ShapelyToAxis(p, axis=ax, color='green', order='i', label='', indices='')

for i, p in enumerate(w.definition):
    ax = ShapelyToAxis(p, axis=ax, color='blue', order='b', indices='', label=i)

for i, l in enumerate(w.lines):
    ax = ShapelyToAxis(l, axis=ax, color='red', order='iv', indices='', label=i)

for i, l in enumerate(w.arcs):
    ax = ShapelyToAxis(l, axis=ax, color='yellow', order='iv', indices='', label=i, alpha=0.7)


ax.get_figure().savefig('rpoly.pdf')

# check points method
ax2 = ShapelyToAxis(w.shapely, color='gray', label='', indices='', order='i')

ShapelyToAxis(Point(w.points(0).next()), axis=ax2, color='black', alpha=0.2, thickness=0.1) 

for N in [1]:
    iterator = w.points(N, 'arcs')
    for l in iterator:
        print l,
        p = w.points([l]).next()
        print p
        ShapelyToAxis(Point(p), axis=ax2, color='red', alpha=0.1, thickness=0.2/(N+1), label=(N, l))

ax2.get_figure().savefig('rpoly_points.pdf')

#check buffer method
a = ShapelyToAxis(w.shapely, color='blue', alpha=0.9)
for t in [0., 0.5, 1]:
    b = w.buffer(t, t, t)
    ShapelyToAxis(b.shapely, axis=a, color='red', alpha=0.1, label=t)
a.get_figure().savefig('rpoly_buffered.pdf')



