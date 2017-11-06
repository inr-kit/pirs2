# Get isotopic ocmpositions from elements, used in C-Mdoel materials

# Materials from C-model are read in the tbm_mats module


def are_close(a, b, atol=1e-4, rtol=1e-4):
    """
    Check that isotopic compositions a and b are close, i.e. at least one of
    the following holds:

    |b - a| <= atol

    or

     |b - a|
    ---------  <= rtol
    |a| + |b|

    The length |v| of vector v=(v1, v2, ... vn) is defined as

            |v| = sum(|vi|)

    with this choice all isotopic compositions have lenght 1.
    """
    # Isotopic compositions as dictionaries
    da = dict(zip(a[0::2], a[1::2]))
    db = dict(zip(b[0::2], b[1::2]))
    # Vector d = a - b:
    d = {}
    s = set(a[0::2] + b[0::2])   # Common set of vector elements:
    for e in s:
        d[e] = db.get(e, 0.0) - da.get(e, 0.0)

    # Lenghts of vectors a, b and d:
    ld = sum(map(abs, d.values()))
    l1 = sum(map(abs, a[1::2]))
    l2 = sum(map(abs, b[1::2]))

    return ld <= atol or ld/(l1 + l2) <= rtol


def read_input(iname):
    """
    Read input and write dump for later use.

    The dump is used only when younger than the original input file.
    """
    import cPickle
    import os
    from numjuggler.parser import get_cards, CID
    from pirs.mcnp import Material

    inp = iname
    dmp = '.{}.matdump'.format(iname)
    print inp
    print dmp
    mats = None
    try:
        if os.stat(dmp).st_mtime > os.stat(inp).st_mtime:
            mats = cPickle.load(open(dmp, 'r'))
            print 'Materials read from previous dump ', dmp
    except Exception as e:
        print e

    if mats is None:
        cards = filter(lambda c: c.ctype == CID.data, get_cards(inp))
        for c in cards:
            c.get_values()
        cards = filter(lambda c: c.dtype == 'Mn', cards)
        mats = {}
        for c in cards:
            m = Material.parseCard(c)
            m.name = str(c.name)
            m.T = None
            mats[c.name] = m
        with open(dmp, 'w') as d:
            cPickle.dump(mats, d)
            print 'Materials dumped to ', dmp
    return mats


def find_elements(mlist):
    """
    Extract elemental compositions from all materials in the list mlist.
    """
    elements = {}  # dictionary of dictionaries
    for m in mlist:
        edict = m.elements()
        for en, ed in edict.items():
            # en -- string name of element
            # ed -- definition of isotopic composition as a tuple
            if en not in elements.keys():
                elements[en] = {}  # This dictionary  has keys as tuples ed, and values -- lists of material names, where this definition was found.
            edd = elements[en]  # element definition dictionary
            for eed, ml in edd.items():
                if are_close(eed, ed):
                    ml.append(m.name)
                    break
            else:
                edd[ed] = [m.name]
    return elements


def report_element(edd, ename, fout):
    """
    Print table containing all isotopic compositions in edd.

    edd is a dictionary with keys -- tuples of the form (ZA1, f1, ZA2, f2, ...),
    and keys -- list of material names. This dictionary is prepared by
    find_elements() above.
    """
    print >> fout, '"{}" composition:'.format(ename)
    # common list of ZAIDs
    zaids = set(sum(map(lambda l: l[0::2], edd.keys()), ()))
    zaids = sorted(zaids)
    print >> fout, '    ', ''.join(map('{:>14d}'.format, zaids)), '  in materials'

    for ed, ml in edd.items():
        d = dict(zip(ed[0::2], ed[1::2]))
        print >> fout, '     ',
        for za in zaids:
            print >> fout, '{:>13.4e}'.format(d.get(za, 0.0)),
        print >> fout, ' ', ml


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Extract elemental '
                                     'compositions from MCNP input file')
    parser.add_argument('--input',
                        help='MCNP input file with material specifications')
    parser.add_argument('--out', default=None,
                        help='Output filename')
    args = parser.parse_args()
    if args.out is None:
        args.out = '{}.isocomps'.format(args.input)

    mats = read_input(args.input)
    elements = find_elements(mats.values())
    fout = open(args.out, 'w')
    for ename, edd in sorted(elements.items()):
        report_element(edd, ename, fout)


if __name__ == '__main__':
    main()
