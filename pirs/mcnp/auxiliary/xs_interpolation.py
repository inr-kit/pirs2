"""
Function(s) to represent doppler broading temperature by mixing two other temperatures.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

import warnings


def sqrT(T, T1, T2, rtol=0.1):
    """Returns fractions of XS at temperatures T1 and T2 to represent temperature T.

    Computes fractions of cross-sections at T1 and T2 to represent temperature
    T using the square-root temperature interpolation. T, T1 and T2 must be
    given in absolute units (Kelvin or MeV, for example). 

    Returns a tuple (f1, f2), where f1 and f2 are fractions of cross-sections
    at T1 and T2, respectively.

    Optional argument ``rtol`` is used to specify distance from T1 or T2, at which
    interpolation takes place.  For example, if T is close to T1, i.e. when ::
    
        |T-T1| < |T1-T2|*rtol,
        
    interpolation is not done, tuple (1.0, 0.0) is returned. In
    this way one can exclude interpolation, when T differs from existing
    temperatures T1 or T2 only negligibly.


    >>> sqrT(350, 300, 400)   #doctest: +ELLIPSIS
    (0.48207..., 0.5179...)
    >>> sqrT(350, 400, 300)   #doctest: +ELLIPSIS
    (0.5179..., 0.48207...)
    >>> sqrT(300, 300, 400)   #doctest: +ELLIPSIS
    (1.0, 0.0)
    >>> sqrT(400, 300, 400)   #doctest: +ELLIPSIS
    (0.0, 1.0)

    Fractions f1 and f2 are defined from the following equations::

        (1)  sigma(T) = sigma(T1)*f1  +  sigma(T2)*f2     # this is how cross-sections can be mixed in MCNP 
        (2)  sigma(T) is proportional to T^1/2            # see van der Marck, Meulekamp, Hogenbirk, M&C2005
        (3)  f1 + f2 = 1                                  # this is how nuclide fractions normed in MCNP material. 

    from this equaitons, given T, T1 and T2, one can express f1 and f2::

        (4)   f1 = (T^1/2 - T2^1/2) / (T1^1/2 - T2^1/2)
        (5)   f2 = 1. - f1

    """
    # explicitly go to float
    # t = float(T)
    # t1 = float(T1)
    # t2 = float(T2)
    #! float cannot be upplied to uncertainties.Variable class
    t = T
    t1 = T1
    t2 = T2

    # if T is close to T1 or T2, treat in special way:
    dTmin = abs(t1-t2) * rtol
    if abs(t-t1) < dTmin:
        return (1.0, 0.0)
    if abs(t-t2) < dTmin:
        return (0.0, 1.0)
    # if T is somewhere in between T1 and T2:
    if (t1 < t < t2) or (t2 < t < t1):
        s2 = t2**0.5
        f1 = (t**0.5 - s2) / (t1**0.5 - s2)
        f2 = 1. - f1
        return (f1, f2)
    else:
        # if T is outside the interval (T1, T2), issue a warning and use the
        # closest T, without interpolation
        if abs(t-t1) < abs(t-t2):
            return (1.0, 0.0)
        else:
            return (0.0, 1.0)



def linT(T, T1, T2):
    """
    Similar to sqrT(), but uses linear interpolation.

    >>> linT(310, 300, 400)   #doctest: +ELLIPSIS
    (0.9, 0.0999...)
    >>> linT(300, 300, 400)
    (1.0, 0.0)
    >>> linT(400, 300, 400)
    (0.0, 1.0)
    >>> linT(310, 400, 300)
    (0.1, 0.9)
    """
    # explicitly go to float
    # t = float(T)
    # t1 = float(T1)
    # t2 = float(T2)
    #! float cannot be upplied to uncertainties.Variable class
    t = T
    t1 = T1
    t2 = T2

    if (t1 <= t <= t2) or (t2 <= t <= t1):
        f1 = (t - t2) / (t1 - t2)
        f2 = 1. - f1
        return (f1, f2)
    else:
        # if T is outside the interval (T1, T2), issue a warning and use the
        # closest T, without interpolation
        if abs(t-t1) < abs(t-t2):
            return (1.0, 0.0)
        else:
            return (0.0, 1.0)


