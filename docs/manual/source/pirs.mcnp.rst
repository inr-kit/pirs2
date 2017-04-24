.. _mcnp:


pirs.mcnp subpackage
=======================

This package provides a low-level interface to the MCNP5 code. 

It defines classes to represent cells, surfaces, materials and tallies. There is also
a class representing the MCNP model as a collection of cells, surfaces,
materials, etc; this class takes the task of setting cell, surface and
material numbers (IDs) and has methods to generate valid MCNP input file. Moreover,
there is a class that describes a workplace -- a directory that contains all
files necessary to start MCNP job and there is a method to start MCNP
executable. Also, functions to read MCNP-generated files, are defined in this
package.

.. Note:: 
   In contrast to the low-level interface, the high-level interface translates the code-independent
   geometry described with the help of the :mod:`pirs.solids` package into the
   low-interface MCNP model instance, and puts back results of MCNP run, read
   by the low-level interface methods, back to the code-independent geometry.

An MCNP model is represented by the :class:`pirs.mcnp.Model` class. It consists
of instances of the :class:`pirs.mcnp.Cell` class, each reffering to a material
represented by the :class:`pirs.mcnp.Material` and with geometry defined by
instances of the :class:`pirs.mcnp.Surface` and :class:`pirs.mcnp.Volume`
classes.

Materials
------------

The :class:`pirs.mcnp.Material` class is used to represent material
composition, temperature and optional use of thermal data.  It inherits the
:class:`pirs.core.tramat.Mixture`, described in details in :ref:`tramat`. Here
we overview only MCNP-related features, added to the
:class:`pirs.mcnp.Material` class.

Frist of all, this class can take information about available cross-sections
from an xsdir file.  The :attr:`pirs.mcnp.Material.xsdir` attribute is an
instance of the :class:`pirs.mcnp.Xsdir` class able to read xsdir file
and to store information. By default, each material instance is supplied with
an xsdir containing data from ``$DATAPATH/xsdir`` file.

The :meth:`pirs.mcnp.Material.card` method generates a multi-line string
containing the material card describing the material in the MCNP input file.
When the ``card()`` method is called, cross-sectin data sets are searched in
the specified xsdir object for each nuclide and for the temperature specified
in the :attr:`pirs.mcnp.Material.T` attribute. If a cross-section data set for
particular nuclide and particular temeprature is found, its suffix is used in
the card. If there is no cross-section data exactly at the temperature ``T``,
two cross-sections are found with temepratures above and below ``T``, and both
suffices enter the material card.

.. literalinclude:: examples/mcnp.mat_e1.py


.. literalinclude:: examples/mcnp.mat_e1.out
   :language: none

In this example, a material representing Iron with natural isotopic abundancies
is created and material card corresponding to temepratures 300, 350 and 400 K
is printed. Default xsdir, read from ``$DATAPATH/xsdir`` file is used to find
cross-section suffices. As one can note, cards cannot be used directly in the
MCNP input file, since material numbers are not given explicitly, there are
format placeholders instead. 

For temperatures 300 and 400 K data for all Fe isotopes exist in the xsdir and
denoted by suffices ``31c`` and ``32c`` (this example uses xsdir file from the
multi-temperautre data set `JEFF-3.1
<https://www.oecd-nea.org/dbprog/Njoy/Cabellos-report_mcjeff31-v36.pdf>`_).


For the material at 350 K, both suffices are used in proportions defined by the
material temeprature and temeratures of available cross-sections. How these
proportions are computed, depends on the :attr:`pirs.mcnp.Material.Tif`
attribute that by default set to the
:func:`pirs.mcnp.auxiliary.xs_interpolation.sqrT` function that implements the
square-root temperature interpolation, but can be changed by the user to
anything else.

Use of thermal data is controlled by the :attr:`pirs.mcnp.Material.thermal` attribute. By default it is ``None``
and no thermal data is used. When this attribute is set to a string, thermal data with names containing this string
will be searched in the xsdir file and, if found, will be mentioned in the ``mt`` card corresponding to the material.
If there are more than one thermal data set, the set with the closest temeprature will be chosen. 

