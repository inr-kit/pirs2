
Introduction
============

.. role:: raw-latex(raw)
    :format: latex


The HPMC project :raw-latex:`\cite{hpmc}` aims full-core coupled calculations
including Monte Carlo (MC) neutronics, thermo-hydraulics (TH), burnup and time dependence.  This goal
will be achieved in steps, starting from coupling two physics domains (e.g.
neutronics and thermo-hydraulics, neutronics and nuclide kinetics, etc.) for
simple pin and assembly geometries and gradually increasing complexity. It is
assumed in the HPMC project that on certain stage cluster computers will be
used for MC neutronics calculations.


These two aspects of the project imply that the coupling procedure need to
be reusable for different types of problems (like pin, assembly and whole core
models) and should be flexibly applied on different types of computers (like
small desktop machines and supercomputers).


Coupled neutronics -- TH calculations are widely used in reactor engineering and several
different approaches have been established to couple neutronics and TH codes. The
fastest in implementation approach to organize data flow between two particular
N and TH codes is to prepare input file templates and to write an interface
program (this approach is followed, for example,  in
:raw-latex:`\cite{HoogenboomMC2011}`).  The interface program reads output from
one code, prepares data for the other code and inserts them into the correspondent
input file template. Both templates and the interface program are usually
written considering particular geometry type, which on the one hand
simplifies coding, but on the other hand makes it difficult to reuse the
coupling scheme for a different type of geometry. 

Another way to couple neutronics and TH codes is to use a common platform 
that provides means to integrate codes and to organize data flow between
them.  An example of this approach is the NURESIM system
:raw-latex:`\cite{nuresimICONE2006,nuresimWEB}` that utilizes the SALOME
platform :raw-latex:`\cite{salomeWEB}`. This approach results in much more
flexible solution as compared to the approach described above, but also has
some drawbacks. For example, integration of a code into the platform might
require changes in the code itself, which is not always possible due to e.g.
licensing limitations. Moreover, requirements to computer (hardware and OS) imposed by
SALOME are quite restrictive :raw-latex:`\cite{salomeWEB}`.

In the present work we propose a coupling approach that can be applied to
different types of calculation geometry and does not require changes in the
code to be integrated. This approach is implemented as a set of Python
:raw-latex:`\cite{pythonWEB}` packages called PIRS -- Python Interfaces for
Reactor Simulations that currently provides interfaces to MCNP
:raw-latex:`\cite{mcnpREF}` and SCF codes :raw-latex:`\cite{scfREF}`. 

In this paper we describe  the concept of PIRS, give an example of neutronics
specifications for a simplified pin model, and report results of coupled
MCNP-SCF calculations for a PWR assembly organized by means of PIRS.



Concept of the coupling framework
=================================

Python classes provided by PIRS can be classified by their functionality into
three groups: low-level interfaces, general model classes and high-level
interfaces, see figure :raw-latex:`\ref{pic:classes}`.  Classes of the first
group describe an interface between Python and a particular code (low-level
interfaces). A low-level interface class allows to set any parameter in the
input file, generates it, provides means to execute the code and defines
procedures to read output files directly from the Python interpreter or a
Python script. Low-level classes ensure that the generated input files have
correct syntax and often saves a user from specifying auxiliary or non-used
parameters.

.. figure:: pics/scheme_en.pdf

    PIRS Classes and their interaction with computational codes. :raw-latex:`\label{pic:classes}`

General model classes can be used to describe calculation geometry and
meshes to represent system variables.

High-level interface classes are used to convert geometry described with general 
model classes to instances of low-level interface classes and to put results
of code calculations (read by low-interface classes) back to general model.

To organize coupled neutronics -- TH calculations, a user defines parameters, common to
both neutronics and TH domains, in a variable (say, ``a1``) by means of general model 
classes. This variable contains information about geometry and axial
meshes for heat deposition, temperature and density. An instance of one of the 
high-level interfaces (let call it ``i1``) is used to set
code-specific information, like cross-sections data sets for MCNP. Variable
``i1`` has a method that takes ``a1`` as an input model, prepares an input file
based on the common information stored in ``a1`` and code-specific data stored
in ``i1``, executes the code, reads the code output and returns ``a2`` that is
a copy of ``a1`` except some system variables which are replaced with the results of
calculations. Variable ``a2`` can be passed to a high-level interface of
another code as the input model; in this way one can organize data flow between
codes. A user can arbitrarily change parameters of a model, e.g. to describe a
relaxation scheme.

This framework structure allows to develop independently code back ends (i.e.
low-level and high-level classes for a code), once the structure of the classes
representing general model is defined.

