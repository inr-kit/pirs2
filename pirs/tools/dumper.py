"""
Interface to the pickle dump and load functions.
"""

import cPickle as pickle
import sys, os
from time import gmtime, strftime
from string import digits, ascii_uppercase, ascii_lowercase


def dump(filename, protocol=1, owerwrite=True, **kwargs):
    """
    Dump to a file the keyword arguments.

    Argument protocol is an integer specifying the protocol used. -1 -- for the
    highest protocol version, 1 for binary.

    >>> dump('tmp.dump', a1='abs', a2='kwd')
    >>> d = load('tmp.dump')
    >>> for (k, v) in d.items():     # doctest: +ELLIPSIS
    ...     print k, v
    ...
    a1 abs
    _main_script ...
    a2 kwd
    _timestamp ...

    There are some additional values saved: path to the program, and the time
    dump was created.

    """

    if owerwrite:
        output = open(filename, 'wb')
    else:
        raise NotImplementedError
            

    # put some description to the dumped objects
    kwargs['_main_script'] = os.path.abspath(sys.argv[0])
    kwargs['_timestamp'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    pickle.dump(kwargs, output, protocol)
    output.close()
    return

def load(filename):
    """
    Read dump from filename. 

    A dictionary specifying the keyword arguments used in dump() is returned.

    >>> d = load('tmp.dump')
    >>> for (k, v) in d.items():     # doctest: +ELLIPSIS
    ...     print k, v
    ...
    a1 abs
    _main_script ...
    a2 kwd
    _timestamp ...
    """

    with open(filename, 'rb') as input_:
        dict_ = pickle.load(input_)
    return dict_




if __name__ == '__main__':
    import doctest
    doctest.testmod()

