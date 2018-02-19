A snippet to put the content of the
external file "incl.txt" into the 
resulting file. For details see 
description of the open() Python 
function. '
c     print
c     for l in open("incl.txt", "r"):
c         print l,'
1 This is the content
2 of file
3 incl.txt        

Or as one-liner:
'print; print open("incl.txt").read()'
1 This is the content
2 of file
3 incl.txt

