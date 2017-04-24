.. _tramat:


pirs.core.tramat subpackage
================================

This package defines classes to represent mixture of nuclides. The classes are
not used directly, they serve as parent classes providing base functionality
for example, to the :class:`pirs.mcnp.Material` class.

Nuclides
--------------

The basic element of any material mixture is a nuclide represented by 
the :class:`pirs.core.tramat.Nuclide` class. Instances of this
class have attributes for mass and charge numbers, for molar mass and for the
isomeric state.  The main functionality of this class is to 'understand'
nuclide specifications of different forms; it also defines arithmetical operations of addition of two nuclides and
multiplication of a nuclide by scalar.

How nuclides can be defined:

.. literalinclude:: examples/tramat_e1.py

.. literalinclude:: examples/tramat_e1.out
   :language: none


In all these examples the molar mass was not specified. In this case, it is
taken from the class attribute :attr:`pirs.core.tramat.Nuclide.AWR_SET`, which
is a dictionary of the form ``ZAID: awr``.  By defualt, this class attribute
links to the :data:`pirs.core.tramat.data_masses.xsdir1` dictionary, which
contains awr masses from the xsdir file distributed with MCNP5.

Two nuclide instances can be added and an instance can be multiplied by a scalar::

    a = n1 + n2
    b = 3*n1

Both operations result in an instance of the :class:`pirs.core.tramat.Mixture`
class. In the example, ``a`` is a mixture of one mole of nuclide ``n1`` and one
mole of nuclide ``n2``, and ``b`` is a mixture consisting of 3 moles of nuclide
``n1``.  

Mixtures
-----------

The :class:`pirs.core.tramat.Mixture` class represents a mixture of nuclides or
other mixtures. Its constructor takes arguments that define the mixture recipe
-- what materials at which amount constitute the mixture. In the most simple
case, there can be only one integer argument specifying ZAID, or a string
specifying chemical name. In general case, the constructor accepts several
tuples each defining material and its amount used to construct the mixture.


.. literalinclude:: examples/tramat_e2.py


In this example, ``m1`` is a mixture consisting of one nuclide H-1, and ``m2``
is a mixture of He isotopes with natural abundancies. Note that the string
representation of a nuclide, in the form ``'He-4'`` cannot be used in the
Mixture constructor, while a string is assumed to define a chemical element
name.  Mixtures ``m3``, ``m4`` etc. are defined using the general form of
constructor arguments.  Each tuple defines the material, amount and units in
which amound should be understood: 1 for moles, 2 for grams and 3
for cubic cm; the latter is only possible for materials with specified density
or concentration. 

In the above example, mixture ``m3`` has two ingredients: 0.1 mole (last tuple element
is 1) of ``m1`` and 0.9 moles of ``m2``.  Mixture ``m4`` is defined using
grams: it consists of 0.1 g of ``m1`` and 0.9 g of ``m2``. Note that one can
mix units, see definition of ``m5``. 

One can specify ingredient amount in cubic centimeters, as for the mixture
``m6`` above. For this to have sense, the ingredient material, ``m1`` in this case,
should have the :attr:`pirs.core.tramat.Mixture.dens` or
:attr:`pirs.core.tramat.Mixture.conc` attribute defined. 

Main properties of a mixture can be inquired by the
:meth:`pirs.core.tramat.Mixture.report` method.  It returns a multi-line string
where mixture ingredients and mixture nuclide composition is summarized.  The
above script produces the following output:


.. literalinclude:: examples/tramat_e2.out
   :language: none

The name of a mixture, printed in the first line returned by the report()
method, is given by the :attr:`pirs.core.tramat.Mixture.name` attribute. If not
specified explicitly by the user (as in the example above), it is generated
based on the chemical element names that constitute the mixture.

The first part of report, between the lines ``Mixture ...`` and ``Nuclide
composition:``, lists ingredients used to construct the mixture. The second
part, after the line ``Nuclide composition:``, shows nuclide composition,
computed from the mixture recipe and recipies of its ingredients, recursively. 

Mixtures can be added to each other and multiplied by a scalar, as shown in the
follwing example. 
 
.. literalinclude:: examples/tramat_e3.py


.. literalinclude:: examples/tramat_e3.out
   :language: none

Result of adition of two mixtures is a new mixture that is a mix 
of the operands in equal proportions. Note, however, that the resulting mixture
recipe does not refer directly to the operands, they are first expanded to
nuclides (see the :meth:`pirs.core.tramat.Mixture.expanded` method). In the
above example, the recipe of ``m1`` consists of 4 nuclides, not of two
mixtures ``h1`` and ``he``.

Multiplication of a mixture by a scalar returns a new mixture with only one
ingredient -- the operand, which amount in moles is given by the scalar, see
mixture ``m2``. Note, in this case the operand is not expanded to
nuclides. 

Note that the total amount of ingredients in the mixture ``m4`` sums up to 5 moles,
although it is defined as ``2*m1 + 3*m2``, where ``m1`` and ``m2`` have itself
2 moles in their recipes. This behaviour is chosen deliberately, the scalar
before the mixture is not a coefficient for the amount of its ingredients, it
specifies the amount of mixture itself.

Data modules
--------------
Mapping between charge numbers and chemical names are defined in the :mod:`pirs.core.tramat.data_names` module.
This module also contains functions to parse nuclide names and  to define isomeric names from special ZAIDS.

Default awr masses are taken from the :mod:`pirs.core.tramat.data_masses` module. 

Naturall abundancies of isotopes are taken from the module :mod:`pirs.core.tramat.data_natural`.


Docstrings
------------

Nuclide class
...............
.. autoclass:: pirs.core.tramat.Nuclide
   :members:

   .. autoattribute:: pirs.core.tramat.Nuclide.AWR_SET
      :annotation: Dictionary with default awr masses.

Mixture class
...............
.. autoclass:: pirs.core.tramat.Mixture
   :members:

data_masses module
...................
.. automodule:: pirs.core.tramat.data_masses

   .. autodata:: pirs.core.tramat.data_masses.xsdir1
      :annotation:

data_names module
....................
.. automodule:: pirs.core.tramat.data_names
   :members:

   .. data:: pirs.core.tramat.data_names.name
      :annotation: Dictionary Z: name

   .. data:: pirs.core.tramat.data_names.charge
      :annotation: Dictionary name: Z


data_natural module
......................
.. automodule:: pirs.core.tramat.data_natural
   
   .. data:: pirs.core.tramat.data_natural.d1
      :annotation: dictionary ZAID: af. For reference see the ``reference`` key.
      
