from a_mcnp import MI
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

from a_scf import si as SI

print 'Initial models'
print MI.gm.str_tree(['id()', 'name'])
print SI.gm.str_tree(['id()', 'name'])


sres = SI.run('R')
print 'result of the 1-st SCF run:'
print sres.str_tree(['id()', 'name'])


MI.gm = sres
MI.run('r')
print 'MI.gm after the first MCNP run'
print MI.gm.str_tree(['id()', 'name'])


sres = SI.run('R')
print 'result of the 2-nd SCF run'
print sres.str_tree(['id()', 'name'])



MI.gm = sres
MI.run('r')
print 'MI.gm after the 3-rd run'
print MI.gm.str_tree(['id()', 'name'])

