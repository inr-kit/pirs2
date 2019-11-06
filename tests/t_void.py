# Check "emply" mixture as void.

from pirs.mcnp import Material

v = Material()  # This should be void. It can be added only with vol. fractions
u = Material('U')
u.dens = 18.0

uu = Material(u, (1, 3),
              v, (1, 3))

print(uu.report())

