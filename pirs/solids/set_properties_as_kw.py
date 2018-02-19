
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

class SetPropertiesAsKW(object):

    """
    Class that defines neseccary methods to pass optional keyword arguments
    to the constructor.
    """
    def __init__(self, **kwargs):
        """
        The method shows the structure of the __init__ method of the children
        classes.

        """
        # first set attribute/property default values:
        # ...

        # second, call the setp() method:
        self.setp(**kwargs)
        return

    def setp(self, **kwargs):
        """
        Set attributes and properties specified in the keyword arguments.

        If an attribute or a property does not exist, the AttributeError is
        raised.
        """
        for (name, value) in kwargs.items():
            if name[:2] != '__':
                if name in self.__dict__.keys():
                    # name is an attribute?
                    setattr(self, name, value)
                elif name in self.properties():
                    # name is a property?
                    setattr(self, name, value)
                else:
                    raise AttributeError('Cannot set ', (name, value))
        return

    @classmethod
    def properties(cls):
        """
        Returns a list of property names defined in the class, including all
        inherited properties.
        """
        # own properties
        res = [n for (n, v) in cls.__dict__.items() if type(v) is property]
        # proerties of parent classes 
        for par in cls.__bases__:
            try:
                res += par.properties()
            except AttributeError:
                # do not take into account properties of the parent that has no
                # properties() method.
                pass
        return res


if __name__ == '__main__':

    class C2(SetPropertiesAsKW):
        def __init__(self, **kwargs):
            self.a2 = 'c2.a2'
            self.__p2 = 'c2.p2'

            self.setp(**kwargs)

        @property
        def p2(self):
            return self.__p2

        @p2.setter
        def p2(self, value):
            self.__p2 = value


    class C3(C2):
        def __init__(self, **kwargs):
            super(C3, self).__init__()
            self.a3 = 'c3.a3'
            self.__p3 = 'c3.p3'
            self.setp(**kwargs)
            return

        @property
        def p3(self):
            return self.__p3

        @p3.setter
        def p3(self, value):
            self.__p3 = value



    # check C2
    c21 = C2()                     # no args
    c22 = C2(a2='a2m', p2='p2m')   # existing attributes
    try:                           # non-existing attributes
        c23 = C2(n2='a3m')
    except AttributeError as e:
        print e
    c21.n2 = 'n2'                  # dynamically created attribute is Ok.
    c21.setp(n2='n2m')

    # check C3
    c31 = C3()                     # no args
    c32 = C3(a2='a2m', p2='p2m')   # inherited attributes
    c33 = C3(a3='a3m', p3='p3m')   # own attributes
    try:                           # non-existing attributes
        c33 = C2(n3='a3m')
    except AttributeError as e:
        print e
    c31.n3 = 'n3'                  # dynamically created attribute is Ok.
    c31.setp(n3='n3m')

