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

Representation of MCNP workplace.

MCNP workplace is a directory containing all files that are necessary to start MCNP.
"""
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import os

from ..core import scheduler
from . import outp

#: $MCNP environment variable.
MCNPPATH = os.environ.get('MCNP', scheduler.enva('MCNP'))


class McnpWorkPlace(scheduler.WorkPlace):
    """Describes directory containing all files necessary to start MCNP.

    This class also defines a method to start MCNP in several modes (plot, transport, continue).

    """
    def __init__(self):
        super(McnpWorkPlace, self).__init__()
        self.prefix = 'mcnp'

        # Input deck. Input
        self.__inp = scheduler.InputFile()
        self.__inp.basename = 'i_'

        # batch files. There are three parts: 
        #  1: before the MCNP command line
        #  2: the MCNP command line
        #  3: after the MCNP command line
        #
        # Parts 1 and 3 can become useful when preparing 
        # scripts to a cluster scheduler.
        self.__bat1 = scheduler.InputFile()
        self.__bat1.basename = 'batch.bat'
        self.__bat1.executable = True
        self.__bat2 = scheduler.InputFile()
        self.__bat2.basename = 'batch.bat'
        self.__bat2.executable = True
        self.__bat2.mode = 'a'
        self.__bat3 = scheduler.InputFile()
        self.__bat3.basename = 'batch.bat'
        self.__bat3.executable = True
        self.__bat3.mode = 'a'

        # plotting commands file. Input
        self.__com = scheduler.InputFile()
        self.__com.basename = 'c_'
    
        # srctp. input and output
        self.__srctp = scheduler.InputFile()
        self.__srctp.basename = 'i_s'

        # runtpe. input and output
        self.__runtpe = scheduler.InputFile()
        self.__runtpe.basename = 'i_r'

        # mctal. input (can be!) and output
        self.__mctal = scheduler.InputFile()
        self.__mctal.basename = 'i_m'

        # MCNP command line and path to MCNP executable
        self.__cmd = None      # MCNP command line parameters and options
        self.__exe = MCNPPATH  # MCNP executable
        self.__exep = ''       # part of the line before call to MCNP
        self.__exes = ''       # part of the line after call to MCNP.

        # MCNP stdout and outp are not needed to be of the InputFile
        # class. The following definitions are just to provide common
        # interface to all MCNP-related files.
        self.__log = scheduler.InputFile()
        self.__log.basename = 'mcnp.stdout'
        self.__out = scheduler.InputFile()
        self.__out.basename = 'i_o'
        self.__meshtal = scheduler.InputFile()
        self.__meshtal.basename = 'meshtal'
        return


    @property
    def batch(self):
        """
        Part of the batch file with the command line to start MCNP.

        Content of the batch file is defined by three attributes: batch_before,
        batch and batch_after.  These attributes are of the scheduler.InputFile
        class and by default have the same basename and modes 'w', 'a' and 'a',
        respectively. Thus, thier content is written to one external file.

        The line containig the command to start MCNP is concatenated the sum of
        exe_prefix, exe and exe_suffix attributes.
        
        To provide commands to be executed before and after MCNP start, define
        batch_before and batch_after attributes.

        """
        return self.__bat2

    @property
    def batch_before(self):
        """
        Content of the batch file before the line starting MCNP.

        See description of batch.
        """

        return self.__bat1

    @property
    def batch_after(self):
        """
        Content of the batch file after the line starting MCNP.

        See description of batch.
        """
        return self.__bat3

    @property
    def inp(self):
        """
        MCNP input file.

        Instance of scheduler.InputFile.
        """
        return self.__inp

    @property
    def com(self):
        """
        MCNP com file (contains commands for the MCNP geometry plotter).

        Instance of scheduler.InputFile.
        """
        return self.__com

    @property
    def srctp(self):
        """
        MCNP srctp file. 

        This is a binary file written by MCNP after a
        criticality run. Use this attribute only to put to
        workplace an existing srctp.

        Instance of scheduler.InputFile.
        """
        return self.__srctp

    @property
    def runtpe(self):
        """
        MCNP runtpe file. 

        This is a binary file written by MCNP during execution.
        Use this attribute only to put to workplace an existing
        runtpe.

        Instance of scheduler.InputFile.
        """
        return self.__runtpe

    @property
    def outp(self):
        """
        MCNP outp file. 

        An ASCII file written by MCNP. Contains detailed
        information about problem.

        Instance of scheduler.InputFile.
        """
        return self.__out

    @property
    def meshtal(self):
        """
        MCNP meshtal file.

        An ASCII file written by MCNP.

        Instance of scheduler.InputFile
        """
        return self.__meshtal

    @property
    def mctal(self):
        """
        MCNP mctal file.

        An ASCII file written by MCNP containing tally 
        results and values of Keff on each cycle.

        An instance of the scheduler.InputFile
        """
        return self.__mctal

    @property
    def exe(self):
        """
        Path to MCNP executable. 
        
        By default set to the $MCNP environmental
        variable. 
        """

        return self.__exe

    @exe.setter
    def exe(self, value):
        self.__exe = str(value)
        return

    @property
    def exe_prefix(self):
        """
        First part of the line containing the command to start MCNP.
        """
        return self.__exep 

    @exe_prefix.setter
    def exe_prefix(self, value):
        self.__exep = str(value)

    @property
    def exe_suffix(self):
        """
        Final part of the line containing the command to start MCNP.

        See exe and exe_prefix attributes.
        """
        return self.__exes

    @exe_suffix.setter
    def exe_suffix(self, value):
        self.__exes = str(value)

    def run(self, mode='r', **kwargs):
        """
        Prepares directory where MCNP will be started.

        The mode argument must be one character from 'cCpPrR'.
        Uppercase means to prepare the directory and to start MCNP,
        lowercase -- only to prepare the directory, without actually starting MCNP.

        'P': plot geometry. Requires inp or runtpe. Optionally uses com.

        'R': Initial run. Requires inp, optionally uses srctp.

        'C': Continue run. Requires runtpe, optionally uses ccard if given as an optional keyword argument.
        """
        self.files[:] = []  # clears list in-place.
        lmode = mode.lower()
        self.__cmd = ''
        if lmode == 'r':
            # run the transport problem

            # inp
            self.__cmd = ' ixr name={0}'.format(self.inp.basename)
            self.files.append(self.inp)

            # srctp, if defined
            if self.srctp.defined:
                self.__cmd += ' srctp={0}'.format(self.srctp.basename)
                self.files.append(self.srctp)

        elif lmode == 'p':
            # plot geometry

            # inp or runtpe, inp preffered:
            if self.inp.defined:
                self.__cmd = ' ip name={0}'.format(self.inp.basename)
                self.files.append(self.inp)
            elif self.runtpe.defined:
                self.__cmd = ' p runtpe={0}'.format(self.runtpe.basename)
                self.files.append(self.runtpe)
            else:
                raise IOError('inp and runtpe are not defined.')

            # com file, optional
            if self.com.defined:
                self.__cmd += ' com={0}'.format(self.com.basename)
                self.files.append(self.com)

            # MCNP must plot to a postscript, not to a screen.
            self.__cmd += ' notek plot={0}'.format(self.inp.basename)

        elif lmode == 'c':
            # continue run.

            # runtpe required
            self.__cmd = ' c runtpe={0}'.format(self.runtpe.basename)
            self.files.append(self.runtpe)

            # inp optional, if ccard is given in kwargs
            if 'ccard' in kwargs:
                # if number of cycles in the kcode card exceeds MRKP set in the previous run, warning is issued.
                # Change the kcode card, if specified, to ensure that MRKP is set explicitly.
                if 'kcode' in kwargs['ccard'].lower():
                    tokens = kwargs['ccard'].split()
                    if len(tokens) < 8:
                        tokens = tokens[:] + ['j'] * (7 - len(tokens))
                        tokens.append(tokens[4])
                    elif tokens[7].lower() == 'j':
                        tokens[7] = tokens[4]
                    kwargs['ccard'] = ' '.join(tokens)
                self.inp.string = 'CONTINUE\n{0}\n\n'.format(kwargs['ccard'])
                self.__cmd += ' name={0}'.format(self.inp.basename)
                self.files.append(self.inp)
        elif lmode == 'z':
            # TODO
            # plot (mesht)allies. This requires a runtpe file. If not specified
            # from previous run, first start the transport (similar to the  'r'
            # mode).
            raise NotImplementedError

        else:
            raise ValueError('Unknown mode: ', mode)

        # try to run parallel:
        tasks = kwargs.get('tasks', 0)
        if tasks > 0:
            self.__cmd += ' tasks {0} '.format(tasks)

        # batch file, needed allways
        self.__bat2.string = ' '.join([self.exe_prefix, self.exe, self.__cmd, self.exe_suffix, ' > mcnp.stdout'])
        if lmode in ['p', 'z']:
            # this is plot mode. MCNP generates ps file. It is always converted to pdf
            # and can be optionally converted from pdf to png.
            self.__bat2.string += '\nps2pdf {0}.ps'.format(self.inp.basename)
            formats = kwargs.get('fmt', 'pdf')
            if 'png' in formats:
                self.__bat2.string += '\nconvert {0}.pdf {0}.png'.format(self.inp.basename)
        self.files.append(self.__bat1)
        self.files.append(self.__bat2)
        self.files.append(self.__bat3)

        # prepare the working place
        super(McnpWorkPlace, self).prepare()

        # deduce next outp filename
        nout = outp.next_outp(self.__cmd, self.lcd)

        #prepare job
        j = scheduler.Job(os.path.join(os.path.curdir, self.batch.basename), self.lcd)
        s = scheduler.Scheduler()
        s.add('j', j)
        print 'Started mcnp {0} mode={1}, kwargs={2}'.format(j, mode, kwargs)

        # start Job:
        if mode.isupper():
            self.stdout = s.run('j', files=[nout], llines=[outp.RELL], sec=kwargs.get('sec', 5))
            self.run_time = s.run_time
            # NOTE: under windows, a long stdout results in
            #       hanging the process started by job.run(). Therefore,
            #       the MCNP std.out is redirected to mcnp.stdout in the 
            #       batch file.

            # update filenames, if run was successful

            # the outp name:
            self.__out.exfile = os.path.join(self.lcd, nout)

            names = outp.get_filenames(self.__out.exfile)
            if names['terminated'] is not None and 'fatal' in names['terminated']:
                raise OSError('MCNP ended with fatal errors\n', self.stdout)
            else:
                # update filenames only if they were
                # actually generated. If no new file
                # was generated, do nothing.
                if names['srctp'] is not None:
                    self.__srctp.exfile = names['srctp']
                if names['runtpe'] is not None:
                    self.__runtpe.exfile = names['runtpe']
                if names['meshtal'] is not None:
                    self.__meshtal.exfile = names['meshtal']
                if names['mctal'] is not None:
                    self.__mctal.exfile = names['mctal']
            # append log to the report file:
            log = open(os.path.join(self.lcd, 'workplace.report'), 'a')
            print >>log
            print >>log, 'files generated by MCNP: ', names
            print >>log
            log.close()
        return



