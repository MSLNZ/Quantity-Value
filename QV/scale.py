from __future__ import division 
import numbers 
 
__all__ = ( 'Scale', 'Unit', )

#----------------------------------------------------------------------------
class Scale(object):

    """
    Measured values of a quantity are reported on a scale.  
    For example, the SI scale for length measurement is the metre.   
        
    A Scale object has a name (and a short name, or term) 
    and contains a reference to the associated kind of quantity.
    """
    
    def __init__(self,kind_of_quantity,name,term):
        self._kind_of_quantity = kind_of_quantity
        self._name = str(name)
        self._term = str(term)

    def __repr__(self):
        return "{!s}({!r},{!r},{!r})".format(
            self.__class__.__name__,
            self.kind_of_quantity,
            self._name,
            self._term
        )
        
    # __hash__ and __eq__ are required for mapping keys
    def __hash__(self):
        return hash( ( self._name, self._term ) )
        
    def __eq__(self,other):
        return (
            self._name == other.name 
        and 
            self._term == other.term 
        ) 
        
    def __str__(self):
        return self._term
        
    @property 
    def name(self):
        """The quantity name"""
        return self._name
        
    @property 
    def term(self):
        """Short name for the quantity"""
        return self._term
        
    @property 
    def kind_of_quantity(self):
        """The associated kind of quantity"""
        return self._kind_of_quantity
  
#----------------------------------------------------------------------------
# A Scale (correctly) does not refer to a register, but the implementation 
# of Unit would be awkward without such a reference. Unit is therefore 
# really part of the implementation of the UnitRegister. 
class Unit(object):

    """
    A Unit class implements the behaviour of a measurement scale. 
    
    A :class:`Unit` is associated with a :class:`Scale` and with a :class:`.UnitRegister`. 
    
    Multiplication and division of units is supported. 
    
    The 'floor' division operator supports retention of 
    information about the dimensions of 'dimensionless' quantities 
    (ratios of the same kind of quantity). 
    
    """

    def __init__(self,kind_of_quantity,name,term,register,multiplier):
        self._scale = Scale(kind_of_quantity,name,term)
        self._kind_of_quantity = self._scale.kind_of_quantity
        self._register = register
        self._multiplier = multiplier   
        
    # Units for the same kind of quantity can have different multipliers. 
    # A unit with multiplier of unity is the reference unit.
    # It is perhaps better to hold the multipliers in the unit register?
    
    @property 
    def scale(self):
        """The unit scale"""
        return self._scale 

    @property 
    def kind_of_quantity(self): 
        """The associated kind of quantity"""
        return self._kind_of_quantity

    @property 
    def multiplier(self):
        try:
            return self._multiplier
        except AttributeError:
            return 1 

    @property 
    def is_dimensionless(self):
        """True when the associated kind of quantity is dimensionless in the current context"""
        context = self.register.context 
        return context.dimensions( self.kind_of_quantity ).is_dimensionless

        
    def is_ratio_of(self,other_koq):
        """
        True when the kind of quantity of ``self`` is a dimensionless 
        ratio and the dimensions of the kind of quantity of ``other_koq``
        match the numerator dimensions of the kind of quantity of ``self``.
        
        """
        context = self.register.context 
        lhs = context.dimensions( self.kind_of_quantity )
        rhs = context.dimensions( other_koq )
        
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
            self.scale.term,
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

    def __pow__(self,rhs):
        assert isinstance(rhs,numbers.Real),\
            "A real exponent is required"
        
        # work in progress!
        return NotImplemented
  
    # def ratio(self,rhs):
        # return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

    # def reference_unit(self):
        # """
        # Return the reference unit

        # There can be only one reference unit in a register for each 
        # kind of quantity, but there can be many other related units,
        # which are multiples of the reference.
        
        # """
        # return self.register.reference_unit_for( self.kind_of_quantity ) 

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

    # def reference_unit(self):
        # return self.register.reference_unit_for( self.kind_of_quantity ) 
    
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

    # def reference_unit(self):
        # return self.register.reference_unit_for( self.kind_of_quantity ) 

#----------------------------------------------------------------------------
#
# Operations implement manipulations of multipliers and kinds
# of quantity simultaneously. 
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
           
    @property 
    def kind_of_quantity(self):  
        return self.arg.kind_of_quantity._simplify()
        
    @property 
    def multiplier(self):
        return self.arg.multiplier

#----------------------------------------------------------------------------
class Ratio(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def __repr__(self):
        return "({!r}//{!r})".format(self.lhs,self.rhs)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "({!s}//{!s})".format(self.lhs,self.rhs)
           
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity // self.rhs.kind_of_quantity
        
    @property 
    def multiplier(self):
        return self.lhs.multiplier / self.rhs.multiplier

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
        
    @property 
    def multiplier(self):
        return self.lhs.multiplier * self.rhs.multiplier
        
#----------------------------------------------------------------------------
class Div(BinaryOp):   

    def __init__(self,lhs,rhs):
        super(Div,self).__init__(lhs,rhs) 

    def __repr__(self):
        return "({!r})/({!r})".format(self.lhs,self.rhs)

    def __str__(self):
        # TODO: need to treat a numeric as a special case
        return "({!s})/({!s})".format(self.lhs,self.rhs)
    
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity / self.rhs.kind_of_quantity

    @property 
    def multiplier(self):
        return self.lhs.multiplier / self.rhs.multiplier

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )