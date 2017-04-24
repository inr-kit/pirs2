"""
Functions to read the output.txt
"""
import re

def _heading(h1, h2):
    """
    Returns a list of column names specified at two lines h1 and h2.

    The returned list has the following form:

    [  ('name1upper', 'name1lower'), ('name2upper', 'name2lower'), ...]

    Algorithm:
      1. Split to compound words (A compound word is a series of words
      separated only with one character) 

      2. In the second line empty places (i.e. consisting only of ' ')
      correspondent to the first line are replaced with '_'

      3. Both lines are splitted. In the second list, '__' are replaced back
      with empty line.
    """
    h1 = h1.replace(' t_sat', '  t_sat')  # in bundle average, there is only one space before t_sat.
    H1  = re.sub(r'([a-zA-Z]) ([a-zA-Z])', r'\1_\2', h1)
    h1 = h1.replace('  t_sat', ' t_sat')  # return one space 
    r1 = H1.split()
    H2 = h2
    for n in r1:
            i1 = h1.find(n)
            ln = len(n)
            i2 = i1 + ln
            if H2[i1:i2] == ' '*ln:
                H2 = H2[:i1] + '_'*ln + h2[i2:]
    r2 = []
    for n in H2.split():
        if n == '_'*len(n):
            r2.append('')
        else:
            r2.append(n)
    return zip(r1, r2)


class OutputTable(object):
    """
    O-O representation of tables in the output.txt. It provides access to data
    and column names.  Usualy, instances of this class are created by the
    function read_output(), see below.

    """
    def __init__(self, columns, cnames, N=0):
        self.__c = columns[:]
        self.__n = cnames[:]
        self.__fmt = '{:>12}'
        self.number = N
        return

    @property
    def columns(self):
        """
        List of data columns.
        """
        return self.__c

    @property
    def column_names(self):
        """
        List of column names. Each element of the list is a tuple specifying
        the upper and lower part of the column's heading. Usually, it is 
        the column data name and dimension.
        """
        return self.__n

    def column(self, name_upper, name_lower=None):
        """
        Returns a copy of the data column whose heading's upper part is
        name_upper.
        """
        if name_lower is not None:
            raise NotImplementedError('search for lower name is not implemented')

        i = map(lambda cname: cname[0], self.__n).index(name_upper)
        return self.__c[i][:]

    def row(self, i):
        """
        Returns a copy of i-th row.
        """
        return map(lambda x: x[i], self.__c)

    # for compatibility with old code, when output table is represented by a
    # tuple (columns, cnames), where columns is a list of columns,  and cnames
    # is a list of names.
    def __getitem__(self, i):
        if i == 0:
            return self.__c
        elif i == 1:
            return self.__n
        else:
            raise IndexError('Index can be 0 or 1 but recieved ', i)

    @property
    def fmt(self):
        """
        Format string used to convert table to a strinng (when e.g. printing
        the table).

        Can be a string or a list of strings, representing valid format
        specifications, as understood by the str.format() method.

        If a string is given, it is used for all columns. If a list of strings
        is given, its length must coincide with the number of columns in the
        table. In this case, each column gets its own format string.

        not implemented: If fmt is None, each column's width is defined by its header's length.
        """
        return self.__fmt

    @fmt.setter
    def fmt(self, value):
        if value is None:
            raise NotImplementedError
        else:
            self.__fmt = value

    def __str__(self):
        # algorithm is the following:
        # First, the self.fmt is used to format all data.
        # Second, the column width are defined to ensure that
        # all formatted data fit in the columns.

        # define minimal column width by the headers
        wdth = []
        for (u, l) in self.__n:
            wdth.append(max(len(u), len(l)))
            wdth[-1] += 1 # ensure at least one space between columns.
        # define data format
        if isinstance(self.fmt, str):
            # one format for all columns.
            fdata = [self.fmt] * len(self.__n)
        elif isinstance(self.fmt, list) or isinstance(self.fmt, tuple):
            # own format for every column:
            fdata = self.fmt[:]
        else:
            raise NotImplementedError
        # format data and check width of each column
        rows = []
        for i in range(len(self.__c[0])):
            # apply format to all data in row i
            row = map(lambda s,v:s.format(v), fdata, self.row(i))
            rows.append(row)
            # modify, if necessary, column width
            for (i, e) in enumerate(row):
                if len(e) > wdth[i]:
                    wdth[i] = len(e)
        # generate format that reflects column width 
        fmt = map(lambda (i,w):'{{{0}:>{1}}}'.format(i,w), enumerate(wdth))
        fmt = ''.join(fmt)
        # use this format to put headers and data (allready formatted) to one
        # multi-line string
        res = []
        res.append(fmt.format( *(map(lambda x: x[0], self.__n))))
        res.append(fmt.format( *(map(lambda x: x[1], self.__n))))
        for row in rows:
            res.append(fmt.format( *row))
        return '\n'.join(res)

