from hmcnp4 import mi
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

