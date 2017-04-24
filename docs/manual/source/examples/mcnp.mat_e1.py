from pirs.mcnp import Material

fe = Material('Fe') # Fe chemical element with nat. occuring isotopes

for T in [300, 350 ,400]:
    fe.T = T
    print fe.card()
