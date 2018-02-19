from pin_mcnp import MI
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from qcore_model import model, ap, ah

MI.gm = model
MI.bc['key'] = 0


from qcore_materials import mats 
MI.materials.update(mats)
for (n, m) in MI.materials.items():
    try:
        m.isotope_format_string = '{0:>6d}.{1}    {2:21.15e}'
        m.normalize(1)
    except:
        print 'cannot set format string to ', (n, m)

print 'materials updated'

if __name__ == '__main__':
    plst = []
    for element in MI.gm.children[1].children:
        p = element.abspos()
        p.x += 1.26
        p.y -= 1.26
        plst.append(p)
    ksrc = 'ksrc ' + ''.join(map(lambda p: ' {0} {1} {2}'.format(*p.car), plst))
    MI.adc[-1] = ksrc 
    print 'ksrc computed'

    # set up temperatures and densities for water
    for e in MI.gm.values():
        mat = str(e.material)
        if mat == 'swater':
            e.temp.clear()
            e.temp.set_values(560)
            e.dens.clear()
            e.dens.set_values(0.75206)
        elif mat == 'bwater':
            e.temp.clear()
            e.temp.set_values(580)
            e.dens.clear()
            e.dens.set_values(0.71187)
        elif mat == 'zirc':
            e.temp.clear()
            e.temp.set_values(600)
        elif len(mat) > 2 and mat[:2] in ['u4', 'm4']:
            e.temp.clear()
            e.temp.set_values(600)
            

    MI.kcode.Nh = 20000
    MI.kcode.Nct = 100
    MI.kcode.Ncs = 30

    qcore = model.get_child(0)
    fm4 = 'fmesh4:n geom=xyz'
    fm4 += '\n      origin={0} {1} {2}'.format(-ap/2., -ap*10 + ap/2., -ah/2)
    fm4 += '\n      imesh {0}'.format(ap*10 - ap/2.)
    fm4 += '\n      jmesh {0}'.format(ap/2.)
    fm4 += '\n      kmesh {0}'.format(ah/2.)
    fm14 = fm4.replace('fmesh4:', 'fmesh14:')
    fm4 += '\n      iints {0}'.format(170)
    fm4 += '\n      jints {0}'.format(170)
    fm4 += '\n      kints {0}'.format(20)
                    
    fm14 += '\n      iints {0}'.format(10)
    fm14 += '\n      jints {0}'.format(10)
    fm14 += '\n      kints {0}'.format(20)

    fm24 = fm4.replace('fmesh4:', 'fmesh24:')
    fm24 += '\nfm24 -1 0 -6 -8 '

    fm34 = fm14.replace('fmesh14:', 'fmesh34:')
    fm34 += '\nfm34 -1 0 -6 -8 '

    MI.adc.extend([fm4, fm14, fm24, fm34])
    print 'mesh tallies added'
    # MI.run('P', element=MI.gm.children[0])

    from myplatrofm import node
    if 'ic2' in node:
        # this is the ic2 cluster
        MI.wp.exe = 'job_submit -t 40 -m 4000 -p 1/16 -c d mpirun ' + MI.wp.exe
        MI.run('R', tasks=32, file='meshtal')
    elif 'hc3' in node:
        # hc3 cluster
        pass
    elif 'inr149059' in node:
        # this is the local desktop
        pass
    else:
        pass

    
