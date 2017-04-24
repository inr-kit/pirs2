from pirs.core.scheduler import WorkPlace

w = WorkPlace()
w.prefix = 'wp'

# create directory
w.prepare()
print w.report

# create another directory,
# do not interfere with previously 
# created
w.prepare()
print w.report