Example: a simplified pin model
================================

A simplified pin model is considered to illustrate steps necessary to perform
neutronics calculations. First, a geometry of a model is described using general model
classes, and second, MCNP-specific date are specified with the help of
the MCNP high-level interface.


Calculation geometry
----------------------

The simplified pin model consists of two regions: a vertical cylinder (fuel) is
immersed into a rectangular parallelepiped (moderator). The following Python
script defines this model:

.. literalinclude:: geom.py

The ``Cylinder`` and ``Box`` classes are imported from the ``hpmc`` module provided by PIRS.
These classes are used to set the geometrical elements --
constituents of the pin model.  Variable ``b`` is an instance of the ``Box``
class; it describes a rectangular parallelepiped with sides 1.2 x 1.2 x 110
cm. Variable ``c`` is an instance of the ``Cylinder`` class and represents a
vertical cylinder with radius 0.5 cm and height 100 cm. The ``insert`` method of
variable ``b`` is used to specify positional relationship between solids ``b``
and ``c``: cylinder ``c`` is inserted into box ``b``. Coordinates of ``c`` with
respect to ``b`` are not given explicitly and by default ``c`` is centered
with respect to ``b``.

A material name can be given to each model's element, by means of the ``material``
attribute.  This attribute is set by default  to ``'void'`` and can take
any string value.  Actual meaning of the material name must be defined for each
code using correspondent high-level interface.

Next, meshes to represent system variables are defined. Attributes ``dens``,
``temp`` and ``heat`` represent density, temperature and heat deposition axial
distributions for each model's element, respectively. In the example above,
density of the element ``b`` is represented by an axial mesh with two equidistant
mesh elements; in both mesh elements density is set to 1.  Temperature of the element ``c`` is given by
an axial mesh with three equidistant mesh elements, temperatures are 300 K in the
lower mesh element, 500 K in the middle element and 350 K in the upper mesh
element. Additionally we specified that heat deposition should be represented by an axial
mesh with 10 equidistant elements, but no values are given explicitly.


high-level interface to MCNP
------------------------------

The above script describes only geometry of the model. MCNP-specific data are
specified by means of the ``MCNPInterface`` class from the ``hpmc`` module.
This includes specification of material isotopic compositions, boundary
conditions and neutron source for criticality calculations.

.. literalinclude:: mc_int.py
    :start-after: #1

The ``m`` variable is an instance of the ``McnpInterface`` class; its
constructor takes optionally a variable representing general model (in this
example, the variable ``b`` defined earlier). Any geometry described using
``Cylinder`` and ``Box`` classes and their arbitrary combinations can be
handled (understood) by the MCNP interface.

The ``Material`` class imported from the ``mcnp`` module (this module describes
low-level interface to MCNP) is used to define material compositions. Variables
``u``, ``o`` and ``h`` represent isotopic compositions of chemical elements
uranium, oxygen and hydrogen. Uranium
isotopic composition is given in weight fractions, for oxygen and hydrogen
natural abundance data :raw-latex:`\cite{natAbund2011}` are used. Arithmetical
operations for instances of the ``Material`` class are defined in the way that
can be used to define new mixtures. In the example, variable ``f`` is a mixture
of 1 atomic part of uranium and two atomic parts of oxygen and represents
uranium dioxide.  The ``w`` variable represents water. Optionally, one can
specify a string pattern that will be used to find cross-section data for
thermal scattering, see the ``thermal`` attribute. In the example, thermal data
set for water will be chosen among thermal data sets with names containing
``'lwtr'`` string with the closest temperature.

Materials ``f`` and ``w`` contain all
stable isotopes of oxygen, among them isotope 8018. In the
cross-section data set applied implicitly in this example, there is no data for
this isotope. To handle such situations, there is the ``sdict`` attribute of the
dictionary class that defines a substitution table: if for a given isotope (in
our example 8018) there is no cross-section, it is substituted with another one
(in our example 8016).

Correspondence between material compositions and general model material names 
is defined in the attribute ``materials``. It is a dictionary with
material names as keys and instances of the ``Material`` class as values.

Boundary conditions are set up using the ``bc`` attribute. It is an instance of
a dictionary-based class that admits only two keys, ``radial`` and ``axial``.
By default, the values are empty strings meaning no reflection on radial and
axial general model outer boundaries. One can set them alternatively to ``'*'``
or  ``'+'`` which means reflective or white boundary conditions, respectively
(similar to MCNP syntax). In the example we specify reflective radial boundary
conditions (for our model, the radial boundaries are the boundaries of the
water box that are perpendicular to the vertical axis) and leave default axial
boundary conditions.

