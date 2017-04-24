Python-based framework for coupled neutronics-thermohydraulics reactor calculations
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Abstract
=========
We develop a set of python packages to provide modern programming interface to
neutronics and TH codes. Curently implemented interfaces to the MCNP and SCF
codes allow efficient description of neutronics and thermo-hydraulics domains
and provide framework for coupling.



Introduction
============

The HPMC project [1] aims full-core coupled calculations including neutronics,
thermo-hydraulics, burnup and time dependence.  This goal will be achieved in
steps, starting from coupling of two physics domains (e.g. neutronics and
termohydraulics, neutronics and nuclide kinetics, etc.) for simple pin and assembly
geometries. The transition from simple geometries to more general and complex
implies that the coupling code developed for simple geometry at the first stage
of the project should be reused on later stages. 

It assumed in the HPMC project that on certain stage cluster computers will be
used for Monte-Carlo neutronics caluclations. This means that the developed
code should work on local desktops as well on cluster nodes. 

These two aspects of the project led us to development of a python-based
framework for coupling.  The concept of this framework, the current development
stage, code examples and some calculation resutls are presented in this work.



Concept of the coupling framework
=================================
The coupling framework includes (a) means to describe a general calculation model,
where data common for all physics domain can be specified, and (b) particular
code backends. The code backends 'understand' the general model, provide interface to 
code-specific data, and handle the code input and output files.

This framework structure allows to develop independently code backends, once
the structure of the general model is defined. To a user (a nuclear reactor physisist
performing computations), this framework structure provides convenient
possibility to define common data only once, as a general model, and to use these
data in each code involved into coupled calculations.


General model
--------------

The general model, as currently implemented, describes geometry of the
calculation domain.

To represent a PWR- or BWR-like geometry, two types of solids are defined: a
rectangular parallelepiped (box), and a vertical cylinder. There are several
rules that the solids obey: A solid can be inserted into another one, and can
be positioned arbitrarily with respect to its container; Several solids can be
inserted into the same container, the recently inserted covers the previously
inserted; A solid can be inserted into only one container at the same time.

For example, a general model describing one fuel pin with surrounded coolant
can have the following elements:

    - A box representing the coolant,

    - a cylinder inserted into the coolant box, reprsenting the cladding,

    - a cylinder inserted into the cladding cylinder, representing the gap,

    - a cylinder inserted into the gap cylinder, representing the fuel pellets.

Each element of the general model has attributes to represent state variables.
Currently implemented are heat, temperature and density axial profiles. Each
state variable attribute has its own axial meshing. Each axial mesh of every
state variable has its own value. Thus, axial profiles for heat, density and
temperature are represented by piecewise-constant functions.

A material name can be assigned to each general model element. Currently, these
are just strings, the meaning of the material name must be specified to every
particular code backend.

The following code is an example of a pin model with the structure as described above:

.. ipython:: python

    from hpmc import Box, Cylinder

    w = Box(X=1.27, Y=1.27, Z=390+50)                # water box

    c = w.insert('clad', Cylinder(R=0.475, Z=3400))  # clad
    g = c.insert('gap',  Cylinder(R=0.411, Z=390))   # gap
    f = g.insert('fuel', Cylinder(R=0.4025, Z=g.Z))  # pellets

    # material names
    w.material = 'water'
    c.material = 'zirc'
    f.material = 'uo2'

    # water density 
    w.dens.set_grid([1]*10)  # 10 equal axial mesh elements
    w.dens.set_values(1)     # constant density, g/cm3

    # water temperature
    w.temp.set_grid([1]*7)   # 7 mesh elements
    w.temp.set_values(580.)  # const. temp, K

    # fuel temperature
    f.temp.set_grid([1]*6)   # 6 mesh elements
    f.temp.set_values(1200)  

    # mesh for heat:
    f.heat.set_grid([1]*10)  # 10 mesh elements
    f.heat.set_values([1, 2, 3, 4, 5, 
                       5, 4, 3, 2, 1]) # initial heat axial profile

    # fuel and clad densities are constant:
    c.dens.set_values(4.)
    f.dens.set_values(10.)

The 'hpmc' package is the package where the solids and axial mesh classes are
defined. The insert() method puts a solid given as its second argument with the
key, specified as the first argument, and returns the inserted solid. The
set_grid() and set_values() methods of the heat, temp(erature) and dens(ity)
attributes are used to specify the piecewise constant representation of the
correspondent state variables.


