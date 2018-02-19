"""
Classes to construct a SCF model.

Bundle() and Rod() represent bundles and rods. A bundle has a wall, and can be
filled with other bundles and/or rods. A rod is specified by its radius.

The same instance of rod or bundle can be inserted into multiple containers (A
container is an instance of the Bundle class, where an element is inserted).
Properties of an inserted element in its container (like position of element in
the container) are given in a separate object, an instance of the Relation()
class. Thus, technically, insertion means to proveide not only an element to
insert (bundle or a rod), but also a Relation()  instance:

    c = Bundle() # container
    e = Bundle() # element to be inserted into container c
    r = Relation() # describes properties of e in c
    c.interior.append((e, r))

Container knows about its interior elements, but interior elements do not know its
containers.

The interior property is a list of tuples (element, relations), where element
is an interior object and relations is an object that defines relation
parameters, i.e. position of element in interior.

The form of the bundle's wall is defined by an instance of the RPoly class.
This class represents a polygon with rounded corners, it is defined as a convex
hull of a set of shapely polygons (particularly, these polygons can represent
circles, so that the convex hull perimeter will consist of linear segments that
connect different circles, and arcs -- parts of circles).
"""



from shapely.geometry import LineString, Polygon, Point
from shapely.geometry.polygon import orient
from shapely.ops import cascaded_union
from shapely.affinity import translate

from pirs.tools.plots.plot_shapely import ShapelyToAxis
from qhull_interface import Triangulation

from random import uniform

