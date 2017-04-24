from pirs.solids import Box, Cylinder

# surrounding water
b = Box(material='water')
b.X = 1.26
b.Y = b.X
b.Z = 400

# clad
c = Cylinder(material='steel')
c.R = 0.4583
c.Z = 360

# fuel 
f = Cylinder(material='fuel')
f.R = 0.3951
f.Z = 350

# construct model
b.insert(c)    # put clad into box
c.insert(f)    # put fuel into clad
c.pos.y = 0.1  # shift clad with resp. to container

if __name__ == '__main__':
    from pirs.tools.plots import colormap
    colormap(b, {'z':0}, filename='ex2z.pdf')
    colormap(b, {'x':0}, filename='ex2x.pdf', aspect='auto')

