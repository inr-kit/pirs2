Here we loop over three values of N. 
For each N, the main template is 
processed and the result is written
into a file. All this is done in the
following snippet: 
'
for N in ["V1", "V2", "V3"]:
    f = open( "input_"+N, "w")
    f.write(pre_pro("main.t"))
    f.close()
'