class RPoly(object):
    """
    Polygon with rounded corners.

    Constructed as a convex hull of a set of shapely polygons.

    Has method to iterate over linear segments (that are connections between
    shapely objects) and parts of the boundary that touches the shapely objects for
    definition.
    """

    def __init__(self, definition, orientation=1):
        # the convex hull polygon:
        hull = cascaded_union(definition).convex_hull
        hull = orient(hull, orientation)

        # set of definition polygons that define the hull
        ext = hull.exterior
        def_short = []   # definition list, without unrelevant polygons (that lie inside the hull).
        for p in definition:
            if p.intersection(ext):
                def_short.append(p)

        corners = [] # tuples of (polygon, coord)
        for c in ext.coords:
            p = Point(c)
            for rp in def_short:
                if p.intersection(rp):
                    corners.append((rp, c))
                    break

        rp_list = [] # list of relevant polygons
        ls_list = [] # list of linear segments
        as_list = [] # list of arc segments

        
        arc = []
        for (rp1, c1), (rp2, c2) in zip(corners[:-1], corners[1:]):
            if not rp1 is rp2:
                # linear segment
                segment = LineString([c1, c2])
                ls_list.append(segment)
                rp_list.append(rp1)
                # arc segment of rp1:
                if arc:
                    # arc consists of several line segments
                    arc.append(c1)
                    segment = LineString(arc)
                else:
                    # arc represented by a point
                    segment = LineString([c1, c1])
                as_list.append(segment)
                arc = []
            else:
                arc.append(c1)
        # do not forget the last arc:
        if rp1 is rp2:
            arc.append(c2)
            as_list.append(LineString(arc))
            if rp2 not in rp_list:
                rp_list.append(rp2)

        # combine first and last arc, if necessary:
        if len(as_list) > len(rp_list):
            c_list = []
            for arc in [as_list[-1], as_list[0]]:
                if not arc.is_empty:
                    c_list += arc.coords
            as_list[0] = LineString(c_list)
            as_list.pop(-1)

        # shift lists so that the first relevant polygon from definition is the
        # first element.
        idx = rp_list.index(def_short[0])
        rp_list = rp_list[idx:] + rp_list[:idx]
        ls_list = ls_list[idx:] + ls_list[:idx]
        as_list = as_list[idx:] + as_list[:idx]

        self.__d = tuple(rp_list)
        self.__l = tuple(ls_list)
        self.__a = tuple(as_list)
        self.__o = orientation

        # the boundary of hull starts at arbitrary point. I want it to start at
        # a particular position, namely, at the begin of the 1-st arc.
        coords = []
        for (a, l) in zip(self.__a, self.__l):
            for s in (a, l):
                for c in s.coords:
                    if not coords or coords[-1] != c:
                        coords.append(c)
        self.__s = Polygon(coords)
        assert len(self.__s.boundary.coords) == len(hull.boundary.coords)
        return

    @property
    def definition(self):
        """
        Tuple of shapely polygons passed to the constructor in the definition list.

        Only relevant polygons are returned.
        """
        return self.__d

    @property
    def lines(self):
        """
        Tuple of line segments.

        Elements are instances of the shapely.geometry.LineString() class.
        """
        return self.__l
        
    @property
    def arcs(self):
        """
        Tuple of arc segments.

        Elements are instances of the shapely.geometry.LineString() class.
        """
        return self.__a

    @property
    def orientation(self):
        """
        Orientation used in the initialization.
        """
        return self.__o

    @property
    def shapely(self):
        """
        A shapely polygon representing the form of RPoly.
        """
        return self.__s
        
    def points(self, N=0, where='boundary'):
        """
        Returns an interator over points on the RPoly's boundary.

        if where is 'boundary' (default):

            if N is a list of numbers, assume it is relative distances along
            the boundary and returs correspondent coordinates.

            If N is 0, returns the coordinate of initial point of the boundary. 

            if N is a number greater than 0, returns a list of int(N) rel.
            distances with 1./N step.

        If where is 'lines'/'arcs'/'segments':

            if N is a number, returns a list of rel. distances to each line/arc
            segment ends, plus N internal points inside each line/arc segment
            (N can be 0).

            If N is a list, returns a list of rel. distances to each line/arc
            segment ends, plus N[i] internal points inside the i-th line/arc segment
            (N[i] can be 0).

            The segments where points are added, is defined by the keyword: if
            'lines', points are added only to the line segments, if 'arcs' --
            points are added to the arc segments only, and if 'segments',
            points are added to both line and arc segments. 

        Note that this method can get a list of relative distances, and can
        translate such a list into a list of coordinates.  If it gets simply a
        list of numbers, they are assumed as rel. distances along the boundary
        and the list of coordinates is returned. In all other cases, a list of
        rel.  distances is returned.

        To get a list of coordinates of all vertices, use self.shapely.boundary.coords.

        """
        
        whlow = where.lower()
        if where == 'boundary':
            if N == 0:
                yield self.__s.exterior.coords[0]
            else:
                try:
                    # is N an iterable?
                    iterator = iter(N)
                except TypeError:
                    # N is not iterable, assume it is a number convertable to integer.
                    dl = 1./N
                    for i in range(int(N)):
                        yield i*dl
                else:
                    # yes, it is.
                    boundary = self.__s.boundary # not exterior!
                    for n in iterator:
                        assert 0 <= n <= 1, 'rel.length must be in [0, 1] but recieved {}'.format(n)
                        p = boundary.interpolate(n, normalized=True)
                        yield p.coords[0]
        elif whlow in ['lines', 'arcs', 'segments']:
            boundary = self.__s.boundary # not exterior!
            if whlow == 'lines':
                segments = self.lines
            elif whlow == 'arcs':
                segments = self.arcs
            elif whlow == 'segments':
                segments = self.lines + self.arcs
            else:
                raise ValueError("Unknown keyword 'where': {}".format(repr(where)))
            try:
                # is N an iterable?
                NI = iter(N)
            except TypeError:
                # No, N is not an iterable, assume it is a number of points in each segment
                def qqq(n):
                    while True:
                        yield n
                NI = qqq(N)# iter( [N]*len(segments) )

            if where[0].isupper():
                Imin = 0
            else:
                Imin = 1
            if where[-1].isupper():
                Imax = 1
            else:
                Imax = 0

            for (n, s) in zip(NI, segments):
                if s.length > 0:
                    dl = 1./(n+1)
                    for i in range(Imin, n+1+Imax):
                        length = i*dl
                        p = s.interpolate(length, True)
                        l = boundary.project(p, True)
                        yield l # p.coords[0]
        else:
            raise ValueError('Unsupported type of segments: {}'.format(repr(where)))

    def buffer(self, shiftx=0., shifty=0., thickness=0., resolution=16):
        """
        Returns a copy of self shifted by shiftx, shifty and increased in
        dimensions by thickness.

        Thickness can not be negative (while in the shapely.buffer it can).
        """
        newdef = []
        assert thickness >= 0
        for d in self.__d:
            nd = translate(d, shiftx, shifty) 
            if thickness == 0 and d.geom_type is 'Point':
                nd = nd
            else:
                nd = nd.buffer(thickness, resolution)
            newdef.append(nd)
        return self.__class__(newdef, orientation=self.__o)



