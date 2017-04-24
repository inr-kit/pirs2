from pirs.core.scheduler import InputFile, WorkPlace

# MCNP input file
i1 = InputFile()
i1.basename = 'inp'
i1.string = 'c input file'

# Srctp from previous run
i2 = InputFile()
i2.basename = 'srctp2'
i2.exfile = './srctp1'

# shell script to start MCNP
i3 = InputFile()
i3.basename = 'start.sh'
i3.string = '$MCNP inp=inp srctp=srctp2'
i3.executable = True

# workplace
w = WorkPlace()
w.suffix = 'wp'
w.files.append(i1)
w.files.append(i2)
w.files.append(i3)

w.prepare()
print w.report
out = w.run(sec=1)
print out
