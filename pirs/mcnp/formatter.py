"""
Functions to wrap long lines.

Rationale is to wrap string representation of MCNP input file cards to fit to
80 characters allowed by MCNP5 input file format.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


def format_card(string, maxLen=80, indent=' '*5, eol='$', cl='c ', propagate_comments=True):
    """Wrap lines from string to fit to maxLen characters.

    Returns a multi-line string where lines from `string` are wrapped to be
    shorter than specified by `maxLen`. Continuation lines denoted by
    indentation `indent`.

    The `string` can contain comments. Character that comments the whole line
    is given by `cl` optional argument, and the comment part of line is denoted
    by `eol` optional argument.
    
    Optional boolean argument `propagate_comments` specifies whether in the output multiline string the 
    first line will contain comment specified in the original string.
    """

    lind = len(indent)
    res = []
    for line in string.splitlines():
        if line[:lind].lstrip().lower().find(cl) == 0:
            # this line is commented out. Put it as is
            if propagate_comments:
                res.append(line)
        else:
            if line[:lind] == indent:
                meaning, c, comment = line[lind:].partition(eol)
                prefix = indent  
            else:
                meaning, c, comment = line.partition(eol)
                prefix = ''

            assert meaning.find('&') == -1
            meaning = meaning.strip()
            while meaning:
                if len(prefix) + len(meaning) <= maxLen:
                    res.append(prefix + meaning)
                    meaning = ''
                else:
                    idx = meaning.rfind(' ', 0, maxLen - len(prefix))
                    if idx == -1:
                        # space not found in first maxLen characters. Put the whole line as is.
                        part = meaning
                        meaning = ''
                    else:
                        part = meaning[:idx]
                        meaning = meaning[idx:].lstrip()
                    res.append( prefix + part )
                prefix = indent
            if comment.strip() != '' and propagate_comments:
                last = res[-1]
                res[-1] = last + ' '*(maxLen - len(last) + 2) + eol + ' ' + comment
    return '\n'.join(res)

        



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    s = 'this can happen if the datapath is too long: datapath = /an_extremely_long_directory_name_exceeding_by_far_the_limit_of_eighty_characters_imposed_by_MCNP_input_syntax'