# Some class methods below assume optional arguments as functions. These
# definitions are used as default values:

def _trivial_true(*args):
    """
    Returns always True
    """
    return True

def _trivial_false(*args):
    """
    Returns always False
    """
    return False

def _trivial(arg):
    """
    Returns the argument, without any modifications.
    """
    return arg


class Bundle(object):
    """
    Represents a bundle of rods and other bundles. Characterized by a polygonal
    wall of finite thickness.

    A bundle can be filled with other objects (rods and/or bundles), i.e. is a
    container.  To add an object to the container, add a tuple (obj, rel) to
    the .interior list attribute, where obj is the object to be added, and rel
    is an instance of Relations() class that describes properties of the
    connection between the container and inserted object.
    """
    @classmethod
    def box(cls, ll=(0,0), ur=(1,1), r=0., resolution=16, orientation=1):
        """
        Returns an box with sides parallel to axes with lower left corner at ll and
        upper right corner at ur, with r -- radius of the rounded corners.

        If r is positive, the dimensions of the box are bigger than that defined by ll and ur.
        
        If negative, the dimensions of the box are defined by ll and rr.
        """
        x1, y1 = ll
        x2, y2 = ur

        dr = 0.
        if r < 0: 
            r = -r
            dr = r
        s1 = Point((x1+dr, y1+dr)).buffer(r, resolution=resolution)
        s2 = Point((x1+dr, y2-dr)).buffer(r, resolution=resolution)
        s3 = Point((x2-dr, y2-dr)).buffer(r, resolution=resolution)
        s4 = Point((x2-dr, y1+dr)).buffer(r, resolution=resolution)
        b = cls()
        b.iwall = RPoly([s1, s2, s3, s4], orientation=orientation)
        return b

    # @classmethod
    # def regular_polygon(cls, origin=(0,0), R=1, N, r=0., resolution=16, orientation=1):
    #     """
    #     Returns regular polygon with radius R and N vertices, rounded with radius r, with center located at origin.
    #     """
    #     from trageom import Vector3, pi
    #     o = Vector3(car=(origin[0], origin[1], 0))
    #     v = Vector3(cyl=(R, 0, 0))



    def __init__(self):
        """
        Bundle is a holder of bundle properties. During initialization time
        nothing happens.

        Computation of subchannels and their properties are triggered by
        respective methods.
        """
        self.__iw = None
        self.__v = [] # list of rel.lengths to define points on the inner wall for triangulation.
        self.__wt = 0.

        self.gtype = 'b' # read-only

        self.color = 'green'

        self.interior = []
        return

    @property
    def iwall(self):
        """
        An instance of RPoly class that describes the form of the bundle's inner wall.
        """
        return self.__iw

    @iwall.setter
    def iwall(self, value):
        self.__iw = value

    @property
    def vertices(self):
        """
        A list of rel. lenghts along the inner wall (iwall property) perimeter that
        defines trinagulationpoints on the inner wall.

        Proprety itself is read-only, but elements of the can be added/removed arbitrarily.
        """
        return self.__v

    @property
    def wt(self):
        """
        The wall thickness.
        """
        return self.__wt
    @wt.setter
    def wt(self, value):
        self.__wt = float(value)

    def owall(self, x, y):
        """
        Returns an instance of the RPoly() class that describes the outer
        wall's shape of the bundle.

        The outer wall is defined by the inner wall's shape, see iwall
        property, and the wall's thickness, see wt property.

        Arguments x and y are coordinates of self in its container. Note that
        the outer wall shape is needed only to triangulate the container, thus
        these arguments are always needed.

        """
        if self.iwall is None:
            return None
        else:
            t = self.wt
            return self.iwall.buffer(x, y, t)

    def shapely(self, key=None):
        """
        Returns shapely representation of the interior object specified by key
        in c.s. of self.

        If key is None (by default), returns the objects inner wall shapely
        representation.

        If key is an iterable, this is a key specifying the child. Returns
        shapely representation of this child in c.s. of self.

        If key is an instance of the Relation class, returns shapely
        representation of self shifted according to key.
        """
        if key is None:
            return self.iwall.shapely
        elif isinstance(key, Relation):
            return self.owall(key.x, key.y).shapely
            # return translate(self.iwall.shapely, key.x, key.y)
        else: 
            # assume key is a list or a tuple of indices.
            if len(key) == 0:
                return self.owall(0,0).shapely
            else:
                x, y = 0., 0.
                c = self
                for (c, r) in self.branch(key):
                    x += r.x
                    y += r.y
                s = c.shapely([])
                return translate(s, x, y) 


    def iterate(self, order='breadth-first'):
        """
        Returns a generator that iterates over all model's elements,
        recursively.

        Returned values are tuples (key, i, p), where key is a tuple of
        indices, i is the interior object and p its relation to the container.

        Optional argument order is a string that can take one of the following values:

            * 'breadth-first' (default)
            * 'pre-order'
            * 'post-order'

        Meaning of order names see in
        http://en.wikipedia.org/wiki/Tree_traversal.
        """
        if order == 'breadth-first':
            queue = list(enumerate(self.interior))
            while queue:
                nip = queue.pop(0)
                key = nip[:-1]
                i, p = nip[-1]
                yield key, i, p
                for n, ip in enumerate(i.interior):
                    queue.append( key + (n,) + (ip,))
        elif order == 'pre-order':
            for n, ip in enumerate(self.interior):
                yield (n,), ip[0], ip[1]
                for key, i, p in ip[0].iterate(order):
                    yield (n,) + key, i, p
        elif order == 'post-order':
            for n, ip in enumerate(self.interior):
                for key, i, p in ip[0].iterate(order):
                    yield (n,) + key, i, p
                yield (n,), ip[0], ip[1]
        else:
            raise TypeError('Unknown order ', order)

    def check(self, recursive=False):
        """
        Checks all interior elements recursively.
        """
        for key, i, p in self.iterate():
            # existence of .interior and .iterate attributes checked by iterate()
            
            # check for self inclusion:
            if self is i:
                raise ValueError('Self inclusion ', key)
            # check that p is correct:
            try:
                p.check()
            except Exception as e:
                print 'Error in relation of element {}'.format(key)
                raise e

            # check recursively:
            if recursive:
                try:
                    i.check(recursive)
                except Ecxeption as e:
                    print 'Error in element {}'.format(key)
                    raise e

    def element(self, key):
        """
        Returns the model's element defined by the key -- list of indices.
        """
        for ip in self.branch(key):
            pass
        return ip

    def branch(self, key):
        """
        Returns a generator that iterates from self down to the
        element defined by the key.

        In other words, iterates over all parents of the element defined by the key,
        starting from self.
        """
        r = (self, None)
        for i in key:
            r = r[0].interior[i]
            yield r


    def xy(self, key):
        """
        Returns the coordinate of model's element defined by key with respect to self.

        The tuple (x, y) is returned.
        """

        x = 0.
        y = 0.
        for i, p in self.branch(key):
            x += p.x
            y += p.y
        return (x, y)
            

    def copy(self, filter_=_trivial):
        """
        Returns a copy of self. 

        The returned copy is filled with the original's interiors filtered
        through the filter_ function.
        
        By default, filter_ is trivial, i.e. filter_(arg) -> arg, this means
        that the returned copy is a shallow copy containing the same interior
        elements as the origin.
        
        The relations are always new objects.
        """
        new = self.__class__()
        new.__iw = self.__iw
        new.__wt = self.__wt
        new.__v = self.__v[:]
        new.color = self.color
        for ip in self.interior:
            i = filter_(ip[0])
            p = ip[1].copy()
            new.interior.append((i, p))
        return new

    def __str__(self):
        return 'Bundle(wt={})'.format(self.wt)

    def plot(self, x=0, y=0, axis=None, color=None, order='iopt', alpha=0.7):
        """
        Plots own wall and own content to the axis.

        Characters for order:

            i: inner wall
            o: outer walls
            p: triangulation points,
            t: triangle boundaries.
            c: subchannels.

        """

        # some parameters to make picture better.
        lw = 0.1 # linewidth
        pr = 0.005 # with respect to the model
        bx,by,bX,bY = self.shapely([]).bounds
        bx += x
        bX += x
        by += y
        bY += y
        pr = max(bY-by, bX-bx)*pr

        if color is None:
            clr = self.color
        else:
            clr = color

        for o in order:
            if o == 'i':
                # the inner wall's line:
                l = translate(self.shapely().boundary, x, y)
                axis = ShapelyToAxis(l, axis=axis, indices='', label='', order='i', color=clr, thickness=lw, alpha=alpha )

            elif o == 'o':
                # outer boundaries of the interior objects:
                for (i, r, s, cover) in self.visible_interior():
                    if cover is None:
                        axis = ShapelyToAxis(translate(s, x, y), axis=axis, indices='', label='', order='b', color=clr, thickness=lw, alpha=alpha)

            elif o == 'p':
                # plot own triangulation points:
                for (px, py) in self._vertices():
                    axis = ShapelyToAxis(Point((x+px, y+py)), axis=axis, indices='', label='', color=clr, thickness=pr, alpha=alpha)

            elif o == 't':
                # plot own triangles:
                t = self.own_triangulation()
                axis = ShapelyToAxis(t.sMultiLine(x, y), axis=axis, indices='', label='', color=clr, thickness=lw/2., alpha=alpha*uniform(0.5, 0.8), order='i')

            elif o == 'c':
                # plot subchannels:
                for sc in self.own_subchannels():
                    axis = ShapelyToAxis(translate(sc, x, y), axis=axis, indices='', label='', order='i', color=clr, thickness=lw, alpha=alpha*uniform(0.5, 0.8))
            
            else:
                raise ValueError('Unknown order character, ', o)

        # call recursively:
        rorder = order.replace('p','')
        rorder = rorder.replace('t', '')
        rorder = rorder.replace('c', '')
        for (i, r, s, cover) in self.visible_interior():
            if cover is None:
                i.plot(r.x+x, r.y+y, axis=axis, color=color, order=rorder, alpha=alpha/2.)
        return axis

    def visible_interior(self):
        """
        Iterates over interior bundles and rods. Returned elements are tuples
        (i, r, s, c), where i is the interior object, r its relation to the
        bundle, s -- its shapely representation in the bundle, c -- covering
        object: if i is visible, c is None; if i is outside the bundle's
        internal wall, c is -1; if i is covered by an interior bundle, c is the
        index (nonnegative) of that binterior bundle.

        A rod is visible if it is within the iwall and not covered by any of
        the bundles.

        A bundle is visible if it is within the iwall.
        """
        # shapely representation of iwall
        iwall = self.iwall.shapely

        # list of bundles:
        bundles = {} 
        self.__bundles = bundles # this dict will be needed in own_subchannels()
        Nb = 0
        for (c, r) in self.interior:
            if c.gtype == 'b':
                sh = c.shapely(r)
                if sh.within(iwall):
                    cover = None
                else:
                    cover = -1
                bundles[Nb] = (sh, cover)
            Nb += 1

        # list of rods
        for i, (c, r) in enumerate(self.interior):
            if c.gtype == 'r':
                sh = c.shapely(r)
                if sh.within(iwall):
                    cover = None # cover  = True
                    for Nb, (bs, bc) in bundles.items():
                        if bs.intersection(sh):
                            cover = Nb
                            break
                else:
                    cover = -1
                yield (c, r, sh, cover)
            else:
                sh, cover = bundles[i]
                yield (c, r, sh, cover)



    def _vertices(self, relation=None):
        """
        Returns an iterator over triangulation points. Yields tuples (x,y).

        If relation is None (default), returns the list of points necessary for
        own channels triangulation.

        Otherwise (relation must be an instance of the Relation class), returns
        points on the self's outer wall necessary to triangulate the container.
        """

        if relation is None:
            self.__po = [] # point origins: list of interior object index that caused the triangulation point. 
            # points from own internal wall:
            wall = self.iwall.shapely.boundary
            for rl in self.vertices:
                p = wall.interpolate(rl, True)
                c = p.coords[0]
                self.__po.append(self)
                yield c 

            # points from interior objects:
            Ni = 0
            for (i, r, s, cover) in self.visible_interior():
                for c in i._vertices(r):
                    self.__po.append((Ni, cover))
                    yield c
                Ni += 1
        else:
            # return points on the outer wall for 
            # the container's triangulation
            x = relation.x
            y = relation.y
            wall = self.owall(x, y).shapely.boundary
            for rl in relation.vertices:
                p = wall.interpolate(rl, True)
                c = p.coords[0]
                yield c

    def own_triangulation(self):
        """
        Returns an instance of the Triangulation() class that represents
        triangulation of the bundle.

        Note that each call to this method results in qhul run, that might be
        time consuming. Consider saving results of this method in a variable.
        """
        # collect vertices, 
        # sites = list(self._vertices())
        # return Triangulation([v for v in self._vertices()]) 
        return Triangulation( list(self._vertices()) )

    def own_subchannels(self):
        """
        Returns shapely representation of subchannels.
        """

        triang = self.own_triangulation()

        iwall = self.iwall.shapely
        for (df, ie, nb) in triang._regions:
            # create shapely representation of triangulation region:
            sp = [Point(triang._sites[i][:2]) for i in df]
            sreg = cascaded_union(sp).convex_hull

            print 'region ', df, ie, nb
            indent = ' '*8

            # subtract rods and interior bundles
            for i in df:
                po = self.__po[i]
                print indent, 'point index ', i, po
                # subtract all interior bundles:
                for (Nib, (bsh, bcov)) in self.__bundles.items():
                    sreg = sreg.difference(bsh)
                if po is self:
                    # point i is on the inner boundary of the bundle
                    print indent, 'point on the inner boundary'
                    pass
                else:
                    # point i corresponds to a rod or an internal bundle.
                    Ne, cover = po # interior's index and index of element that covers Ne
                    e, r = self.interior[Ne] # interior element and its relation
                    print indent, 'element for the point: ', e, r
                    if cover is None:
                        # element e is visible
                        if e.gtype == 'r':
                            # e is a visible rod. Substract it
                            print indent, 'substract visible rod'
                            ss = e.shapely(r)
                            sreg = sreg.difference(ss)
                        else:
                            # i is a visible internal bundle. Do nothing
                            print indent, 'point from visible inner bundle boundary'
                            pass
                    elif cover == -1:
                        # element e is outside the bundle's inner wall.
                        # 
                        print indent, 'point from rod outside the bundle iwall'
                        sreg = sreg.intersection(iwall)
                    else:
                        # cover is the index of internal bundle that
                        # covers element e.
                        pass
                        # print indent, 'point from rod covered by bundle ', cover
                        # sb = self.shapely([cover])
                        # sreg = sreg.difference(sb)
                print indent, '---'
            yield sreg

            
            
        

            


