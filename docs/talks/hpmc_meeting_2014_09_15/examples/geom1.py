from pirs.solids import Box, Cylinder

cnt = Box(X=2.53, Y=2.53, Z=365, material = 'water')
r = Cylinder(R=0.4583, Z=365, material = 'steel')
f = Cylinder(R=0.3951, Z=365, material = 'fuel')

r.insert(f)
cnt.insert(r)

r2 = cnt.insert(r.copy_tree())
r2.pos.x = 0.8 
r2.pos.y = 0.8

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    pz = colormap(cnt, plane={'z':0})
    px = colormap(cnt, plane={'x':0}, aspect='auto')
    py = colormap(cnt, plane={'y':0}, aspect='auto')
    pz.get_figure().savefig('geom1_pz.pdf')
    px.get_figure().savefig('geom1_px.pdf')
    py.get_figure().savefig('geom1_py.pdf')

