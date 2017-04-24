c ''
Example of including another template.
File "itempl.txt" is first preprocessed
and its result is inserted here:

-d'print pre_pro("itempl.txt"),'

Note that variable A defined in the 
included template is available here:
A = 'A'.