def read_output(output='output.txt'):
    """
    Reads rod and channel results from the specified output.txt file. 

    Returns a tuple with elements reprepresenting result for each rod (keys
    are rod numbers)

    >>> (rr, cc) = read_output('scf0/output.txt')
    >>> for r in rr:
    ...     print r



    """

    outp = open(output, 'r')

    def skiplines(n=2):
        for i in range(n):
            outp.next()

    rods = []
    channels = []
    data_block = 'none'
    for l in outp:
        if data_block == 'none' and ' results for channel' in l and l.split()[3] != 'exit:':
            Nr = int(l.split()[3])
            skiplines(3)
            h1 = outp.next()
            h2 = outp.next()
            head = _heading(h1, h2)
            data = []
            skiplines(1)

            data_block = 'channels'
            # print 'data block ', data_block
        elif data_block == 'channels':
            w = l.split()
            if len(w) == 0:
                # table ended. Prepare data for return.

                # column names
                cname = head
                
                # columns:
                columns = []
                for n in cname:
                    columns.append([])
                for d in data:
                    for (i, v) in enumerate(d):
                        columns[i].append(v)

                channels.append(OutputTable(columns, cname, N=Nr))
                data_block = 'none'
                # print 'data block ', data_block
            else:
                # convert to float and int:
                data.append(map(float, w))
        elif data_block == 'none' and ' results for bundle average' in l:
            skiplines(3)
            h1 = outp.next()
            h2 = outp.next()
            head = _heading(h1, h2)
            data = []
            skiplines(1)

            data_block = 'bundle_average'
            # print 'data block ', data_block
        elif data_block == 'bundle_average':
            w = l.split()
            if len(w) == 0:
                # table ended. Prepare data for return.

                # column names
                cname = head
                
                # columns:
                columns = []
                for n in cname:
                    columns.append([])
                for d in data:
                    for (i, v) in enumerate(d):
                        columns[i].append(v)

                bundle_ave = OutputTable(columns, cname, N=0)
                data_block = 'none'
                # print 'data block ', data_block
            else:
                # convert to float and int:
                data.append(map(float, w))

        elif data_block == 'none' and ' results for rod' in l:
            lsp = l.split()
            Nr = int(lsp[3]) # rod number
            Mr = int(lsp[6]) # rod material
            skiplines()
            h1 = outp.next()
            h2 = outp.next()
            head1 = _heading(h1, h2)
            data1 = []
            data2 = []
            skiplines(1)

            data_block = 'rods-1'
            # print 'data block ', data_block

        elif data_block == 'rods-1':
            w = l.split()
            if len(w) == 0:
                # table's first part ended; go to the second part.
                head2 = _heading(outp.next(), outp.next())
                outp.next()
                data_block = 'rods-2'
                # print 'data block ', data_block
            else:
                # remove '-' between Zmin and Zmax:
                w.pop(1)
                # convert to float and int:
                data1.append(map(float, w[0:4]) + map(int, w[4:6]) + map(float, w[6:]))
        elif data_block == 'rods-2':
            w = l.split()
            if len(w) == 0:
                # table ended. Prepare data for return.

                # column names
                cname = []
                cname.append(('Zmin', head1[0][1]))
                cname.append(('Zmax', head1[0][1]))
                cname += head1[1:] + head2[1:]
                
                # columns:
                columns = []
                for n in cname:
                    columns.append([])
                for (d1, d2) in zip(data1, data2):
                    for (i, v) in enumerate(d1 + d2):
                        columns[i].append(v)

                rods.append(OutputTable(columns, cname, N=(Nr, Mr)))
                data_block = 'none'
                # print 'data block ', data_block
            else:
                data2.append(map(float, w[3:]))
    channels.append(bundle_ave)
    outp.close()
    return (rods, channels)


def read_pl_rod(pl_rod='pl_rod_+0.000E+00.txt'):
    """
    Generator iterating over data from the file pl_rod_*.txt.

    Each element is a tuple (Nr, table), where Nr is the rod's number and
    table is a list of lists representing data for the  Nr-th rod.

    Excerpt from the SCF manual, columns in the pl_rod file:

    0 Z middle ,    
    1 coolant temperature, 
    2 Tclad_out, 
    3 Tclad_in, 
    4 Trod_out, 
    5 Trod_center, 
    6 Rho_cool, 
    7 heat_flux,
    8 heat transfer coeff
    9 departure of nucleate boiling ratio
    10 heat transfer mode
    11 fuel cladding gap width
    12 fuel cladding heat transfer coefficient

    """

    plrod = open(pl_rod, 'r')
    
    table = None
    for line in plrod:
        if line[:4] == 'zone':
            # yield previous table:
            if table:
                yield (Nr, table)
            # start data for new rod
            table = []
            Nr = int( line[line.index('d')+1:] )
        else:
            row = map(float, line.split())
            if row:
                table.append(row)
            # else:
            #     print 'line skipped:---'
            #     print repr(line)
            #     print row
            #     print '---'
    yield (Nr, table)
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()


    

