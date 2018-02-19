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

Counters and collections are used to represent set of indexed unique objects. 

Rationale is to make simple numeration of unique materials for MCNP input.
Particular implementation for MCNP materials is done in the mcnp.materials
module, here only basic functionality, common to collection of general objects,
is implemented.

"""
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

class Counter(object):
    """
    Generator of increasing numbers.

    >>> g = Counter(iv=1, step=1)
    >>> g.get_next()
    1
    >>> g.get_next()
    2

    where iv -- initial values, returned by the first call to the get_next() method.

    TODO: can it be replaced with simple generator (i.e. funtion with yield statement)? 

    """
    def __init__(self, iv=1, step=1):
        self.reset(iv, step)
        return

    def get_next(self):
        """
        Returns the next value equal to the previous one increased by step.
        """
        c = self.__c
        self.__c += self.__s
        return c

    def reset(self, iv=1, step=1):
        """
        Resets the generator, so that the next get() returns the initial value iv.
        """
        self.__c = iv
        self.__s = step

    @property
    def step(self):
        """Step. 
        
        Can be set only when new generator initialized or with the reset() method.
        """
        return self.__s




class Collection(object):
    """
    Parent class for collections.

    This class represents a collection of different objects, each of them
    having an index. An object is added to the collection by the index() method,
    which takes the object as the argument and returns its index. If the object
    is allready in the collection, it is not added again.

    >>> c = Collection(iv=1, step=1)
    >>> c.index('a')
    1
    >>> c.index('b')
    2
    >>> c.index('a')
    1
    >>> c.items()
    {1: 'a', 2: 'b'}
    """
    def __init__(self, iv=1, step=1):
        """Initializes new collection.

        iv: initial value, the first elements index.
        step: step for indices.
        """
        self.__c = Counter()
        self.clear(iv, step)
        return

    def clear(self, iv=1, step=1):
        """Resets collection.

        Resets the indexing counter and removes previously added items.
        """
        self.__c.reset(iv, step)
        self.__d = {}
        return

    def index(self, o):
        """Returns index of object o.

        If o is not in the collection, it is added and new index for this object is generated.
        """
        return NotImplemented

    def items(self):
        """Returns all collection items.

        Retrned is a dictionary with indices as keys and objects as values.
        """
        return self.__d.items()

    def keys(self):
        """Returns set of indices of allready added objects.
        """
        return self.__d.keys()

    def values(self):
        """Returns set of objects, allready in the collection.
        """
        return self.__d.values()

    def _add(self, value, mapping=lambda x:x):
        k = mapping(self.__c.get_next())
        self.__d[k] = value
        return k

    def _find(self, obj):
        """Returns index of object obj.

        If obj is not in the collection, None is returned.
        """
        for (k, v) in self.__d.items():
            if v == obj:
                return k
        return None

    def __getitem__(self, index):
        """
        Returns the item stored in the collection under index.
        """
        return self.__d[index]


class SimpleCollection(Collection):
    """
    Example class based on Collection.
    """
    def index(self, obj):
        """Returns index of obj.

        If obj is not in the collection, it is added with a unique index.
        """
        # if obj allready in the collection, return its index
        k = self._find(obj)
        if k is None:
            k = self._add(obj)
        return k


