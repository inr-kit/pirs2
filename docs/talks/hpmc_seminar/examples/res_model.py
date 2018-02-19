from pirs.tools import load
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

from pirs.tools.plots import colormap

dmp = load('results/b_iteration_056.dump')
sr = dmp['scf_result']
mr = dmp['mcnp_result']

gm = sr.copy_tree()
gm.remove_by_criteria(name=-1)
agm = colormap(gm, plane={'z':1}, var='material')

agm.get_figure().savefig('res_model.pdf')

fltr = lambda e: e.name == 'fuel'
atx = colormap(sr, plane={'x':0}, var='temp', aspect='auto', filter_=fltr)
aty = colormap(sr, plane={'y':0}, var='temp', aspect='auto', filter_=fltr)
atx.get_figure().savefig('res_tx.pdf')
aty.get_figure().savefig('res_ty.pdf')

ahx = colormap(sr, plane={'x':0}, var='heat', aspect='auto', filter_=fltr)
ahy = colormap(sr, plane={'y':0}, var='heat', aspect='auto', filter_=fltr)
ahx.get_figure().savefig('res_hx.pdf')
ahy.get_figure().savefig('res_hy.pdf')

ahz = colormap(sr, plane={'z':1}, var='heat', filter_=fltr)
ahz.get_figure().savefig('res_hz.pdf')

fltr = lambda e: e.name == -1 
adx = colormap(sr, plane={'x':0}, var='dens', aspect='auto', filter_=fltr)
ady = colormap(sr, plane={'y':0}, var='dens', aspect='auto', filter_=fltr)
adx.get_figure().savefig('res_dx.pdf')
ady.get_figure().savefig('res_dy.pdf')
