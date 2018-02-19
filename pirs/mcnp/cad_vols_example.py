import glob
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

from pirs.mcnp.cad_vols import compare, get_cad, get_mctal


# def get_cad(model):
#     # cad data
#     try:
#         n = numpy.loadtxt(model + '.cad_volumes', usecols=(0,), dtype=int)
#         v = numpy.loadtxt(model + '.cad_volumes', usecols=(1,), dtype=float)
#         return (n, v *1e-3)
#     except:
#         return None
#
#
# def get_mctal(model):
#     # MCNP data, all possible:
#     for mctal in glob.glob('{}.inp.vol*m'.format(model)):
#         m = Mctal()
#         m.read_complete(mctal)
#         t = m.mctaltallies[4]
#         nl = t.fnl_numpy
#         vl = t.vals_numpy
#
#         yield nl, vl.transpose()



if __name__ == '__main__':
    from sys import argv
    model = argv[1]
    c = get_cad(model + '.cad_volumes')

    m = []
    for mfile in glob.glob('{}.inp.vol*m'.format(model)):
        m.append(get_mctal(mfile))

    if c is None:
        c = m.pop(0)
        print 'FIrst MCNP data is used as a reference'

    if len(argv) > 2:
        ecells = map(int, argv[2:])
    else:
        ecells = ()

    i = 0
    for mm in m:

        fig = compare(c, mm, exclude_cells = ecells)
        fig.savefig('{}_{}.pdf'.format(model, i))
        i += 1
