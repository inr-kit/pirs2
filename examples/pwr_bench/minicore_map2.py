from pirs.tools import LoadMap
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


m = LoadMap()
m.string = """
    $3
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  G  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1
"""
m.origin = m.tindex('G')
m.rdict['G'] = 'c'
m.rdict['g'] = 'c'
# m.rdict['i'] = 'u'

if __name__ == '__main__':
    print m.string
