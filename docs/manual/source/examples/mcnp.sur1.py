from pirs.mcnp import Surface

s1 = Surface('px 1.0 $ a plane')
s2 = Surface('* pz 5.1')

s3 = Surface(type='c/z', plst=[0, 0, 6], cmnt='cylinder at z axis')
s4 = Surface('rcc 0 0 0  0 0 5  3')

#surface cards
for s in [s1, s2, s3, s4]:
    print s.card()