Currently, there is no high-level interface to specify neutron source
parameters for an MCNP problem. As a workaround, a user can use possibility to
specify directly lines for the input file, provided by the low-level MCNP
interface. Attributes ``adc``, ``asc``, ``acc`` and ``amc`` are lists of lines that will
be appended to the data cards block, surface cards block, cell cards block and message cards
block, respectively. In the example we append two lines to the data cards
block, specifying initial spatial distribution of fission neutrons and
parameters of criticality calculations.

The ``run`` method generates the MCNP input file and starts the code. The first
call to the ``run`` method, with ``'P'`` argument, starts MCNP in the
geometry plotter mode.  In the second call with ``'R'`` argument, MCNP is
started in the particle transport mode. In this mode the interface waits until
MCNP finishes, reads heat deposition computed by mesh tallies and returns a
copy of the general model with heat attributes containing MCNP
results. Heat deposition mesh tallies are computed for each element of the
general model with non-trivial (non-zero or with more than 1 mesh element)
``heat`` attribute. In the first example we specified ten equidistant mesh
elements for the ``heat`` attribute of the fuel cylinder while the ``heat``
attribute of the box is by default trivial. Thus, heat deposition is
computed in the fuel cylinder only and the cylindrical element of the returned
general model, ``r``, will contain the results.

The MCNP input file generated during the first call to the ``run`` method is listed below, and 
figure :raw-latex:`\ref{pic:plot}` shows a plot produced by MCNP.

.. literalinclude:: mcnp0/i_

.. figure:: mcnp0/i__p02.pdf

    Vertical section of MCNP model, plotted with MCNP. :raw-latex:`\label{pic:plot}`

Cell and surface numbers used in the input file are assigned automatically by
the MCNP interface, so that a user does not need to invent them and check their
uniqueness. 

Density and temperature axial distributions are represented as a
set of cells with different density iand filled with different materials.
One can see three U-O mixtures, ``m1``, ``m2`` and ``m3`` that represent the
same fuel isotopic composition but use different data suffixes. If there is no
cross-section data set prepared for a given temperature, it is interpolated
using two data sets with temperatures below and above the specified value, see
material ``m2``. This technique is reffered to as pseudo-material cross-section
interpolation and is used for different type of reactors
:raw-latex:`\cite{pseudoMat2008,pseudoMatAlHamry}`.  Note that we didn't
specify cross-section suffixes in the code above. Their choice depends on the
``$DATAPATH`` environmental variable (must be set before using PIRS), name of
the xsdir file (``xsdir`` by default) and by material temperatures. When a
material is specified to the MCNP interface, it looks in the xsdir files for
the cross-sections with the closest temperature and correspondingly chooses the 
suffix. 

Mesh tallies are used to compute axial distribution of heat. Mesh tally parameters
are defined by the geometry element dimensions and its ``heat`` attribute. In
the example, the mesh tally covers a region that coincides with the fuel
cylinder and has ten axial equidistant mesh elements.


High-level interface to SCF
-------------------------------

The SCF code interface can handle only particular types of geometries described
by the general model classes. This limitation is due to the origin of problems
solved with SCF. Particularly, the general model defined above,  ``b``, cannot be
handled with the current implementation of the SCF interface, since it needs a
model representing at least one rod -- a set of two or three coaxial cylinders
representing clad, gap and fuel regions of a rod. Thus the usage of the SCF 
interface will be shown only schematically::


    from hpmc import ScfInterface

    s = ScfInterface(r)

    # ...
    
    s.inlet_temperature = 560 # K
    s.total_power = 3e4 # W
    s.inlet_flow_rate = 400 # g/s
    s.exit_pressure = 15.5e6 # Pa

    p = s.run('R')

The usage of the SCF interface is similar to the usage of the MCNP interface.
First, an instance of the ``ScfInterface`` is created , its constructor takes a
general model as an argument. Additionally one needs to specify parts of the
general model representing fuel rods and optionally -- the part representing a
container (coolant channel wrapper).

In the current implementation, there are rather simplified possibilities to
specify boundary conditions. One can specify inlet temperature, total power,
inlet flow rate, exit pressure and some other (the SCF code has more
possibilities to specify boundary and initial conditions, for example one can
set inlet temperature to each subchannel).

Similar to the MCNP interface, the SCF code is started by calling the ``run``
method of the interface. The SCF input file is generated, based on the geometry
information from the general model and SCF-specific data provided to the SCF
interface, the code is executed, and results -- fuel temperature, coolant
temperature and densities -- are read and returned in the general model copy.


Example results for PWR assembly
=================================

Assembly model
--------------