class Rod(object):
    """
    Represents a heated cylindrical rod that can be inserted into a bundle.

    A rod is characterized by its radius, internal design and material
    properties.

    Instances of this class can be inserted into a bundle together with
    instances of the Bundle() class. To ensure similar API of both classes,
    this class has some attributes that make sence for bundles but for rods are useless.
    """

    def __init__(self, radius=1):
        self.radius = radius
        self.interior = () # shouldn't be used

        self.gtype = 'r' # read-only

        self.color = 'red'
        return

    def iterate(self, order=None):
        """
        Dummy method to provide similar API to Bundle()
        """
        return []

    def check(self, recursive=True):
        """
        Dummy method, currently nothing to check
        """
        return True

    def copy(self, filter_=None):
        """
        Returns a new rod with the same properties.
        """
        new = self.__class__()
        new.radius = self.radius
        new.color = self.color
        return new

    def __str__(self):
        return 'Rod(radius={})'.format(self.radius)

    def shapely(self, key=None):
        if isinstance(key, Relation):
            return Point((key.x, key.y)).buffer(self.radius)
        else:
            return Point((0., 0.)).buffer(self.radius)

    def plot(self, x=0, y=0, axis=None, color=None, order=None, alpha=0.7):
        if color is None:
            color = self.color
        return ShapelyToAxis(Point((x, y)).buffer(self.radius*0.9), color=color, alpha=alpha, indices='', label='', axis=axis, order='i')

    def _vertices(self, relation):
        """
        Yields the triangulation points for the rod in its container.
        """
        yield (relation.x, relation.y)


