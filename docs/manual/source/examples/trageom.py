from pirs.core.trageom import Vector3, pi2, pi

v1 = Vector3(car=(1, 0, 0))   # x, y, z
v2 = Vector3(cyl=(1, 0, 1))   # r, theta, z
v3 = Vector3(sph=(1, 0, 0))   # R, theta, phi

print 'rotate v1:'
print v1.car
v1.t += pi2
print v1.car

print 'stretch v2 2 times:'
print v2.car
v2.R *= 2.
print v2.car

print 'flip v3:'
print v3.car
v3.p = pi 
print v3.car
