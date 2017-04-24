from pirs.mcnp import Surface

c = Surface('rcc 0 0 0   0 0 10  4')

# mapping surface -> ID
l = []
for f in c.facets():
    l.append(f.a1[1])
m = lambda s: l.index(s) + 1

# macrobody exterior defined by simple surfaces
v = c.volume(m)
print ' c cells'
print '1 0 ',  v, ' $ cylinder exterior'
print '2 0 ', -v, ' $ cylinder interior'

print ''
print 'c surfaces:'
for s in l:
    print str(s).format(m(s))
