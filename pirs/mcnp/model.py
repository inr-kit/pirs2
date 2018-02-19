"""
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

Class to represent MCNP model in terms of cells, surfaces, materials, etc.
"""
#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import time

from .cells import Cell
from .auxiliary import Counter 
from .surfaces import SurfaceCollection, Volume, Surface
from . import xsdir
from .material import MaterialCollection, Material
from .tallies import TallyCollection
from .mctal import Mctal
from . import workplace
from . import formatter
from . import card_classes

class Model(object):
    """
    Model is a list of cells with common collection of
    materials, surfaces and tallies.

    One setups the model by adding instances of the Cell class to the model.cells
    list. When the model is processed (for example, when converted to a
    string), each cell from the list is analysed: cells are added to a
    collection of cells, materials and surfaces used in the definition of cells
    are added to the material and surface collections. Collections are used to
    assign unique numbers (IDs) to cells, materials, surfaces, etc. When IDs
    are defined, a multi-line string representing the content of MCNP input
    file, is generated.
    
    Cell, material, surface and tally IDs are assigned automatically.

    In this way, cell and surface blocks, as well as part of the data block
    containig material and tally description of MCNP input file are generated
    automatically. One has also possibility to add lines to each block
    manually.

    """
    def __init__(self, SurfaceCollectionClass=SurfaceCollection, 
                       MaterialCollectionClass=MaterialCollection, 
                       TallyCollectionClass=TallyCollection, 
                       CellCounterClass=Counter):

        super(Model, self).__init__()

        self.__SCC = SurfaceCollectionClass
        self.__MCC = MaterialCollectionClass
        self.__TCC = TallyCollectionClass
        self.__CCC = CellCounterClass

        self.__mc = self.__MCC()
        self.__sc = self.__SCC()
        self.__cc = self.__CCC()
        self.__tc = self.__TCC()
        self.clear()

        self.__amc = [] # additional message cards
        self.__acc = [] # additional cell cards
        self.__asc = [] # additional surface cards
        self.__adc = ['prdmp j j 1   $ write mctal file'] # additional data cards

        self.__t = 'title' # title card.

        self.__kcode = card_classes.KcodeCard() 
        self.__kcode.active = False

        # workplace
        self.__wp = workplace.McnpWorkPlace()

        # mctal
        self.__mctal = Mctal() 

    @property
    def kcode(self):
        """kcode card.

        An instance of the card_classes.KcodeCard class.
        """
        return self.__kcode

    # FIXME provide safe way to set kcode property
    @kcode.setter
    def kcode(self, value):
        self.__kcode = value

    def clear(self):
        """
        Removes all cells, materials and surfaces from the correspondent collections. The lists of
        additional cards remain.
        """
        self.__sc.clear()
        self.__mc.clear()
        self.__tc.clear()
        self.__cc.reset()
        self.__cl = [] # cell instances.

    @property
    def wp(self):
        """
        Instance of the McnpWorkPlace() class. 
        
        Prepares working directory for MCNP and starts the code.
        """
        return self.__wp

    # FIXME provide safe method to copy workplaces
    @wp.setter
    def wp(self, value):
        self.__wp = value

    def run(self, mode='r', **kwargs):
        """
        Prepares content of the input file and starts MCNP job.
        """
        if len(self.__cl) > 0:
            # there are some cells in the model. Generate input 
            # file, if necessary.
            if mode.lower() != 'c':
                self.__wp.inp.string = str(self)
        self.wp.run(mode, **kwargs)

    def keff(self):
        """
        Reads last mctal file and returns the combined Keff and its st.dev.
        """
        self.__mctal.read(self.__wp.mctal.exfile)
        return self.__mctal.final()

    @property
    def cells(self):
        """
        List of cells. The elements of the list must be instances of the Cell() class.

        Elements can be added to and removed from the list. The processing of
        the cells in the list, i.e. adding the materials and surfaces to the
        common model collections, is done inside the method _process_cells.
        This method is called each time the model is converted to a string.

        Note that the default value of the Cell.vol attribute is a string. This cannot
        be used directly in the MCNP model; geometry of cells that are used in the model
        must be defined with the help of the Volume() and Surface() classes.
        
        """
        return self.__cl

    @property 
    def title(self):
        """
        String title of the problem. Goes to the title card in MCNP input file.

        """
        return self.__t

    @title.setter
    def title(self, value):
        self.__t = str(value)

    @property
    def surfaceCollection(self):
        """
        Instance of the SurfaceCollection class. Surfaces used to define
        geometry of cells are collected in this object. 
        
        This collection is used to define unique surface IDs and to ensure that
        a surface does not appear in the surface block of MCNP input file
        several times.

        Run the _process_model() method to ensure that the surface collection
        corresponds to the actual list of cells.

        """
        return self.__sc

    @property
    def materialCollection(self):
        """
        Instance of the MaterialCollection class. Cell materials are collected
        in this object. 
        
        The MaterialCollection is used to assign unique IDs to each material
        and to ensure that a material does not appear several times in the data
        block of MCNP input file.

        Run _process_model to ensure that the material collection corresponds
        to the actual list of cells.

        """
        return self.__mc

    @property
    def tallyCollection(self):
        """
        Instance of the TallyCollection class. Tallies (currently, only mesh tallies)
        can be added to the model by adding them manually to the collection.
        """
        return self.__tc

    @property
    def cellCounter(self):
        """
        The instance of the auxiliary.Counter class to enumerate cells.
        """
        return self.__cc

    @property
    def xsdir(self):
        """
        xsdir of the material collection of the model. It is used to define
        suffices in the material cards. Note that instances of Material class
        used in the description of cells can have their own xsdir objects that
        differ from the collection xsdir; the collection xsdir is always used
        to generate string representation of materials of the model.  

        """

        return self.__mc.xsdir

    @xsdir.setter
    def xsdir(self, value):
        self.__mc.xsdir = value

    @property
    def amc(self):
        """
        List of additional message cards. Each list element must be a string
        representing one message line (do not forget to put 5 spaces at the begining)

        String from this list are added to the message block after the automatically generated cards.

        >>> m = Model()
        >>> m.amc.append('     runtpe=rtp1')
        >>> m.amc.append('     srctp=__s')
        >>> print m                                # doctest: +ELLIPSIS
        MESSAGE:
             datapath=D:\MCNPDATA\jeff31
             runtpe=rtp1
             srctp=__s
        <BLANKLINE>
        c title
        ...

        """
        return self.__amc

    @property
    def acc(self):
        """
        List of additional cell cards. Each list element must be a string
        representing one cell card. 

        Strings from the list are added to the cell block after the cell cards generated automatically.

        """
        return self.__acc

    @property
    def asc(self):
        """
        List of additional surface cards. Each list element must be  a string
        representing one surface card. 

        Strings from the list are added to the surface block after the surface cards generated automatically.

        """
        return self.__asc

    @property
    def adc(self):
        """
        List of additional data cards. Each list element must be a string
        representing one data card. 

        Strings from this list are added to the data block after the material and tally cards generated automatically.

        Note, that the kcode card is treated specially, see the kcode attribute.

        """
        return self.__adc

    def _process_cells(self):
        """Add materials and surfaces of each cells to the respective collections, and assign unique ID to each cell.

        """
        self.__cc = self.__CCC() # Cell counter. 
        for c in self.__cl:
            #print 'processing cell ', c
            cid = self.__cc.get_next()
            mid = self.__mc.index(c.mat)
            if isinstance(c.vol, Volume):
                # self.__vid.append( str(c.vol.copy(self.__sc.index)._simplify()) )
                # self.__vid.append( str(c.vol.copy(self.__sc.index)) )
                vid = str(c.vol.copy(self.__sc.index)) 
            else:
                # let user define the cell geometry description
                vid = str(c.vol)
                # raise TypeError('Cell geometry must be specified by an instance of the Volume class, bu recieved ', repr(c.vol), c.vol.__class__.__name__)

            c.__cid = cid
            c.__mid = mid
            c.__vid = vid
            
    def _message_block(self):
        """
        Returns a list of strings representing the message block.
        """
        mess = ''
        datapath = self.__mc.xsdir.datapath
        filename = self.__mc.xsdir.filename
        if datapath != '':
            # dummy condition, which is allways True.
            mess += ' datapath={0}'.format(datapath)
        if filename.lower() != 'xsdir':
            mess += ' xsdir={0} '.format(filename)
        if len(mess) > 0:
            mess = 'MESSAGE: ' + mess
        return [mess] + self.__amc

    def _cell_block(self):
        """
        Returns a list of strings for the cell block. 
        
        Note that _process_cells() must be called first to assign cell IDs. 
        """
        ccards = ['c ' + self.__t] # title
        # for (cell, ID, mat, vol) in zip(self.__cl, self.__cid, self.__mid, self.__vid):
        for cell in self.__cl:
            ID = cell.__cid
            mat = cell.__mid
            vol = cell.__vid
            rho = cell.rho
            # density can be of the uncertainties.Variable class
            if hasattr(rho, 'nominal_value'):
                rho = rho.nominal_value
            elif isinstance(rho, tuple) and len(rho) == 2:
                rho = rho[0]
            ccards.append( cell.card(False).format(ID=ID, mat=mat, rho=rho, geom=vol) )
        return ccards + self.__acc

    def _surface_block(self):
        """
        Returns a list of cards for the surface block.

        Note that _process_cells() must be called first to put surfaces unsed
        in cell definitions to the collection of surfaces and thus to define
        unique surface IDs.

        """
        scards = ['c surfaces']
        scards += self.__sc.cards(formatted=False)
        scards += self.__asc
        return scards

    def _data_block(self):
        """
        Returns a list of cards for the data block.

        Note that _process_cells() must be called first to put materials used
        in cell definitios to the collection of materials, which is necessary
        to define unique material IDs.

        """
        dcards = ['c data cards']
        dcards += self.__mc.cards(formatted=False)
        dcards += self.__tc.cards(formatted=False)
        dcards += [self.__kcode.card(formatted=False)]
        
        dcards += self.__adc
        return dcards

    def cards(self, formatted=True):
        """
        Returns list of strings representing  MCNP input file.

        If optional argument formatted set to True (default),
        strings can contain the new-line characters so that the 
        lines fit to the 80-characters limit imposed by the MCNP
        input file syntax.
        """
        t1 = time.time()
        self._process_cells()
        clist = []
        clist += self._message_block()
        clist += ['']
        clist += self._cell_block()
        clist += ['']
        clist += self._surface_block()
        clist += ['']
        clist += self._data_block()
        clist += ['']
        if formatted:
            clist = map(formatter.format_card, clist)
        t2 = time.time()
        self.cards_time = t2 - t1
        return clist

    def __str__(self):
        res = self.cards()
        res += ['', '', '']
        return '\n'.join(res)

    def _filling_mats(self, u):
        """
        Returns list of materials that fill directly or indirectly the universe u.
        """
        cells = self.__cl[:]
        
        while cells:
            c = cells.pop(0)
            if c.opt.getvalue('u') == u:
                    # yield c.mat
                    if c.__mid > 0:
                        yield c.__mid
                    fill = c.opt.getvalue('fill')
                    if isinstance(fill, int):
                        filllst = [fill]
                    else:
                        filllst = fill[6:] 
                    for fill in filllst:
                        if fill not in [0, u]:
                            for mm in self._filling_mats(fill):
                                yield mm
    def _mat_matrices(self):
        """
        For all lattice cells returns the fill array with universes replaced by
        the first fuel material of that universe.

        This method is only relevant for the modified version of MCNP developed by A. Ivanov at KIT.

        """
        cells = []
        for c in self.__cl:
            if c.opt.getvalue('lat') != 0:
                fl = c.opt.getvalue('fill')
                if isinstance(fl, list):
                    cell = Cell()
                    cell.ID = c.__cid
                    cell.opt['u'] = c.opt['u']
                    cell.cmt = 'c cell {0} universe {1}\n     '.format(c.__cid, c.opt['u'])
                    newfill = '{0}:{1} {2}:{3} {4}:{5}'.format(*fl[:6])
                    fl = fl[6:]
                    for u in fl:
                        fuelmat = 0
                        for m in self._filling_mats(u):
                            if self.__mc[m][0].isfuel():
                                fuelmat = m
                                break
                        newfill += ' {0}'.format(fuelmat)
                    cell.opt['fill'] = newfill
                    cells.append(cell)
        return cells


