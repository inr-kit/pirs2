
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

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


from numpy.linalg import solve as NLsolve
from numpy import column_stack, array

from .vector import _are_close

class Plane(object):

    @classmethod
    def normal(cls, p, n):
        """
        return plane instance, which normal is n and which goes through point p.
        """
        # ensure that n is a vector and normalize it
        n = Vector3( n )
        n.R *= 1./n.R

        # set v1 arbitrarily, but v1 perpendicular to n:
        v1 = n._arbitrary_normal()
        # define v2 as [n,v1]:
        v2 = n.cross(v1)

        return cls(p, v1, v2)


    def __init__(self, p, v1, v2):
        """
        Define plane that goes through point p spanned on vectors v1 and v2.
        """
        self.p = Vector3(p)

        self.v1 = Vector3(v1)
        self.v2 = Vector3(v2)

    def __getattr__(self, name):
        if name == 'n':
            v1 = self.v1.copy()
            v2 = self.v2.copy()
            v1.R = 1.
            v2.R = 1.
            return v1.cross(v2)
        else:
            return self.__dict__[name]

    def _project_point(self, P, cs='local'):
        """Return coordinates of the projection of P onto plane.
        
        If cs='local', return 2d coordinates in the basis {self.v1, self.v2}. 
        Otherwise return 3d coordinates in the general basis."""
        # third vector
        v3 = self.n

        # coordinates of P can be represented using vectors v1, v2 and v3 and point self.p
        # as
        #    P = p + x*v1 + y*v2 + z*v3
        # where x, y and z are coordinates of P in the basis {v1,v2,v3}:

        xyz = _coord_transform( (Vector3(P) - self.p).car,   self.v1, self.v2, v3)
        xyz = xyz.car

        if cs == 'local':
            return (xyz[0], xyz[1])
        else:
            return self.p + self.v1*xyz[0] + self.v2*xyz[1]


    def is_in_plane(self, P):
        """
        plane contains other plane, if they coincide. They
        coincide if their normals are parallel and they have a 
        common point.
        """            
        return self.n.is_parallel(P.n) and self.p.is_in_plane(P) 


    def contains(self, othr):
        """
        return True if othr lies in the plane.

        This method calls is_in_plane method of othr.
        """

        return othr.is_in_plane(self)


    def distance(self, othr):
        return othr.distance_to_plane(self)


    def distance_to_plane(self, P):
        """if self and plane P are parallel, return distance. Othrewise, none"""
        if self.n.is_parallel(P.n):
            return self.p.distance_to_plane(P)
        else:
            return None

    def _intersect_with_plane(self, P, cs=''):        
        """Return intersection of two planes self and P.
        
        If they coincide, return one of them. 
        
        Otherwise, if they are not parallel, find the intersection
        line.
        
        cs is a string representing coordinate system in which the result is returned.
           ''      -- c.s. in which self and P are specified.
           'local' -- c.s. with basis vectors self.v1 and self.v2
           'plane' -- c.s. with basis vectors of the plane P
        """
        if cs != '':
            return NotImplemented

        if self.contains(P):
            return P
        elif not self.n.is_parallel(P.n):
            # There must be an intersection line. Its direction must be 
            # perpendicular to both plane normals.
            v = self.n.cross(P.n)
            # Common point can be found using the algorithm of 
            # plane with line intersection.
            # Point self.p and vector [self.n, v] define a line, which 
            # intersects P in point P1'. Similarly, point P.p and
            # vector [P.n, v] define another line, which intersect 
            # self at P2'. P1' and P2' both valid answers. For symmetry,
            # I will use the point between, P' = (P1'+P2')/2.
            p1 = Line(self.p, self.n.cross(v))._intersect_with_plane(P) 
            p2 = Line(P.p, P.n.cross(v))._intersect_with_plane(self) 
            p = (p1+p2) * 0.5
            return Line(p, v)
        else:
            return None

    def intersect(self, othr):
        """return intersection of self with othr.  
        
        Allways call _intersect_with_plane() method of the othr instance."""

        return othr._intersect_with_plane(self)


class Line(object):
    def __init__(self, p, v):
        """Line along vector v through point p"""
        self.p = Vector3( p )
        self.v = Vector3( v )

    def distance_to_plane(self, P):
        """If self is parallel to plane P, return distance from
        arbitrary point on the line to its projection onto P"""
        if P.n.is_perpendicular(self.v):
            return self.p.distance_to_plane(P)
        else:
            return None

    def _intersect_with_plane(self, P):
        """
        return intersection of line with plane P.

        If the line lies in the plane, return the line
        itself.  If the line is not parallel to the plane, find the
        intersection point.
        """            
        if P.contains(self):
            return self
        elif not self.v.is_perpendicular(P.n):
            # the line is not parallel to the plane, there
            # is an intersection point.
            # 
            # Intersection point is found from the
            # following system: Any point on the line is
            # given by chosing z in the expression
            #     self.p + z*self.v
            # This point must be also represented in P as
            #     P.p + x*P.v1 + y*P.v2
            # The system is:
            #     self.p - P.p = x*P.v1 + y*P.v2 - z*self.v
            # This system can be interpreted as searching 
            # coordinate transformation to the basis {v1, v2, -v}
            xyz = _coord_transform( self.p-P.p,
                        P.v1, P.v2, -self.v)
            xyz = xyz.car
            return self.p + xyz[2]*self.v
        else:
            return None

    def is_in_plane(self, P):
        """
        plane contains a line if (1) line is perpendicular to
        the normal of the plane, and (2) arbitrary point on the
        line belongs also to the plane.
        """            
        return ( self.v.is_perpendicular(P.n) and 
             self.p.is_in_plane(P))

        


