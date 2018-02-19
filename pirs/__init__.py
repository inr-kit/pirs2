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

PIRS stands for Python Interfaces for Reactor Simulations. 

This package provides classes to interact with codes from the
Python. Currently implemented are interfaces to MCNP (Monte-Carlo 
neutronics) and SCF (sub-channel thermo-hydraulics).

An interface to a code is implemented in two levels: 

    *
      The low-level interface describes classes for object-oriented
      representation of data needed for the code input, defines routines to
      read the code's output and has means to start the code from a Python
      script (or from interactive the Python interpreter).
      
    * 
      The high-level interface converts code-independent description of
      geometry into input file(s) and puts the results of the code into the
      geometry back using the low-level interface.


Subpackages of PIRS are organized into several groups:

    pirs.solids: 
        Classes representing solids to build computational geometry

    pirs.hli:
        Subpackages describing high-level interfaces
"""

from .hli.mcnp.interface import McnpInterface
# from .hli.scf.interface import ScfInterface
from .hli.scf2.interface import Model as ScfInterface
