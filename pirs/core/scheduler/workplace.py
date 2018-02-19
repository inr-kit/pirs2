import os
import stat
import shutil
import __main__ as main
from datetime import datetime

from .scheduler import Scheduler, Job

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


def find_highest_index(dir_, prefix):
        #
        # author: Richard Molitor, KIT, 2012
        #
        files    = os.listdir(dir_)
        matches  = filter(lambda f: f.startswith(prefix), files)
        # suffixes = map(lambda f: f.strip(prefix), matches)  # this strips all characters specified in prefix from both sides of f. Try: 'c1wp1'.strip('c1wp')
        l = len(prefix)
        suffixes = map(lambda f: f[l:], matches)
        indexes  = list(map(lambda f: int(f) if f.isdigit() else 0, suffixes))

        indexes.append(0)
        return sorted(indexes, reverse=True)[0]

class InputFile(object):
    """File to be written to a workplace.

    Content of the file is specified as a string or as a link to
    existing file.

    """
    def __init__(self, **kwargs):
        """
        Keyword arguments can specify all properties of the instance.

        If arguments 'exfile', 'string' and 'spf' are specified in kwargs,
        the order they are set is exactly as specified here.

        >>> f = InputFile(basename='if.init', string='string', exfile='_inp')
        >>> f.write()
        >>> print open(f.basename).read()

        >>> f = InputFile(basename='if.init', exfile='_inp', psf=True)
        >>> f.write()
        >>> print open(f.basename).read()

        """
        self.__str = None
        self.__exf = None
        self.__psf = True # the "Prefer String Flag"

        self.__rep = None # report

        self.__bn = 'inputfile'
        self.__mode = 'w'
        self.__executable = False
        self.__cmd = None

        # process keyword arguments
        pkeys = ['basename', 'mode', 'exfile', 'string', 'psf'] # possible keys. The order is imoprtant!
        gkeys = kwargs.keys()                                   # given keys
        for key in pkeys:
            if key in gkeys:
                setattr(self, key, kwargs[key])
        return

    @property
    def string(self):
        """
        String to be written into the target file.
        """
        return self.__str

    @string.setter
    def string(self, value):
        self.__str = value
        if value is not None:
            self.__psf = True
        else:
            self.__psf = False
        return

    @property
    def exfile(self):
        """
        Path to the external file, to be copied to the target file.
        """
        return self.__exf

    @exfile.setter
    def exfile(self, value):
        self.__exf = value
        if value is not None:
            self.__psf = False
        else:
            self.__psf = True
        return

    @property
    def psf(self):
        r"""
        The "Prefer String Flag".

        Specifies what to put to the target file if both ``string`` and ``exfile``
        attributes are specified. If True, string is preffered, if False, exfile
        is preffered.

        This property set automatically each time string or exfile is set.

        Can be manually set by user.

        >>> f = InputFile(string='string', exfile='existting.file', basename='if.psf')
        >>> f.psf = True
        >>> f.write()
        >>> print open(f.basename).read()

        >>> f.psf = False
        >>> f.write()
        >>> print open(f.basename).read()

        """
        return self.__psf

    @psf.setter
    def psf(self, value):
        self.__psf = value
        return

    @property
    def report(self):
        """
        Report about the last written target file.
        """
        return self.__rep

    @property
    def defined(self):
        """
        Returns True if string or exfile is specififed.
        """
        return (self.string is not None) or (self.exfile is not None)

    @property
    def mode(self):
        """
        Writing mode. Can be 'w'  or 'a'.

        If mode is 'w', the target file is rewritten. In this case, exfile is
        copied.

        If mode is 'a', file fileName is appended. In this case, exfile is read
        and appended to fileName line by line. This might be inappropriate for
        a binary exfile.

        >>> f = InputFile(basename='if.mode', string='Line 1')
        >>> f.write()
        >>> print open(f.basename).read()
        >>> f.mode = 'a'
        >>> f.write()
        >>> print open(f.basename).read()


        """
        return self.__mode

    @mode.setter
    def mode(self, value):
        if value in ['w', 'a']:
            self.__mode  = value
        else:
            raise ValueError('Undefined value for mode: ', value)
        return

    @property
    def executable(self):
        """
        True this file should be marked executable (necessary for scripts);
        False otherwise (appropriate for input and output files). Default value
        is False.

        """
        return self.__executable

    @executable.setter
    def executable(self, value):
        if isinstance(value, bool):
            self.__executable = value
        else:
            raise ValueError('Non-boolean value for executable flag: ', value)
        return

    @property
    def cmd(self):
        """
        Command used to run input file. Setting this value also sets
        `executable` property to True.
        """
        if self.__cmd is None:
            return './' + self.basename
        else:
            return self.__cmd

    @cmd.setter
    def cmd(self, value):
        self.__cmd = str(value)
        self.executable = True
        return

    @property
    def basename(self):
        """
        Basename of the file to be written.
        """
        return self.__bn

    @basename.setter
    def basename(self, value):
        self.__bn = value
        return

    def write(self, path=os.curdir):
        """Write file to disk.

        Create a new file containing string if ``string`` attribute is specified,
        or copy existing file pointed to by the ``exfile`` attribute.

        """

        target = os.path.join(path, self.basename)

        if not self.defined:
            self.__rep = 'nothing written'
        elif self.__psf:
            # put string to the target file
            if isinstance(self.__str, list):
                string = '\n'.join(self.__str)
            elif isinstance(self.__str, str):
                string = self.__str[:]
            else:
                raise TypeError('Wrong type of string: ', self.string.__class__.__name__)
            i = open(target, self.__mode)
            i.writelines(string)
            i.close()
            self.__rep = "generated from string"
        else:
            # copy the external file to the target file
            if self.__mode == 'w':
                shutil.copy(self.__exf, target)
                self.__rep = r"copied from '{0}'".format(self.__exf)
            else:
                t = open(target, 'a')
                t.write('\n') # otherwise, the first line of the apended file concatenates to the last line of axisting file.
                t.writelines(open(self.__exf, 'r').readlines())
                t.close()
                self.__rep = r"added content of '{0}'".format(self.__exf)

        if self.defined and self.__executable:
            mode = os.stat(target).st_mode
            os.chmod(target, mode | stat.S_IXUSR)

        return

    def __str__(self):
        return "<InputFile basename={0} mode={1} string={2} exfile={3}>".format(self.basename, self.__mode, repr(self.__str), repr(self.__exf))