MCNP backend
-------------

The MCNP backend is implemented in two steps. The stand-alone python package
'mcnp' provides object-oriented description of cells, surfaces, tallies and
materials. The MCNP interface, defined as a part of the 'hpmc' package
describing the general model, can convert solids of the general model to cells
and surfaces of the 'mcnp' package.

The MCNP interface needs certain MCNP-specific data to convert a general model
to a valid MCNP input file. This includes material composition, boundary
conditions, source specification.

In the following example we show the definintion of water for MCNP:

.. ipython:: python

    import mcnp

    # natural element compositions
    h = mcnp.Material('H')
    o = mcnp.Material('O')
    # water chemical composition
    water = h*2 + o
    # thermal data for H in water
    water.thermal = 'lw'
    # substitution dictionary:
    water.sdict[8018] = 8016

The Material class has predefined natural isotopic compositions, taken from
`Pure Appl. Chem., vol. 83, No 2, pp. 397-410, 2011
<http://www.iupac.org/publications/pac/83/2/0397/>`_ Instances of this class
can be mixed using weight atomic and volume (if material density is specified)
fractions. Cross-section suffices are not set directly. Instead, a user
specifies path to an xsdir file and specifies material temperature. Based on
the content of the xsdir file, proper suffices are chosen automatically. One
can also specify interpolation law (in cases when material temperature is
represented as a mixture of materials at two different temperatures). To 
illustrate this functionality let us see the MCNP material specification generated by the
water material defined above:

.. ipython:: python

    print water.card()

Note the use of thermal data. No temperature interpolation is implemented for
thermal data, the code only choose the data with most close temperature.

A user must correspond the MCNP material to particular material name of the
general model.  in the next example it is shown how to create an MCNP interface
for the general model defined above and how to specify the material
composition, relevant to MCNP:

.. ipython:: python

    from hpmc import McnpInterface

    mci = McnpInterface(w)
    mci.materials['water'] = water

The McnpInterface class provides also means to define lateral and axial
boundary conditions, to specify initial neutron source and number of cycles in
a criticality run.

After all relevant data are specified, one can start MCNP with the run()
method. This method requires one argument, which specifies the MCNP execution
mode. For example, the following code creates a folder, generates the input
file corresondent to the geometry of the general model, starts MCNP in the
initial run execution mode and returns results of calculations as the copy of
the input general mode:

.. ipython:: python

    mc_result = mci.run('r')

The lower-cased mode 'r' means that MCNP workplace (i.e. folder with all
necessary files) is prepared, but MCNP is not actually started. Even in this
case the returned model has some arbitrary heat profile. This option is usefull
to test scripts, when not actual results, but only the formal coupling and
coding is checked.

SCF backend
------------

An interface to the SCF [] code is implemented similar to the MCNP interface.
There is stand-alone package 'scf' whose classes describe object-oriented
representation of SCF input data. And there is an ScfInterface class that 'knows' 
how to convert general model geometry into the SCF geometry.

Cuurently, the SCF interface is in the development stage and some of the  
material properties as well as some calculation control parameters are hardcoded.
However, allready on this stage, the CSF interface can handle the pin general model
described above.

An example of the SCF interface to the pin model from above:

.. ipython:: python

    from hpmc import ScfInterface

    sci = ScfInterface(mc_result)

    sci.Tin = 580.  # coolant inlet temp, K
    sci.Ptot = 30e3 # total rod power, J/s
    sci.Gr = 3.6e2  # mass flow rate, g/cm3

    sc_result = sci.run('r')

Note that we passed to the SCF interface the general model returned by the MCNP
interface. in this way, results of MCNP run appear in the input for SCF. This
technique provides the basis for effective and transparent data handling
between codes.

Additionally, one can perform mathematical operations (currently implemented
addition, subtraction, multiplication) on the attributes representing density,
temperature and heat. For example, a relaxation formula of this kind:

.. math::
    
    P_{r, i} = \alpha  P_{r, i-1}  +  (1. - \alpha) P_{m, i}

where subscript r denotes relaxed power used as input for SCF, and the m
subscript denotes the power computed by MCNP an i-th iteration, can be
described as the following code:

