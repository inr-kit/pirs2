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

Functions to read outp file.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import os.path
import os
from datetime import datetime
import sys
import glob

#: Regex string for the last outp line.
RELL = '^ mcnp  *version .* probid'

def get_filenames(outp):
    """Extracts filenames written by MCNP from outp.

    Reads outp and returns a dictionary with other filenames written by MCNP
    and mentioned in the outp.

    """
    meshtal = None
    srctp = None
    runtpe = None
    mctal = None
    terminated = None

    for l in open(outp, 'r'):
        if meshtal is None  and ' Mesh tallie' == l[0:12]:
            # This line has different format in mcnp5.1.4 and mcnp5.1.6
            meshtal = l.split()[5]
        elif srctp is None  and ' source dist' == l[0:12]:
            srctp = l.split()[5]
        elif runtpe is None and ' dump no. '  == l[0:10]:
            runtpe = l.split()[5]
        elif mctal is None  and ' tally data wri'  == l[0:15]:
            mctal = l.split()[5]
        elif terminated is None  and ' run terminated'  == l[5:20]:
            terminated = l[20:-1]  # cut the new-line character

        if None not in [meshtal, srctp, runtpe, mctal, terminated]:
            break
    res = {}
    res['meshtal'] = meshtal
    res['srctp'] = srctp
    res['runtpe'] = runtpe
    res['mctal'] = mctal

    # append directory name, if outp has dirname.
    dirname = os.path.dirname(outp)
    for (k,v) in res.items():
        if v is not None:
            res[k] = os.path.join(dirname, v)

    res['terminated'] = terminated
    res['outp'] = outp[:]

    return res

            
def get_outp_name(stdout):
    """
    Returns the outp filename, if it is mentioned in the std.out of MCNP.

    Finds in the MCNP standard output redirected to file stdout the name of
    outp file and returns it. 

    The stdout argument is a file containing MCNP standard output.

    """
    name = 'outp'
    for l in stdout.splitlines():
        if name == l[:10]:
            name = l.split()[3]
    return os.path.join(os.path.dirname(stdout), name)

def outp_name(folder, inp=None):
    """
    Return name of the outp file, that will be created by next mcnp run in the
    folder.

    If inp is None (default), it is assumed that outp files are named using the
    pattern 'out*'. 
    
    If inp is a string, it is interpreted as the input file name. String
    inp+'o' is returned in this case.
    """
    if inp:
        return inp + 'o'
    else:
        outps = []
        for f in os.listdir(folder):
            if len(f) == 4 and f[:3] == 'out':
                outps.append(f)
        return 'out' + chr(ord(max(outps)[-1])+1)

def next_outp(cl=None, dir_='.'):
    """
    Return name of outp file, created by the next mcnp run.

    cl:
        command line supplied to the mcnp executable. If None (default), it is assumed that
        outp files are named using the pattern 'out*'.

        There are two assumptions:

            1. files in cl are specified using the equal sign
               without spaces, exactly as described in MCNP 5 manual, p. 1-12, i.e. 
               'name=i_ scr=_s'.
            2. The 'name' keyword is not abbreviated.

    dir_:
        optional (defaults to '.') path to folder where the outp file name is
        defined.
    """
    if cl is None or 'name=' not in cl:
        outps = []
        for f in os.listdir(dir_):
            if len(f) == 4 and f[:3] == 'out':
                outps.append(f)
        return 'out' + chr(ord(max(outps)[-1])+1)
    else:
        # if 'name' in cl, deduce outp filename from the name of input
        for token in cl.split():
            if 'name' in token:
                return token.split('=')[1] + 'o'


def wall_time(outp):
    """
    Reads timestamps from the outp file and returns them as datetime instances.

    Returned: (probid, transport, endstamp), where transport and endstamp can be None.

        probid -- start of the job.

        transport -- when transport terminated (this is reported on the line starting with '+' sign)

        endstamp -- timestamp on the last line.


    """
    # read only the last line, recipe taken from  
    # http://stackoverflow.com/questions/3346430/most-efficient-way-to-get-first-and-last-line-of-file-python
    fmt = '%m/%d/%y %H:%M:%S'
    with open(outp, 'r') as f:
        probid = None
        transp = None
        for l in f:
            if probid is None and 'probid' in l:
                # read probid stamp:
                probid = datetime.strptime(' '.join(l.split()[-2:]), fmt)
                
            elif transp is None and l[:2] == '+ ':
                transp = datetime.strptime(' '.join(l.split()[-2:]), fmt)

            if probid is not None and transp is not None:
                break

        # try to read the last line:
        endstm = None
        f.seek(-200, 2) # go to 200 chars before the file's end
        l = f.readlines()[-1] # this is the last line
        st = filter(lambda s: '/' in s and ':' in s, l.split('    ')) # and these are the stamps
        if st:
            try:
                endstm = datetime.strptime(st[0].strip(' \n\r\t'), fmt)
            except:
                print 'Cannot read timestamp.'
                print 'Last line:', repr(l)
                print 'Timestamps:', st
                print 'Error:', sys.exc_info()[0]

    return probid, transp, endstm 
