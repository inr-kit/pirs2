#!/usr/bin/env python
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
        for z in e.keys():
            w = m.how_much(2, Z=z)
            print ' ', f.format(chemical_names[z], z, w/wtot*factor)




if __name__ == '__main__':
    main()

