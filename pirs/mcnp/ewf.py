#!/usr/bin/env python
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

# -*- coding: utf-8 -*-

"""
Script to extract elemental weight fractions
from material cards in MCNP input file.
"""

def get_clp():
    """
    Analyse command line parameters and return needed info.
    """
    import argparse
    p = argparse.ArgumentParser(description='Extract elemental weight fractions from input file')
    p.add_argument('--mats', nargs='+', type=int,
                   help='Material numbers to output')
    p.add_argument('--input', type=str,
                   help='MCNP input file')
    p.add_argument('--fmt', type=str, default='{:>9.6f}',
                   help='Format specifier for weight fractions')
    p.add_argument('--factor', type=float, default=1.0,
                   help='Factor to multiply weight fraction (put 100 to get %)')

    args = p.parse_args()
    return args.fmt, args.input, args.mats, args.factor


def main():
    fmt, iname, mats, factor = get_clp()

    from pirs.mcnp import Material
    from pirs.core.tramat.data_names import name as chemical_names

    d = Material.read_from_input(iname)
    f = '{{:>2s}}-{{:<3d}}: {}'.format(fmt)

    for mn in mats:
        m = d.get(mn, None)
        if m is None:
            continue

        print 'Material ', mn
        e = m.elements(keyform='Z')
        wt = m.amount(2)
        for z in e.keys():
            we = m.how_much(2, Z=z)
            print ' ', f.format(chemical_names[z], z, we/wt*factor)




if __name__ == '__main__':
    main()

