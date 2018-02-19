"""
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

Customization of the uncertainties.Variable class.

Instances of the original class (see http://pythonhosted.org/uncertainties/)
do not permit the float() type transform. To get the nominal value one should
use the nominal_value attribute.

In the customization, the float() type transformation is allowed. It returns the
nominal value.
"""

# this is a copy-paste of the original function, except part disabling conversions to 
# float, int, etc., is commented out.
def add_operators_to_AffineScalarFunc_customized():
    """
    Adds many operators (__add__, etc.) to the AffineScalarFunc class.
    """
    
    ########################################

    #! Derivatives are set to return floats.  For one thing,
    # uncertainties generally involve floats, as they are based on
    # small variations of the parameters.  It is also better to
    # protect the user from unexpected integer result that behave
    # badly with the division.

    ## Operators that return a numerical value:

    # Single-argument operators that should be adapted from floats to
    # AffineScalarFunc objects, associated to their derivative:
    simple_numerical_operators_derivatives = {
        'abs': lambda x: 1. if x>=0 else -1.,
        'neg': lambda x: -1.,
        'pos': lambda x: 1.,
        'trunc': lambda x: 0.
        }

    for (op, derivative) in (
          simple_numerical_operators_derivatives.iteritems()):
        
        attribute_name = "__%s__" % op
        # float objects don't exactly have the same attributes between
        # different versions of Python (for instance, __trunc__ was
        # introduced with Python 2.6):
        try:
            setattr(AffineScalarFunc, attribute_name,
                    wrap(getattr(float, attribute_name),
                                 [derivative]))
        except AttributeError:
            pass
        else:
            _modified_operators.append(op)
            
    ########################################

    # Reversed versions (useful for float*AffineScalarFunc, for instance):
    for (op, derivatives) in _ops_with_reflection.iteritems():
        attribute_name = '__%s__' % op
        # float objects don't exactly have the same attributes between
        # different versions of Python (for instance, __div__ and
        # __rdiv__ were removed, in Python 3):
        try:
            setattr(AffineScalarFunc, attribute_name,
                    wrap(getattr(float, attribute_name), derivatives))
        except AttributeError:
            pass
        else:
            _modified_ops_with_reflection.append(op)

    # ########################################
    # # Conversions to pure numbers are meaningless.  Note that the
    # # behavior of float(1j) is similar.
    # for coercion_type in ('complex', 'int', 'long', 'float'):
    #     def raise_error(self):
    #         raise TypeError("can't convert an affine function (%s)"
    #                         ' to %s; use x.nominal_value'
    #                         # In case AffineScalarFunc is sub-classed:
    #                         % (self.__class__, coercion_type))

    #     setattr(AffineScalarFunc, '__%s__' % coercion_type, raise_error)

    


from uncertainties import Variable

class Var(Variable):
    pass
    def __float__(self):
        return self.nominal_value

    def __copy__(self):
        return self.__class__(self.nominal_value, self.std_dev(), self.tag)


