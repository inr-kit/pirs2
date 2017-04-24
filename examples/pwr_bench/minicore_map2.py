from pirs.tools import LoadMap

m = LoadMap()
m.string = """
    $3
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  G  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u
      u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u
      u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u
      u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u
      u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u
      u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u
      i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  g  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  g m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  u  u  i  u  u  i  u  u  i  u  u  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2  u  i  c  i  i  c  i  i  c  i  i  c  i  i  c  i  u m2 m2  w m3 m3  w m3 m3  w m3 m3  w m3 m3  w m2 m2
     m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2  u  u  i  i  u  i  u  u  i  u  u  i  u  i  i  u  u m2 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m3 m2
     m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2  u  u  i  c  i  i  u  u  i  u  u  i  i  c  i  u  u m2 m3 m3  w m3 m3 m3 m3 m3 m3 m3 m3 m3  w m3 m3 m2
     m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2  u  u  u  i  i  c  i  i  c  i  i  c  i  i  u  u  u m2 m2 m3 m3 m3  w m3 m3  w m3 m3  w m3 m3 m3 m2 m2
     m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1  u  u  u  u  u  i  u  u  i  u  u  i  u  u  u  u  u m1 m2 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m3 m3 m2 m2 m1
     m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1  i  u  u  u  u  u  u  u  u  u  u  u  u  u  u  u  i m1 m1 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m2 m1 m1
"""
m.origin = m.tindex('G')
m.rdict['G'] = 'c'
m.rdict['g'] = 'c'
# m.rdict['i'] = 'u'

if __name__ == '__main__':
    print m.string
