"""
Extracts scf_result data from dump and put it in a text form.

This needs that version of PIRS is installed, that was used to
generate dupms.

"""
import sys
from pirs.tools import dump, load

dfile = sys.argv[1]

print 'extracting from {}'.format(dfile)

dorig = load(dfile)
sres = dorig['scf_result']

print 'sres extracted'

for c in sres.children.values():
    for cc in c.values():
        if cc.local_key == 'fuel':
            # print c.ijk, cc.material
            print cc.get_key()
            print cc.temp._zmesh__z
            print cc.temp._zmesh__v
            break

            