.. literalinclude:: examples/mcnp.mat_e2.py


.. literalinclude:: examples/mcnp.mat_e2.out
   :language: none

In this example, the material ``h2o`` is created. Thremal data for hydrogen
bound in water are all named ``lwtr??.31t`` in the default xsdir file. To use
them, we set the ``thremal`` attribute to the common part of the names, which
is ``'lwtr'``. Depending on the material temperature, particular data set is
chosen. Note that thermal cross-sections are not interpolated. Note also that
both ``m`` and ``mt`` cards followed by the format placeholder with the same
index, to ensure that both cards will correspond to the same material.

Another feature shown in this example is the :attr:`pirs.mcnp.Material.sdict`
attribute.  This dictionary specifies substitution rules for cases when
particular nuclide cannot be found in the xsdir file. Particularly, the default
xsdir file contains no cross-section data for nuclide 8018, which however,
enters to the ``h2o`` material since it was defined using natural isotopic
composition of oxygen. Without specifying the substitution rule, the call to
the ``card`` method would result in error. With the help of ``sdict`` we can
avoid this error.


Surfaces and volumes
----------------------
There are two classes to describe geometry of an MCNP model.

The :class:`pirs.mcnp.Surface` class is a container for data to describe an
MCNP surface. It can hold data for both simple surfaces and macrobodies,
'knows' about the order of facets for macrobodies, can generate the surface
card for the MCNP input file.

.. literalinclude:: examples/mcnp.sur1.py


.. literalinclude:: examples/mcnp.sur1.out
   :language: none

Surface parameters can be specified in two ways: the surface class constructor
accepts surface cards (so it can be used as a parser), or surface type, list of
parameters, reflection etc. can be specified as keyword arguments. At the
initialization surfaces are simplified, when possible, as shown for surface ``s3``.
The surface card generated by the :meth:`pirs.mcnp.Surface.card` method
is a formatting string with placeholder for the surface ID number.

A surface separates the space into two volumes, 'above' and 'below'.
Representation these volumes and operations of union and intersections are
implemented in the :class:`pirs.mcnp.Volume` class. The constructor of this
class takes two arguments: the first argument specifies part of the space (1
means 'above' and -1 -- 'below'), the second argument defines the surface. The
main functionality of the volume class is to provide operations of union and
intersection and to represent these operations in terms used in the MCNP input
file; it should be noted however, that result of these operations is not
evaluated. Thus, the second argument must not necesserily be an instance of the
:class:`pirs.mcnp.Surface` class, one can use abstract string names. 


.. literalinclude:: examples/mcnp.vol1.py


.. literalinclude:: examples/mcnp.vol1.out
   :language: none

String representation of a volume uses the space for intersection and the colon
for union, and can therefore be used in the description of cell geometry in the
MCNP input file, if surface ID numbers are used as abstract surface
definitions. One can also use volumes with arbitrary (not necesserily integer)
surface definitions together with the :meth:`pirs.mcnp.Volume.copy` method.
Optional argument of this method must be a mapping (function or dictionary)
that will replace original surface defition in the returned copy. 

This, for the first glance over-engineering approach   
allows to use macrobodies to define geometry and then, if necessary (for example, when 
different boundary conditions must be set to facets of a macrobody), to represent 
this geometry in the MCNP input file using simple surfaces. The following example 
illustrates this:

.. literalinclude:: examples/mcnp.vol2.py

.. literalinclude:: examples/mcnp.vol2.out
   :language: none

The ``c`` surface is a cylinder macrobody. Its :meth:`pirs.mcnp.Surface.facets`
method returns a list of volumes 'above' each macrobody's facet. The
:attr:`pirs.mcnp.Volume.a1` attribute of a simple volume (i.e. defined directly
by the class constructor, not as union or intersection) returns the constructor
arguments, thus the second element of this attribute is the surface definition.
In the loop all surfaces are collected into the list ``l`` that is used to map
each surface instance to an integer number, see function ``m``.  The
:meth:`pirs.mcnp.Surface.volume` method returns a volume representing the
macrobody's exterior in terms of simple surfaces. It is used in the example to
generate geometry description of cells representing both interior and exterior
of the macrobody.  Using the same mapping, we generate the surface cards, thus
ensuring that surface IDs in the surface cards block is consistent with
description of cells.