class Relation(object):
    """
    Represents properties of the connection between a container (an instance of the Bundle() class)
    and an interior object (instances of Rod() or Bundle() classes).
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.__v = [] # list of rel.lengths to define points on the outer wall of correspondent interior object to triangulate container.
        return

    @property
    def vertices(self):
        """
        A list of rel. lenghts along the outer wall of the interior object, that define
        the triangulation points for the container.
        """
        return self.__v

    def check(self):
        """
        Check that relation has all necessary properties
        """
        float(self.x)
        float(self.y)
        assert all(0 <= rl <=1. for rl in self.__v)
        return

    def copy(self):
        new = self.__class__()
        new.x = self.x
        new.y = self.y
        new.__v = self.__v[:]
        new.check()
        return new

    def __str__(self):
        return 'Relation(x={}, y={})'.format(self.x, self.y)


if __name__ == '__main__':
    import resource
    print 'ru_maxrss ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # a small bundle 
    c1 = Bundle()
    c1.iwall = RPoly([Point(c) for c in Point((0,0)).buffer(0.7, resolution=1).boundary.coords])
    c1.wt = 0.3
    c1.vertices.extend([0, 0.3333, 0.6666])
    c2 = c1.copy()
    c2.iwall = c2.iwall.buffer(0,0, 0.2)

    p1 = Point(( 0,  0)).buffer(3)
    p2 = Point(( 0, 25)).buffer(3)
    p3 = Point((25, 25)).buffer(3)
    p4 = Point((25,  0)).buffer(3)

    # Assembly type 1
    a1 = Bundle() 
    a1.iwall = RPoly([p1, p2, p3, p4])
    a1.wt = 0.5
    a1.vertices.extend([0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9])
    p1 = Rod(0.8)
    p2 = Rod(1.0)
    pp = 2.5
    for i in range(10):
        for j in range(10):
            x = i*pp
            y = j*pp
            if (i,j) == (2, 3):
                p = c1
                points = [0, 0.25, 0.5, 0.75]
            elif (i,j) == (8, 9):
                p = c2
                points = [0, 0.25, 0.5, 0.75]
            elif (i+j) % 2 is 0:
                p = p1
                points = []
            else:
                p = p2
                points = []
            r = Relation(x, y)
            r.vertices.extend(points)
            a1.interior.append((p, r))
    a1.plot(order='iopc').get_figure().savefig('assembly1.pdf')

    # Assembly type 2
    p3 = Rod(1.2)
    p4 = Rod(0.6)
    c3 = c1.copy()
    c4 = c2.copy()
    c3.iwall = c3.iwall.buffer(-0.2, -0.2, 0)
    c4.iwall = c4.iwall.buffer( 0.2,  0.2, 0)
    def filter_(o):
        if o is c1:
            return c3
        if o is c2:
            return c4
        if o is p1:
            return p3
        if o is p2:
            return p4

    a2 = a1.copy(filter_)
    a2.plot().get_figure().savefig('assembly2.pdf')

    # the core:
    
    core = Bundle()
    N = 2
    ap = 33
    core.iwall = RPoly([Point(c) for c in Point((ap*N/2., ap*N/2.)).buffer(ap*(N+2)/2.).boundary.coords])
    for i in range(N):
        for j in range(N):
            x = i*ap
            y = j*ap
            if (i+j)%2 is 0:
                a = a1
            else:
                a = a2
            r = Relation()
            r.x = x
            r.y = y
            r.vertices.extend(a.owall(0,0).points(0, 'LineS'))
            core.interior.append((a, r))
    core.vertices.extend([0, 0.2, 0.4, 0.6, 0.8])
    print 'ru_maxrss ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    core.plot(order='ioptc').get_figure().savefig('core.pdf')
        
    exit()


    # iterate over all models elements:
    core.interior[10][0].interior[5][1].x = 'a'
    for c in core.iterate():
        print c[0], c[1], c[2],
        ip = core.element(c[0])
        print ip[0] is c[1], ip[1] is c[2]


    print 'ru_maxrss ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    for c in core.iterate('pre-order'):
        print c[0], c[1], c[2],
        ip = core.element(c[0])
        print ip[0] is c[1], ip[1] is c[2]

    print 'ru_maxrss ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


    # check the model:
    try:
        core.check()
    except Exception as e:
        print e
    core.element((10, 5))[1].x = 55
    # core.element(10, 5)[1].x = 'b'
    core.check()
    print 'ru_maxrss ', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    # try to create a2 as a copy of a1.
    p3 = Rod(2.11)
    p4 = Rod(2.21)
    def cond(p):
        if p is p1:
            return p3
        if p is p2:
            return p4
        else:
            return p
    a3 = a1.copy(cond)
