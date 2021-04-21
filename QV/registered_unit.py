from __future__ import division 

from QV.scale import * 
from QV.unit_register import UnitRegister

__all__ = (
    'RegisteredUnit', 
)

#----------------------------------------------------------------------------
# A Scale does not refer to a register (correctly), but the implementation 
# of units would be awkward without such a reference, hence we need this class.  
class RegisteredUnit(object):

    """
    A :class:`.RegisteredUnit` is associated with a :class:`.Scale` 
    and a :class:`.UnitRegister`. 
    
    Multiplication and division of units is delegated to the scale
    and will be checked during execution. 
    
    The 'floor' division operator supports retention of 
    information about the signature of 'dimensionless' quantities 
    (ratios of the same kind of quantity). 
    
    """

    def __init__(self,register,scale):
        self._scale = scale
        self._register = register
            
    @property 
    def scale(self):
        """The scale"""
        return self._scale 

    # @property 
    # def kind_of_quantity(self): 
        # """The kind of quantity"""
        # return self._scale._kind_of_quantity

    @property 
    def is_dimensionless(self):
        """True when the associated kind of quantity is dimensionless in the current context"""
        context = self.register.context 
        return context.signature( self.kind_of_quantity ).is_dimensionless

        
    def is_ratio_of(self,other_koq):
        """
        True when the kind of quantity of ``self`` is a dimensionless 
        ratio and the signature of the kind of quantity of ``other_koq``
        match the numerator in the signature of the kind of quantity of ``self``.
        
        """
        context = self.register.context 
        lhs = context.signature( self.kind_of_quantity )
        rhs = context.signature( other_koq )
        
        if lhs.numerator == lhs.denominator and rhs.is_simplified:
            return lhs.numerator == rhs.numerator
        else:
            return False

    @property 
    def register(self):
        """The associated unit register"""
        return self._register
        
    @register.setter
    def register(self,register):
        if self._register is None:
            self._register = register
        else:
            raise RuntimeError(
                "Unit register is assigned: {}".format(self.register)
            )
        
    def __str__(self):
        return "{!s}".format(self.scale)
        
    def __repr__(self):
        return "{!s}({!r},{!r},{!r},{!r})".format(
            self.__class__.__name__,
            self.kind_of_quantity,
            self.scale.name,
            self.scale.symbol,
            self._register
        )     

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    # def __div__(self,rhs):
        # return self.__truediv__(rhs)
        
    def __floordiv__(self,rhs):
        return Ratio(self,rhs)

    # def __pow__(self,rhs):
        # assert isinstance(rhs,numbers.Real),\
            # "A real exponent is required"
        
        # # work in progress!
        # return NotImplemented
  
    # def ratio(self,rhs):
        # return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

#----------------------------------------------------------------------------
# The following classes support simple manipulation of units by
# multiplication and division, declaring a ratio of units 
# and of simplifying a ratio of units is also supported. 
# The base classes  `UnaryOp` and `BinaryOp` establish the interface. 
# These classes provide a representation for 
# an equation involving units, but do not resolve into a unit.
#
#----------------------------------------------------------------------------
class UnaryOp(object):   

    def __init__(self,arg):
        self.arg = arg
        self._register = arg.register

    @property 
    def register(self):
        return self._register

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    # def __div__(self,rhs):
        # return self.__truediv__(rhs)
        
    def __floordiv__(self,rhs):
        return Ratio(self,rhs)

    # def ratio(self,rhs):
        # return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)
    
#----------------------------------------------------------------------------
class BinaryOp(object):   

    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs
        
        assert lhs.register is rhs.register
        self._register = lhs.register
        
    @property 
    def register(self):
        return self._register

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    # def __div__(self,rhs):
        # return self.__truediv__(rhs)
        
    def __floordiv__(self,rhs):
        return Ratio(self,rhs)

    # def ratio(self,rhs):
        # return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

#----------------------------------------------------------------------------
#
# The operations are performed simultaneously on the kinds of quantity. 
#       
#----------------------------------------------------------------------------
class Simplify(UnaryOp):

    def __init__(self,arg):
        UnaryOp.__init__(self,arg) 
        
    def __repr__(self):
        return "simplify({!r})".format(self.arg)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "simplify({!s})".format(self.arg)
           
    # Perform the operation on the quantities involved 
    @property 
    def kind_of_quantity(self):  
        return self.arg.kind_of_quantity._simplify()
        
#----------------------------------------------------------------------------
class Ratio(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def __repr__(self):
        return "({!r}//{!r})".format(self.lhs,self.rhs)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "({!s}//{!s})".format(self.lhs,self.rhs)
           
    # Perform the operation on the quantities involved 
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity // self.rhs.kind_of_quantity
 
    # Perform the operation on the scales involved 
    @property 
    def scale(self):  
        self.lhs.scale // self.rhs.scale
 
#----------------------------------------------------------------------------
class Mul(BinaryOp):   

    def __init__(self,lhs,rhs):
        super(Mul,self).__init__(lhs,rhs) 

    def __repr__(self):
        return "({!r})*({!r})".format(self.lhs,self.rhs)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "({!s})*({!s})".format(self.lhs,self.rhs)
           
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity * self.rhs.kind_of_quantity
        
    # Perform the operation on the scales involved 
    @property 
    def scale(self):  
        self.lhs.scale * self.rhs.scale
        
#----------------------------------------------------------------------------
class Div(BinaryOp):   

    def __init__(self,lhs,rhs):
        super(Div,self).__init__(lhs,rhs) 

    def __repr__(self):
        return "({!r})/({!r})".format(self.lhs,self.rhs)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "({!s})/({!s})".format(self.lhs,self.rhs)
    
    # Perform the operation on the quantities involved 
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity / self.rhs.kind_of_quantity

    # Perform the operation on the scales involved 
    @property 
    def scale(self):  
        self.lhs.scale / self.rhs.scale
        
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )