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

Function recipe(Z) defined in this module returns a list of tuples describing a
natural composition recipe of chemical element Z

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at
import autologging

from . import data_natural
from . import data_names


# short-hand links to the natural abundances data and isotope masses.
__natabu = data_natural.d1

def get_default_isotopic_composition(element=1):
    """
    Returns an instance of the :class:`_recipe` class, representing natural
    isotopic composition of chemical element.

    Natural isotoic abundancies are taken from the :mod:`data_natural`
    module, see references there.

    :arg element:

        The chemical element can be specified by an integer (treated as Z
        number) or by a string with one or two characters (treated as the
        chemical name).

    """

    # analyse argument:
    if   isinstance(element, int):
        Z = element
    elif isinstance(element, basestring):
        try:
            Z = data_names.charge['{0:>2s}'.format(element)]
        except KeyError:
            raise ValueError('Unknown element name: ' + element)
    else:
        raise TypeError('Unsupported argument type: ' + element.__class__.__name__)

    # By default, use predefined natural abundancies from data_natural
    nat_ab = __natabu
    r = tuple() 
    for (k, v) in nat_ab.items():
        if type(k) is int and k/1000 == Z:
            # add this nuclide to material recipe
            r += (k, (v, 1))
    if len(r) == 0:
        raise ValueError('No natural abundancy data found for element: ' + str(element))
    return r

import re

# Capital letter followed optionally with small letter, followed optionally with digits
re_names = re.compile('(([A-Z][a-z]*)(\d*))')

@autologging.logged
@autologging.traced
def formula_to_tuple(cf, names={}):
    """
    Return a tuple that can be passed to the Mixture constructor.

    Chemical composition string is a concatenation of valid chemical element
    names as defined in ./data_names._symbol dictionary, concatenated
    optionally with an integer value. For example:

        Al2O3
        H2O
        C2H5OH

    Chemical element name has 1 or two letters, the 1-st one is capital, the
    second one -- small. Chemical element names are not checked whether they are
    valid names.
    """
    check = ''
    res = tuple() 
    for part, elem, mult in re_names.findall(cf):
        # use part to check whether all parts of cf are parsed
        formula_to_tuple._log.info("Part {}: element {}, amount {}".format(part, elem, mult))
        check += part
        if check not in cf:
            raise ValueError('Cannot process chemical formula {}, see part ',
                             'preceeding {}'.format(repr(cf), repr(part)))

        # convert integer to amount of moles (chemical formulae always express amount, not weight/mass)
        mult = 1 if mult == '' else int(mult)
        mult = (mult, 1)

        # convert chemical name to a tuple of isotopes with their abundancies.
        if elem in names.keys():
            # this chemical element is specified in names. Use definition from here.
            elem = names[elem]
        else:
            elem = get_default_isotopic_composition(elem)
            if len(elem) == 2 and elem[1] == (1, 1):
                elem = elem[0]
        res += (elem, mult)
        formula_to_tuple._log.info(repr(res))
    # Simplify definition, if necessary
    if len(res) == 2 and res[1] == (1, 1) and isinstance(res[0], tuple):
        res = res[0]
    return res


