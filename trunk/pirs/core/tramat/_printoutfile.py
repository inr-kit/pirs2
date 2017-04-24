"""
The functinality, provided with this module was 'copied' from the original fortran code tramat.

In the fortran implementation, it was necessary to simplify management of output files, where 
info about materials and nuclides was printed out.

In the python implementation this functionalyity is not needed any more, therefore, this
module is not used.

"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at

class _PrintOutFilesClass:
    """
    Internal class that describes (only one) object -- dictionary of files where
    print out will be done. This object has a special method of writing to a file:
    if specified file does not exist, it is opened first, see print method.

    Files for printing out enter as input parameter of methods of several classes.
    Therefore they do not belong to a class of nuclide, element or material, but
    must comprise a stand-alone class (or object). This class or object must have a
    method to open file, if not opened before.
    """
    def __init__(self):
        """
        Each instance has a dictionary. If a print-out into a new file (i.e.  which is
        not in the dictionary yet) is required, the file is opened and added to this
        dictionary with its name as the key.
        """
        self.opened_files = {} 

    def _write(self, fname='', string='', prefix='-'*80+'\n'):
        """
        Prints string prefixed with prefix into file fname. The default fname is empty
        string, which means to print to standard output.

        The method first checks whether fname allready in the dictionary. If not, the
        file is initialized for writing and is appended to the dictionary.

        In this way the following functionalyty is obtained: If a file is mentioned in
        a programm for the first time, it is first emptied.  If a file was allready
        used in the program, it is just appended. So, all files mentioned in the
        program contain output only from this program.
        """
        if fname == '':
            print prefix
            print string
        else:    
            if fname not in self.opened_files.keys():
                self.opened_files[fname] = open(fname, 'w')
            self.opened_files[fname].write(prefix)
            self.opened_files[fname].write(string)

