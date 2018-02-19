T = [
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

    (300.98,  334.01,  317.04),
    (337.05,  469.42,  400.18),
    (365.08,  584.55,  468.46),
    (396.75,  726.64,  550.27),
    (464.22, 1076.01,  743.14),
    (513.25, 1354.55,  892.93),
    (456.43,  961.75,  688.67),
    (419.22,  743.69,  570.61),
    (397.16,  627.50,  505.75),
    (335.28,  366.13,  350.29),
    (327.08,  336.46,  331.67),
    ]
a1 = 0.7
a2 = 1. -0.7
for (t1, t2, t3) in T:
    print t1, t2, t3, a2*t2 + a1*t1
