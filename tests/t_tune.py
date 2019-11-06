# import logging, sys
# from autologging import TRACE
# logging.basicConfig(level=TRACE, stream=sys.stdout, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')


from pirs.core.tramat import Mixture


# Check the tune method.
m = Mixture(1001, (1, 1),
            1002, (1, 1))


def do_check(m, types, coeffs, ofg, i1, i2):
    print(m.report())
    for typ in types:
        print('******'*10)
        tmax = m.amount(typ).v
        for coef in coefs:
            tval = tmax * coef
            print('Target value:', tval, typ)
            try:
                m.tune(ofg(typ, tval), (i1, i2))
            except ValueError as e:
                if tval < 0 or tval > tmax:
                    print('Raised ValueError on an invalid target value')
                else:
                    raise e
            else:
                # This branch executed only when no expection was thrown.
                cval = m.how_much(typ, i1).v  # control value. Should be equal to target.
                assert abs(cval - tval) <= 1e-5

coefs = (-1, 0, 0.2, 0.1, 0.75, 2, 0.99)
def ofg1(typ, tval):
    def objfunc(m):
        return tval - m.how_much(typ, ZAID=1001).v
    return objfunc

do_check(m, (1, 2), coefs, ofg1, 1001, 1002)

# Tune volumetric fration
i1 = Mixture(1001)
i2 = Mixture(1002)
i1.dens = 1.0
i2.dens = 2.0
m = Mixture(i1, (1, 3), i2, (1, 3))
def ofg2(typ, tval):
    def of(m):
        return tval - m.how_much(typ, ZAID=1001).v
    return of
do_check(m, (1, 2, 3), coefs, ofg2, i1, i2)
