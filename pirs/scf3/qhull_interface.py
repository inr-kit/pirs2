# pyhull does not allow option 'Qz i Fx' for pyhull.delaunay() function, although this option is accepted
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

# by the command line utility qdelaunay. Thus I write own wrapper that simply calls the external command qdelaunay.

from subprocess import Popen, call, PIPE
import itertools
from shapely.geometry import Polygon, MultiLineString



                    
                            
def _prepare_input(points):
    # convert points to the input for qdelaunay: 
    inp = []
    inp.append(str(len(points[0]))) # dimension
    inp.append(str(len(points)))    # number of points
    inp.extend( ' '.join(map(str, xy)) for xy in points) # point coordinates
    inp = '\n'.join(inp)
    return inp

def _run(program, options, inp):
    command = [program] + options.split()
    p = Popen(command, stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate(input=inp)
    return stdout, stderr

def qhull(points):
    # convert points to the input for qdelaunay: 
    inp = _prepare_input(points)
    stdout, stderr = _run('qhull', 'Fx', inp)

    # process the output:
    res = []
    outp = stdout.splitlines()
    N = int(outp.pop(0)) # number of indices
    for l in outp:
        res.append(int(l))

    return res 
        

def qdelaunay(points, options='i Fx Fn FN FP'):
    """
    Returns a dictionary {option: output}, where option is the output option
    passed to qdelaunay, and output is a list of values (not strings!) of the correspondent
    output.

    points is a list (any iterable) of tuples (x, y) with point coordinates.

    options is a string with options for qdelaunay. Options can be specified in
    arbitrary order, see qhull manual.
    """
    # convert points to the input for qdelaunay: 
    inp = _prepare_input(points)

    # run qdelaunay and catch the stdout
    stdout, stderr = _run('qdelaunay', 'Qz ' + options, inp)

    # process the output:
    stdoutlines = stdout.splitlines()
    output = {} # dictionary {option: output}, where option is output option passed to qdelaunay and output is the correspondent output.

    for option in options.split():
        if option == 'i':
            # output for the 'i' option:
            out_i = [] # list of lists [ region_definition1, region_definition2, ...], where region_definitionI is a list of input site indices that define region with index I.
            N = int(stdoutlines.pop(0)) # number of facets
            for i in range(N):
                # list of input sites that define the Delaunay region
                slist = map(int, stdoutlines.pop(0).split())
                out_i.append(slist)
            output[option] = out_i

        elif option == 'Fx':
            # output for the 'Fx' option:
            out_Fx = [] # list of extreme site indices.
            N = int(stdoutlines.pop(0))
            for i in range(N):
                n = int(stdoutlines.pop(0))
                out_Fx.append(n)
            output[option] = out_Fx

        elif option == 'Fn':
            # output for the 'Fn' option:
            out_Fn = [] # list of lists [ region_neighbours1, region_neighbours2, ...], where regoin_neighboursI is a list of region indices adjacent to the region with index I.
            N = int(stdoutlines.pop(0))
            for i in range(N):
                nlist = map(int, stdoutlines.pop(0).split())[1:] # the first element is the number of regions, not needed.
                out_Fn.append(nlist)
            output[option] = out_Fn

        elif option == 'FN':
            # output for the 'FN' option:
            out_FN = [] # list of lists [region_neighbours1, region_neighbours2, ...], where regoin_neighboursI is a list of region indices adjacent to the site with index I.
            N = int(stdoutlines.pop(0))
            for i in range(N):
                nlist = map(int, stdoutlines.pop(0).split())[1:] # the first element is the number of regions, not needed.
                if nlist:
                    out_FN.append(nlist)
            output[option] = out_FN

        elif option == 'FP':
            # output for the 'FP' option:
            out_FP = [] # list of deleted site indices. 
            N = int(stdoutlines.pop(0))
            for i in range(N):
                nlist = map(int, stdoutlines.pop(0).split()) 
                out_FP.append(nlist[1])
            output[option] = out_FP

        else:
            raise NotImplementedError('Processing of the output option {} is not implemented'.format(repr(option)))

    return output

class Triangulation(object):
    """
    Represents triangulation. Takes as input a list of triangulation points
    (sites), and provides methods to access information about triangulation
    regions.

    """

    def __init__(self, points):
        """
        points is a list of tuples (x,y) with point coordinates.
        """
        self.__input = points[:]

        regions = [] # list of ([definition], is_extreme, set(neighbour regions))
        sites = []   # list of (x, y, is_extreme, set(neighbour regions))

        output = qdelaunay(points, 'i Fx Fn FN FP')
        for definition, neighbours in zip(output['i'], output['Fn']):
            is_extreme = any(i < 0 for i in neighbours)
            regions.append((definition, is_extreme, set(neighbours)))

        unused = set(output['FP'])
        extreme_sites = output['Fx']
        for site, neighbours in enumerate(output['FN']):
            x, y = points[site]
            if site not in unused:
                is_extreme = site in extreme_sites
                sites.append((x, y, is_extreme, set(neighbours)))


        self.__r = regions
        self.__s = sites

        # print 'Triangulation has {} sites and {} regions'.format(len(self.__s), len(self.__r))
        return

    __index_err_msg = 'Index cannot be zero. Use positive indices for sites and negative for regions'

    def coords(self, i=None):
        """
        i is None: returns list of site cooordinates.

        i>0: returns coordinate of (i-1)-th site, (x,y)

        i<0: returns list of coordinates of |i+1|-th region.
        """
        if i is None:
            return map(lambda s: s[:2], self.__s)
        elif i > 0:
            return self.__s[i-1][:2]
        if i < 0:
            return map(lambda k: self.__s[k][:2], self.__r[-i-1][0])
        else:
            raise IndexError(self.__index_err_msg)

    def sites(self, i=None):
        """
        i is None: returns list of site indices starting from 1.
        i>0: returns set of adjacent sites to site (i-1)
        i<0: returns list of sites that define regions adjacent to region |i+1|
        """
        if i is None:
            return range(1, len(self.__s)+1)
        elif i > 0:
            # raise NotImplementedError
            s = set()
            for ir in self.__s[i-1][3]:
                s.update(set(self.__r[ir][0]))
            return s
        elif i < 0:
            # raise NotImplementedError
            s = set()
            for ir in self.__r[-i+1][2]:
                s.update(set(self.__r[ir][0]))
            for i in self.__r[-i+1][0]:
                s.remove(i)
            return s
        else:
            raise IndexError(self.__index_err_msg)

    def is_external(self, i):
        """
        i>0: returns True if site (i-1) is an extreme point (lies on the convex hull around all sites)
        i<0: returns True if region |i+1| neighbours the "other world"
        """
        if i > 0:
            return self.__s[i-1][2]
        elif i < 0:
            return self.__r[-i-1][1]
        else:
            raise IndexError(self.__index_err_msg)

    def region(self, i):
        """
        Returns list of sites that define region (i-1).
        """
        return self.__r[i-1][0][:]

    def regions(self, i=None):
        """
        i is None: returs list of region indices
        i>0: returns list of regions around site (i-1)
        i<0: returns list of regions around region |i+1|
        """
        if i is None:
            return range(-1, -len(self.__r)-1, -1)
        elif i > 0:
            return self.__s[i-1][3].copy()
        elif i < 0:
            return self.__r[-i-1][2].copy()
        else:
            raise IndexError(self.__index_err_msg)

    @property
    def _regions(self):
        """
        Direct access to the list of regions. 
        
        This list is generated at the instance initialization time and should
        not be changed at later times.

        List elements are tuples of the following form: ([definition],
        is_extreme, set(neighbours)).  Here:
        
            [definition] is a list of site indices that define the region, 
            
            is_extreme is boolean flag, True means that the region has common
            edge with 'other world'.

            set(neighbours) is a set of region indices that are adjacent to the
            region.

        """

        return self.__r

    @property
    def _sites(self):
        """
        Direct access to the list of sites.

        This list is generated at the instance initialization time and should
        not be changed at later times.

        List elements are tuples of the following form: (x, y, is_extreme,
        set(neighbours)), where:

            x, y are coordinates of the site,

            is_extreme is boolean flag, True if the site is on the convex hull
            of all sites.

            set(neighbours) is a set of region indices that surround the site.
        """
        return self.__s


    # convert Triangulation to a shapely:
    def sMultiLine(self, x=0, y=0):
        """
        Returns an instance of shapely.geometry.MultiLIneString that represeents edges
        of the triangulation.
        """
        ss = set() # set of ordered (from site with lower index) line segments. 
        for (d, f, n) in self.__r:
            s = set()
            for (i1, i2) in zip(d, d[1:] + [d[0]]):
                s.add(tuple(sorted([i1, i2])))
            ss.update(s)

        # build argument for MultiLIneString:
        a = []
        for (i1, i2) in ss:
            x1, y1 = self.__s[i1][:2]
            x2, y2 = self.__s[i2][:2]
            a.append(((x1+x, y1+y), (x2+x, y2+y)))
        # print 'Trinagulation.sMultiLine has {} segments'.format(len(a))
        return MultiLineString(a)
                
                


        




if __name__ == '__main__':
    points = [(0,0), (1,1), (1,0), (0,1), (0.33, 0.33), (0.5, 0.5), (0.66, 0.66), (0,0)]

    # usage of qdelaunay function
    for outp in qdelaunay(points).items():
        print outp[0] + '-'*80
        for l in outp[1]:
            print l

    # usage of Triangulation class:
    t1 = Triangulation(points)
    print '-'*80
    print '-'*80
    for r in t1._regions:
        print r
    print '-'*80
    for i in t1.regions():
        print t1.coords(i), t1.is_external(i), t1.regions(i)

    print '-'*80
    for s in t1._sites:
        print s
    print '-'*80
    for i in t1.sites():
        print t1.coords(i), t1.is_external(i), t1.regions(i)




