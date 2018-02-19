"""
Example for WorkPlace and InputFile usage.
"""

from pirs.core.scheduler import WorkPlace, InputFile

w = WorkPlace()
i = InputFile() # for input
o = InputFile() # for output
s = InputFile() # for script that produces output (in reality it starts the code)

i.string = 'Input file 1'
i.basename = 'inp'

o.basename = 'out'

s.basename = 'scr.sh'
s.string = """#!/bin/bash -l
cat inp > out
"""
s.executable = True

w.files.append(i)
w.files.append(o)
w.files.append(s)

w.prepare()
i.string = 'Input file 2'
w.prepare()
w.run()

