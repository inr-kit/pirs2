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

import platform
_proc_status = '/proc/{0}/status'.format(os.getpid())

# 1

def relaxed(a1, a2, m1, m2):
    """
    Returns m1*a1 + m2*m2
    """
    m = m1.copy_tree()
    if (a1, a2) == (0., 0.):
        # put all zeroes to m:
        for e in m.values():
            e.heat.clear()
    else:
        # assume that m1 and m2 have the same structure.
        for (e, e1, e2) in zip(m.values(), m1.values(), m2.values()):
            e.heat = e1.heat*a1 + e2.heat*a2
    return m

# 2

def have_zeroes(m):
    """
    Returns True if some of heat values in m are zeroes.
    """
    for e in m.heats():
        if not e.heat.is_constant() and e.heat.has_zeroes():
            print 'zero heat found in ', e.get_key()
            return True
    return False

# -------------------------------------------
def print_dens(m, comment=''):
    """
    For debug only.
    """
    print 'Density of scf_0 ' + comment
    print m.get_child('scf_c0').dens.get_grid()


def print_model(m, comment=''):
    print '*'*40 + comment
    for e in m.values():
        print 'model element ', e.get_key()
        for n in ['temp', 'dens', 'heat']:
            print '    {0}: '.format(n)
            g = getattr(e, n)
            print g.get_grid()
            print g.values()
    print '*'*40 

if platform.system() == 'Linux':

    def get_memory():
        """
        If on Linux, returns the string specifying the memory usage of the current python program
        """

        global _proc_status
        t = open(_proc_status)
        for l in t:
            if 'VmSize' in l:
                break
        t.close()
        return l[:-1] # cut the newline character
else:
    def get_memory():
        """
        On non-linux get_memory does nothing.
        """
        return '--------'


