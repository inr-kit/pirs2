"""
Default list of colors.
"""

#: List of color names.
LST = ['aqua', 'blue', 'fuchsia', 'navy', 'olive', 'purple', 'red', 'green', 'lime', 'maroon', 'silver', 'teal', 'yellow']


def cgen(clist=LST):
    """
    Infinite generator of color names. 
    
    Returns color names in the order specified in clist, looped infinitely.
    """
    while True:
        for c in clist:
            yield c
