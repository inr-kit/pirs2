"""
Functions to read the output.txt
"""
import re

def heading(h1, h2):
    """
    Returns a list of column names specified at two lines h1 and h2.

    Algorithm:
      1. Split to compound words (A compound word is a series of words separated only with one character) 

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
    def __init__(self, columns, cnames):
        self.__c = columns[:]
        self.__n = cnames[:]
        return

    @property
    def columns(self):
        return self.__c

    @property
    def column_names(self):
        return self.__n

    def column(self, name_upper, name_lower=None):
        if name_lower is not None:
            raise NotImplementedError('search for lower name is not implemented')

        i = map(lambda cname: cname[0], self.__n).index(name_upper)
        return self.__c[i][:]

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


def read_output(output='output.txt'):
    """
    Read rod and channel results. 

    Output is a tuple with elements reprepresenting result for each rod (keys
    are rod numbers)

    >>> (rr, cc) = read_output('scf0/output.txt')
    >>> for r in rr:
    ...     print print_table(r)



    """

    outp = open(output, 'r')

    def skiplines(n=2):
        for i in range(n):
            outp.next()

    rods = []
    channels = []
    data_block = 'none'
    for l in outp:
        if l.find('trace back') != -1:
            raise ValueError('scf run did not complete successfully')

        if data_block == 'none' and ' results for channel' in l and l.split()[3] != 'exit:':
            Nr = int(l.split()[3])
            skiplines(3)
            h1 = outp.next()
            h2 = outp.next()
            head = heading(h1, h2)
            data = []
            skiplines(1)

            data_block = 'channels'
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

                channels.append(OutputTable(columns, cname))
                data_block = 'none'
            else:
                # convert to float and int:
                data.append(map(float, w))
        elif data_block == 'none' and ' results for bundle average' in l:
            skiplines(3)
            h1 = outp.next()
            h2 = outp.next()
            head = heading(h1, h2)
            data = []
            skiplines(1)

            data_block = 'bundle_average'
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

                bundle_ave = OutputTable(columns, cname)
                data_block = 'none'
            else:
                # convert to float and int:
                data.append(map(float, w))

        elif data_block == 'none' and ' results for rod' in l:
            Nr = int(l.split()[3])
            skiplines()
            h1 = outp.next()
            h2 = outp.next()
            head1 = heading(h1, h2)
            data1 = []
            data2 = []
            skiplines(1)

            data_block = 'rods-1'

        elif data_block == 'rods-1':
            w = l.split()
            if len(w) == 0:
                # table's first part ended; go to the second part.
                head2 = heading(outp.next(), outp.next())
                outp.next()
                data_block = 'rods-2'
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

                rods.append(OutputTable(columns, cname))
                data_block = 'none'
            else:
                data2.append(map(float, w[3:]))
    channels.append(bundle_ave)
    outp.close()
    return (rods, channels)

def print_table(t, cw=12):
    """
    t must be a tuple (or a list with two elements). The first element is a list of columns. The second
    element is a list with column names.
    """
    # define format strings.
    if isinstance(cw, int):
        #cw is the column width for all columns
        # fhead = '{{0:>{0}}}'.format(cw) * len(t[1])
        # fdata = '{{0:>{0}}}'.format(cw) * len(t[1])

        # implementation that works with python 2.6 and below
        f = map(lambda i: '{{{0}:>{1}}}'.format(i,cw), range(len(t[1])))
        fhead = ''.join(f)
        fdata = ''.join(f)
    else:
        raise NotImplementedError
    res = []
    # table heading
    res.append(fhead.format( *(map(lambda x: x[0], t[1]))))
    res.append(fhead.format( *(map(lambda x: x[1], t[1]))))
    # table rows
    for i in range(len(t[0][0])):
        row = map(lambda x: x[i], t[0])
        res.append(fdata.format(*row))
    return '\n'.join(res)

def get_rod_temp(t, mode='avg'):
    """
    Return axial map of the fuel temperature of this rod. Two modes are
    possible, 'ave' returns the volume average, 'dop' returns the doppler
    average.

    """
    zmin_i = t[1].index(('Zmin', '(m)'))
    zmax_i = t[1].index(('Zmax', '(m)'))
    zmin = t[0][zmin_i]
    zmax = t[0][zmax_i]

    fueli_i = t[1].index(('tfueli', '(c)'))
    fuelc_i = t[1].index(('tfuelc', '(c)'))
    fuela_i = t[1].index(('tfuave', '(c)'))

    if mode == 'avg':
        fuelt = t[0][fuela_i]
    elif mode == 'dop':
        fuelt = map(lambda x,y: 0.3*x + 0.7*y, t[0][fueli_i], t[0][fuelc_i])
    else:
        raise NotImplementedError

    return zip(zmin, zmax, fuelt)

def get_channel_temp_and_dens(c):
    """
    Return axial map of coolant temperature and density in this channel.

    """
    dist_i = c[1].index(('distance', '(m)'))
    temp_i = c[1].index(('temperature', '(c)'))
    dens_i = c[1].index(('density', '(kg/m3)'))

    return zip(c[0][dist_i], c[0][temp_i], c[0][dens_i])


def read_pl_rod(pl_rod='pl_rod_+0.000E+00.txt'):
    """
    Generator iterating over data from the file pl_rod_*.txt.

    Each element is a tuple (Nr, table), where Nr is the rod's number and
    table is a list of lists representing data for the  Nr-th rod.
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
        elif len(line) == 0:
            # skip empty line
            pass
        else:
            table.append( map(float, line.split()) )
    yield (Nr, table)
    
            
            
        








if __name__ == '__main__':
    import doctest
    doctest.testmod()


    

