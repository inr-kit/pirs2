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

Classes to represent MCNP cells.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

from .surfaces import Volume, Surface
from .material import Material            # for checks only
from . import formatter


def _fill_entries(fillstr):
    # assumes that fillstr is a string
    vals = fillstr.split(':')
    Imin = int(vals[0])
    Imax, Jmin = map(int, vals[1].split())
    Jmax, Kmin = map(int, vals[2].split())
    array = vals[3].split()
    Kmax = int(array.pop(0))
    return ([Imin, Imax, Jmin, Jmax, Kmin, Kmax], array)

class CellOpts(dict):
    """A dictioary to store cell options. 
    
    This is a dictionary that allows only particular string keys. Additionally,
    its string representation can be used directly in the input file within
    cell card.

    """
    #: tuple of valid cell option names.
    VALIDKEYS = ('imp:n', 'u', 'fill', 'tmp', 'lat')

    def __setitem__(self, key, value):
        """
        Check additionally that key is a valid MCNP cell option
        """
        k = key.lower()
        if k not in self.VALIDKEYS:
            raise KeyError('Wrong key ', key)
        super(CellOpts, self).__setitem__(key, value)

    def __str__(self):
        res = ''
        for (k, v) in sorted(self.items(), key=lambda x: x[0]):
            if k in ['u', 'fill', 'lat', 'tmp'] and v == 0:
                # do not print default values.
                pass
            else:
                if k == 'tmp':
                    v *= 8.617343e-11 
                    if hasattr(v, 'nominal_value'):
                        # v is of uncertanties.ufloat type. Only its nominal 
                        # value is needed:
                        v = v.nominal_value
                    elif isinstance(v, tuple) and len(v) == 2:
                        v = v[0]
                    fmt = '{0}={1:12.6e} '
                elif k == 'fill' and isinstance(v, str) and ':' in v:
                    # if fill array is given, represent it by multiline
                    # vals = v.split(':')
                    # Imin = int(vals[0])
                    # Imax, Jmin = map(int, vals[1].split())
                    # Jmax, Kmin = map(int, vals[2].split())
                    # array = vals[3].split()
                    # Kmax = int(array.pop(0))
                    ([Imin, Imax, Jmin, Jmax, Kmin, Kmax], array) = _fill_entries(v)
                    fmt = ' fill={0}:{1} {2}:{3} {4}:{5}'.format(Imin, Imax, Jmin, Jmax, Kmin, Kmax)
                    # check that fill array has seferal universes. Otherwise represent it using repetition syntax
                    if len(set(array)) == 1:
                        if len(array) > 1:
                            fmt += ' {0} {1}R'.format(array[0], len(array)-1)
                        else:
                            fmt += ' {0}'.format(array[0])
                    else:
                        ef = '{{0:>{0}}}'.format(max( map(len, array)) + 1) # formatter for fill array entries
                        array = map(int, array)
                        for k in range(Kmin, Kmax+1):
                            fmt += '\nc  k={0}'.format(k)
                            for j in range(Jmin, Jmax+1):
                                fmt += '\n     '
                                for i in range(Imin, Imax+1):
                                    fmt += ef.format(array.pop(0))
                                    
                    fmt += ' {0}{1}' # placeholders for k, v
                    k = ''
                    v = ''
                else:
                    fmt = '{0}={1} '
                res += fmt.format(k, v)
        return res

    def getvalue(self, key):
        """Returns meaningfull part of the value for options 'fill', 'u' and 'lat'. 
        
        In general, 'fill' is a (mulli-line) string that can optionally contain comments.
        This method returns a list of values of this cell option.

        If options were not defined, return 0.

        """
        if key == 'fill':
            v = self.get(key, 0)
            if isinstance(v, str) and ':' in v:
                ([Imin, Imax, Jmin, Jmax, Kmin, Kmax], array) = _fill_entries(v)
                array = map(int, array)
                return [Imin, Imax, Jmin, Jmax, Kmin, Kmax] + array
            else:
                return int(v)
        elif key == 'u':
            return int(self.get(key, 0))
        elif key == 'lat':
            return int(self.get(key, 0))
        else:
            raise NotImplementedError


