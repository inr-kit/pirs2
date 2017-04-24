from hmcnp4 import mi

# set heat meshes
for v in mi.gm.values():
    if v.material == 'fuel':
        v.heat.set_grid([1]*20)

if __name__ == '__main__':
    mi.wp.prefix = 'm5_'
    mi.run('R', tasks=3)

    from pirs.tools import dump
    dump('m5_.dump', gm=mi.gm)


    from pirs.tools.plots import colormap
    hx1 = colormap(mi.gm, plane={'x':-0.63}, var='heat', aspect='auto')
    hx2 = colormap(mi.gm, plane={'x': 0.63}, var='heat', aspect='auto')
    hy1 = colormap(mi.gm, plane={'y':-0.63}, var='heat', aspect='auto')
    hy2 = colormap(mi.gm, plane={'y': 0.63}, var='heat', aspect='auto')
    hx1.get_figure().savefig('hmcnp5_hx1.pdf')
    hx2.get_figure().savefig('hmcnp5_hx2.pdf')
    hy1.get_figure().savefig('hmcnp5_hy1.pdf')
    hy2.get_figure().savefig('hmcnp5_hy2.pdf')
else:
    from pirs.tools import load
    mi.gm = load('m5_.dump')['gm']

