from pirs.tools import load
from pirs.tools.plots import colormap

dmp = load('results/b_iteration_056.dump')
sr = dmp['scf_result']
mr = dmp['mcnp_result']

gm = sr.copy_tree()
gm.remove_by_criteria(name=-1)
agm = colormap(gm, plane={'z':1}, var='material')

agm.get_figure().savefig('res_model.pdf')

fltr = lambda e: e.name == 'fuel'
atx = colormap(sr, plane={'x':0}, var='temp', aspect='auto', filter_=fltr)
aty = colormap(sr, plane={'y':0}, var='temp', aspect='auto', filter_=fltr)
atx.get_figure().savefig('res_tx.pdf')
aty.get_figure().savefig('res_ty.pdf')

ahx = colormap(sr, plane={'x':0}, var='heat', aspect='auto', filter_=fltr)
ahy = colormap(sr, plane={'y':0}, var='heat', aspect='auto', filter_=fltr)
ahx.get_figure().savefig('res_hx.pdf')
ahy.get_figure().savefig('res_hy.pdf')

ahz = colormap(sr, plane={'z':1}, var='heat', filter_=fltr)
ahz.get_figure().savefig('res_hz.pdf')

fltr = lambda e: e.name == -1 
adx = colormap(sr, plane={'x':0}, var='dens', aspect='auto', filter_=fltr)
ady = colormap(sr, plane={'y':0}, var='dens', aspect='auto', filter_=fltr)
adx.get_figure().savefig('res_dx.pdf')
ady.get_figure().savefig('res_dy.pdf')
