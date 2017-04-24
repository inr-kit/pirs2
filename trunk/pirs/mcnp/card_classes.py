"""
Classes to represent some MCNP input cards.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at


from . import formatter

class KcodeCard(object):
    """Representation of kcode card.
    """

    def __init__(self):
        self.__nsh = 500 # number of source histories
        self.__rkk = 1.  # initial Keff guess
        self.__ncs = 20  # number of cycles to be skipped
        self.__nct = 100 # total number of cycles
        self.__MSRK = 'j'
        self.__KNRM = 'j'
        # it seems that mrkp is hardcoded and is not changed even 
        # if specified in the kcode card. Thus, nct should not 
        # 6500 (this value specified on p. 3-77 of the manual.
        self.__MRKP = int(1e5) # needed to continue runs.
        self.__KC8 = 'j'

        # active card or not?
        self.__active = ''
        return

    @property
    def active(self):
        """
        Boolean. If False, the card is commented out.
        """
        return self.__active == 'c'

    @active.setter
    def active(self, value):
        if value:
            self.__active = ''
        else:
            self.__active = 'c'
        return

    @property
    def Nh(self):
        """
        Number of histories in a cycle
        """
        return self.__nsh

    @Nh.setter
    def Nh(self, value):
        self.__nsh = int(value)


    @property
    def Ncs(self):
        """
        Number of cycles to skip
        """
        return self.__ncs

    @Ncs.setter
    def Ncs(self, value):
        self.__ncs = int(value)

    @property
    def Nct(self):
        """
        Number of cycles, total (i.e. number of active cycles is Nct - Ncs)
        """
        return self.__nct

    @Nct.setter
    def Nct(self, value):
        self.__nct = int(value)

    def card(self, formatted=True):
        """
        String representing the card in the input file.
        """
        res = '{0} kcode'.format(self.__active)
        args = [self.__nsh, self.__rkk, self.__ncs, self.__nct, self.__MSRK, self.__KNRM, self.__MRKP, self.__KC8]
        for arg in args:
            if isinstance(arg, int) or isinstance(arg, float):
                res += ' {0} '.format(arg)
            else:
                res += ' j '

        if formatted:
            res = formatter.format_card(res) #### multiline(res)
        return res

    def __str__(self):
        return self.card(True)



