from pirs.mcnp import Material
from pin_mcnp import MI, u, o 
from assembly_model import model


# Optionally, one can provide ksrc point
# for each fuel element:
ksrc = 'ksrc'
for e in model.values():
    if 'fuel' in e.get_key():
        x, y, z = e.abspos().car
        ksrc += '   {0} {1} {2}'.format(x, y, z)
MI.adc[-1] = ksrc

# 1

if __name__ == '__main__':
    MI.gm = model
    MI.run('P')

