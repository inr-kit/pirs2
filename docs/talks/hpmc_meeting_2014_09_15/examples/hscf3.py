from pirs.scf2 import RodMaterial
from hscf2 import si

cld = RodMaterial()
cld.fp = 'benpwr'
cld.fd = -1
cld.ct = -1 
cld.cp = 'zircaloy'

si.materials['steel'] = cld
si.materials['zirc'] = cld

if __name__ == '__main__':
    si.wp.prefix = 's3_'
    si.run('R')

    from pirs.tools import dump
    dump('s3_.dump', gm=si.gm)

    from pirs.tools.plots import colormap
    fltr = lambda e: e.material not in ['zirc', 'steel']
    tz  = colormap(si.gm, plane={'z':1},     var='temp', aspect='auto')#  , filter_=fltr
    tx1 = colormap(si.gm, plane={'x':-0.63}, var='temp', aspect='auto')#  , filter_=fltr
    tx2 = colormap(si.gm, plane={'x': 0.63}, var='temp', aspect='auto')#  , filter_=fltr
    ty1 = colormap(si.gm, plane={'y':-0.63}, var='temp', aspect='auto')#  , filter_=fltr
    ty2 = colormap(si.gm, plane={'y': 0.63}, var='temp', aspect='auto')#  , filter_=fltr
    tz.get_figure().savefig('hscf3_tz.pdf')                            #                
    tx1.get_figure().savefig('hscf3_tx1.pdf')                          #  
    tx2.get_figure().savefig('hscf3_tx2.pdf')                          #  
    ty1.get_figure().savefig('hscf3_ty1.pdf')                          #  
    ty2.get_figure().savefig('hscf3_ty2.pdf')                          #                
                                                                       #                
    fltr = lambda e: e.name == -1                                      #                
    dz  = colormap(si.gm, plane={'z':1},     var='dens', aspect='auto')#  , filter_=fltr
    dx1 = colormap(si.gm, plane={'x':-0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dx2 = colormap(si.gm, plane={'x': 0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dy1 = colormap(si.gm, plane={'y':-0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dy2 = colormap(si.gm, plane={'y': 0.63}, var='dens', aspect='auto')#  , filter_=fltr
    dz.get_figure().savefig('hscf3_dz.pdf')
    dx1.get_figure().savefig('hscf3_dx1.pdf')
    dx2.get_figure().savefig('hscf3_dx2.pdf')
    dy1.get_figure().savefig('hscf3_dy1.pdf')
    dy2.get_figure().savefig('hscf3_dy2.pdf')
else:
    from pirs.tools import load
    si.gm = load('s3_.dump')['gm']


