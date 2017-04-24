from hmcnp3 import mi
# additional cell cards
mi.acc.append('c commented cell card')

# additional surface cards
mi.asc.append('c commented surface card')

# additional data cards
ksrc = 'ksrc '
for v in mi.gm.values(True):
    if v.material == 'fuel':
        x, y, z = v.abspos().car
        ksrc += '  {0} {1} {2}'.format(x, y, z-v.Z*0.49)
        ksrc += '  {0} {1} {2}'.format(x, y, z)
        ksrc += '  {0} {1} {2}'.format(x, y, z+v.Z*0.49)
mi.adc.append(ksrc)

# kcode card
mi.kcode.active = True # otherwise commented
mi.kcode.Nh = 1000 # histories per cycle
mi.kcode.Ncs = 20 # cycles to skip
mi.kcode.Nct = 100 # total num of cycles

if __name__ == '__main__':
    mi.wp.prefix = 'm4_'
    mi.run('P')

