from geom2 import cnt

r1 = cnt.children[0]
r2 = cnt.children[1]

r1.material = 'zirc'
r1.ijk = (0, 0, 0)
r2.ijk = (1, 0, 0)
r2.pos *= 0.

cnt.grid.x = 1.26 
cnt.grid.y = 1.30
cnt.grid.z = cnt.Z
r3 = cnt.grid.insert((1, 1, 0), r2.copy_tree())
r4 = cnt.grid.insert((0, 1, 0), r2.copy_tree())
# r4.R = 0.56

# cnt.grid.set_origin((0, -1, 0), (0.,-0.5,0.))
cnt.grid.center()

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    pz = colormap(cnt, plane={'z':0})
    px1 = colormap(cnt, plane={'x':-0.63}, aspect='auto')
    px2 = colormap(cnt, plane={'x':0.63}, aspect='auto')
    py1 = colormap(cnt, plane={'y':-0.63}, aspect='auto')
    py2 = colormap(cnt, plane={'y':0.63}, aspect='auto')
    pz.get_figure().savefig('geom3_pz.pdf')
    px1.get_figure().savefig('geom3_px1.pdf')
    px2.get_figure().savefig('geom3_px2.pdf')
    py1.get_figure().savefig('geom3_py1.pdf')
    py2.get_figure().savefig('geom3_py2.pdf')

