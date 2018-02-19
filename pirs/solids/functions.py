"""
Functions to work with solids.
"""

def max_diff(s1, s2, var, norm=abs, rel=False, filter_=None):
    """
    Returns v1, v2, key, iz
    """
    dmax = None
    for e1, e2 in zip(s1.values(True), s2.values(True)):
        if filter_ is None or filter_(e1):
            if e1.has_var(var):
                # assert e1 == e2
                m1 = e1.get_var(var)
                m2 = e2.get_var(var)
                if rel:
                    dm = (m2-m1)/m2
                else:
                    dm = (m2-m1)
                dv, z = dm.get_max(norm)
                if dmax is None or dv > dmax:
                    dmax = dv
                    kmax = e1.get_key()
                    zmax = z
    v1 = s1.get_child(kmax).get_var(var).get_value_by_coord(zmax)
    v2 = s2.get_child(kmax).get_var(var).get_value_by_coord(zmax)
    return v1, v2, dmax, kmax, zmax 

def max_err(s, var, filter_=None):
    """
    Returns v, rel.err, key, iz
    """
    dmax = None
    for e in s.values(True):
        if filter_ is None or filter_(e):
            if e.has_var(var):
                dv, z = e.get_var(var).get_max(lambda var: var.std_dev/abs(var.nominal_value))
                if dmax is None or dv > dmax:
                    dmax = dv
                    kmax = e.get_key()
                    zmax = z
    v = s.get_child(kmax).get_var(var).get_value_by_coord(zmax)
    return v, dmax, kmax, zmax 

def max_var(s, var, filter_=None):
    vmax = None
    for e in s.values(True):
        if filter_ is None or filter_(e):
            if e.has_var(var):
                v, z = e.get_var(var).get_max()
                if vmax is None or v > vmax:
                    vmax = v
                    kmax = e.get_key()
                    zmax = z
    return vmax, kmax, zmax

def has_zeroes(s, var, filter_=None):
    for e in s.values(True):
        if filter_ is None or filter_(e):
            if e.has_var(var) and e.get_var(var).has_zeroes():
                return e
    return False