class Sphere(object):
    def __init__(self, p, R):
        """Define a sphere at position v with radius R"""
        self.p = Vector3(p)
        self.R = float(R)

    def _intersect_with_plane(self, P):
        """return circle if P intersects self. Otherwise, return none"""

        # circle's center is a projection of the sphere's center onto plane
        cntr = P._project_point(self.p, cs='')
        # distance from sphere's center to the plane:
        dist = (self.p - cntr).R
        if dist <= self.R:
            # if distance from sphere's center to plane P less than self.R, return circle,
            # which is an ellipse with equal r1 and r2
            r = (R**2. - dist**2.)**0.5
            return Ellipse(cntr, P.v1, P.n.cross(P.v1), r, r)
        else:
            return None

    def distance_to_plane(self, P):
        return self.p.distance_to_plane(P)

class Cylinder(Line):
    def __init__(self, p, v, r):
        """define cylinder with axis along Line(p,v) with radius r"""
        # call Line initialization
        super(Cylinder, self).__init__(p, v)
        # save cylinder radius to the length of v:
        self.v.R = float(r)

    def _intersect_with_plane(self, P):
        """return line, two parallel lines, ellipse or none"""
        dist = self.distance_to_plane(P)
        if dist == None:
            # If cylinder's axis not parallel to P, dist is none.
            # In this case return an ellipse Ellipse center is at
            # the intersection of the cylinder's axis with P.
            cnt = super(Cylinder, self)._intersect_with_plane(P)

            # Below I use P.n several times,
            # just compute it once:
            Pn = P.n
            if self.v.is_parallel(Pn):
                # if cylinder axis is perpendicular to the plane normal,
                # use plane's v1 as ellipse 1-st vector
                v1 = P.v1.copy()
                v2 = Pn.cross(v1)
                r1 = r2 = self.v.R
            else:
                # vector product [self.v, P.n] gives direction of the
                # short ellipse axis: 
                v2 = Pn.cross(self.v)
                v1 = v2.cross(Pn)
                # ellipse radii
                r2 = self.v.R
                r1 = r2 * (self.v.R*Pn.R/self.v.dot(Pn))
            return Ellipse(cnt, v1, v2, r1, r2)
        elif _are_close(dist, self.v.R):
            # plane P only touches the cylinder. Return one line
            return Line( P._project_point(self.p, cs=''), self.v )
        elif dist < self.v.R:
            # return two lines. 
            p = P._project_point(self.p, cs='')
            # shift vector:
            sv = self.v.cross(P.n)
            sv.R = (self.v.R**2. - dist**2)**0.5
            l1 = Line( p+sv,  self.v )
            l2 = Line( p-sv, -self.v )
            return (l1, l2)
        else:
            return None


class Ellipse(Plane):        
    def __init__(self, p, v1, v2, r1, r2):
        """ Ellipse with center at position p, one axis along vector v1
        has radius r1, the other axis is along vector v2 ahs radius
        r2"""
        if v1.is_perpendicular(v2):
            super(Ellipse, self).__init__(p, v1, v2)
        else:
            raise ValueError(v1, v2, ' must be perpendicular')

        self.v1.R = r1
        self.v2.R = r2

    def intersect(self, othr):
        return NotImplemented


    def _intersect_with_plane(self, P):
        """return intersection of the ellipse with a plane.
        
        Can return one point, or two points, or none."""
        # If self lies in P, return Ellipse itself. Otherwise, if P and
        # self not parallel, find point(s) of intersection
        if self.is_in_plane(P):
            return self
        elif not self.n.is_parallel(P.n):
            # Ellipse and plane can intersect. Find the intersection line of the ellipse' plane with P.
            # This line lies in the ellipse' plane so the intersection of the line with ellipse
            # can be searched in 2d space on the ellipse plane.

            # to find the intersection line, call the base class method
            L = super(Ellipse, self)._intersect_with_plane(P)

            # 2d coordinate vectors on the ellipse plane:
            i = self.v1.copy() / self.v1.R
            j = self.v2.copy() / self.v2.R

            # meaning of the following see in the draft from 21.03.12
            x0 = (L.p - self.p).dot(i)
            y0 = (L.p - self.p).dot(j)
            a = L.v.dot(i)
            b = L.v.dot(j)
            r1 = self.v1.R
            r2 = self.v2.R
            D = (r1*r2)**2. * ( 2.*x0*y0*a*b - (b*x0)**2. - (a*y0)**2. + (r1*b)**2. + (r2*a)**2. )

            if D < 0.:
                # there are no intersection points
                return None
            else:
                # there are two intersection points, which may coincide
                AA = x0*a*r2**2. + y0*b*r1**2.
                BB = (b*r1)**2. + (a*r2)**2.
                xi1 = (  D**0.5  -  AA ) / BB
                xi2 = ( -D**0.5  -  AA ) / BB

                return (L.p + xi1*L.v, 
                    L.p + xi2*L.v)
        else:
            return None




def _coord_transform(P, v1, v2, v3):
    """return coordinates of point P in the basis {v1, v2, v3}

    P can be represented as superposition of v1, v2 and v3:

        P = a1*v1 + a2*v2 + a3*v3
    
    substituting in this vector equation vectors with their coordinates
    one gets a system of linear equations

        P = M a,
    
    where columns of matrix M are vectors v1, v2 and v3. This system is solved by numpy.linalg.solve()
    """
    M = column_stack( ( array( Vector3(v1).car ), 
                        array( Vector3(v2).car ), 
                        array( Vector3(v3).car ) ) )

    a = NLsolve(M, array( Vector3(P).car ) )

    return Vector3( a )



