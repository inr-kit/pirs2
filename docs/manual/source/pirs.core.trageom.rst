.. _trageom:


pirs.core.trageom subpackage
=================================

.. currentmodule:: pirs.core.trageom

This subpackage defins only one class, :class:`pirs.core.trageom.Vector3`
representing a vector (coordinate) in three-dimensional space. The main
functionality of this class is to perform conversion between cartesian,
cylindrical and spherical coordinate systems (CS). A user can work (set and get)
attributes representing coordinates in these coordinate systems and the class
unsures that all coordinates are everytime consistent.


.. literalinclude:: examples/trageom.py

.. literalinclude:: examples/trageom.out
   :language: none

A vector instance is initialized by passing a coordinate 3-tuple to the
constructor. Read-only attributes :attr:`~Vector3.car`, :attr:`~Vector3.cyl`
and :attr:`~Vector3.sph` return coordinates in the correspondent CS.
Properties :attr:`~Vector3.x`, :attr:`~Vector3.y`, , :attr:`~Vector3.z`,
:attr:`~Vector3.r`, :attr:`~Vector3.t`, :attr:`~Vector3.z`, :attr:`~Vector3.R`,
:attr:`~Vector3.t`, :attr:`~Vector3.p` can be set. In the above, the ``v1``
vector is first specified using the cartesian CS. The coordinates and the CS
type is stored internaly and can be used later to compute coordinates in the
other CS. When :attr:`~Vector3.t` is changed, first, coordinates in the
cylindrical CS are computed from the previously defined cartesian coordinates.
Then, the theta cylindrical variable is updated and the internal CS type is set
to the cylindrical CS. When we call the :attr:`Vector3.car` for the second
time, i.e. after :attr:`Vector3.t` was set, the cartesian coordinates are
computed from internally stored cylindrical coordinates and returned as a
3-tuple.




.. autoclass:: pirs.core.trageom.Vector3
   :members:

