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

import time
import platform
import subprocess
import re

from ...tools.file_lines import get_last_line

#rm
# Author: Richard Molitor, richard.molitor@student.kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#rm

def enva(varname):
    """
    Returns the OS-aware name of the environment variable ``varname``.

    For example, for varname 'PATH', it returns '$PATH' under linux and
    '%PATH%' under windows.
    """
    psystem = platform.system()
    if psystem == 'Linux':
        res = '${0}'.format(varname)
    elif psystem == 'Windows':
        res = '%{0}%'.format(varname)
    else:
        raise NotImplementedError('Function not implemented for OS ' , psystem)
    return res

class Job(object):
    """
    A shell job to be executed by the OS shell. A job is described by a command
    and a working directory. The working directory is optional, if ommited, the
    current directory is used. For example:

    >>> j = Job('echo hello')
    >>> j
    <job cd '.'; echo hello>

    >>> j = Job('sleep 4', '/home')
    >>> j
    <job cd '/home'; sleep 4>

    If the string you pass as working directory does not describe a directory
    on your current machine, a ValueError is raised, e.g.

    >>> j = Job('sleep 1', '+4w34"\d')
    Traceback (most recent call last):
    	...
    ValueError: not a directory: +4w34"\d

    To execute a job, add it to a scheduler, queue() it and wait().

    """

    def __init__(self, cmd, dir = os.curdir):
        """
        Create a new job consisting of a shell command cmd to run and a working
        directory dir in which to execute.

        If dir is not a directory or not accessible by the current user, a
        ValueError is raised. If no directory is specified, the current working
        directory is used.

        """

        self.cmd = cmd
        self.dir = dir

    @property
    def cmd(self):
        """Command to be run in the OS shell.

        Must be a string.
        """
        return self.__cmd

    @cmd.setter
    def cmd(self, value):
        self.__cmd = str(value)

    def __repr__(self):
        return "<job cd '%s'; %s>" % (self.dir, self.cmd)

    @property
    def dir(self):
        """Working directory.

        Directory where cmd OS shell command is started.
        """
        return self.__dir

    @dir.setter
    def dir(self, value):
        if not os.path.isdir(value):
            raise ValueError('not a directory: %s' % dir)

        if not os.access(value, os.X_OK):
            raise ValueError('cannot access directory: %s' % dir)
        self.__dir = value


