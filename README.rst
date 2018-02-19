(P)ython (I)nterfaces for (R)eactor (S)imulations 
===================================================

The package provides Python interface to nuclear reactor simulation codes with the primary
goal to organize data flow.

Cuurently implemented are MCNP and SCF interfaces; they can be used to organize
coupled neutronics- and thermohydraulic calculations.

Documentation sources are in `docs`_. An HTML version (possibly outdated) can
be found in http://travleev.github.io/PIRSdocs/

.. _docs: ./docs

History
-----------

PIRS evolved from a set of Python scripts helping to read/write MCNP-related files. 
It was mainly developed and applied for coupled MCNP-SCF simulations of square PWR 
assemblies and parts of the core. Documentation found in `docs`_ refers to large extent 
to that state of the code.

Occasionally, some modules were modified to meet other needs, without thorough
checking of back compatibility and without reflecting the changes in
documentation. 

Outlook
-----------

The package shall be refactored to fix the mentioned above incompatibilites.  
Some code (e.g. for reading meshtal files) was rewritten from scratch in another packages
(see numjuggler_, `tovtk`_). Refactoring should take this into account and extract code with 
the same functionality into separate packages.

.. _tovtk: https://github.com/inr-kit/tovtk
.. _numjuggler: https://github.com/inr-kit/numjuggler


