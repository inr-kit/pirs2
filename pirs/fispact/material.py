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

Classes to describe FISPACT material composition.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from ..core import tramat


class Material(tramat.Mixture):
    """
    Object-oriented representation of material composition for FISPACT.

    Constructor arguments are passed to the constructor of the parent class, see
    description of available arguments there.

    One can setup material composition.
    """
    def __init__(self, *args, **kwargs):
        super(Material, self).__init__(*args, **kwargs)
        self.__fmt = {}
        self.__fmt['zaid'] = '{0}'
        self.__fmt['fraction'] = '{0:12.5e}'

    def copy(self):
        new = super(Material, self).copy()
        new.__fmt = self.__fmt
        return new

    @property
    def fmt(self):
        """
        Dictionary of format strings used to generate card representation of the
        material.

        The following keys have sense:

        'zaid': format string for ZAIDs
        'fraction': format string for fraction.

        If explicit field index is used (for Python versions < 2.6), it should
        be set to 0.
        """
        return self.__fmt

    def card_fuel(self, comments=True, sort=False):
        """
        Returns a multi-line string for input file.

        """
        res = []
        # Representation by `FUEL` keyword. It should contain number of atoms,
        # not moles. Therefore NA here:
        NA = tramat.mixer.NAVOGAD
        me = self.expanded()
        for n, a in me.recipe(1):
            nn = n.name.replace('-00', '')
            nn = nn.replace('-0', '')
            nn = nn.replace('-', '')
            l = '    {} {}'.format(nn, a.v * NA)
            res.append(l)
        res.insert(0, 'FUEL {}'.format(len(res)))
        if comments:
            res.insert(1, '<< {} {}>>'.format(self.name, self.amount(2)))
        return '\n'.join(res)

    def __eq__(self, othr):
        """
        Redefinition of the tramat.Mixture.__eq__ method!
        """
        if self is othr:
            return True

        if isinstance(othr, Material):
            return (self.recipe() == othr.recipe() and
                    self.__fmt == othr.__fmt)
        else:
            return False
