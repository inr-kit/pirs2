def format_valerr(value, mark=None, fmt='{:.4f}'):
    """
    Return a string of the form 1.2345(6) representing the value
    and its absolute error.
    """
    try:
        val, rerr = value
    except (TypeError, ValueError):
        val = value
        rerr = None

    if rerr is None:
        s = fmt.format(val)
    elif rerr == 0:
        s = fmt.format(val)
    elif val == 0:
        s = '0({})'.format(val)
    else:
        aer = abs(val * rerr)  # absolute error
        # Define precision using e-formatting
        v, pre = '{:.0e}'.format(aer).split('e')  # presicion based on error
        v, prv = '{:.0e}'.format(val).split('e')  # presicion based on value
        pre = -int(pre)
        prv = -int(prv)
        pr = max((pre, prv))
        fv = u'{{:.{}f}}'.format(pr)   # value's format depends on precision
        fe = u'({:1.0f})'              # error's format -- always one digit
        s = fv.format(val)
        s += fe.format(aer * 10**pr)
        if mark and abs(val) > aer:
            s += '!'
    # s = u'``{}``'.format(s)  # .replace(u'+', u'\u00A0'))
    return s

