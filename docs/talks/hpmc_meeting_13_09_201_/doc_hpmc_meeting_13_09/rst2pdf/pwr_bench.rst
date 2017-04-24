

Geometry: horizontal cross-section
===================================

+---------------------------------------------------------------------------------------------+-----------------------+
|                                                                                             |                       |
|   .. figure:: pics/i__p01.pdf                                                               |  * lattice card       |
|       :height: 6in                                                                          |  * coolant-centered   |
|                                                                                             |    channels           |
|                                                                                             |  * 2 fuel types       |
|                                                                                             |  * water channels     |
|                                                                                             |                       |
+---------------------------------------------------------------------------------------------+-----------------------+
                        
                       


  
  
Geometry: vertical cross-section
==================================

+---------------------------------------------------------------------------------------------+-----------------------+
|                                                                                             |                       |
| .. image:: pics/i__p02.pdf                                                                  | * non-uniform         |
|     :height: 6in                                                                            |   axial mesh          |
|                                                                                             |                       |
|                                                                                             | * changing T and      |
|                                                                                             |   density of          |
|                                                                                             |   coolant water       |
|                                                                                             |                       |
|                                                                                             | * constant water      |
|                                                                                             |   properties in       |
|                                                                                             |   water channels      |
|                                                                                             |                       |
+---------------------------------------------------------------------------------------------+-----------------------+
    

Keff behaviour
================

.. image:: pics/b_iteration_062_keff.pdf
    :height: 6in




    
Heat and water density
========================

.. image:: pics/b_iteration_062_dens50_0.pdf  
    :height: 6in

Fuel and water temperature
============================

.. image:: pics/b_iteration_062_temp50_0.pdf
    :height: 6in


Axial distribution in pin (4,4)
================================

.. image:: pics/b_iteration_062_4_4.pdf
    :height: 6in


Python scripts 
================

``driver.py``
    Main script that controls calculation flow and describes relaxation scheme

|
|

``rod_models.py``
    Dimensions, description of UOX and IFBA fuel pins

``pin_model.py``
    Geometry of one-pin model

``pin_mcnp.py``
    MCNP-specific data for one-pin model

``pin_scf.py``
    SCF-specific data for one-pin model

|
|


``assembly_model.py``
    Geometry of assembly model

``assembly_map.py``
    Pseudo-graphics definition of the assembly map

``assembly_mcnp.py``
    MCNP-specific data for assembly model

``assembly_scf.py``
    SCF-specific data for assembly model



``driver.py``
===============

.. code-block:: python
    :include: driver.py

``rod_models.py``
===================

.. code-block:: python
    :include: rod_models.py


``pin_model.py``
===================

.. code-block:: python
    :include: pin_model.py

``pin_mcnp.py``
========================

.. code-block:: python
    :include: pin_mcnp.py

``pin_scf.py``
================
.. code-block:: python
    :include: pin_scf.py



``assembly_model.py``
=======================

.. code-block:: python
    :include: assembly_model.py


``assembly_map.py``
=======================

.. code-block:: python
    :include: assembly_map.py


``assembly_mcnp.py``
=======================

.. code-block:: python
    :include: assembly_mcnp.py


``assembly_scf.py``
=======================

.. code-block:: python
    :include: assembly_scf.py