At the current stage, the MCNP and SCF interfaces allow to model a
assembly-like geometries.  Test calculations have been performed for a PWR
assembly  model based on the PWR benchmark specifications
:raw-latex:`\cite{PWRbenchmark}`.

The assembly contains 264 UOX fuel pins and 25 guide tubes, positioned in a
square 17x17 lattice with 1.26 cm pitch; the model's horizontal cross-section
is a square with sides 21.42 cm. The model's height of 408.6 cm is defined by
the active length of fuel pins, plus lower and upper water reflectors, each
21.42 cm thick.  There are  two types of fuel pins: usual pins and pins with
IFBA (integrated fuel burnup absorber).

The coolant inlet temperature is 560 K. This temperature and correspondent
density (0.752 g/cm3 at 15.5 MPa) is used for the lower reflector.
Temperature and density of water in guide tubes is 580 K and 0.712 g/cm3,
respectively. The fuel and coolant in the active length region are divided into
11 axial layers of varying thickness to represent the fuel temperature, coolant
density and coolant temperature axial distributions. In the upper reflector,
the coolant properties are heterogeneous and correspond to the channel exit
parameters, as calculated by SCF.

All fuel pins have the same fuel composition: UO2 with U enriched to 4.2 % (in
mass). The pin cladding and guide tube wall are represented by zircaloy-2 :raw-latex:`\cite{PWRbenchmark}`.
Coolant is pure water. Gaps in fuel pins are filled with oxygen. The IFBA pins
have additional cylindrical layer of zirconium diboride (ZrB2).


In the MCNP models, in the active length region and in the upper reflector, the
coolant temperature and density as well as the fuel temperature are defined by
the SCF calculations. In the SCF models, the power profile is based on the MCNP
results.

.. figure:: pics/i__p01.pdf

   Horizontal section of MCNP model at iteration 62. Different colors
   correspond to materials with different temperatures.
   :raw-latex:`\label{pic:hor}`


.. figure:: pics/i__p02.pdf

   Vertical section of MCNP model at iteration 62. :raw-latex:`\label{pic:ver}`


Figures :raw-latex:`\ref{pic:hor}` and  :raw-latex:`\ref{pic:ver}` show MCNP
plots for the model. The plots illustrate some capabilities of the MCNP and SCF
interfaces:

    * the active length region can be split into axial layers arbitrarily;
      in the assembly model we apply a non-uniform pattern with thiner layers at
      the bottom and top of the model. The non-uniform pattern should represent a
      cosine-like distribution of power density axial profile more accurately.

    * Subchannels in SCF are "coolant-centered". The subchannels are converted
      into the MCNP model exactly, thus no interpolation or averaging of coolant
      properties is necessary.
     
    * Bundle of pins is represented in the MCNP model using the lattice cell.
      Another way to represent bundles of rods, without lattice cells, is also
      implemented in the MCNP interface, but cannot be applied to a model with
      17x17 elements.

     
The following boundary conditions are specified for SCF models: the coolant
inlet temperature is 560 K in all subchannels. Assembly thermal power is 18.47
MW; this value is obtained by dividing the core thermal power to the number of
assemblies in the core. The inlet mass flow rate is 82.12 kg/s; this value is
obtained also by dividing the average core mass flow rate to the number of
assemblies. The exit pressure is set to 15.5 MPa.

Thermo-physical properties of cladding and fuel pellets, specified in the
benchmark, are hard-coded in the SCF code under the name ``'benpwr'``. These
properties are applied in the SCF calculations to compute fuel temperature.

The relaxation scheme :raw-latex:`\cite{dufek2006}` is applied for the
coupled calculations. This scheme assumes an increase of statistical precision of
the MCNP results on each iteration. This is implemented by increasing the number of cycles. On
the first iteration, MCNP sampled 50 cycles with 1000 histories per cycle and
skipped first 10 cycles. On the 32-th iteration, MCNP sampled 835 cycles and on
the 62-nd iteration, MCNP sampled 1673 cycles.

For the demonstration calculations we have chosen an xsdir
with cross-sections sets for only two temperatures, 300 K and 1800 K (suffixes
31c and 40c, respectively). Thus, any fuel temperature is represented by a
mixture of only these two data sets, that minimizes the initialization time for
MCNP. To perform calculations with a finer cross-section temperature mesh, one
needs only to provide an xsdir with more data sets; no modifications in the
scripts describing the coupled calculations are needed.

The fuel temperature passed from SCF to MCNP is the radially-averaged
temperature, reported in the SCF output file in tables with rod results in the
column named ``tfuave``.