.. ipython:: python

    # i-1 heat, used for scf input
    Pr = sci.gm.values()[-1].heat

    # i-th mcnp result:
    Pm = mc_result.values()[-1].heat

    # relaxation factor
    a = 0.5

    # new relaxed power:
    Pr = a*Pr  +  (1. - a)*Pm


Results of illustrative coupled calculations
----------------------------------------------

To test the developed framework and to provide a real-world example, we define
a model to represent a PWR fuel pin. Two coupling schemes are coded: one
utilizes relaxation of the power axial profile with MCNP statistics increase on
each iteration [Dufek], the other utilizes relaxation of the fuel temperature axial
profile with the constant MCNP statistics [Alex]. 

Figure 1 shows axial profiles of fuel heat and temperature, and water
temperature adn density after the 22-nd iteration. At this iteration MCNP was
scheduled to sample about 2400 cycles, 50 of them are inactive, each cycle has
500 particle histories. 
Black line on the upper plot shows the relaxed power obtained on this
iteration, :math:`P_{i}`, computed as superposition of the MCNP result (yellow
line, :math:`p_i`) and previous relaxed power (grey line, :math:`P_{i-1}`). One
can see that on this iteration the new MCNP result does not introduce
considerable changes to the relaxed distribution.

The lower plots show behaviour of temperature and density as computed with SCF
for the relaxed power :math:`P_i`. For comparison, the correspondent axial
profiles obtained on the previous iteration, are shown.

.. figure:: ../../c1_022.pdf
    :scale: 70 %

    Heat, temperature and density axial profiles on the 22-nd iteration of the
    1-st coupling scheme.  In this scheme, the number of cycles to sample in
    MCNP run increases to about 100 each iteration. At the first iteration
    there were 200 total cycles, thus the total amount of cycles sampled in all
    iteratins si about 29000.
    

The second figure shows results on the 30-th iteration of the second coupling
scheme. The upper plot shows the relaxed fuel temperature (black line,
:math:`T_{f,i}`), which is abtained as superposition of SCF result (yellow
line, :math:`{f,i}`) and relaxed fuel temperature on the previous step (grey
line, :math:`T_{f,i-1}`). Next two plots show relaxed water temperature and
water density, obtained with the same relaxatin schem as the fuel temperature.
The lowest plot shows the fuel heat axial profile, as computed by MCNP for the
model with relaxed fuel temperature, water temperature and density.


.. figure:: ../../c2_030.pdf
    :scale: 70 %

    Fuel temperature, water temperature and density, and the heat axial
    profiles obtained on the 30-th iteration of the second coupling scheme.  In
    this scheme, the number of cycles is constant over iterations. The 30-th
    cycle correspond thus to about 30000 cylces sampled in all iterations.


Current state and outlook
--------------------------

The example code snippets above show the most important allready implemented
features of the framework. Additionally, there are some auxiliary mechanisms
that simplify everyday life of a user running coupled calculations. Among them
is the ability to dump current iteration, so it can be continued later, and
an automatic generation of figure reports similar to the plots shown above. 

The documentation is developed in sync with the packages, with a small delay
necessary to exclude documenting of experimentall stuff. The Sphinx system is used to
write documentation. This system provides an environment, where the code
examples written in the documentation can be run through the Python
interpreter, ensuring that the documentationis in takt with the code.

The presented framework, although allready can be used to perform coupled
simulations of a stand-alone pin, is under development. The nearest plans,
according to the goals of the HPMC project, is to improve MCNP and SCF
interfaces to the level that allows modelling and coupling calculations of a
nuclear reactor core detailed down to assembly- and pin-level. Additionally, an
interface to the Serpent [] code must be provided. 

Since the full reactor core simulations with Monte-Carlo codes are feasible
only when run in parallel, transition from desktops (currently, the packages
work both on Windows and Linux machines) to clusters is unavoidable. A basement
for this transition is ready, however, implementation details will depend on
the cluster's job scheduling environment.

Further plans may include coupling to the parts of KANEXT system and some
burnup codes. This, however lies beyond the HPMC project.



Acknoledgement
---------------
This work is funded by the European Commission via the FP7 project HPMC
“High-Performance Monte Carlo Reactor Core Analysis” under contract no. 295971.




