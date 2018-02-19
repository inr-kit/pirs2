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

Pseudo-graphics input of the assembly map.
"""


# g -- guide tube
# u -- uox pins
# i -- ifba pins
# c -- control rods or guide tubes

# map with guide tubes and IFBA pins
map_string1 = """
    i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i 
    u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u 
    u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u 
    u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u 
    u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u 
    u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u 
    u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
    u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
    u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u 
    u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
    u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
    u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u 
    u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u 
    u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u 
    u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u 
    u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u 
    i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i 
    """

# map with guide tubes, without IFBA
map_string2 = """
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  c  u  u  c  u  u  c  u  u  u  u  u 
    u  u  u  c  u  u  u  u  u  u  u  u  u  c  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  c  u  u  c  u  u  c  u  u  c  u  u  c  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  c  u  u  c  u  u  g  u  u  c  u  u  c  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  c  u  u  c  u  u  c  u  u  c  u  u  c  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  c  u  u  u  u  u  u  u  u  u  c  u  u  u 
    u  u  u  u  u  c  u  u  c  u  u  c  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    """

# trivial map, only usual pins
map_string3 = """
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u 
    """

# for mox assembly, with 3 fuel materials.
# g:  guide tube 
# w:  WABA pin
# m1, m2, m3: mox fuels
map_string4 = """
   m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1 
   m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1 
   m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2 
   m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2 
   m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
   m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2 
   m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2 
   m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1 
   m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1 
    """

# what map is modelled.The map_string2 was 
# used to get results for D1.4, part II.
map_string = map_string2

def str2dict(mlstring):
    map_dict = {}
    j = 0
    for l in reversed(mlstring.splitlines()):
        row = l.split()
        if len(row) > 0:
            i = 0
            for e in row:
                map_dict[(i,j)] = e
                i += 1
            j += 1
    return map_dict

map_dict = str2dict(map_string)

