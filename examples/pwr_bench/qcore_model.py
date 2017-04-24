from pirs.solids import Box, Cylinder


from qcore_map import core_map, uox_map, mox_map, ref_map, emp_map 
from rod_models import ap, ah, pp
from rod_models import uox, mox1, waba, tube, chan, ifba, fuel_key, ifba_fuel_key, ifba_ab_key, waba_ab_key

# for 1/4 model heat tallies not needed:
for pin in [uox, mox1, ifba]:
    for c in pin.values():
        c.heat = None

# steel pin for reflector assembly:
cyl = uox.copy_tree()
for c in cyl.children: #### .values():
    c.withdraw()

vessel = Cylinder(Z=ah+2*ap, R=9*ap)
awater = Box(X=9*ap, Y=9*ap, Z=ah+2*ap)
awater.material = 'bwater'
awater.temp.set_values(580.)
awater.dens.set_values(0.8)
awater.name = 'axial_reflector'
awater.pos.x =  awater.X/2.
awater.pos.y = -awater.Y/2.

qcore = Box(X=9*ap, Y=9*ap, Z=ah)

vessel.insert(awater)
vessel.insert(qcore)
qcore.name = 'core_container'
qcore.pos.x =  qcore.X/2.
qcore.pos.y = -qcore.Y/2.

qcore.grid.x = ap
qcore.grid.y = ap
qcore.grid.z = qcore.Z


# master assembly model:
a = Box(Z=ah, X=ap, Y=ap)
a.material = 'bwater'
a.temp.set_values(580.)
a.dens.set_values(0.8)
a.grid.x = pp # * 1.00001
a.grid.y = pp # * 1.00001
NZ = 1 
a.grid.z = a.Z/NZ

# master reflector model
aref = a.copy_tree()
baffled = True
if baffled:
    baffle = aref.insert(Box(X=ap-2.53, Y=ap-2.53, Z=ah, material='zirc'))
    iwater = baffle.insert(Box(X=baffle.X-2.53*2, Y=baffle.Y-2.53*2, Z=ah, material='bwater'))
    baffle.temp.set_values(580)
    baffle.dens.set_values(6.504)
    iwater.temp.set_values(580)
    iwater.dens.set_values(0.8)

map_dict = {}
map_dict['u'] = uox_map
map_dict['m'] = mox_map
map_dict['r'] = ref_map
map_dict['_'] = emp_map

rod_dict = {}
rod_dict['u'] = uox
rod_dict['i'] = ifba
rod_dict['c'] = chan
rod_dict['g'] = tube
rod_dict['m1'] = mox1
rod_dict['m2'] = mox1
rod_dict['m3'] = mox1
rod_dict['w'] = waba
rod_dict['r'] = cyl

adict = {}
for (i, j, e) in core_map.items():
    ass = adict.get(e, None)
    if ass is not None:
        ass = ass.copy_tree()
    else:

        if e[0] == '_':
            # reflector assembly.
            ass = aref.copy_tree()
        else:
            ass = a.copy_tree()
            for (ii, jj, ee) in map_dict[e[0].lower()].items():
                rod = rod_dict.get(ee, None)
                if rod is None:
                    print 'Unknown rod in the assembly map. Skip it', ee
                    pass
                else:
                    rod = rod.copy_tree()
                    key = '{0} {1},{2}'.format(ee, ii, jj)
                    if ee in ['u', 'i', 'm1', 'm2', 'm3']:
                        if e[0] == 'u':
                            fmaterial = e
                            amaterial = e[:3] + '_ifba' + e[3:] 
                        elif e[0] == 'm':
                            fmaterial = e[:3]
                            if ee == 'm1':
                                fmaterial += '_25'
                                rod.name = 'mox1_pin'
                            elif ee == 'm2':
                                fmaterial += '_30'
                                rod.name = 'mox2_pin'
                            elif ee == 'm3':
                                if e[1:3] == '43':
                                    fmaterial += '_50'
                                elif e[1:3] == '40':
                                    fmaterial += '_45'
                                else:
                                    raise ValueError(ee)
                                rod.name = 'mox3_pin'
                            fmaterial += e[-2:]
                        else:
                            raise ValueError(e)
                        if ee == 'i':
                            fkey = ifba_fuel_key
                            akey = ifba_ab_key 
                            babs = rod.get_child(akey)
                            babs.material = amaterial
                            babs.dens.clear()
                        else:
                            fkey = fuel_key
                        fuel = rod.get_child(fkey)
                        fuel.material = fmaterial
                        fuel.dens.clear()
                    elif ee == 'w':
                        amaterial = e[:3] + '_waba' + e[-2:]
                        babs = rod.get_child(waba_ab_key)
                        babs.material = amaterial
                        babs.dens.clear()
                    for k in range(NZ):
                        # key = '{0} {1},{2},{3}'.format(ee, ii, jj, k)
                        key = '{0}'.format(ee)
                        rrr = rod.copy_tree()
                        ass.grid._append((ii, jj, k), rrr)
                        rrr.name = key

            ass.grid.center()
        adict[e] = ass

    qcore.grid._append((j, i, 0), ass)
    ass.name = '{0} {1} {2}'.format(e, i, j)
    print 'assembly {0} added'.format((i,j,e)), ass.name

qcore.grid.set_origin((0, 9, 0), (-qcore.X/2, qcore.Y/2., 0))
print 'model completed.'
    
model = vessel


if __name__ == '__main__':
    pass
    for e in model.values(True):
        if str(e.material)[0] in ['u', 'm']:
            print repr(e.name), repr(e.material)

    exit()
    from pirs.tools.plots import colormap
    for k, a in adict.items():
        print 'plotting assembly ', k
        az = colormap(a, plane={'z':0}, linewidth=0.01, nmarker={'coat':'rx'})
        az.get_figure().savefig('qc.{}.pdf'.format(k))
        rset = set()
        for r in a.children:
            plotted = False
            for rprev in rset:
                if r.name[:2] == rprev:
                    plotted = True
                    break
            if not plotted:
                print 'plotting rod ', r.name, r.ijk
                ar = colormap(r, plane={'z':0}, linewidth=0.01)
                ar.get_figure().savefig('qc.{}.{}.pdf'.format(k, r.name))
                rset.add(r.name[:2])

