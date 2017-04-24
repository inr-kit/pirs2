class LoadMap(object):
    """
    Convenient definition of a loading map.

    A loading map can be first specified as a multi-line string with
    pseudo-graphics. See string property. After setting this property, the
    attribute table is generated that is a list of rows. Each map's element can
    be accessed by table[Nrow][Ncolumn], where Nrow=0 corresponds to the first
    line, and Ncolumn=0 corresponds to the first (leftmost) position.

    Elements of the loading can be indexed by line and position indices of the
    given multi-line string, or by user-defined indices. For later, one needs
    to set the element that has user-defined indices (0, 0) and direction of
    the indices. See attributes origin and dir. Method get(i,j) returns the map
    element correspondent to the user-defined indices (i, j).

    Conversion from the row and column indices to the user-defined indices is
    done by methods i(row), j(col), row(i) and col(j).

    """
    def __init__(self):
        self.dir = (-1, 1)
        self.comment = '$'
        self.default = '_'
        self.origin = (0, 0) # position of the origin element.
        self.rdict = {} # replacement dictionary.

        self._all_items = None
        return

    @property
    def string(self):
        """
        Multi-line string representation of the loading map.

        The first line (its content in the input file is defined by characters
        after the opening three double quotes till the end of the line), is
        skipped.

        The second line is used to define indentation, commenting character and
        the tabulation length. 
        
        Next lines contain core loading representation. Each line describes one
        row. Element on the row must fit to the tabulation length. Empty lines
        and comments (everything after the commenting character) are skipped.

        Example:
        \"""                      # 1-st line
            $3                   # 2-nd line: indent, commenting character, table field length
              1  2  4  5
              a  b  c  d  $ comment

              e  f  g  h
        
        \"""

        """
        # first, look for the tab length and for the number of columns:
        tlen = 0
        for r in self.table:
            n = 0
            for c in r:
                n += 1
                lc = len(c)
                if lc > tlen:
                    tlen = lc
        tlen += 2
        fmts = '{{0:>{0}s}}'.format(tlen)
        fmti = '{{0:>{0}d}}'.format(tlen)
        # prepare output multi-line string
        res = ''
        indent = ' '*self.__indent
        nr = 0
        for r in self.table:
            res += '\n' + indent 
            nc = 0
            for c in r:
                res += fmts.format(c)
                nc += 1
            while nc < self.__ncol:
                res += fmts.format('')
                nc += 1
            # add comment with row index:
            res += '{} {}'.format(self.comment, self.i(nr))
            nr += 1


        # heading
        h1 = '\n' + ' '*(self.__indent-1) + self.comment
        head = h1 + str(tlen) + h1

        for j in range(self.__ncol):
            head += fmti.format(self.j(j))


        return head + res

    @string.setter
    def string(self, value):
        lines = value.splitlines() 
        l = lines.pop(0) # this is the rest of the line after opening """. Usualy not used.
        l = lines.pop(0) # this is the next line after """. Get indent, commenting character and tab from this line.
        ll = l.lstrip(' ')
        nlsp = len(l) - len(ll) + 1 # number of leading spaces, i.e. indentation.
        cmnt = ll[0]            #  commenting character
        ntab = int(ll[1:].split()[0])      # tab length
        # print nlsp, repr(cmnt), ntab

        tbl = []

        ncol = 0
        for l in lines:
            # print 'raw original line:', repr(l)
            # remove comment, if any
            i = l.find(cmnt)
            if i > -1:
                l = l[:i]
            # print 'without comments: ', repr(l)
            if len(l) > nlsp:
                # remove indentation
                l = l[nlsp:]
                # print 'deindented   line:', repr(l)
                row = []
                while len(l) > 0:
                    if len(l) > ntab:
                        lpart = l[:ntab]
                        l = l[ntab:]
                    else:
                        lpart = l
                        l = ''
                    e = lpart.strip()
                    if e == '':
                        e = self.default
                    row.append(e)
                    # print '   lpart, e, new l: ', repr(lpart), repr(e), repr(l)
                if row:
                    tbl.append(row)
                    ncol = max(ncol, len(row))

        self.table = tbl
        self.__indent = nlsp
        self.comment = cmnt
        self.__ncol = ncol
        return

    def tindex(self, e):
        """
        Returns table index of the element e.
        """
        row = 0
        for r in self.table:
            if e in r:
                return (row, r.index(e))
            row += 1
        raise ValueError('{} not in table'.format(repr(e)))

    def col(self, j):
        """
        Returns table column index that corresponds to the user column index j.
        """
        return j*self.dir[1] + self.origin[1]

    def row(self, i):
        """
        Returns table row index that corresponds to the user row index i.
        """
        return i*self.dir[0] + self.origin[0]

    def j(self, col):
        """
        Returns user column index that corresponds to the table column col.
        """
        return self.dir[1] * (col - self.origin[1])

    def i(self, row):
        """
        Returns user row index that corresponds to the table row 'row'.
        """
        return self.dir[0] * (row - self.origin[0])

    def get_element(self, i, j):
        """
        Returns element correspondent to the user indices i, j.
        """
        r = self.table[self.row(i)]
        col = self.col(j)
        try:
            c = r[col]
        except IndexError:
            c = self.default
        return self.rdict.get(c, c)

    @property
    def irange(self):
        """
        Returns tuple for range() function correspondent
        to the user-defined i index.
        """
        if self.dir[0] > 0:
            return self.i(0), self.i(len(self.table)-1)
        else:
            return self.i(len(self.table)-1), self.i(0)+1

    @property
    def jrange(self):
        """
        Returns tuple for range() function correspondent
        to the user-defined j index.
        """
        if self.dir[1] > 0:
            return self.j(0), self.j(self.__ncol)
        else:
            return self.j(self.__ncol), self.j(0)+1

    @property
    def colrange(self):
        """
        Returns tuple for range() function correspondent
        to the table column indices.
        """
        return (0, self.__ncol)

    @property
    def rowrange(self):
        """
        Returns tuple for range() function correspondent
        to the table row indices.
        """
        return (0, len(self.table))

    def __str__(self):
        res = ''
        for r in self.table:
            for c in r:
                res += '{0:>4s}'.format(c)
            res += '\n'
        return res

    def items(self):
        """
        Iterator over all defined elements.

        Returns tuples (i, j, e), where i and j are user-defined indices of the element e.
        """
        Nr = 0
        for row in self.table:
            Nc = 0
            for e in row:
                if self._all_items is None:
                    yield (self.i(Nr), self.j(Nc), self.rdict.get(e, e))
                else:
                    yield (self.i(Nr), self.j(Nc), self._all_items)
                Nc += 1
            Nr += 1


if __name__ == '__main__':
    mp = Map()
    mp.string = """$
    $3 
    $ an example core loading
    $  0  2  3  4  5  6  7  8  9  0

                      a  b  c  d  e       $ 0
                f  g  i  j  k  l  m       $ 1
          n  o  p  q  r  s  t  u  v       $ 2
       w  x  y  z  1  2  3  4  5  6       $ 3
       8  9 10 11 12 13 14 15 16 17       $ 4
    """
    mp.origin = mp.tindex('y') 
    print mp.origin
    print mp.string
    print mp.table

    print 'irange: ', mp.irange
    print 'jrange: ', mp.jrange

    for i in range(*mp.irange):
        for j in range(*mp.jrange):
            print i, j, mp.get_element(i, j)



