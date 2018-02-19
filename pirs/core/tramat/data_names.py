"""
Module contains mapping from Z number to chemical element names.
For the chemical element names, the following rules apply:

    * each name is a string of length 2. If chemical name is of length one, it
      is preceeded by space.

    * The first letter is capital. The second (if any) -- small.

There are two dictionaries defined in the module: ``name`` and ``charge``
defining mappings ``Z: name`` and ``name: Z``.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


_symbol = {
             0 : ' n',
             1 : ' H',
             2 : 'He',
             3 : 'Li',
             4 : 'Be',
             5 : ' B',
             6 : ' C',
             7 : ' N',
             8 : ' O',
             9 : ' F',
            10 : 'Ne',
            11 : 'Na',
            12 : 'Mg',
            13 : 'Al',
            14 : 'Si',
            15 : ' P',
            16 : ' S',
            17 : 'Cl',
            18 : 'Ar',
            19 : ' K',
            20 : 'Ca',
            21 : 'Sc',
            22 : 'Ti',
            23 : ' V',
            24 : 'Cr',
            25 : 'Mn',
            26 : 'Fe',
            27 : 'Co',
            28 : 'Ni',
            29 : 'Cu',
            30 : 'Zn',
            31 : 'Ga',
            32 : 'Ge',
            33 : 'As',
            34 : 'Se',
            35 : 'Br',
            36 : 'Kr',
            37 : 'Rb',
            38 : 'Sr',
            39 : ' Y',
            40 : 'Zr',
            41 : 'Nb',
            42 : 'Mo',
            43 : 'Tc',
            44 : 'Ru',
            45 : 'Rh',
            46 : 'Pd',
            47 : 'Ag',
            48 : 'Cd',
            49 : 'In',
            50 : 'Sn',
            51 : 'Sb',
            52 : 'Te',
            53 : ' I',
            54 : 'Xe',
            55 : 'Cs',
            56 : 'Ba',
            57 : 'La',
            58 : 'Ce',
            59 : 'Pr',
            60 : 'Nd',
            61 : 'Pm',
            62 : 'Sm',
            63 : 'Eu',
            64 : 'Gd',
            65 : 'Tb',
            66 : 'Dy',
            67 : 'Ho',
            68 : 'Er',
            69 : 'Tm',
            70 : 'Yb',
            71 : 'Lu',
            72 : 'Hf',
            73 : 'Ta',
            74 : ' W',
            75 : 'Re',
            76 : 'Os',
            77 : 'Ir',
            78 : 'Pt',
            79 : 'Au',
            80 : 'Hg',
            81 : 'Tl',
            82 : 'Pb',
            83 : 'Bi',
            84 : 'Po',
            85 : 'At',
            86 : 'Rn',
            87 : 'Fr',
            88 : 'Ra',
            89 : 'Ac',
            90 : 'Th',
            91 : 'Pa',
            92 : ' U',
            93 : 'Np',
            94 : 'Pu',
            95 : 'Am',
            96 : 'Cm',
            97 : 'Bk',
            98 : 'Cf',
            99 : 'Es',
           100 : 'Fm',
           101 : 'Md',
           102 : 'No',
           103 : 'Lr',
           104 : 'Rf',
           105 : 'Db',
           106 : 'Sg',
           107 : 'Bh',
           108 : 'Hs',
           109 : 'Mt',
           110 : 'Ds',
           111 : 'Rg',
           112 : 'Cn'}

z = {}
for (k,v) in _symbol.items():
    z[v] = k

# Dictionary Z: name
name = _symbol

# Dictionary name: Z
charge = z

def str2ZAI(name):
    """
    Returns (Z, A, I) tuple for the nuclide name specified in the form ``%s-%i[m[I]]``
    """
    # ID must be of the form %s-%i[m]
    n, a = name.split('-')

    # convert a to A:
    a = a.lower()
    I = 0 # isomeric state
    if a == 'nat':
        a = 0 
    elif 'm' in a:
        a, I = a.split('m')
        if I == '':
            I = 1
        else:
            I = int(I)
    a = int(a)

    n = n.strip()
    if len(n) == 1:
        # ensure that capital letters are used
        n =  ' ' + n.upper()
    elif len(n) == 2:
        n = n[0].upper() + n[1].lower()
    else:
        raise ValueError('Wrong chemical name ', n)
    z = charge[n]
    return (z, a, I)

def ZAID2ZAI(ZAID):
    """
    Returns (Z, A, I) tuple for the nuclide specified by its ZAID.

    Rules to construct ZAIDs for isomeric states are from 
    https://www.oecd-nea.org/dbprog/RPSD2008-endf70-paper2.pdf ::

        if I < 1:
            ZAID = Z*1000 + A 
        else:
            ZAID = Z*1000 + (A + 300) + I*100

    """
    z = ZAID / 1000
    a = ZAID % 1000

    I = 0
    if   (z, a) == (95, 242):
        I = 1
    elif (z, a) == (95, 642):
        I = 0
        a = 242
    elif a > 400:
        aa = a - 300
        az = z * 2 # estimate for a
        for I in range(1, 10):
            aa = aa - I * 100
            if abs(aa - az) < 90:
                break
        a = aa
    return (z, a, I)

def zai(ID):
    """
    Returns a tuple (Z, A, I), where I is the isomeric state. 
    """
    if isinstance(ID, str):
        z, a, I = str2ZAI(ID)
    elif isinstance(ID, int):
        z, a, I = ZAID2ZAI(ID)
    else:
        try:
            # assume ID is an iterable
            z, a, I = ID
        except TypeError:
            raise ValueError('Unknown nuclide ID: ', ID)

    return (z, a, I)


def ZAI2ZAID(z, a, i):
    """Inverse function to ``ZAID2ZAI``
    """
    if (z, a, i) == (95, 242, 0):
        zaid = 95642
    elif (z, a, i) == (95, 242, 1):
        zaid = 95242
    else:
        zaid = z*1000 + a
        if i > 0:
            zaid += 300 + i*100
    return zaid


                        
                        
                    
        
        
        