class Scheduler(object):
    """Scheduler for jobs.

    A scheduler for running shell jobs. A scheduler consists of a dict of jobs
    and a queue. The ``add()`` method registers a new job, the ``queue()`` method adds
    a job to the queue and the ``wait()`` method waits for a queued job to finish.
    The convenience method ``run()`` does both queuing and waiting in one call and
    returns the result of the wait.

    Currently, all jobs will be run in the OS shell using the subprocess
    module, this may change at some point in the future.

    """

    def __init__(self):
        """
        Create a new empty job scheduler.

        """

        self.jobs = {}
        self.queued = {}
        return

    def __repr__(self):
        return self.jobs.__repr__()

    def get_job(self, j):
        """
        Get a job that was added to the scheduler, identified by its name.
        Alternatively just use dictionary syntax (see last example):

        >>> s = Scheduler()
        >>> j = Job('echo hello world')
        >>> s.add('j', j)
        >>> s.get_job('j')
        <job cd '.'; echo hello world>
        >>> s['j']
        <job cd '.'; echo hello world>
        """
        return self.jobs[j]

    def __getitem__(self, j):
        return self.get_job(j)

    def add(self, name, job):
        """
        Add a job to the scheduler. It will be identified by name, any existing
        job with the same name is replaced.

        """

        self.jobs[name] = job
        self.queued[name] = []

    def run(self, name, **kwargs):
        """
        Queue the job identified by name to the job queue wait for it to finish
        and return the result. For example:

        >>> s = Scheduler()
        >>> s
        {}
        >>> s.add('hi', Job('echo hi'))
        >>> s.run('hi')
        'hi\\n'

        You can also wait for a number of seconds or for the creation of a file
        in the execution directory of the Job. You can combine these options:

        >>> s = Scheduler()
        >>> s.add('t', Job('touch test'))
        >>> s.run('t', sec=1, file='test')
        ''

        The kwargs dictionary is passed to the wait() method, see description of
        allowed keyword arguments there.

        """

        t1 = time.time()
        self.queue(name)
        r = self.wait(name, **kwargs)
        t2 = time.time()
        self.run_time = t2 - t1
        return r

    def queue(self, name):
        """
        Add the job identified by name to the current job queue. The same job
        may be queued several times.

        If no job by the given name exists, a ValueError is raised, e.g:

        """

        if name in self.jobs:
            job = self.get_job(name)
            print 'scheduler queued job', job, name
            data = self.__queue_shelljob(job)
            self.queued[name].append(data)
        else:
            raise ValueError('no such job: %s' % name)
        return

    def _wait(self, name, **kwargs):
        """
        Wait for the queued job identified by name to finish. If the same job
        is queued several times, only wait for the first completion.

        If the job identified by name is not queued, a ValueError is raised,
        e.g:

        >>> s = Scheduler()
        >>> s.add('j', Job('echo hi'))
        >>> s.wait('j')
        Traceback (most recent call last):
            ...
        ValueError: job not in queue: j

        Additionally, you can pass 'sec' and 'file' as keyword arguments:

        >>> s = Scheduler()
        >>> s.add('t', Job('touch test'))
        >>> s.queue('t')
        >>> s.wait('t', sec=1, file='test')
        ''

        """

        # wait for creation of file f:
        # there's better ways to do this, but not easily portable between
        # Windows and Unix without extra dependencies
        def waitFile(f):
            # print 'scheduler.wait(): waits for file ', f
            # try: os.access(f, os.R_OK)
            # except ValueError: # could not access, try again in 1 second
            #     print 'scheduler.wait(): sleep for 5 sec'
            #     time.sleep(5)
            #     waitFile(f)
            while not os.access(f, os.R_OK):
                # print 'scheduler.wait(): sleep for 5 sec'
                time.sleep(5)


        try:

            for arg in kwargs:
                if arg == "sec":
                    time.sleep(kwargs[arg])
                else:
                    if arg != "file":
                        raise ValueError('unsupported keyword argument %s' % arg)

            data = self.queued[name].pop()
            r = self.__finish_shelljob(data)

            dir = self.get_job(name).dir

            for arg in kwargs:
                if arg == "file":
                    waitFile(os.path.join(dir, kwargs[arg]))

        except IndexError:
            raise ValueError('job not in queue: %s' % name)

        return r

    def wait(self, name, **kwargs):
        """
        Wait for the started job to finish.

        Criteria to define whether job is finished or not, depend on the specified
        keyword arguments:

            sec:
                number of seconds to wait.

            files:
                list of filenames. Wait untill all files specified in the list
                exist (created by the job).  If this argument specified, the
                sec argument defines the period to check file existence.

            llines:
                list of regexp strings (not regex objects!) to compare with the
                last string of file specified in the files argument. The
                llines argument implies that the files argument is given and
                that they have equal lengths. Criteria meet, if all files
                exist and their last lines match the regexp strings.
        """
        # default: wait for 5 sec.
        args = {'sec':5}
        args.update(kwargs)
        sec = args['sec']

        print 'scheduler waits with parameters', args

        if 'llines' in args.keys():
            # check that files exist and compare last lines
            files = map(lambda f: os.path.join(self.get_job(name).dir, f), args['files'])
            regex = map(lambda s: re.compile(s), args['llines'])
            passed = False
            while not passed:
                print time.strftime('%c', time.localtime())
                for f, r in zip(files, regex):
                    print '    ', f,
                    if os.access(f, os.R_OK):
                        print 'exists',
                        ll = get_last_line(f)
                        if ll and r.match(ll):
                            print 'last line matches'
                            passed = True
                        else:
                            print 'last line mismatch'
                            passed = False
                            break
                    else:
                        print "doesn't exist"
                        passed = False
                        break
                time.sleep(sec)
        elif 'files' in args.keys():
            # check that files exist
            files = map(lambda f: os.path.join(self.get_job(name).dir, f), args['files'])
            passed = False
            while not passed:
                for f in files:
                    if os.access(f, os.R_OK):
                        passed = True
                    else:
                        passed = False
                        break
                time.sleep(sec)
        else:
            # simply wait for sec seconds
            time.sleep(sec)

        data = self.queued[name].pop()
        r = self.__finish_shelljob(data)
        return r


    def __queue_shelljob(self, j):
        return subprocess.Popen(j.cmd, shell=True, stdout=subprocess.PIPE, cwd=j.dir)

    def __finish_shelljob(self, proc):
        """
        proc is an instance of subprocess.Popen() created in __queu_shelljob.
        """
        # proc.wait()
        (out,err) = proc.communicate()
        return out

if __name__ == '__main__':
    import doctest
    doctest.testmod()
