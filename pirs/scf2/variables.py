
def _quoted(value):
    """
    Returns value surrounded by quotes, if value is a string and it has spaces.
    """
    if isinstance(value, str):
        q = '' # no quotes
        if ' ' in value:
            # there are space(s), surrounding quotes are necessary:
            if '"' not in value:
                q = '"'
            elif "'" not in value:
                q = "'"
            else:
                # assume that a user allready prepared value in proper way.
                q = ''
        return '{0}{1}{2}'.format(q, value, q)
    else:
        return value

class ScfVariable(object):
    """
    SCF valiable. 
    
    Has name and value. Its string representation is a valid entry for an SCF
    input file. Value can contain spaces; in this case it will appear in the
    input file surrounded with quotes.  Value can even have quoted strings.

    >>> v = ScfVariable()
    >>> v.name = 'Var_name'
    >>> v.value = 1.
    >>> print v
    Var_name = 1.0
    >>> v.matches_substring('r_n', 'var') # only 1-st argument is actually used.
    True

    """
    def __init__(self, name='var_name', value=''):
        self.name = name
        self.value = value
        return

    def clear(self):
        """
        Sets value to empty string. Does not change the variable's name.
        """
        self.value = ''
        return

    def __str__(self):

        # Append quotes, if necessary.
        #       Note that SCF treats in correct way both cases 
        #       (checked for the title):
        #       title = ' title of the problem is "name" '
        #       title = " title of the problem is 'name' "
        value = _quoted(self.value)
        return '{0} = {1}'.format(self.name, value)

    def help(self):
        """
        Returns strings describing the variable.
        """
        return ScfHelpDictionary[self.name]

    def matches_substring(self, substr, *args):
        """
        Returns True if substr is a substring of the variable's name.

        The other arguments, *args, are dummy; they are necessary to make
        signature of the method equal in all three classes: ScfVariable,
        ScfTable and ScfSwitch.
        """
        return substr in self.name


