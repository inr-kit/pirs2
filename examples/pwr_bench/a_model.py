from pirs.solids import Box, Cylinder


from qcore_map import uox_map  
from minicore_map2 import m as uox_map
from rod_models import ap, ah, pp
from rod_models import uox, mox1, mox2, mox3, waba, tube, chan, ifba, fuel_key


# master assembly model, Npi x Npj:
Ia = (0, 2)# assembly indices to model (0,0) -- lower left, (2,2) -- upper right 
Ja = (0, 2)
Nai = (Ia[1] - Ia[0] + 1)
Naj = (Ja[1] - Ja[0] + 1)
Na = Nai*Naj
Nap = 17 #: Number of rods per assembly
Npi = Nap * Nai
Npj = Nap * Naj

a = Box(Z=ah, X=Npi*pp, Y=Npj*pp)
a.material = 'bwater'
a.temp.set_values(580.)
a.dens.set_values(0.8)
a.grid.x = pp
a.grid.y = pp
a.grid.z = a.Z


rod_dict = {}
rod_dict['u'] = uox
rod_dict['i'] = ifba
rod_dict['c'] = chan
rod_dict['g'] = tube
rod_dict['_'] = tube
rod_dict['m1'] = mox1
rod_dict['m2'] = mox2
rod_dict['m3'] = mox3
rod_dict['w'] = waba

# for plotting
uox.name = 'uox'
ifba.name = 'ifba'
chan.name = 'chan'
tube.name = 'tube'
mox1.name = 'mox1'
mox2.name = 'mox2'
mox3.name = 'mox3'
waba.name = 'waba'

uox_map.rdict['i'] = 'u' # no ifbas.

# index boundaries for the whole map
Imin, Imax = uox_map.irange
Jmin, Jmax = uox_map.jrange
# index boundaries for Nai and Naj array of assemblies
Imin = Imin + Nap * Ja[0]
Jmin = Jmin + Nap * Ia[0]
Imax = Imin + Npj
Jmax = Jmin + Npi 

for i in range(Imin, Imax):
    for j in range(Jmin, Jmax):
        e = uox_map.get_element(i, j)
        rod = rod_dict[e]
        a.grid.insert((j, i, 0), rod.copy_tree())
a.grid.center()

if __name__ == '__main__':
    # from pirs.tools.plots import colormap
    from pirs.tools.plots import colormap

    cls = {}
    cls['swater'] = 'LightSteelBlue'
    cls['bwater'] = 'DeepSkyBlue'
    cls['uo2'] = 'Fuchsia'
    cls['mox1'] = 'Orange'
    cls['mox2'] = 'OrangeRed'
    cls['mox3'] = 'Red'
    cls['zirc'] = 'Gray'
    cls['waba'] = 'Yellow'
    cls['ifba'] = 'Gold'

    print 'generate plots'
    az = colormap(a, plane={'z':0}, colors=cls)
    ay = colormap(a, plane={'y':0}, aspect='auto', colors=cls)
    ax = colormap(a, plane={'x':0}, aspect='auto', colors=cls)

    print 'saves plots to pdf'
    az.get_figure().savefig('a_model_z.pdf')
    ay.get_figure().savefig('a_model_y.pdf')
    ax.get_figure().savefig('a_model_x.pdf')


    if Nai == 3 and Naj == 3:
        # UOX and MOX assemblies
        print 'generate assembly plots'
        az = colormap(a, plane={'z':0}, nmarker={'ifba':'kx'}, colors=cls)
        ap2 = ap/2.0
        az.set_xlim(-ap2, ap2)
        az.set_ylim(-ap2, ap2)
        az.get_figure().savefig('a_model_zu.pdf')
        az.set_xlim(-ap2-ap, ap2-ap)
        az.set_ylim(-ap2-ap, ap2-ap)
        az.get_figure().savefig('a_model_zm.pdf')

        # rod types:
        print 'generate rod plots'
        pset = set(['uox', 'ifba', 'chan', 'tube', 'mox1', 'mox2', 'mox3', 'waba'])
        for r in a.children:
            if r.name in pset:
                print 'found rod ', r.name, r.get_key(), r.ijk
                ar = colormap(r, plane={'z':0}, colors=cls)
                ar.get_figure().savefig('rod_{}.pdf'.format(r.name))
                pset.remove(r.name)
            if not pset:
                break

    else:
        azh = colormap(a, plane={'z':0}, var='heat')
        axh = colormap(a, plane={'x':0}, var='heat', aspect='auto')

        azh.get_figure().savefig('a_heat_z.pdf')
        axh.get_figure().savefig('a_heat_x.pdf')
