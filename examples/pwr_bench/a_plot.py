from sys import argv
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

from pirs.tools import load
from pirs.tools.plots import colormap

dmp = load(argv[1])

sres = dmp['scf_result']

x = -2.5
x = 1.2 
x=0.
z = 1.

a = {}
a['gm'] = colormap(sres, plane={'z':z}, var='material')

a['zh'] = colormap(sres, plane={'z':z}, var='heat', filter_=lambda e: e.name == 'fuel')
a['xh'] = colormap(sres, plane={'x':x}, var='heat', filter_=lambda e: e.name == 'fuel', aspect='auto')

a['zft'] = colormap(sres, plane={'z':z}, var='temp', filter_=lambda e: e.name == 'fuel')
a['zct'] = colormap(sres, plane={'z':z}, var='temp', filter_=lambda e: e.name == -1)
a['xft'] = colormap(sres, plane={'x':x}, var='temp', filter_=lambda e: e.name == 'fuel', aspect='auto')
a['xct'] = colormap(sres, plane={'x':x}, var='temp', filter_=lambda e: e.name == -1, aspect='auto')

a['zd'] = colormap(sres, plane={'z':z}, var='dens', filter_=lambda e: e.name == -1)
a['xd'] = colormap(sres, plane={'x':x}, var='dens', filter_=lambda e: e.name == -1, aspect='auto')

for (n, ax) in a.items():
    ax.get_figure().savefig(argv[1].replace('.dump', n+'.pdf'))