class Cell(object):
    """Representation of the MCNP cell card.

    This is a container for cell material, density, geometry description and options,
    that can generate string representation of the cell for the MCNP input file.

    Constructor can take optional keyword arguments to specify cell paramters and options:

    >>> c = Cell(mat=1, rho=-10., vol=(-1, 1), cmt='comment', ID=10, 'imp:n'=2.5)
    >>> print c
    10 1 -10.0 -1 imp:n=2.5  $ comment

    Cell parameters can be changed after initialization by setting the correspondent attributes:

    >>> c.ID = 5
    >>> c.mat = 4
    >>> c.rho = -1.
    >>> c.vol = (-1, 'a')
    >>> c.opt['imp:n'] = 0
    >>> print c
    5 4 -1.0 -a imp:n=0  $ comment

    """
    def __init__(self, **kwargs):
        self.__v = '{geom}'
        self.__m = 0
        self.__r = 1.0
        self.__o = CellOpts()
        self.__o['imp:n'] = 0
        self.__c = 'comment'
        self.__id = '{ID}'
        for (n,v) in kwargs.items():
            if n == 'vol':
                self.vol = v
            elif n == 'mat':
                self.mat = v
            elif n == 'rho':
                self.rho = v
            elif n == 'cmt':
                self.cmt = v
            elif n == 'ID':
                self.ID = v
            elif n in CellOpts.VALIDKEYS:
                self.__o[n] = v
            else:
                raise TypeError(n, ' is an invalid keyword argument for this function.')
        return

    @property
    def vol(self):
        """Cell geometry (cell volume). 

        Can be set to an integer, string, or to an instance of the Volume()
        class.

        The setter method accepts also a tuple of the form (sign, def), which
        is transformed to an instance of the Volume() class.

        >>> c1 = Cell()
        >>> c2 = Cell()
        >>> c1.vol = Volume(-1, ['px', 0.])
        >>> c2.vol = (-1, ['px', 0.])
        >>> c1.vol == c2.vol
        True
        """
        return self.__v

    @vol.setter
    def vol(self, value):
        if isinstance(value, tuple):
            v = Volume(*value)
        else:
            v = value
        self.__v = v
        return

    @property
    def mat(self):
        """Material of the cell.

        Can be an integer or an instance of the Material() class.
        """
        return self.__m

    @mat.setter
    def mat(self, value):
        self.__m = value

    @property
    def rho(self):
        """Cell density.
        """
        return self.__r

    @rho.setter
    def rho(self, value):
        self.__r = value

    @property
    def opt(self):
        """Dictionary of cell options.

        An instance of the CellOpt() class.
        """
        return self.__o

    @property
    def cmt(self):
        """Cell comment.
        """
        return self.__c

    @cmt.setter
    def cmt(self, v):
        self.__c = v

    @property
    def ID(self):
        """Cell ID.

        At initialization set to the string '{ID}'.
        """
        return self.__id

    @ID.setter
    def ID(self, v):
        self.__id = v




    def card(self, formatted=True):
        """Returns a string representing the cell in the MCNP input file.

        If optional argument formatted set to True (default), the returned
        string can contain new-line characters delimiting the string to lines
        that fit to 80-characters limit imposed by the MCNP input file syntax.

        Representation of cell ID, material and volume depends on the type of
        correspondent attributes.

        If cell ID is a positive integer or a string, it is printed as is.
        Otherwise, placeholder {ID} is printed.

        If mat is an nonnegative integer or a string, it is printed
        together with density rho.  Otherwise, placeholder {mat} {rho} is
        printed.

        If vol is an instance of the Volume() class containing definitions that
        utilize the Surface() class, or if it is an instance of the Surface()
        class, placeholder {geom} is printed. Otherwise, the string
        representation of vol is printed.
        
        """
        # cell ID
        ID = self.__id
        if isinstance(ID, int) and ID > 0 or isinstance(ID, str):
            cellID = str(ID) 
        else: 
            cellID = '{ID}'

        # material ID and density
        # Density can be of uncertainties.Variable class. Use its nominal value
        rho = self.__r
        if hasattr(rho, 'nominal_value'):
            rho = rho.nominal_value
        elif isinstance(rho, tuple) and len(rho) == 2:
            rho = rho[0]
        mat = self.__m
        if isinstance(mat, int):
            if mat != 0:
                matID = '{0} {1}'.format(mat, rho)
            else:
                matID = '0 '
        elif isinstance(mat, str):
            matID = '{0} {1}'.format(mat, rho)
        else:
            matID = '{mat} {rho}' # placeholder for both material ID and density/concentration
        # volume representation
        vol = self.__v
        if isinstance(vol, Volume):
            ff = True # flag to print vol directly. If the volume contains definitions of the Surface type, set this flag to False
            for s in vol.surfaces():
                if isinstance(s, Surface):
                    ff = False
                    break
            if ff:
                volID = str(vol)
            else:
                volID = '{geom}'
        elif isinstance(vol, Surface):
            volID = '{geom}'
        elif vol is None:
            volID = '{geom}'
        else:
            volID = str(vol)
        # compile the whole string for the cell representation:
        res = '{0} {1} {2} {3}'.format(cellID, matID, volID, str(self.opt))
        # add comment, if necessary
        cmt = self.__c
        if len(cmt) > 0:
            res += ' $ ' + cmt
        # wrap lines to fit to 80 character line
        if formatted:
            res = formatter.format_card(res)
        return res

    def __str__(self):
        return self.card(True)



