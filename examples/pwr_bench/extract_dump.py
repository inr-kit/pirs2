"""
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

Extracts scf_result data from dump and put it in a text form.

This needs that version of PIRS is installed, that was used to
generate dupms.

"""
import sys
from pirs.tools import dump, load

dfile = sys.argv[1]

print 'extracting from {}'.format(dfile)

dorig = load(dfile)
sres = dorig['scf_result']

print 'sres extracted'

for c in sres.children.values():
    for cc in c.values():
        if cc.local_key == 'fuel':
            # print c.ijk, cc.material
            print cc.get_key()
            print cc.temp._zmesh__z
            print cc.temp._zmesh__v
            break

            