class ScfTable(object):
    """
    O-O representation of an SCF table. 
    
    The class gives possibility to set  table column names and data. String
    representation of an instance of this class is a valid entry for the SCF input file.

    Work with external files not implemented.

    Column names can be specified at the initialization or later,
    using the columns attribute:

    >>> t = ScfTable('col_1', 'col_2', 'col_3')
    >>> t.columns.append('col_4')
    >>> print t
    file = this_file
    col_1   col_2   col_3   col_4
    !

    Check if the table column names contain substrings. This method is used to find
    particular table by its columns names:

    >>> t.matches_substring('col_')
    True
    >>> t.matches_substring('col_', 'a')
    False

    Table data is set by adding rows to the rows attribute:

    >>> t.rows.append([0, 1, 5, 'a'])
    >>> t.rows.append([1, 1, 4])
    >>> t.rows.append([2, 1, 3, 'c'])
    >>> t.rows.append([3, 1, 2])
    >>> print t
    file = this_file
    col_1   col_2   col_3   col_4
        0       1       5       a
        1       1       4       /
        2       1       3       c
        3       1       2       /
    !

    To get table data one can use directly the rows attribute, or one can use
    indexes. If index in an integer, it is the row's index. If index is a
    string matching a column name, a list containing a copy of the column data
    is returned. If index is a tuple of two integers, they are row and column
    indexes.

    >>> t[0]       # 0-th row
    [0, 1, 5, 'a']
    >>> t['col_3'] # column
    [5, 4, 3, 2]
    >>> t['col_4'] # note that column name need not be complete
    ['a', None, 'c', None]
    >>> t[0, 2]    # (row, column)-th table element.
    5

    A string representation of a ScfTable is valid for the SCF input file. the
    number of columns is determined by the columns and rows attributes.  A
    special case: number of columns is less than the number of row elements.
    This case appears, for example, when representing the second table of the
    channel_layout group. In this case one has to set explicitly the
    maximal number of columns to the NCmax attribute.

    >>> t = ScfTable()
    >>> t.columns.append('channel')
    >>> t.columns.append('max_40_x_(neighbour+gap+distance)')
    >>> t.rows.append([1, 2, 1., 1.])
    >>> t.rows.append([2, 3, 1., 1.])
    >>> print t      # wrong table, rows do not end with /
    file = this_file
    channel   max_40_x_(neighbour+gap+distance)            
          1                                   2   1.0   1.0
          2                                   3   1.0   1.0
    !

    >>> t.NCmax = 19
    >>> print t      # correct table, rows do end with /
    file = this_file
    channel   max_40_x_(neighbour+gap+distance)                                                          
          1                                   2   1.0   1.0   /                                          
          2                                   3   1.0   1.0   /                                          
    !

    """
    def __init__(self, *args):
        self.__c = list(args)     # column names.
        self.__r = []             # list with rows. Each element -- a list of table entries.
        self.__n = None           # max. number of columns.

    def __getitem__(self, key):
        if isinstance(key, int):
            # only one index given. Assume it is row's index,
            # return the whole row
            return self.__r[key]
        elif isinstance(key, tuple):
            # tuple is given. Assume this is (row, column) indices.
            i, j = key
            return self.__r[i][j]
        elif key in self.__c:
            # key is the name of the column. Return the whole column
            j = self.__c.index(key)
            col = []
            for r in self.__r:
                try:
                    e = r[j]
                except IndexError:
                    e = None
                col.append(e)
            return col
        else:
            raise ValueError('Unsupported index value', i)

    @property
    def rows(self):
        return self.__r

    @property
    def columns(self):
        return self.__c

    def clear(self):
        """
        Removes all table's data.

        Does not change the column names and the number of columns!
        """
        self.__r = []

    def help(self):
        """
        Returns help entries for all table columns. 
        """
        res = []
        for cn in self.columns:
            res.append(cn)
            res.append('-'*len(cn))
            res.append(ScfHelpDictionary[cn])
            res.append('\n')
        return '\n'.join(res)


    @property
    def NCmax(self):
        """
        Maximal number of columns. 
        
        By default, it is set to None. In this case, the number of columns in
        the table is defined by the actually specified colmun names and by the
        actual table data.
        
        NCmax can be set manually. In this case, only this amount of column
        names and row elements is printed out.

        If a row contains less than NCmax elements, the corresponding string
        ends with the '/' character. Missing column names are replaced with
        empty string, '', so that they are not seen in the print-out.
        """
        if self.__n is None:
            NC1 = len(self.__c)
            NC2 = max( [0] + map(len, self.__r) )
            NCmax = max(NC1, NC2)
            return NCmax
        else:
            return self.__n

    @NCmax.setter
    def NCmax(self, value):
        self.__n = int(value)
        return

    def __str__(self):
        # prepare column names
        NCmax = self.NCmax
        Ncol = len(self.__c)
        if NCmax >= Ncol:
            cols = self.__c + ['']*(NCmax - Ncol)
        else:
            cols = self.__c[:NCmax]

        # prepare rows
        rows = []
        for r in self.__r:
            Nrow = len(r)
            if NCmax > Nrow:
                row = r[:] + ['/'] + ['']*(NCmax - Nrow - 1)
            elif NCmax == Nrow:
                row = r[:]
            else:
                row = r[:NCmax]
            # add quotes, if necessary:
            row = map(_quoted, row)
            rows.append(row)


        res = []
        res.append('file = this_file')

        # find columns width
        wmax = map(len, cols)
        for r in rows:
            w = map(lambda x: len(str(x)), r)
            wmax = map(max, zip(wmax, w))

        # format string
        f = map(lambda (i, x): '{{{0}:>{1}}}'.format(i, x), enumerate(wmax))
        f = '   '.join(f)

        # table head
        res.append(f.format(*cols))
        # table data
        for r in rows:
            res.append(f.format(*r))
        # end table with !, otherwise the end is not detected.
        res.append('!')

        return '\n'.join(res)

    def matches_substring(self, *args):
        """
        Returns true if each of the arguments is a substring of the table's
        column names.
        """
        for ss in args:
            found = False
            for c in self.__c:
                if ss in c:
                    found = True
                    break
            if not found:
                return False
        return True


class ScfSwitch(list):
    """
    O-O representation of a switch group.

    Switch group is a list of state names (order of states in the SCF input file
    is predefined). State of the switch is allways specified. State can
    be negative, in this case all states are 'off' (default). String representation 
    of an instance of the ScfSwitch class is a valid entry for the SCF input.

    >>> ss = ScfSwitch()
    >>> ss.append('levy')
    >>> ss.append('zuber')
    >>> print ss
    levy = off
    zuber = off
    <BLANKLINE>

    The switch state can be specified as an integer (index of the state, the
    first state has index 0), or as a string containing part of the state name.
    If state set to a negative integer, all states are turned off.

    >>> ss.state = 0  # set state by integer
    >>> print ss
    levy = on
    zuber = off
    <BLANKLINE>
    >>> ss.state = 'zub' # set state by (unique) part of the state name
    >>> print ss
    levy = off
    zuber = on
    <BLANKLINE>
    >>> ss.state = -1  # turn off switch.
    >>> print ss
    levy = off
    zuber = off
    <BLANKLINE>

    Check if a switch state names have particular substrings:

    >>> ss.matches_substring('lev')
    True
    >>> ss.matches_substring('lev', 'za')
    False

    """
    def __init__(self, *args):
        super(ScfSwitch, self).__init__(args)
        self.__s = None # initial state.
        return

    def clear(self):
        """
        Resets the switch state to the default position. 
        
        Does not change the switch options!
        """
        self.state = None

    @property
    def state(self):
        """
        Integer index representing the switch's current state. Can be negative.

        When set, one can set it to an integer or a string. In the latter
        case the state with matching name will be chosen.

        By default is None.

        """
        return self.__s

    @state.setter
    def state(self, value):
        if isinstance(value, str):
            # value can be part of the state's name
            for (i, name) in enumerate(self):
                if value in name:
                    self.__s = i
                    break
        elif isinstance(value, int):
            self.__s = value
        else:
            raise ValueError('Unknown state')
        return

    def __str__(self):
        vals = ['off'] * len(self)
        if self.__s >= 0:
            # self.__s is the index.
            vals[self.__s] = 'on'

        res = []
        for (n, v) in zip(self, vals):
            var = ScfVariable(n, v)
            res.append(str(var))
        res.append('')
        return '\n'.join(res)

    def help(self):
        """
        Returns description of the SCF switch. 
        """
        res = []
        for e in self:
            res.append(cn)
            res.append('-'*len(e))
            res.append(ScfHelpDictionary[e])
            res.append('\n')
        return '\n'.join(res)

    def matches_substring(self, *args):
        """
        Returns True if each of the arguments is a substring of the switch' state name
        """
        for ss in args:
            found = False
            for n in self:
                if ss in n:
                    found = True
                    break
            if not found:
                return False
        return True


