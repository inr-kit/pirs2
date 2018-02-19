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

Classes describing keywords, tables and switches of SCF input, and the input itself.
 
Input is a list of elements of the ScfGroup class. ScfGroup is a list of 
elements those are instances of ScfVariable, ScfSwitch or ScfTable classes.

    Input
            ScfGroup1
                    ScfVar1
                    ScfTable2
                    ...
            ScfGroup2
                    ScfVar
                    ScfSwitch
                    ...
            ...

Classes ScfVariable, ScfSwitch and ScfTable provide method matches_substring().
This method can be used to check if the variable name, table column names or
switch state names contain particular substring. The ScfGroup class also
provides this method.

Classes Input and ScfGroup provide method find(). It returns a list of all
elements whose names match strings specified as arguments. The ScfGroup.find
searches for all elements inside the group, the Input.find method searches
for the group names and for the element names inside each group.

Classes Input and ScfGroup accept also string indexes (although inherited
from the list internal class). When string index is given, the first element
matching this string is returned (thi is similar to the find method). If no
elements match, the KeyError is raised.

"""

from . import workplace
from .input_help import hd as ScfHelpDictionary

from .variables import ScfVariable, ScfSwitch, ScfTable
from . import template25
from . import defaults


class Input(list):
    """
    O-O representation of all keywords, tables and switches of the SCF input file.

    Input is a list, but string indexes are accepted as well.

    
    >>> scf = Input()

    Particular elements can be found using indexes or the find method.

    >>> print scf.find('relative_heat')[0]
    file = this_file
    relative_axial_location   relative_heat_flux
    !

    >>> print scf['relative_heat']
    file = this_file
    relative_axial_location   relative_heat_flux
    !


    """

    def __getitem__(self, *keys):
        """
        Indexing supports also string indices.

        A string index returns a group, variable, table or a switch matching
        the key.
        """
        if len(keys) == 1 and isinstance(keys[0], int):
            return super(Input, self).__getitem__(keys[0])
        else:
            res = self.find(*keys)
            if len(res) == 0:
                raise KeyError('Input contains no group or element with name specified by ', *keys)
            else:
                return res[0]
                
    def __init__(self, version='2.5', defaults=defaults.pwr_pin):
        # workplace
        self.__wp = workplace.ScfWorkPlace()

        super(Input, self).__init__()

        if version == '2.5':
            template25.init(self)
        else:
            raise NotImplementedError()
        defaults(self)
        return

    @property
    def wp(self):
        """
        Instance of the ScfWorkPlace() class.

        Prepares working directory for SCF and starts the code.
        """
        return self.__wp

    @wp.setter
    def wp(self, value):
        self.__wp = value

    def run(self, mode='r', **kwargs):
        """
        Prepares content of the input file and starts an SCF job.
        """
        self.__wp.input.string = str(self)
        self.wp.run(mode, **kwargs)


    def clear(self):
        """
        Clears all data from variables, switchs, tables.
        """
        for g in self:
            g.clear()
        return

    def __str__(self):
        res = []
        for g in self:
            res.append(str(g))
        res.append('end')
        return '\n'.join(res)

    def find(self, *names):
        """
        Returns list of all groups and group elements (i.e. switches, tables,
        variables) whose names contain name as a substring.

        The first argument controls what is searched.

            'a' -- (default) search all: group names, variables, switches and tables.
            'g' -- search group names only
            'v', 's' or 't' -- search only among instances of the ScfVarible, ScfSwitch or ScfTable class, respectively.

        If the first argument has another value, 'a' is assumed.
        """
        res = []

        if names[0] in 'agvst':
            where = names[0]
            names = names[1:]
        else:
            where = 'a'

        if where == 'a':
            # check the group names
            for g in self:
                if g.matches_substring(*names):
                    res.append(g)
            # check the names of group elements:
            for g in self:
                for e in g:
                    if e.matches_substring(*names):
                        res.append(e)
        elif where == 'g':
            # check the group names
            for g in self:
                if g.matches_substring(*names):
                    res.append(g)
        elif where in 'vst':
            cls = {}
            cls['v'] = ScfVariable
            cls['s'] = ScfSwitch
            cls['t'] = ScfTable
            for g in self:
                for e in g:
                    if isinstance(e, cls[where]) and e.matches_substring(*names):
                        res.append(e)
            
        return res




if __name__ == '__main__':
    import doctest
    doctest.testmod()


