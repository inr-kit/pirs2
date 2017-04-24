.. _intro:


Introduction
==============

PIRS (Python Interfaces for Reactor Simulations) is a package for the Python
programming language that contains bindings to nuclear reactor computational
codes. This package simplifies workflow with the computational  codes  by
providing a geometry constructor that can be used to describe a model geometry,
and interfaces to computational codes.

Currently implemented are interfaces to the MCNP5_ Monte-Carlo neturon transport
code and to the SCF_ sub-channel thermo-hydraulics code.

.. _MCNP5: https://mcnp.lanl.gov/

.. _SCF: http://www.inr.kit.edu/632.php

This software was originally developed to provide a framework for coupled
neutronics Monte-Carlo -- thermo-hydraulics sub-channel calculations for
PWR-like geometries. This has defined the choice of codes for which interfaces
were implemented in the first place, and type of solids used for geometry
construction.

The concept behind PIRS, however, allows to use it not only for organization of
coupled calculations. Model description, all necessary calculation parameters
and calls to computational codes are spesified as a Python script, which make
it suitable to e.g. organize parametric studies.  Moreover, communication with
a code is organized via its input and output files, thus a user not familiar
with the code can get examples of valid input files and a tool to process its
output.

PIRS is lightweight and simple to install. It was tested with Python versions
2.6 and 2.7 under different linux distributions.  Its installation does not
require any compilation (i.e. PIRS is pure Python). All its dependencies are
optional: PIRS can utilize the uncertainties_ Python package to handle
statistical results of Monte-Carlo calculations, and the Matplotlib_ package to
plot geometries and results of calculations. This allows to install PIRS to a local account on a cluster
and use it to run computational codes parallel.

.. _uncertainties: http://pythonhosted.org/uncertainties

.. _Matplotlib: http://matplotlib.org/


On a linux computer with installed Python, the installation is done with the commands::

    $> tar -xsf pirs-X.Y.Z.tar.gz
    $> cd pirs-X.Y.Z
    $> python setup.py install --user

where the ``--user`` command line option in the last command is optional and
specifies that the package should be installed to the user's local account. If
the pip_ Python package manager is used to install PIRS, it will also install
the optional uncertainties_ package.

.. _pip: https://pypi.python.org/pypi/pip


There are several environment variables that PIRS relies on. The ``$MCNP`` and ``$SCF``
variables must show path to executables. Additionally, the path to default xsdir file must 
be specified in the ``$DATAPATH`` variable.

The PIRS package consists of several sub-packages that can be classified by
their functionality into five groups: geometry constructor, low-level code
interfaces, high-level code interfaces, subpackages with base classes used by
others, and utilities. 

The classes used for geometry construction are described in :ref:`solids`. They
are is used to describe model geometry in terms, independent on particular
computational code. Thus, the same geometry definition can be used to setup
MCNP and SCF models and to hold results of their calculations.

Low-level interfaces give possibility to set any paramter in the code's input
file, to start the code and to read the code's output file(s). The low-level
interfaces for MCNP and SCF are described in :ref:`mcnp` and :ref:`scf`.

A high-level code interface converts  code-independent geometry to a
code-specific model representation that can be used to setup code-specific date
(like isotopic compositions for MCNP) and to perform respective calculations
and to put calculation results back to the code-independent model. The
high-level interfaces to MCNP and SCF are described in details in :ref:`hmcnp`
and :ref:`hscf`.

Classes providing basic functionality that are used in the other subpackages,
are described in :ref:`scheduler`, :ref:`tramat` and :ref:`trageom`.