In this example, we defined explicitly the mapping to set surface IDs. This was
done as illustration, there are other means to set automatically surface, cell
and material numbers, see below.

.. warning::
   The low-level interface was developed keeping in mind rather simple
   geometries that can be described by vertical cylinders and boxes with facets
   perpendicular to the coordinate axes. Therefore, only vertical cylinder
   macrobodies (i.e. parallel to the 3-rd coordinate axis) will be handled
   properly, although no parameters check is done at the initialization time.


Cells and models
---------------------

.. currentmodule:: pirs.mcnp

The :class:`pirs.mcnp.Cell` class represents a container that stores
cell-related information: material, geometry and cell options. Cell geometry
must be specified using the :class:`~pirs.mcnp.Volume` and
:class:`~pirs.mcnp.Surface` classes, and material -- useing the
:class:`~pirs.mcnp.Material` class. Cell options (e.g ``lat``, ``fill``,
``imp:n`` etc.) are specified using the :attr:`pirs.mcnp.Cell.opt` attribute,
which is a dictionary with only particular keys allowable (see
:class:`~pirs.mcnp.cells.CellOpts` class).  Although there is a method to
generate cell cards for the MCNP input, :meth:`pirs.mcnp.Cell.card`, its direct
use makes no sense, sinse one still needs to specify durface, cell and material
IDs.


.. literalinclude:: examples/mcnp.cell1.py

.. literalinclude:: examples/mcnp.cell1.out
   :language: none

In this example, neither material nor geometry is resolved when cells ``c1``
and ``c2`` are printed directly, sinse there is no rule to set material and
surface IDs. This task is accomplished by the :class:`pirs.mcnp.Model` class
that is basically a list of cells. Cells describing the model are added to the
:attr:`pirs.mcnp.Model.cells` list attribute. When converting to a string, or
as in the example, when calling the :meth:`pirs.mcnp.Model.cells` method, all
cells in the model are analysed: IDs are set to unique materials and surfaces
thus providing information for the cell, surface and material cards. 

Setting of IDs for surfaces and materials is done with the help of the
:class:`pirs.mcnp.SurfaceCollection` and :class:`pirs.mcnp.MaterialCollection`
classes. They both have the :meth:`~pirs.mcnp.SurfaceCollection.index` method,
which takes as argument a surface or material instance, adds it to the
collection if it is not already there, and returns its index, which was
attached to this particular instance when it was added to the collection.

Start MCNP
--------------

To manually add cards to the automatically generated input files, there are
:attr:`Model.amc`, :attr:`Model.acc`, :attr:`Model.asc` and :attr:`Model.adc`
list attributes containing strings that will be added to the message, cell,
surface or data blocks. In this way one can define the source distribution or
add manually cells. 

The MCNP code can be started on the input file. The :attr:`Model.wp` attribute is 
an instance of the :class:`pirs.mcnp.McnpWorkPlace` that can be used to specify 
directory names where the input file will be written and MCNP code started. The :meth:`Model.run` method
prepares all necessary files and can be used to start MCNP in different modes (neutron transport, plot geometry).

TODO: example showing work with Model.wp and Model.run().

.. inheritance-diagram:: pirs.mcnp.Material



Docstrings
---------------

.. autoclass:: pirs.mcnp.Xsdir
   :members:

.. autoclass:: pirs.mcnp.Material
   :members:

.. autoclass:: pirs.mcnp.Surface
   :members:

.. autoclass:: pirs.mcnp.Volume
   :members:

.. autoclass:: pirs.mcnp.Cell
   :members:

.. autoclass:: pirs.mcnp.cells.CellOpts
   :members:

.. autoclass:: pirs.mcnp.SurfaceCollection
   :members:

.. autoclass:: pirs.mcnp.MaterialCollection
   :members:

.. autoclass:: pirs.mcnp.Model
   :members:


.. automodule:: pirs.mcnp.auxiliary.xs_interpolation
   :members:
   

