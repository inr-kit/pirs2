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

Classes to represent data from xsdir file.
"""
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import os
import sys
import linecache
from pirs.core.trageom.vector import _are_close

#: the $DATAPATH environmental variable.
XSDIRPATH = os.environ.get('DATAPATH')
if XSDIRPATH is None:
    print 'WARNING: Environmental variable DATAPATH is not defined.'
    print '         Current directory will be used to find the default'
    print '         xsdir file.'
    XSDIRPATH = '.'


#: path to the default xsdir file.
XSDIRFILE = os.path.join(XSDIRPATH, 'xsdir')


class Xsdir(object):
    """Container for data from xsdir file.

    Data can be added manually or read from existing file.

    """

    __default = None

    @classmethod
    def default(cls):
        """Default system xsdir file.

        Returns an instance of the ``Xsdir`` class containing data from the ``$DATAPATH/xsdir`` file.
        """

        if cls.__default is None:
            cls.__default = cls(XSDIRFILE)
        return cls.__default

    def __init__(self, path=None):
        self.clear()
        if path is not None:
            self.read(path)

    def __eq__(self, othr):
        if isinstance(othr, self.__class__):
            return (self.__awr == othr.__awr and
                    set(self.__dir) == set(othr.__dir))
        else:
            return False

    def clear(self):
        """
        Removes data from awr, dir and path.
        """
        self.__awr = {}
        self.__dir = []
        self.__pth = None # path to the read xsdir file. Set only when data is read from an xsdir file.
        return

    def read(self, path, append=False):
        """
        Read existing xsdir file.

        The path argument specifies relative or absolute path to the
        xsdir file.

        If the optional argument append is True, data read from the xsdir file are
        appended to the data allready stored in the instance of Xsdir().
        Otherwise, the clear() method is called before reading the file.

        """
        if not append:
            self.clear()

        apath = os.path.abspath(path)
        # print 'READ XSDIR {}'.format(apath)
        # raise ValueError
        xfile = open(apath, 'r')
        self.__pth = apath
        dr = [] # directory records
        ar = [] # awr records
        csec = '' # flag defining the current section
        for l1 in xfile:
            if   'directory' in l1[:13].lower():      # 13 is the sum of 5 + len('directory') - 1 , where 5 is the max. allowable offset of the keyword in xsdir file.
                csec = 'dir'
            elif 'atomic weight ratios' in l1[:24].lower():      # 24 is the sum of 5 + len('atomic weight ratios') - 1 , where 5 is the max. allowable offset of the keyword in xsdir file.
                csec = 'awr'
            else:
                if csec == 'dir':
                    # we are reading directory section.
                    # It goes till the end of file, therefore
                    # there is no need to check if the section
                    # end is reached.

                    # one entry can take two lines. In this
                    # case, the first line ends with '+'.
                    if l1[-2] == '+':              # last character in l1 is new-line
                        l1 = l1[:-2] + xfile.next()

                    self.__dir.append( DirEntry(l1) )
                elif csec == 'awr':
                    # awr section is followed by other sections.  The awr
                    # section ends, when entries on the line cannot be
                    # converted to pairs integer-float.
                    try:
                        lst = l1.split()
                        ilist = map(int,   lst[0::2])
                        flist = map(float, lst[1::2])
                    except ValueError:
                        # if line contains other than integer and float entries,
                        # this means that the awr section ended.
                        csec = ''
                        continue
                    finally:
                        for (zaid, awr) in zip(ilist, flist):
                            self.__awr[zaid] = awr
        xfile.close()
        self._get_thermal_temperatures()
        return

    def _get_thermal_temperatures(self):
        """Reads thermal data temperature from cross-section data file.

        Directory entries with thermal data do not necessarily contain temperature.

        This method reads temperature from the correspondent data file, if it
        is in ASCII format.

        """
        # print 'called mcnp.Xsdir._get_thermal_temperatures()'
        rd = {}  # dictionary to read
        for d in self.__dir:
            if d.TYPE == 't' and d.TEMP == 0.:
                # for thermal data types, if temperature
                # not specified in xsdir, read it from the
                # data file.
                fname = os.path.join(self.datapath, d.PATH)
                if os.path.isfile(fname):
                    hline = linecache.getline(fname, d.ADDR)
                    d.TEMP = float(hline.split()[2])

    def write(self, path):
        return NotImplemented

    def suffix(self, ZAID, T=None, xstype='c', smin=None, smax=None):
        """
        Find suffices of the cross-section data of type xstype describing ZAID
        at temperature T. T must be specified in Kelvin.

        Two suffices are returned, for cross-sections at temperatures closest
        to T, below and above T.

        If smin or smax are specified, they define interval of suffixes that
        are searched for the closest temperature.

        The returned value is always a list of two tuples, in the form [(T1,
        S1), (T2, S2)], where T1 and T2 are cross-section temperatures below
        and above T, and S1 and S2 are the correspondent suffices.

        If T is not specified, T1 and S1 are parameters of the first
        cross-section data found in the directory section for nuclide defined
        by ZAID. In this case, T2 and S2 are the same as T1 and S1.

        """
        if T is not None:
            T1 = T - 10000.
            T2 = T + 10000.
        S1 = ''
        S2 = ''
        for de in self.__dir:
            if de.ZAID == ZAID and de.SUFF[-1] == xstype:
                XX = de.XX
                if (smin is None or smin <= XX) and (smax is None or smax >= XX):
                    deT = de.TEMP / 8.617343e-11 # temperature of de is in MeV, while T and Tol are in Kelvin.
                    if T is None or _are_close(deT, T):
                        return [(deT, de.SUFF), (deT, de.SUFF)]

                    if   T1 < deT <= T:
                        T1 = deT
                        S1 = de.SUFF
                    elif T <= deT < T2:
                        T2 = deT
                        S2 = de.SUFF
        if S1 == '' and S2 == '':
            raise ValueError('Cannot find cross-sections for ZAID ', str(ZAID))
        elif S1 == '':
            T1 = T2
            S1 = S2
        elif S2 == '':
            T2 = T1
            S2 = S1
        return[ (T1, S1), (T2, S2)]

    def find_thermal(self, namepart, T):
        """
        Returns the name of thermal data containing string namepart, closest to
        temperature T (in K).
        """
        Tfin = -1
        name = None
        for d in self.__dir:
            if d.TYPE == 't' and namepart in d.ZAID + d.SUFF:
                deT = d.TEMP / 8.617343e-11
                if abs(T-deT) < abs(T-Tfin):
                    name = d
                    Tfin = deT
        if name is None:
            return (None, Tfin)
        else:
            return (name.NAME, Tfin)

    @property
    def awr(self):
        """
        Property represents the 'atomic weight ratios' section of xsdir
        file. This is a dictionary: keys are ZAIDs, values are nuclide
        masses in terms of awr.
        """
        return self.__awr

    @property
    def dir(self):
        """
        A list whose elements represent lines from the directory section of the
        xsdir file. Elements are instances of the DirEntry() class.
        """
        return self.__dir

    @property
    def datapath(self):
        """
        Returns path to the xsdir file, if the data in the xsdir intance was
        read from a file.
        """
        return os.path.split(self.__pth)[0]

    @property
    def filename(self):
        """
        Returns the name of the xsdir file, if the data in the xsdir instance
        were read from a file.
        """
        return os.path.split(self.__pth)[1]


class DirEntry(object):
    """
    Represents one line from the directory section of an xsdir file.

    Constructor takes a string containigs one line from the directory section.

    >>> e = DirEntry()   # instance with default values
    >>> e = DirEntry(' 16034.31c 33.676200 jeff31_as_300 0 1 1126405 43431 0 0 2.5852E-08')

    """
    def __init__(self, xsdir_line=None, xsdir_path=None):
        self.ZAID = 1001
        self.SUFF = '00a'
        self.PATH = 'file_name'
        self.MASS = 0.999170
        self.TEMP = 0.0
        self.FTYP = 1     # file type
        self.ADDR = 1     # address
        if xsdir_line is not None:
            self.read(xsdir_line)

    def __eq__(self, othr):
        return (self.ZAID == othr.ZAID and
                self.SUFF == othr.SUFF and
                self.PATH == othr.PATH and
                self.MASS == othr.MASS and
                self.TEMP == othr.TEMP)

    @property
    def NAME(self):
        """Cross-section data name, ZAID plus suffix.
        """
        return '{0}.{1}'.format(self.ZAID, self.SUFF)

    def read(self, _str):
        """
        Read data from xsdir line.

        Just pass a line from directory section of an xsdir file.  Currently,
        it understands entries for 'c' and 't' types of cross-sections.

        >>> e0 = DirEntry()
        >>> e1 = DirEntry()
        >>> e2 = DirEntry()
        >>> e3 = DirEntry()
        >>> e1.read(' 1001.31c 0.999170 jeff31_as_300 0 1 1 10161 0 0 2.5852E-08                      ')
        >>> e2.read(' 18038.31c 37.636600 jeff31_as_300 0 1 1388504 16223 0 0 2.5852E-08 ptable       ')
        >>> e3.read(' lwtr11.31t 0.999170 jeff31_a_STL 0 1 781352 83931                              ')
        >>> for e in [e0, e1, e2, e3]:
        ...    print e.ZAID, e.SUFF, e.TYPE, e.MASS, e.PATH, e.TEMP
        ...
        1001 00a a 0.99917 file_name 0.0
        1001 31c c 0.99917 jeff31_as_300 2.5852e-08
        18038 31c c 37.6366 jeff31_as_300 2.5852e-08
        lwtr11 31t t 0.99917 jeff31_a_STL 0.0
        """
        lst = _str.split()
        # zaid and suffix
        self.ZAID, self.SUFF = lst[0].split('.')
        if self.TYPE != 't':
            self.ZAID = int(self.ZAID)
        # awr and file name
        self.MASS = float(lst[1])
        self.PATH = lst[2]
        # file type and address
        self.FTYP = int(lst[4])
        self.ADDR = int(lst[5])
        # temperature
        if self.TYPE == 'c':
            self.TEMP = float( lst[9] )
        elif self.TYPE == 't':
            # for thermal data, temperature in xsdir is optional (no T in
            # jeff31's xsdir, but there is in standard xsdir).
            if len(lst) > 9:
                self.TEMP = float( lst[9] )

    @property
    def TYPE(self):
        """Character specifying type of the data, 'c', 't', etc.
        """
        return self.SUFF[-1].lower()

    @property
    def XX(self):
        """
        Integer value, part of the suffix with digits.
        """
        return int(self.SUFF[:-1])