_default_scheduler = Scheduler()

class WorkPlace(object):
    r"""
    Defines common directory name and a
    list of InputFiles to be put to the directory.

    Method WorkPlace.prepare() creates folder 'nameID', where 'name' is the
    common directory name and 'ID' is an unique integer number. The name of the
    last created folder is saved in the WorkPlace.lcd property.

    >>> wp = WorkPlace()
    >>> print wp.prefix, wp.nextID, wp.lcd
    wp 0 None
    >>> wp.prepare()
    >>> print wp.report
    'wp0' created
    >>> print wp.prefix, wp.nextID, wp.lcd
    wp 1 wp0

    One can specify files to be put to the work place using the WorkPlace.files
    list:

    >>> f1 = InputFile()
    >>> f1.basename = 'f1'
    >>> f1.string = 'f1 content\n'
    >>> f2 = InputFile()
    >>> f2.basename = 'f2'
    >>> f3 = InputFile()
    >>> f3.basename = 'f3'
    >>> f3.string = 'f3 content'
    >>> wp.files.append(f1)
    >>> wp.files.append(f2)
    >>> wp.files.append(f3)
    >>> wp.prepare()
    """

    def __init__(self):
        #: Directory name prefix
        self.prefix = 'wp'

        #: Integer part of the name for the next directory
        self.nextID = 0

        self.__files = []
        self.__rep = None

        #: Default scheduler, used to run executable input file.
        self.scheduler = _default_scheduler # scheduler used to start workplace-related jobs.

        self.__lcd = None  # last created directory. Set by prepare

        return

    @property
    def report(self):
        """
        String describing the last created folder: its name and files in it.
        """
        return self.__rep

    @property
    def lcd(self):
        """
        The name of the last created directory.
        """
        return self.__lcd

    def __cdn(self):
        """
        Method defines how to construct directory name from prefix and nextID.
        """
        return '{0}{1}'.format(self.prefix, self.nextID)

    def prepare(self):
        """
        Creates directory with the next available directory name. If necessary,
        changes the nextID attribute.

        Puts input files.
        """
        # create directory
        try:
            os.mkdir(self.__cdn())
        except OSError:
            self.nextID = find_highest_index(os.curdir, self.prefix) + 1
            os.mkdir(self.__cdn())
        finally:
            self.__lcd = self.__cdn()  # remember the name of the last created directory.
            self.nextID += 1
        # if python is called in interactive mode, main.__file__ is undefined. Take this into account:
        filename = getattr(main, '__file__', 'interactive')
        report = ['{0} created by script {1} at {2}'.format(repr(self.__lcd), filename, datetime.today())]
        # put files
        for f in self.__files:
            f.write(self.__lcd)
            report.append('    {0} {1}'.format(repr(f.basename), f.report))
        self.__rep = '\n'.join(report)
        # write report about the created workplace
        log = open(os.path.join(self.__lcd, 'workplace.report'), 'a')
        log.write(self.__rep)
        log.close()
        return

    @property
    def files(self):
        """List of files to be written to the workplace directory.

        Elements must be instances of the InputFile class.
        """
        return self.__files

    def run(self, **kwargs):
        """
        Find executable input file in files and starts it using scheduler
        module.

        Assumes that directory containing all input files allready created with
        the prepare() method.

        Keyword arguments are all passed to the scheduler.Scheduler.run()
        method, see description there.
        """
        # find 1-st executable InputFile:
        e = None
        for f in self.__files:
            if f.executable:
                e = f
                break
        if e is not None:
            # create Job:
            j = Job(e.cmd, self.lcd)
            n = self.lcd + e.cmd
            self.scheduler.add(n, j)
            r = self.scheduler.run(n, **kwargs)
            return r

    def __str__(self):
        return "<WorkPlace prefix={0} nextID={1}>".format(self.prefix, self.nextID)





if __name__ == '__main__':
    import doctest
    doctest.testmod()

