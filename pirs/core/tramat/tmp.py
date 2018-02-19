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

Example of a Class whose constructor does not necessarily creates a new instance.
"""

class __MyClass(object):
    def __init__(self, name):
        self.name = name


def MyClass(obj):
    # call class constructor only when necessary.
    if isinstance(obj, __MyClass):
        return obj
    else:
        return __MyClass(obj)

# try the game:
m1 = MyClass(1)
m2 = MyClass(m1)
m3 = MyClass(2)

for m in [m1, m2, m3]:
    print m, m is m1

"""
Drawback of the above approach is that in the python interpreter one will see MyClass as a function, and will not access help on attributes of __MyClass.
"""


class MyClass2(object):
    # with modified __cls__

    # Condition used both in new and in init methods
    @classmethod
    def __new_necessary(cls, args):
        """
        args -- positional arguments passed to the constructor, 
        """
        if len(args) <= 2 and isinstance(args[0], cls):
            return False
        else:
            return True

    def __new__(cls, *args):
        # if args contains only one element of MyClass object, simply return it and
        # modify args so that nothing is done in __init__
        if cls.__new_necessary(args):
            res = super(MyClass2, cls).__new__(cls, *args)
        else:
            res = args[0]
        print 'new', args, repr(res)
        return res

    def __init__(self, *args):
        if self.__new_necessary(args):
            self.args = args
        else:
            pass
        print 'init', repr(self), repr(self.args)

    def __str__(self):
        return '<MyClass2 {}'.format(self.args)

"""
This pattern works, but it is necessary to ensure that the same condition is applied both in __new__ and in __init__ methods. This is done
by defining the __new_necessary method.
"""

m1 = MyClass2(1, 2, 3, 4)
m2 = MyClass2(m1)
m3 = MyClass2(m1, 2, m1, 4)


