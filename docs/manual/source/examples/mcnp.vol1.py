from pirs.mcnp import Volume

v1 = Volume(1, 'a')  
v2 = Volume(1, 'b')
v3 = Volume(-1, 'c')

# new volume as intersection and union
r = v1 & v2 | v3

# string representation of volume
print ' r: ', r
print '-r:', -r

# surface definition substitution
s = {}
s['a'] = 1
s['b'] = 2
s['c'] = 3

print ' r: ',  r.copy(s)
print '-r: ', -r.copy(s)


