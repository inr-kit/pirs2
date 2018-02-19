from pirs.scf2 import RodMaterial
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

from hscf2 import si

cld = RodMaterial()
cld.fp = 'benpwr'
cld.fd = -1
cld.ct = -1 
cld.cp = 'zircaloy'

si.materials['steel'] = cld
si.materials['zirc'] = cld

if __name__ == '__main__':
    si.wp.prefix = 's3_'
    si.run('R')

    from pirs.tools import dump
    dump('s3_.dump', gm=si.gm)

    from pirs.tools.plots import colormap
    fltr = lambda e: e.material not in ['zirc', 'steel']
    tz  = colormap(si.gm, plane={'z':1},     var='temp', aspect='auto')#  , filter_=fltr
    tx1 = colormap(si.gm, plane={'x':-0.63}, var='temp', aspect='auto')#  , filter_=fltr
    tx2 = colormap(si.gm, plane={'x': 0.63}, var='temp', aspect='auto')#  , filter_=fltr
    ty1 = colormap(si.gm, plane={'y':-0.63}, var='temp', aspect='auto')#  , filter_=fltr
    ty2 = colormap(si.gm, plane={'y': 0.63}, var='temp', aspect='auto')#  , filter_=fltr
    tz.get_figure().savefig('hscf3_tz.pdf')                            #                
    tx1.get_figure().savefig('hscf3_tx1.pdf')                          #  
    tx2.get_figure().savefig('hscf3_tx2.pdf')                          #  
    ty1.get_figure().savefig('hscf3_ty1.pdf')                          #  
    ty2.get_figure().savefig('hscf3_ty2.pdf')                          #                
                                                                       #                
    fltr = lambda e: e.name == -1                                      #                
    dz  = colormap(si.gm, plane={'z':1},     var='dens', aspect='auto')#  , filter_=fltr
    dx1 = colormap(si.gm, plane={'x':-0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dx2 = colormap(si.gm, plane={'x': 0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dy1 = colormap(si.gm, plane={'y':-0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dy2 = colormap(si.gm, plane={'y': 0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dz.get_figure().savefig('hscf3_dz.pdf')
    dx1.get_figure().savefig('hscf3_dx1.pdf')
    dx2.get_figure().savefig('hscf3_dx2.pdf')
    dy1.get_figure().savefig('hscf3_dy1.pdf')
    dy2.get_figure().savefig('hscf3_dy2.pdf')
else:
    from pirs.tools import load
    si.gm = load('s3_.dump')['gm']


