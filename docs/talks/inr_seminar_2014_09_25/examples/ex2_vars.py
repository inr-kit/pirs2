from ex2_geom import b

f = b.get_child((0, 0))

# fuel temperature axial profile
f.temp.set_grid([1, 1, 1])
f.temp.set_values(350)

# heat deposition axial profile
f.heat.set_grid([1, 1, 2, 3, 2, 1, 1])
f.heat.set_values([1, 2, 3, 4, 3, 2, 1])

# density axial profile in water
b.dens.set_grid([1, 1, 1])
b.dens.set_values([0.7, 0.65, 0.6])

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    colormap(b, {'x':0}, var='heat', filename='ex2t.pdf', aspect='auto')

