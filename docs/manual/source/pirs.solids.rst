.. _solids:


pirs.solids subpackage
==========================

.. currentmodule:: pirs.solids

This package provides description of classes representing solids that can be used to describe model 
geometry. Currently there are :class:`Cylinder`, :class:`Box` and :class:`Sphere` classes.

Model geometry is represented as a set of boxes or cylinders organized in a
tree structure. One solid can be inserted into another one (in this case the
latter is called a container of the former one), can be positioned arbitrarily
within its container (no rotation implemented yet!), and can be partially or
completely covered by another solid.

Simple model
----------------

In the following example, a box with two cylinders is described and plotted.

.. literalinclude:: examples/sol1.py

The :class:`Box` class describes a rectangular parallelepiped with facets
perpendicular to the coordinate axes. Attributes :attr:`Box.X`, :attr:`Box.Y`
and :attr:`Box.Z` describe dimensions of the box. The :attr:`~Box.material`
attribute holds the material name (its particular meaning in the computational
code must be defined separately in the code's high-level interface).

Variable ``c1`` is a cylinder. It is inserted into ``b`` by the
:meth:`~Box.insert` method. The second cylinder, ``c2``, is a copy of ``c1``,
except material and its position in container, represented by :attr:`~Box.pos` (an instance
of the :class:`pirs.core.trageom.Vector3` class) are changed. Cylinder ``c2`` is also
inserted into ``b``.

Cross-sections of the model can be plotted with the help of
:func:`pirs.tools.plots.colormap` function that takes as argument a solid and
returns an instance of the Matplotlib's :class:`Axes` class. If optional argument ``filename`` is given, the plot
will be saved to disk.

.. figure:: _static/sol1z.png
   :scale: 50%

   Vertical cross-section.


.. figure:: _static/sol1x.png
   :scale: 50%

   Horizontal cross-section.

As one can see, cylinder ``c2`` partly covers ``c1``, while it was inserted
into ``b`` after ``c1``. At the second plot showing horizontal cross-section,
cylinder ``c2`` not seen while the cross-section plane, ``x=0`` does not
intersect it.

Assembly-like model
--------------------

The next example shows how an assembly-like geometry can be modelled: 

.. literalinclude:: examples/sol2.py

The ``pin`` variable is a cylinder containing another, 5 cm shorter and 0.05 cm thinner
coaxial cylinder. It represents a pin. Note that attributes of created solids can be set 
by passing correspondent arguments to the constructor.

Next, the box ``a`` is created. Its :attr:`Box.grid` attribute (an instance of
the :class:`pirs.solids.positions.RGrid` class) describes a rectangular grid
(lattice) superimposed over the solid, which can be used to position inserted
elements. In the example, we set grid pitches along axes using
:attr:`~Box.grid.x`, :attr:`~Box.grid.y` and :attr:`~Box.grid.z` attributes of
the grid.

In the nexted loop over ``i`` and ``j`` indices a copy of ``pin`` is inserted
into ``a`` using the :meth:`~pirs.solids.positions.RGrid.insert` method of the grid. Unlike the
:meth:`Box.insert` method of the solid, the grid's ``insert()`` method takes
additional argument -- a 3-tuple with indices ``(i, j, k)``, which define the
grid element where the inserted solid will be positioned. A grid can be shifted as a whole
with respect to its solid. By default, the grid is positioned so that the
center of the ``(0,0,0)`` grid element conicides with the solid's center.  The grid's 
:attr:`~pirs.solids.positions.RGrid.origin` attribute can be used to set grid position. Altenatively, there is
the grid's :meth:`~pirs.solids.positions.RGrid.center` method that centers the grid in the solid. Note
that we have not defined grid dimensions (number of elements in each direction), since 
they are defined automatically to include all inserted elements.


.. figure:: _static/sol2z.png
   :scale: 50%

   Vertical cross-section.


.. figure:: _static/sol2x.png
   :scale: 50%

   Horizontal cross-section.

Axial distribution of dependent variables
-----------------------------------------------

Each solid has :attr:`~Box.heat`, :attr:`~Box.dens` and :attr:`~Box.temp`
attributes, that are instances of the :class:`pirs.solids.zmesh` class,  representing axial distribution of heat deposition, density and
temeprature in the solid. All three axial distributions can be specified 
on independent axial grid. 

.. literalinclude:: examples/sol3.py

To specify the grid for axial distribution, the mesh'
:meth:`~pirs.solids.zmesh.set_grid` method is used. It takes a list of scalars
which define relative heigth of axial layers (the first list element
corresponds to the lowest axial layer). In the example, the axial grid to represent heat
deposition has three axial layers, the middle one is two times thicker as the
others. The temperature grid has 20 equal layers, and density grid -- 5 layers.

Values of axial distribution are set with the help of the
:meth:`~pirs.solids.zmesh.set_values` method. It accepts lists (as used for
heat), mappings (as used for temperature) or scalars (as used for density). 

Axial distribution of heat, temeprature or density can be plotted with the :func:`pirs.tools.plots.colormap` by specifying
the ``var`` argument.



.. figure:: _static/sol3h.png
   :scale: 50%

   Heat.

.. figure:: _static/sol3t.png
   :scale: 50%

   Temperature.

.. figure:: _static/sol3d.png
   :scale: 50%

   Density.


Docstrings
--------------

.. autoclass:: pirs.solids.Box
   :members:
   :inherited-members:
   :private-members:

.. autoclass:: pirs.solids.Cylinder
   :members:
   :inherited-members:
   :private-members:

.. autoclass:: pirs.solids.Sphere
   :members:
   :inherited-members:
   :private-members:

.. autoclass:: pirs.solids.positions.RGrid
   :members:

.. autoclass:: pirs.solids.zmesh
   :members:

.. autofunction:: pirs.tools.plots.colormap