class ScfGroup(list):
    """
    A list of switches, variables, tables.

    The group's name must be specified at the initialization. It can be
    followed by the elements constituting the list.

    >>> g = ScfGroup('group_name')
    >>> g.append(ScfTable('col_1', 'col_2'))
    >>> g[0].rows.append([1, 2])
    >>> g[0].rows.append(['a'])
    >>> g.append(ScfVariable('keyword', 0.))
    >>> g.append(ScfSwitch('state_1', 'state_2'))
    >>> print g
    <BLANKLINE>
    ! --------------------------------------------------------------------------------
    &group_name
    file = this_file
    col_1   col_2
        1       2
        a       /
    !
    keyword = 0.0
    state_1 = off
    state_2 = off
    <BLANKLINE>
    !

    One can search elements of the group by their names.

    >>> g.find('col') # returns all matches in a list          #doctest:+ELLIPSIS
    [<__main__.ScfTable object at ...>]
    >>> g['col']      # returns the first matched element      #doctest:+ELLIPSIS
    <__main__.ScfTable object at ...>

    """
    def __init__(self, name, *args):
        super(ScfGroup, self).__init__(*args)
        self.__n = name
        return

    @property
    def name(self):
        """
        The group's name. Defined at the instance' initialisation.
        """
        return self.__n

    def clear(self):
        """
        Calls clear method of each element in the group
        """
        for e in self:
            e.clear()

    def find(self, *names):
        """
        Returns list of all group elements (i.e. switches, tables, variables)
        whose names contain name as a substring.
        """
        res = []
        for e in self:
            if e.matches_substring(*names):
                res.append(e)
        return res

        # res = []
        # res += self.find_table(name)
        # res += self.find_variable(name)
        # res += self.find_switch(name)
        # return res


    def matches_substring(self, substr, *args):
        """
        Returns True if substr is a substring of the group's name.

        For the meaning of *args see description of 
        ScfVariable.matches_substring()
        """
        return substr in self.__n

    def __getitem__(self, *keys):
        """
        If keys has only one integer element, the method has the usual
        functionality -- it returns the list's item with specified index.

        In other cases the *keys arguments are passed to the find method and
        the first found element is returned.

        The difference between indexing and using find() method: the self.find
        always returns a list of all matched elements, which is possibly emply.
        This method returns only the first matched element and raises the
        KeyError if nothing found.
        """
        if len(keys) == 1 and isinstance(keys[0], int):
            return super(ScfGroup, self).__getitem__(keys[0])
        else:
            res = self.find(*keys)
            if len(res) == 0:
                # return None
                raise KeyError('Group contains no element with name specified by ', *keys)
            else:
                return res[0]

    def set_variables(self, name, *args):
        """
        To all variables of the group having 'name' in the name, set values
        specified in args.

        >>> g = ScfGroup('group_name')
        >>> g.append(ScfVariable('var1'))
        >>> g.append(ScfVariable('var2'))
        >>> g.append(ScfVariable('var3'))
        >>> g.append(ScfVariable('var4'))
        >>> g.set_variables('var', 1, 2, 3, 4)
        >>> print g
        <BLANKLINE>
        ! --------------------------------------------------------------------------------
        &group_name
        var1 = 1
        var2 = 2
        var3 = 3
        var4 = 4
        !

        """
        # prepare list of variables:
        vlist = filter(lambda o: hasattr(o, 'value'), self.find(name))
        for (var, value) in zip(vlist, args):
            var.value = value
        return


    def __str__(self):
        res = ['', '! ' + '-'*80, '&{0}'.format(self.__n)]
        for e in self:
            res.append(str(e))
        res.append('!')
        return '\n'.join(res)
