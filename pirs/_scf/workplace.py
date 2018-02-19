import os
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

from ..core import scheduler

SCFPATH = os.environ.get('SCF', scheduler.enva('SCF'))


class ScfWorkPlace(scheduler.WorkPlace):
    """
    """
    def __init__(self):
        super(ScfWorkPlace, self).__init__()
        self.prefix = 'scf'

        # Input deck. Input
        self.__inp = scheduler.InputFile()
        self.__inp.basename = 'input.txt'

        # batch files. There are three parts: 
        #  1: before the SCF command line
        #  2: the SCF command line
        #  3: after the SCF command line
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

        # SCF output files:
        self.__out = scheduler.InputFile()
        self.__out.basename = 'output.txt'
        self.__clean = scheduler.InputFile()
        self.__clean.basename = 'clean.txt'

        # path to SCF executable
        self.__exe = SCFPATH
        
        return


    @property
    def batch(self):
        return self.__bat2

    @property
    def batch_before(self):
        return self.__bat1

    @property
    def batch_after(self):
        return self.__bat3

    @property
    def input(self):
        return self.__inp

    @property
    def clean(self):
        return self.__clean

    @property
    def output(self):
        return self.__out

    @property
    def exe(self):
        return self.__exe

    @exe.setter
    def exe(self, value):
        self.__exe = os.path.abspath(value)
        return

    def run(self, mode='r', **kwargs):
        self.files = []
        lmode = mode.lower()
        if lmode == 'r':
            # input file
            self.files.append(self.input)

        else:
            raise ValueError('Unknown mode: ', mode)

        # batch file, needed allways
        self.__bat2.string = self.exe + ' > scf.stdout'
        self.files.append(self.__bat1)
        self.files.append(self.__bat2)
        self.files.append(self.__bat3)

        # prepare the working place
        super(ScfWorkPlace, self).prepare()

        # prepare job
        j = scheduler.Job(os.path.join(os.path.curdir, self.batch.basename), self.lcd)
        s = scheduler.Scheduler()
        s.add('j', j)
        print 'Started scf, ', j
        # start Job:
        if mode.isupper():
            self.stdout = s.run('j')
            # NOTE: under windows, a long stdout results in
            #       hanging the process started by job.run(). Therefore,
            #       the MCNP std.out is redirected to mcnp.stdout in the 
            #       batch file.

            # save the name of the output file:
            self.__out.exfile = os.path.join(self.lcd, 'output.txt')


        return



if __name__ == '__main__':
    import doctest
    doctest.testmod()

