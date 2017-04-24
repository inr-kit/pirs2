from pirs.tools import LoadMap as Map
core_map = Map()

# burnup steps are taken from NEA PWR benchmark material specs:
# 0: 0.0
# 1: 0.15
# 2: 17.5
# 3: 20.0
# 4: 22.5
# 5: 32.5
# 6: 35.0
# 7: 37.5
core_map.string = """
    $6
    $     0     1     2     3     4     5     6     7     8
      u42_6 u42_1 u42_4 u45_1 u45_7 m43_2 u45_1 u42_5 rrrrr rrrrr
      u42_1 u42_2 u45_5 m40_4 u42_1 u42_5 m40_1 u45_2 rrrrr rrrrr
      u42_4 u45_5 u42_4 u42_1 u42_4 m43_2 u45_1 m43_6 rrrrr rrrrr
      u45_1 m40_4 u42_1 m40_7 u42_1 u45_3 m43_1 u45_3 rrrrr rrrrr
      u45_7 u42_1 u42_4 u42_1 u42_7 u45_1 u42_2 rrrrr rrrrr rrrrr
      m43_2 u42_5 m43_2 u45_3 u45_1 m43_1 u45_5 rrrrr rrrrr
      u45_1 m40_1 u45_1 m43_1 u42_2 u45_5 rrrrr rrrrr
      u42_5 u45_2 m43_6 u45_3 rrrrr rrrrr rrrrr
      rrrrr rrrrr rrrrr rrrrr rrrrr rrrrr
      rrrrr rrrrr rrrrr rrrrr rrrrr
"""
core_map.origin = (9, 0)
core_map.rdict['rrrrr'] = '_'
core_map.default = '_'
# core_map._all_items = 'rrrr'


uox_map = Map()
uox_map.string = """
    $3
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i 
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u 
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u 
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u 
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u 
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u 
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
      u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u 
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u 
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u 
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u 
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u 
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u 
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u 
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i 
    """
uox_map.origin = uox_map.tindex('g')
# uox_map.rdict['i'] = 'u'
uox_map.rdict['g'] = 'c'


mox_map = Map()
mox_map.string = """
    $3
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1 
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1 
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2 
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2 
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2 
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2 
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m3 m2 
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1 
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1 
    """
mox_map.origin = mox_map.tindex('g')
mox_map.rdict['g'] = 'c'

ref_map = Map()
ref_map.string = """
    $3
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  R  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
      r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r  r
    """
ref_map.origin = ref_map.tindex('R')
ref_map.rdict['R'] = 'r'
ref_map.default = 'r'

emp_map = Map()
emp_map.string = """
    $3
    """


if __name__ == '__main__':
    print core_map.string
    print uox_map.string
    print mox_map.string
    print ref_map.string



