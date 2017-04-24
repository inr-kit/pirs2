from pin_mcnp import MI
from a_model import a 

MI.gm = a
MI.bc['key'] = () # empty tuple means the model itself. 

MI.kcode.Nh = 5000
MI.kcode.Nct = 100
MI.kcode.Ncs = 30

# setup prdmp to dump only each 30 cycles:
for i, c in enumerate(MI.adc):
    if 'prdmp' in c:
        MI.adc[i] = 'prdmp j 30 1'



if __name__ == '__main__':
    from rod_models import pp
    plst = []
    for e in MI.gm.values():
        if e.name == 'fuel':
            p = e.abspos()
            plst.append(p)
    ksrc = 'ksrc ' + ''.join(map(lambda p: ' {} {} {}'.format(*p.car), plst))
    MI.adc[-1] = ksrc 
    print 'ksrc computed'

    MI.kcode.Nh = 10000
    MI.kcode.Nct = 250
    MI.kcode.Ncs = 30

    a = MI.run('r', tasks=3)

    from pirs.tools.plots import colormap
    az = colormap(a, plane={'z':0})
    ay = colormap(a, plane={'y':0}, aspect='auto')
    ax = colormap(a, plane={'x':0}, aspect='auto')

    az.get_figure().savefig('a_model_z.pdf')
    ay.get_figure().savefig('a_model_y.pdf')
    ax.get_figure().savefig('a_model_x.pdf')

    azh = colormap(a, plane={'z':0}, var='heat')
    axh = colormap(a, plane={'x':0}, var='heat', aspect='auto')

    azh.get_figure().savefig('a_heat_z.pdf')
    axh.get_figure().savefig('a_heat_x.pdf')

