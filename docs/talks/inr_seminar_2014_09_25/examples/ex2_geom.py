from pirs.solids import Box, Cylinder
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


# surrounding water
b = Box(material='water')
b.X = 1.26
b.Y = b.X
b.Z = 400

# clad
c = Cylinder(material='steel')
c.R = 0.4583
c.Z = 360

# fuel 
f = Cylinder(material='fuel')
f.R = 0.3951
f.Z = 350

# construct model
b.insert(c)    # put clad into box
c.insert(f)    # put fuel into clad
c.pos.y = 0.1  # shift clad with resp. to container

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    colormap(b, {'z':0}, filename='ex2z.pdf')
    colormap(b, {'x':0}, filename='ex2x.pdf', aspect='auto')

