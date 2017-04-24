from ..mcnp.auxiliary.counters import Collection
class RodMaterial(object):
    """
    Container for data necessary for the tables describing rod material properties.

    Physical units are those used in SCF.
    """
    def __init__(self):
        # fuel properties
        self.fp = 'uo2' # fuel property
        self.fc = 0.0   # fuel_conductivity
        self.fsh = 0.0  # fuel_specific_heat
        self.fD = 0.0 # fuel_density
        self.fe = 0.0 # fuel_emissivity
        self.fte = 0.0 # fuel_thermal_expansion
        self.fd = -1 # fuel_diameter
        self.fir = 0.0 # fuel_inner_radius
        self.ftd = 1.0 # fraction_of_theoretical_density
        self.fop = 0.0 # fraction_of_puo2
        self.fr = 3e-6 # fuel_roughness

        # clad and gap properties
        self.cp = 'zircaloy' # clad property
        self.cc = 0.0 # clad_conductivity
        self.csh = 0.0 # clad_specific_heat
        self.cd = 0.0 # clad_density
        self.ce = 0.0 # clad_emissivity
        self.cte = 0.0 # clad_thermal_expansion
        self.ct = -1 # clad_thickness
        self.gc = 1e5 # gap conductance
        self.fg = 'off' # fill_gap
        self.mg = 'off' # model_gap
        self.cr = 1e-6 # clad_roughness
        self.fgp = 5e5 # fill_gas_pressure
        self.fgv = 6e-6 # fill_gas_volume
        
    def update(self, othr, part='all'):
        """
        Update properties of the RodMaterial instance by the values stored in othr.

        part: 'all' -- all properties will be updated
              'fuel' -- only fuel-related properties will be updated
              'clad' -- only clad-related properties will be updated
              'gap' -- only gap-related properties will be updated.
        """
        if part == 'all':
            self._update_fuel(othr)
            self._update_clad(othr)
            self._update_gap(othr)
        elif part == 'fuel':
            self._update_fuel(othr)
        elif part == 'clad':
            self._update_clad(othr)
        elif part == 'gap':
            self._update_gap(othr)
        else:
            raise ValueError('Wrong argument part: {}'.format(part))

    def _update_fuel(self, othr):
        self.fp  = othr.fp  
        self.fc  = othr.fc  
        self.fsh = othr.fsh 
        self.fd  = othr.fd  
        self.fe  = othr.fe  
        self.fte = othr.fte 
        self.fd  = othr.fd  
        self.fir = othr.fir 
        self.ftd = othr.ftd 
        self.fop = othr.fop 
        self.fr  = othr.fr  

    def _update_clad(self, othr):
        self.cp  = othr.cp 
        self.cc  = othr.cc 
        self.csh = othr.csh
        self.cd  = othr.cd 
        self.ce  = othr.ce 
        self.cte = othr.cte
        self.ct  = othr.ct 
        self.cr  = othr.cr 


    def _update_gap(self, othr):
        self.gc  = othr.gc 
        self.fg  = othr.fg 
        self.mg  = othr.mg 
        self.fgp = othr.fgp
        self.fgv = othr.fgv

    def copy(self):
        new = self.__class__()

        new.fp  = self.fp 
        new.fc  = self.fc 
        new.fsh = self.fsh
        new.fD  = self.fD 
        new.fe  = self.fe 
        new.fte = self.fte
        new.fd  = self.fd 
        new.fir = self.fir
        new.ftd = self.ftd
        new.fop = self.fop
        new.fr  = self.fr 
                 
        new.cp  = self.cp 
        new.cc  = self.cc 
        new.csh = self.csh
        new.cd  = self.cd 
        new.ce  = self.ce 
        new.cte = self.cte
        new.ct  = self.ct 
        new.gc  = self.gc 
        new.fg  = self.fg 
        new.mg  = self.mg 
        new.cr  = self.cr 
        new.fgp = self.fgp
        new.fgv = self.fgv
        return new

    def __str__(self):
        atrl = ['fp', 
                'fc', 
                'fsh', 
                'fD', 
                'fe', 
                'fte', 
                'fd', 
                'fir', 
                'ftd', 
                'fop', 
                'fr', 
                'cp', 
                'cc', 
                'csh', 
                'cd', 
                'ce', 
                'cte', 
                'ct', 
                'gc', 
                'fg', 
                'mg', 
                'cr', 
                'fgp', 
                'fgv']
        res = ''
        for a in atrl:
            res += '{} = {}\n'.format(a, getattr(self, a))
        return res[:-1]
        

    def __eq__(self, othr):
        s = [
            self.fp ,
            self.fc ,
            self.fsh,
            self.fD ,
            self.fe ,
            self.fte,
            self.fd ,
            self.fir,
            self.ftd,
            self.fop,
            self.fr ,
            self.cp ,
            self.cc ,
            self.csh,
            self.cd ,
            self.ce ,
            self.cte,
            self.ct ,
            self.gc ,
            self.fg ,
            self.mg ,
            self.cr ,
            self.fgp,
            self.fgv]

        o = [
            othr.fp ,
            othr.fc ,
            othr.fsh,
            othr.fD ,
            othr.fe ,
            othr.fte,
            othr.fd ,
            othr.fir,
            othr.ftd,
            othr.fop,
            othr.fr ,
            othr.cp ,
            othr.cc ,
            othr.csh,
            othr.cd ,
            othr.ce ,
            othr.cte,
            othr.ct ,
            othr.gc ,
            othr.fg ,
            othr.mg ,
            othr.cr ,
            othr.fgp,
            othr.fgv]
        for (sp, op) in zip(s, o):
            if sp != op:
                return False
        return True

    def __neq__(self, othr):
        return not self.__eq__(othr)
        

class RodMaterialCollection(Collection):
    """
    Collection of rod materials.
    """
    def add(self, mat):
        self.index(mat)
        return

    def index(self, mat):
        if isinstance(mat, int):
            if mat in self.keys():
                return mat
            else:
                raise IndexError('Collection has no element with index {}'.format(mat))
        k = self._find(mat)
        if k is None:
            k = self._add(mat)
        return k