The subchannel coolant temperature and density is reported by SCF at the
boundaries of each axial layer. Coolant parameters for MCNP models must
correspond to the layer interior, they are estimated as a mean of the boundary
values.


Results
--------

Results are shown for the 62-nd iteration. The coupled calculation has been
started with the convergence criterion set to 50 pcm, and should
iterate until the standard deviation of the value of Keff computed with MCNP, and the
difference between two values of Keff computed on subsequent iterations, become
below this value. At the 62-nd iteration, the convergence criterion is not meet yet,
iterations continue, but the intermediate results can be analyzed since all
necessary data is dumped after each iteration and can be processed without
stopping the iterations.

Figure :raw-latex:`\ref{pic:keff}` shows Keff obtained on each cycle. In the
first iteration, the coolant properties correspond to an uniform power profile
and the initial neutron source is axially positioned in the center of the
assembly. These two aspects lead to a larger Keff, as compared to results
obtained on subsequent iterations. The statistical precision of Keff is
improved with iterations, since the number of sampled cycles in increased.


.. figure:: pics/b_iteration_062_keff.pdf

    Value of Keff versus iteration number. :raw-latex:`\label{pic:keff}`


.. figure:: pics/b_iteration_062_temp50_0.pdf

   Coolant and fuel pellets temperature map in axial layer where maximal fuel
   temperature is reached. :raw-latex:`\label{pic:tmap}`


.. figure:: pics/b_iteration_062_4_4.pdf

    Axial distribution of power density and fuel temperature in the pin with
    maximal power density. :raw-latex:`\label{pic:axial}`


The map on figure :raw-latex:`\ref{pic:tmap}` shows radial temperature distribution of 
fuel pellets and coolant. Although radial temperature
deviations are small, one can clearly see the effect of moderator channels to
the coolant temperature in adjacent channels. 

The fuel temperature and power density axial distributions are shown on figure
:raw-latex:`\ref{pic:axial}` for the fuel pin where the maximal power density
and maximal fuel temperature are reached. In the upper plot, the yellow line
shows results of the MCNP calculation on the 62-nd iteration and the black
line shows distribution of the relaxed power density. The later is used to get
fuel temperature axial distribution, which is shown on the lower plot on figure
:raw-latex:`\ref{pic:axial}`.


Current state  and outlook
============================

At the current stage of development, PIRS provides a convenient way to setup
MCNP and SCF calculations for pin- and assembly-like geometries. The example
considered in the paper illustrates that description of a neutronics and TH
model using PIRS classes is more compact as compared to the correspondent input
files but still allows to set all relevant parameters.

The concept of PIRS -- independent description of geometry, and code interfaces that understand this 
description -- establishes basis for coupled calculations. So far a code interface is added to PIRS, 
it can be used to organize data transfer between this code and already integrated into PIRS.

Python runs on Windows, Linux/Unix and other OS :raw-latex:`\cite{pythonWEB}`. Currently, PIRS has been
tested on desktop computers running Windows and Linux and on the JUQUEEN
supercomputer :raw-latex:`\cite{juqueenWEB}`. Most of the PIRS code is OS-independent; 
for OS-dependent parts of the code, Python has well-documented libraries.

Packages provided by the Python community simplify to large extent
post-processing of results obtained with PIRS. The code examples shown in this
paper illustrate only calculations-relevant part of PIRS. There are also
auxiliary classes and functions to dump calculation results for later use, to
generate plots etc. This allows to setup calculation work-flow starting from
input data specifications and up to generation of plots with results in a single 
Python script.

PIRS documentation is written in parallel with the code itself, with a delay
necessary to avoid documenting of experimental stuff. The Sphinx
:raw-latex:`\cite{sphinxWEB}` system is used. It provides environment, where
code examples -- very important part of software documentation -- is simple to
add and to keep updated with permanently developing software.

The presented framework, although already can be used to perform coupled
simulations of a pin- or assembly model, is under further development. The
nearest plans are dictated to large extent by the goals of the HPMC project.
Among them is ability to communicate with the job submission system of JUQUEEN,
which will allow to choose MCNP job parameters dependent on current loading of
the supercomputer. We also plan an interface to the SERPENT code
:raw-latex:`\cite{serpentWEB}`.  Futher plans might include interfaces to the
KANEXT :raw-latex:`\cite{kanext}` system developed at our institute; this
however lies beyond the HPMC project.

Acknowledgment
================

This work is funded by the European Commission via the FP7 project HPMC
"High-Performance Monte Carlo Reactor Core Analysis" under contract no. 295971.







..  BIBLIOGRAPHY

.. raw:: latex
    
    \bibliography{hpmc}
    \bibliographystyle{ans}

