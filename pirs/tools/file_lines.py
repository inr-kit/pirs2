"""
Functions to get particular lines of a file.
"""

def get_last_line(f, llen=200):
    """
    Return string containing the last line of file f.

    Optional argument llen specifies number of characters from the file's end
    to search the last line.

    If file f is empty, None returned.
    """
    with open(f, 'r') as ff:
        ff.seek(0, 2)
        llen = min(ff.tell(), llen)
        ff.seek(-llen, 2)
        lines = ff.readlines()
        if lines:
            return lines[-1]
        else:
            return None

