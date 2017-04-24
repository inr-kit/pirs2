"""
Reads dump file and writes txt file with the table required in 
the benchmark.
"""
import sys
from pirs.tools import load

def _get(d, key):
    v = d.get(key, None)
    if v is None:
        v = []
        d[key] = v
    return v

for dname in sys.argv[1:]:
    dmp = load(dname)
    SI = dmp['SI']
    Wtot = SI.find('total_power')[0].value
    
    m = SI.gm

    # collect data by i, j
    data = {}
    Imin, Imax = None, None
    Jmin, Jmax = None, None
    Sh = 0.
    for e in m.children:
        i, j, k = e.ijk
        ij = (i,j) 
        if Imin is None or Imin > i:
            Imin = i
        if Imax is None or Imax < i:
            Imax = i
        if Jmin is None or Jmin > j:
            Jmin = j
        if Jmax is None or Jmax < j:
            Jmax = j
        if e.name == -1:
            # this is a cnannel.
            l = _get(data, ij)
            l.insert(0, e)
        else:
            # this can be fuel rod.
            f = list(e.heats())
            if f:
                l = _get(data, ij)
                l.append(f[0])
                Sh += sum(f[0].heat.values())



    # normalization
    Cw = Wtot/Sh

    # print out data
    tfile = open(dname.replace('.dump', '.dat'), 'w')

    for i in range(Imax+1-Imin):
        for j in range(Jmax+1-Jmin):
            l = data[(i+Imin,j+Jmin)]
            chT = l[0].temp.values() # channel temperature
            chR = l[0].dens.values() # channel density
            if len(l) > 1:
                fuT = l[1].temp.values()
                fuH = l[1].heat.values()
                mat = l[1].material
            else:
                fuH = [0.] * len(chT)
                fuT = fuH
                mat = ''
            for k in range(len(fuT)):
                print>>tfile, '{0:5d}{1:5d}{2:5d}'.format(i, j, k),
                for v in [fuT[k], chT[k], chR[k], fuH[k]*Cw]:
                    print>>tfile, '{0:17.12f}'.format(v),
                if k == 0:
                    print>>tfile, '# ', mat
                else:
                    print>>tfile
    tfile.close()

            

        
