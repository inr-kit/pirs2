c ''
A snippet to put the content of the
external file "incl.txt" into the 
resulting file. For details see 
description of the open() Python 
function. '
    print
    for l in open("incl.txt", "r"):
        print l,'        

Or as one-liner:
'print; print open("incl.txt").read()'
