
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import os
import stat
import shutil
import datetime
import time

# for results of 'dry run'
from math import cos, pi 
import random 

from ... import mcnp
from ...solids import Sphere, Box, Cylinder
from .convertors import solid2surface, solid2volume, zmesh2volumes, zmesh2mtally, grid2tally, base_element2volume
from ...core import scheduler

_LOG = False #True

class McnpInterface(mcnp.model.Model):
    """
    McnpInterface is an MCNP model with ability to take an instance of one of the
    solids classes as input data.

    Simple box and cylinder
    >>> print McnpInterface(Box())
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1  $ model
    2 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5
    <BLANKLINE>
    c data cards
    c materials
    <BLANKLINE>
    >>> print McnpInterface(Cylinder())
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1  $ model
    2 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
    <BLANKLINE>
    c data cards
    c materials
    <BLANKLINE>

    Box and cylinder with axially distributed density. Note that not only mesh
    itself must be set, but also the values, so the density is not constant:

    >>> s1 = Box()
    >>> s1.dens.set_grid([1]*4)
    >>> s1.dens.set_values([1.1, 1.2, 1.3, 1.4])
    >>> s1.material = 'fuel'
    >>> print McnpInterface(s1)
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1 fill=1  $ model
    2 1 -1.1 2 -3 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    3 1 -1.2 3 -4 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    4 1 -1.3 4 -5 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    5 1 -1.4 5 -6 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    6 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5
    2 pz  -1000.5
    3 pz  -0.25
    4 pz  0.0
    5 pz  0.25
    6 pz  1000.5
    <BLANKLINE>
    c data cards
    c materials
    m1 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    <BLANKLINE>

    >>> s1 = Cylinder()
    >>> s1.dens.set_grid([1]*4)
    >>> s1.dens.set_values([1.1, 1.2, 1.3, 1.4])
    >>> s1.material = 'fuel'
    >>> print McnpInterface(s1)
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1 fill=1  $ model
    2 1 -1.1 2 -3 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    3 1 -1.2 3 -4 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    4 1 -1.3 4 -5 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    5 1 -1.4 5 -6 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    6 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
    2 pz  -1000.5
    3 pz  -0.25
    4 pz  0.0
    5 pz  0.25
    6 pz  1000.5
    <BLANKLINE>
    c data cards
    c materials
    m1 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    <BLANKLINE>


    The temperature mesh:

    >>> b = Box()
    >>> b.material = 'fuel'
    >>> b.temp.set_grid([1]*5)
    >>> b.temp.set_values([300, 320, 340, 400, 420])
    >>> print McnpInterface(b)
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1 fill=1  $ model
    2 1 -1.0 2 -3 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    3 2 -1.0 3 -4 imp:n=1 tmp=2.75754976e-08 u=1  $ comment
    4 3 -1.0 4 -5 imp:n=1 tmp=2.92989662e-08 u=1  $ comment
    5 4 -1.0 5 -6 imp:n=1 tmp=3.4469372e-08 u=1  $ comment
    6 5 -1.0 6 -7 imp:n=1 tmp=3.61928406e-08 u=1  $ comment
    7 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rpp  -0.5  0.5  -0.5  0.5  -0.5  0.5
    2 pz  -1000.5
    3 pz  -0.3
    4 pz  -0.1
    5 pz  0.1
    6 pz  0.3
    7 pz  1000.5
    <BLANKLINE>
    c data cards
    c materials
    m1 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    m2 $ mixture  H-001 at 320.0 K 
         1001.31c 0.788017730687     1001.32c 0.211982269313 $ 0.788017730687 parts of 299.999663469K and 0.211982269313 parts of 400.007287629K
    m3 $ mixture  H-001 at 340.0 K 
         1001.31c 0.5825662186     1001.32c 0.4174337814 $ 0.5825662186 parts of 299.999663469K and 0.4174337814 parts of 400.007287629K
    m4 $ mixture  H-001 at 400.0 K 
         1001.32c 1.0
    m5 $ mixture  H-001 at 420.0 K 
         1001.32c 0.790847540923     1001.33c 0.209152459077 $ 0.790847540923 parts of 400.007287629K and 0.209152459077 parts of 500.003307284K
    <BLANKLINE>

    model consisting of several solids, each with its own material:

    >>> b = Box()
    >>> b.X = 10
    >>> b.Y = 10 
    >>> b.Z = 100
    >>> c = b.insert(1, Cylinder())
    >>> c.R = 1
    >>> c.Z = b.Z
    >>> b.material = 'water'
    >>> c.material = 'pin'
    >>> print McnpInterface(b)
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1 fill=1  $ model
    2 1 -1.0 2 -3 (4:1.5:1.6) imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    3 2 -1.0 -4 -1.5 -1.6 imp:n=1 u=1 tmp=2.5852029e-08  $ 1
    4 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rpp  -5.0  5.0  -5.0  5.0  -50.0  50.0
    2 pz  -1005.0
    3 pz  1005.0
    4 cz  1.0
    <BLANKLINE>
    c data cards
    c materials
    m1 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    m2 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    <BLANKLINE>


    A more complex model consisting of several solids and with density and
    temperature distributions.

    >>> b = Box()
    >>> b.set_radius(10.)
    >>> b.material = 'm1'
    >>> c1 = b.insert(1, Cylinder())
    >>> c2 = b.insert(2, Cylinder())
    >>> c3 = b.insert(3, Cylinder())
    >>> c1.pos.z = -5
    >>> c2.pos.z =  0
    >>> c3.pos.z =  5
    >>> b.dens.set_grid([1,1,1])
    >>> b.dens.set_values( [1, 2, 3] )
    >>> b.temp.set_grid([1,1,1, 1, 1, 1])
    >>> b.temp.set_values( [300, 320, 340, 360, 420, 400.] )
    >>> m = McnpInterface(b)
    >>> print m
    MESSAGE:
         datapath=C:\Python27\lib\site-packages\mcnp
    <BLANKLINE>
    c title
    1 0  -1 imp:n=1 fill=1  $ model
    2 1 -1 2 -3 imp:n=1 tmp=2.5852029e-08 u=1  $ comment
    3 2 -1 3 -4 5 imp:n=1 tmp=2.75754976e-08 u=1  $ comment
    4 3 -2 4 -6 (5.1:7:-8) imp:n=1 tmp=2.92989662e-08 u=1  $ comment
    5 4 -2 6 -9 (5.1:7:-8) imp:n=1 tmp=3.10224348e-08 u=1  $ comment
    6 5 -3 9 -10 (5.1:11:-12) imp:n=1 tmp=3.61928406e-08 u=1  $ comment
    7 6 -3 10 -13 imp:n=1 tmp=3.4469372e-08 u=1  $ comment
    8 0  -5 imp:n=1 u=1  $ 1
    9 0  -5.1 -7 8 imp:n=1 u=1  $ 2
    10 0  -5.1 -11 12 imp:n=1 u=1  $ 3
    11 0  1 imp:n=0  $ The other world
    <BLANKLINE>
    c surfaces
    1 rpp  -10.0  10.0  -10.0  10.0  -10.0  10.0
    2 pz  -1010.0
    3 pz  -6.666666667
    4 pz  -3.333333333
    5 rcc  0.0  0.0  -5.5  0.0  0.0  1.0  1.0
    6 pz  0.0
    7 pz  0.5
    8 pz  -0.5
    9 pz  3.333333333
    10 pz  6.666666667
    11 pz  5.5
    12 pz  4.5
    13 pz  1010.0
    <BLANKLINE>
    c data cards
    c materials
    m1 $ mixture  H-001 at 300.0 K 
         1001.31c 1.0
    m2 $ mixture  H-001 at 320.0 K 
         1001.31c 0.788017730687     1001.32c 0.211982269313 $ 0.788017730687 parts of 299.999663469K and 0.211982269313 parts of 400.007287629K
    m3 $ mixture  H-001 at 340.0 K 
         1001.31c 0.5825662186     1001.32c 0.4174337814 $ 0.5825662186 parts of 299.999663469K and 0.4174337814 parts of 400.007287629K
    m4 $ mixture  H-001 at 360.0 K 
         1001.31c 0.383073636439     1001.32c 0.616926363561 $ 0.383073636439 parts of 299.999663469K and 0.616926363561 parts of 400.007287629K
    m5 $ mixture  H-001 at 420.0 K 
         1001.32c 0.790847540923     1001.33c 0.209152459077 $ 0.790847540923 parts of 400.007287629K and 0.209152459077 parts of 500.003307284K
    m6 $ mixture  H-001 at 400.0 K 
         1001.32c 1.0
    <BLANKLINE>
    """

    def __init__(self, gm=None, **kwargs):
        self.__uC = mcnp.auxiliary.counters.Counter(0) # universe counter.

        self.__gm = gm # general model to be converted.
        self.__mdict = {} # dictionary for material names.
        self.__mdict['void'] = 0
        self.__mdict[0] = 0
        self.__mdefa = mcnp.Material(1001) # default material
        self.__mdefd = 1.0e-5 # default material density
        self.__bc = {'axial':'', 'radial':''}
        super(McnpInterface, self).__init__( **kwargs )


    @property
    def materials(self):
        """
        Dictionary to define the actual meaning of the  material names used in
        the general model.  Keys are strings with material names from the
        general model, values are instances of mcnp.Material class.

        Note that instances of mcnp.Material class have their own property T
        (temperature). This property is not used. The temperature is defined in
        the temp property of each element of the general model.

        Note also that each instance of the mcnp.Material class has its own
        xsdir property.  This will be replaced with the xsdir property set to
        the model.
        """
        return self.__mdict

    @property
    def bc(self):
        """
        Dictionary specifying boundary conditions on the axial and radial
        boundaries of the model.

        Two keys are meaningful: 'axial' and 'radial'. Values can be one of ''
        , '*' and '+' meaning no reflection, mirror and white reflection,
        respectively.

        >>> b = Cylinder()
        >>> m = McnpInterface(b)
        >>> m.bc['axial'] = '*'
        >>> print m     #doctest: +ELLIPSIS
        ...
        1 0  -3 -2 1 imp:n=1  $ model
        2 0  3:2:-1 imp:n=0  $ The other world
        <BLANKLINE>
        c surfaces
        *1 pz  -0.5
        *2 pz  0.5
        3 cz  1.0
        ...

        >>> m.bc['radial'] = '*'
        >>> print m        #doctest: +ELLIPSIS 
        ...
        1 0  -1 imp:n=1  $ model
        2 0  1 imp:n=0  $ The other world
        <BLANKLINE>
        c surfaces
        *1 rcc  0.0  0.0  -0.5  0.0  0.0  1.0  1.0
        ...

        >>> m.bc['radial'] = '+'
        >>> print m        #doctest: +ELLIPSIS 
        ...
        1 0  -3 -2 1 imp:n=1  $ model
        2 0  3:2:-1 imp:n=0  $ The other world
        <BLANKLINE>
        c surfaces
        *1 pz  -0.5
        *2 pz  0.5
        +3 cz  1.0
        ...
        """
        return self.__bc

    @property
    def gm(self):
        """
        Link to the general model. This is the input data for the MCNP input
        file generated by the McnpInterface.
        """
        return self.__gm

    @gm.setter
    def gm(self, value):
        self.__gm = value

    def __str__(self):
        self._process_model()
        s1 =  super(McnpInterface, self).__str__()
        return s1

    
    def _process_tallies(self):
        log = _LOG

        # first, ensure to delete attributes from previous run:
        for v in self.__gm.values(True):
            for a in ['_element', '_rods', '_grid', '_tally']:
                if hasattr(v, a): delattr(v, a)


        for v in self.__gm.values(True):
            if v.grid.used():
                if log:
                    print 'grid used in ', v.name, v.get_key()
                validrods = []
                for r in v.heats():
                    if log:
                        print 'rod with heat: ', r.get_key(), r.name, r.material, r.pos, r.ijk, r.abspos()
                    # r is an element having heat. Find how it is positioned
                    # with respect to v:
                    pr = [r] + list( r.parents(v)) # parents of r till v, including v
                    if log:
                        print 'parents:'
                        for i, p in enumerate(pr):
                            print i, p.id(), p.material, p.ijk, p.indexed()
                            print r.abspos(p)
                    if pr[-2].indexed():
                        # the parent of r directly ineserted into v is indexed
                        if r.abspos(pr[-2]).car == (0,0,0):
                            # and if r is not shifted with respect to the parent, directly
                            # inserted into v
                            validrods.append((r, pr[-2].ijk))
                            if log:
                                print 'rod is valid'
                if log:
                    print 'found {0} rods for gridmesh in grid'.format(len(validrods))
                if validrods:
                    # unify zmeshes for validrods
                    r0 = validrods[0][0]
                    for r, ijk in validrods[1:]:
                        r0.heat.unify(r.heat)
                    for r, ijk in validrods[1:]:
                        r0.heat.unify(r.heat)
                    # create meshtally
                    mt = grid2tally(v, r0)
                    mt._rods = validrods
                    mt._grid = v
                    if log:
                        print 'mesh tally\n', mt
                    It = self.tallyCollection.index(mt)
                    # label rods that they belong to the gridtally
                    for r, ijk in validrods:
                        r._tally = It

        # add individual mesh tallies
        for v in self.__gm.heats():
            if v.heat.values() != [0.]:
                try:
                    It = v._tally
                except AttributeError:
                    mt = zmesh2mtally(v.heat)
                    mt._element = v
                    It = self.tallyCollection.index(mt)
                    v._tally = It
                if log:
                    print 'Fmesh tally for ', v.get_key(), v._tally

        if log:
            print 'tally collection after _process_tallies:', self.tallyCollection



    def _process_model(self):
        log = _LOG
        if log:
            print '_process_model starts'
        time1 = time.time()
        self.clear()
        self.__uC.reset(0)

        if self.__gm is None:
            # this is by default. No processing is necessary.
            return
        if self.__gm.root is not self.__gm:
            raise ValueError('McnpInterface.gm must point to the root of a model')

        # self.__pm = Sphere()
        # self.__pm.R = self.__gm.get_radius(False) # False means circumfered radius
        self.__pm = Sphere()
        self.__pm.circumscribe(self.__gm) 
        self.__pm.__u = self.__uC.get_next()
        if log:
            print 'copy of gm is generated'

        # planes above and below the model. Used to represent upper and lower
        # layers of axial distributions:
        Zmin, Zmax = self.__pm.extension('z')
        self.__whole_volume = mcnp.Surface('pz {0}'.format(Zmin - 1000.)).volume()

        self._process_tallies()
        if log:
            print 'tallies generated'


        # if axial and radial bc are different, do not use macrobody for the model boundary:
        # add surfaces that can contain reflective b.c. in advance:
        ref = self.__gm.get_child(self.__bc.get('key', ())) # element whose surfaaces can be reflective
        if self.__bc['axial'] != self.__bc['radial']:
            for z in ref.extension('z'):
                self.surfaceCollection.index(mcnp.surfaces.Surface(type='pz', plst=[z], refl=self.__bc['axial']))
        self.surfaceCollection.index(solid2surface(ref, refl=self.__bc['radial']))

        self.__pm.insert(self.__gm) 
        self._add_interior(self.__pm, self.__pm.__u, 'Container for model', importance=0)
        time2 = time.time()
        self.process_model_time = time2 - time1 
        self.__gm.withdraw()
        if log:
            print '{0} cells generated.'.format(len(self.cells))
        return

    def _add_lattice(self, element, u, element_name):
        log = _LOG
        if log:
            print '_add_lattice ', element_name
        # add the lattice cell
        lcell = mcnp.Cell()
        self.cells.append(lcell)
        lcell.mat = self._get_material(element.material, T=element.get_value_by_index('temp', 0))
        d = element.get_value_by_index('dens', 0)
        if d == 0. and lcell.mat != 0:
            # if dens is zero, use material's density
            d = lcell.mat[0].dens
        lcell.rho = -d
        lcell.vol = -base_element2volume(element)
        lcell.opt['u'] = u
        lcell.opt['imp:n'] = 1
        lcell.opt['lat'] = 1
        lcell.cmt = 'Lattice cell for {0}'.format(element_name)
        # filling matrix:
        f = '{0}:{1} {2}:{3} {4}:{5}'.format(*element.grid.extension())
        itypel = []
        utd = {}
        utd[0] = u
        it = 0 
        stack = []
        for (ijk, leb, itype) in element.lattice_elements():
            if itype > it:
                # leb was not previously defined.
                unext = self.__uC.get_next() # setup new universe
                utd[itype] = unext
                self._add_interior(leb, unext, 'lattice element {0}'.format(ijk))
                # stack.append((leb, unext, '{} {}'.format(element_name, ijk)))
                it = itype
            itypel.append(itype) 
            # print ' '*16, '{}'.format(ijk)
        for itype in itypel:
            f += ' {0} '.format(utd[itype])
        lcell.opt['fill'] = f
        if log:
            print ' '*8, 'added {0} lebs'.format(len(itypel))
            print ' '*8, 'scheduled {0} leb interiors'.format(len(stack))

        while stack:
            args = stack.pop(0)
            self._add_interior(*args)


    def _add_interior(self, element, u, element_name, importance=1):
        log = _LOG
        if element.grid.used():
            # element will be represented by a lattice cell
            self._add_lattice(element, u, element_name)
                    
        else:
            if log:
                print '_add_interior for ', element_name
            for c in element.children:
                # compute in advance some parameters of the children:
                c.__vol = solid2volume(c)

            Nc = len(element.children)
            stack = []
            # add cells that describe containers of children:
            for Ic in range(Nc):
                child = element.children[Ic]
                cell = mcnp.Cell()
                self.cells.append(cell)
                vol = -child.__vol
                for Ioc in range(Ic+1, Nc):
                    ochild = element.children[Ioc]
                    if child.intersect(ochild):
                        vol = vol & ochild.__vol
                cell.vol = vol
                cell.opt['u'] = u
                cell.opt['imp:n'] = 1
                cell.cmt = 'container for {0}'.format(child.name)
                if len(child.children) == 0 and child.is_constant('temp') and child.is_constant('dens'):
                    t = child.get_value_by_index('temp', 0)
                    cell.mat = self._get_material(child.material, T=t)
                    d = child.get_value_by_index('dens', 0)
                    if d == 0. and cell.mat != 0:
                        # if density is zero, use material value
                        d = cell.mat[0].dens
                    cell.rho = -d
                    cell.opt['tmp'] = t
                else:
                    fill = self.__uC.get_next()
                    cell.opt['fill'] = fill
                    self._add_interior(child, fill, '{0}'.format(child.name))
                    # stack.append((child, fill, '{} {}'.format(element_name, child.name)))
            if log:
                print ' '*8, 'added {0} children containers'.format(Nc)

            # add cells that describe axial distribution of temp and dens in element:
            if not element._no_interior:
                Nl = 0
                for (z1, z2, (t, d), cc, (isf, isl)) in element.layers(True, True, False):
                    if isf:
                        v1 = -mcnp.Volume(0)
                    else:
                        v1 = mcnp.Volume( 1, mcnp.Surface(type='pz', plst=[z1]))
                    if isl:
                        v2 = -mcnp.Volume(0)
                    else:
                        v2 = mcnp.Volume(-1, mcnp.Surface(type='pz', plst=[z2]))
                    vol = v1 & v2 
                    for c in cc:
                        vol = vol & c.__vol
                    if vol.is_universal():
                        # this can be only if there is only one layer and there are
                        # no children . 
                        vol = self.__whole_volume
                    c = mcnp.Cell()
                    self.cells.append(c)
                    c.mat = self._get_material(element.material, T=t)
                    if d == 0. and cell.mat != 0:
                        d = cell.mat[0].dens
                    c.rho = -d
                    c.vol = vol
                    c.opt['tmp'] = t
                    c.opt['imp:n'] = importance
                    c.cmt = 'layer of {0}'.format(element_name)
                    c.opt['u'] = u
                    Nl += 1
                if log:
                    print ' '*8, 'added {0} layers'.format(Nl)

            if log:
                print ' '*8, 'scheduled {0} children interiors'.format(len(stack))
            while stack:
                args = stack.pop(0)
                self._add_interior(*args)

    def _get_material(self, mname, T=None):
        """
        Returns instance of Material class for the string name mname
        """
        if mname in self.__mdict.keys():
            m = self.__mdict[mname]
        else:
            print 'WARNING: material {0} not defined, will be replaced with default'.format(mname)
            m = mcnp.Material(self.__mdefa)
            m.dens = self.__mdefd
            self.__mdict[mname] = m
        if m != 0 and T is not None:
            m = (m, {'T':T})
        return m

    def plot_commands(self, element=None, XYopt={}, XZopt={}, YZopt={}):
        """ 
        A multi-line string representing plot commands, which can be feed to MCNP to produce plots of
        the model.

        By dafault, commands for three plots are written: section by XY, XZ and
        YZ planes.
        
        element -- optional argument. If of one of solids type, its dimensions
        will be used to set extent of the plot.
        
        XYopt -- optional dictionary to provide user-defined options to the XY
        plot. For example, XYopt={'ext':'3.0 6.0'}"""
        res = []
        if element is None:
            e = self.__gm
        else:
            e = element
        if isinstance(e, Sphere):
            X = e.R
            Y = e.R
            Z = e.R
        if isinstance(e, Box):
            X = e.X/2.
            Y = e.Y/2.
            Z = e.Z/2.
        if isinstance(e, Cylinder):
            X = e.R
            Y = e.R
            Z = e.Z/2.
        X *= 1.1
        Y *= 1.1
        Z *= 1.1
        (x,y,z) = e.abspos().car

        XYopt = dict(XYopt)
        XZopt = dict(XZopt)
        YZopt = dict(YZopt)
        XYopt['bas'] = XYopt.get('bas', '1 0 0 0 1 0')
        XZopt['bas'] = XZopt.get('bas', '1 0 0 0 0 1')
        YZopt['bas'] = YZopt.get('bas', '0 1 0 0 0 1')

        for dopt in [XYopt, XZopt, YZopt]:
            if 'ext' in dopt.keys() and isinstance(dopt['ext'], tuple):
                sss = str(dopt['ext'])
                sss = sss.replace('(', ' ')
                sss = sss.replace(')', ' ')
                sss = sss.replace(',', ' ')
                dopt['ext'] = sss

        XYopt['ext'] = XYopt.get('ext', '{0} {1}'.format(X, Y))
        XZopt['ext'] = XZopt.get('ext', '{0} {1}'.format(X, Z))
        YZopt['ext'] = YZopt.get('ext', '{0} {1}'.format(Y, Z))

        XYopt['or'] = XYopt.get('or', '{0} {1} {2}'.format(x, y, z))
        XZopt['or'] = XZopt.get('or', '{0} {1} {2}'.format(x, y, z))
        YZopt['or'] = YZopt.get('or', '{0} {1} {2}'.format(x, y, z))

        XYopt['mesh'] = XYopt.get('mesh', 1)
        XZopt['mesh'] = XZopt.get('mesh', 1)
        YZopt['mesh'] = YZopt.get('mesh', 1)

        XYopt['sca'] = 1
        XZopt['sca'] = 1
        YZopt['sca'] = 1

        XYopt['lab'] = XYopt.get('lab', '0 0.3')
        XZopt['lab'] = XZopt.get('lab', '0 0.3')
        YZopt['lab'] = YZopt.get('lab', '0 0.3')

        # Default colouring depends on presence in the original model non-uniform density meshes
        def_color = 'by mat'
        for v in self.__gm.values(True):
            if not v.is_constant('dens'):
                def_color = 'by den'
                break

        XYopt['color'] = XYopt.get('color', def_color)
        XZopt['color'] = XZopt.get('color', def_color)
        YZopt['color'] = YZopt.get('color', def_color)

        for opt_dict in [XYopt, XZopt, YZopt]:
            required_opts = ['bas', 'ext', 'or', 'lab', 'sca', 'color']
            optional_opts = list( set(opt_dict.keys()) - set(required_opts) )
            line = ''
            for opt in required_opts + optional_opts:
                s = '{0} {1} '.format(opt, opt_dict[opt])
                if len(line) + len(s) >= 78:
                    res.append( line + ' &')
                    line = ''
                line += s
            res.append( line )
        res.append( 'end' )
        return '\n'.join(res)

    def read_meshtal(self, meshtal='meshtal'):
        """
        Reads meshtall to the correspondent meshtallies and returns the copy of the general model containing read values.
        """
        self.tallyCollection.read(meshtal)
        rm = self.gm.copy_tree()
        for mt in self.tallyCollection.values():
            rm.get_child(mt.__ckey).heat.set_values(mt.values)
        return rm

    def run(self, mode, **kwargs):
        # if not continue, generate input file
        # here the _process_model is called. So, this step must be before
        # plot_commands.
        if mode.lower() != 'c':
            self.wp.inp.string = str(self)
            print '   MCNP input file generated in {0} seconds'.format(self.process_model_time)

        # if plot mode, provide plot commands to the workplace
        if mode.lower() == 'p':
            m = kwargs.get('element', self.__gm)
            self.wp.com.string = self.plot_commands(element=m)
            print '   MCNP plotting commands generated'

        # if plot meshtally mode, provide plot commands in an external file:
        if mode.lower() == 'z':
            self.wp.com.exfile = 'commesh'

        # run the job
        self.wp.run(mode, **kwargs)

        # read meshtally
        nm = self.__gm # .copy_tree()
        if mode in 'cCrR':
            if mode.isupper():
                # put computed results to the returned model.
                self.tallyCollection.read(self.wp.meshtal.exfile)
                for (tn, tally) in self.tallyCollection.items():
                    try:
                        # if _rods attribute is defined -- this is a grid tally containing results for all rods.
                        rods = tally._rods
                    except AttributeError:
                        # this is tally for single rod
                        tally._element.heat.set_values(tally.values)
                    else:
                        imin, imax = tally._grid.grid.extension('x') 
                        jmin, jmax = tally._grid.grid.extension('y') 
                        Nx = imax - imin + 1 
                        Ny = jmax - jmin + 1
                        Nz = len(rods[0][0].heat.get_grid())
                        for r, ijk in rods:
                            i, j, k = ijk
                            i = i - imin
                            j = j - jmin
                            n = i*Ny + j
                            vals = tally.values[n*Nz:(n+1)*Nz]
                            r.heat.set_values(vals)
                            # print 'heat set '
                            # print ijk, r.name, r.material, r.abspos()
                            # print vals
                        
                print '   MCNP run took {0} seconds'.format(self.wp.run_time)
            else:
                # MCNP was not actually started. Put some values to the returned model.
                random.seed()
                def f(z):
                    mu = cos(z*pi)
                    sd = mu*0.3
                    return max(0., random.gauss(mu, sd))

                for tally in self.tallyCollection.values():
                    try:
                        # if _rods defined -- this is a grid tally
                        rods = tally._rods
                    except AttributeError:
                        # this is tally for single solid.
                        tally._element.heat.set_values_by_function(f, '1')
                    else:
                        for r, ijk in rods:
                            r.heat.set_values_by_function(f, '1')
            
        return nm
            



if __name__ == '__main__':
    import doctest
    doctest.testmod()

