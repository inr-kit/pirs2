from pirs.core.scheduler import InputFile, WorkPlace
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


# MCNP input file
i1 = InputFile()
i1.basename = 'inp'
i1.string = 'c input file'

# Srctp from previous run
i2 = InputFile()
i2.basename = 'srctp2'
i2.exfile = './srctp1'

# shell script to start MCNP
i3 = InputFile()
i3.basename = 'start.sh'
i3.string = '$MCNP inp=inp srctp=srctp2'
i3.executable = True

# workplace
w = WorkPlace()
w.suffix = 'wp'
w.files.append(i1)
w.files.append(i2)
w.files.append(i3)

w.prepare()
print w.report
out = w.run(sec=1)
print out
