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

Place for description of SCF input fields. The description is accessible through .help() method, defined
for ScfVariable, ScfTable, ScfSwitch.
"""

import warnings

# All text description is saved as a dictionary.  Keys must be a variable name,
# name of a switch state, name of a table or name of a table's column.  A
# switch general description must be provided in the in the switch' first state
# name.

# The dictionary is custom. If it has no key, it returns a warning, not an error.
class HelpDict(dict):
    def __getitem__(self, key):
        """
        If key is undefined, don't raise an error, just print a warning.
        """
        try:
            res = super(HelpDict, self).__getitem__(key)
        except KeyError:
            res = None
            warnings.warn('There is no entry for SCF input element {0}.'.format(repr(key)))
        return res

hd = HelpDict() # the help dictionary.
hd['set_critical_power_iteration'] = """
Switch defines behaviour of the solver. 

Contains only one state, 'set_critical_power_iteration'. If this state is 'on',
the steady-state solution will be repeated for varying values of total power,
until the value correspondent to the critical flux is found.
"""

hd['relative_axial_location'] = """
This table must be present and have at least two entries, for z=0 and z=1 (z is
relative here), even if the actual data for axial heat profile is given in the
last group, ' operating_conditions'.
"""
