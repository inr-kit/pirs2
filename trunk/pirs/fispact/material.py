"""
Classes to describe FISPACT material composition.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from ..core import tramat


class Material(tramat.Mixture):
    """
    Object-oriented representation of material composition for FISPACT.

    Constructor arguments are passed to the constructor of the parent class, see
    description of available arguments there.

    One can setup material composition.
    """
    def __init__(self, *args, **kwargs):
        super(Material, self).__init__(*args, **kwargs)
        self.__fmt = {}
        self.__fmt['zaid'] = '{0}'
        self.__fmt['fraction'] = '{0:12.5e}'

    def copy(self):
        new = super(Material, self).copy()
        new.__fmt = self.__fmt
        return new

    @property
    def fmt(self):
        """
        Dictionary of format strings used to generate card representation of the
        material.

        The following keys have sense:

        'zaid': format string for ZAIDs
        'fraction': format string for fraction.

        If explicit field index is used (for Python versions < 2.6), it should
        be set to 0.
        """
        return self.__fmt

    def card(self, comments=True, sort=False):
        """
        Returns a multi-line string for input file.

        """
        cmnt = '<< {} >>'.format
        res = []
        if comments:
            res.append(cmnt('Material ' + self.name))
        res.append('DENSITY {}'.format(self.dens))
        # Representation by `FUEL` keyword
        me = self.expanded()
        for n, a in me.recipe(1):
            l = '{} {}'.format(n.name.replace('-', ''), a.v)
            res.append(l)
        res.insert(0, 'FUEL {}'.format(len(res)))
        return res

    def __eq__(self, othr):
        """
        Redefinition of the tramat.Mixture.__eq__ method!
        """
        if self is othr:
            return True

        if isinstance(othr, Material):
            return (self.recipe() == othr.recipe() and
                    self.__fmt == othr.__fmt)
        else:
            return False
