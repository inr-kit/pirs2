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

Functions to get particular lines of a file.
"""

def get_last_line(f, llen=200):
    """
    Return string containing the last line of file f.

    Optional argument llen specifies number of characters from the file's end
    to search the last line.

    If file f is empty, None returned.
    """
    with open(f, 'r') as ff:
        ff.seek(0, 2)
        llen = min(ff.tell(), llen)
        ff.seek(-llen, 2)
        lines = ff.readlines()
        if lines:
            return lines[-1]
        else:
            return None

