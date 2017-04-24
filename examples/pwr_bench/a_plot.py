from sys import argv
from pirs.tools import load
from pirs.tools.plots import colormap

dmp = load(argv[1])

sres = dmp['scf_result']

x = -2.5
x = 1.2 
x=0.
z = 1.

a = {}
a['gm'] = colormap(sres, plane={'z':z}, var='material')

a['zh'] = colormap(sres, plane={'z':z}, var='heat', filter_=lambda e: e.name == 'fuel')
a['xh'] = colormap(sres, plane={'x':x}, var='heat', filter_=lambda e: e.name == 'fuel', aspect='auto')

a['zft'] = colormap(sres, plane={'z':z}, var='temp', filter_=lambda e: e.name == 'fuel')
a['zct'] = colormap(sres, plane={'z':z}, var='temp', filter_=lambda e: e.name == -1)
a['xft'] = colormap(sres, plane={'x':x}, var='temp', filter_=lambda e: e.name == 'fuel', aspect='auto')
a['xct'] = colormap(sres, plane={'x':x}, var='temp', filter_=lambda e: e.name == -1, aspect='auto')

a['zd'] = colormap(sres, plane={'z':z}, var='dens', filter_=lambda e: e.name == -1)
a['xd'] = colormap(sres, plane={'x':x}, var='dens', filter_=lambda e: e.name == -1, aspect='auto')

for (n, ax) in a.items():
    ax.get_figure().savefig(argv[1].replace('.dump', n+'.pdf'))


