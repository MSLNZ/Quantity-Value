from __future__ import division 

from quantity import Unit

#----------------------------------------------------------------------------
#
class ValueUnit(object):
    """
    A ValueUnit pairs a number and a unit.
    The unit must be associated with a system of units.
    Arithmetic expressions involving ValueUnit objects 
    apply the rules of quantity calculus to the associated units.
    In general, this will create a temporary object representing 
    the unit expression, which must be explicitly resolved to the 
    corresponding unit in the unit system.
    """
    __slots__ = ("value", "unit")
    
    def __init__(self,value,unit):
        self.value = value     
        self.unit = unit
        
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            'qvalue',
            self.value,
            self.unit 
        )
        
    def __str__(self):
        return "{!s} {!s}".format(
            self.value,
            self.unit 
        )
        
    def __add__(self,rhs):  
        lhs = self         
        if not lhs.unit.system is rhs.unit.system:
            raise RuntimeError("Different unit systems: {}, {}".format(
                lhs.unit.system, rhs.unit.system)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( lhs.unit.multiplier*self.value, lhs.unit.reference_unit_for() ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( rhs.unit.multiplier*rhs.value, rhs.unit.reference_unit_for() ) 
            
        if lhs.unit is rhs.unit:
            return ValueUnit( lhs.value + rhs.value, lhs.unit )
         
        if lhs.unit.kind_of_quantity is rhs.unit.kind_of_quantity:
            ml = lhs.unit.multiplier
            mr = rhs.unit.multiplier 
            if ml < mr:
                return ValueUnit( lhs.value + (mr/ml)*rhs.value, lhs.unit )
            else:
                return ValueUnit( (ml/mr)*lhs.value + rhs.value, rhs.unit )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    lhs.unit.kind_of_quantity,rhs.unit.kind_of_quantity)
            )    

    def __radd__(self,lhs):
        rhs = self
        # Can add numbers to numeric QVs
        if rhs.unit.kind_of_quantity is Numeric:
            return ValueUnit( lhs + rhs.value, rhs.unit )
        else:
            return NotImplemented
  
    def __sub__(self,rhs):
        lhs = self
        if not lhs.unit.system is rhs.unit.system:
            raise RuntimeError("Different unit systems: {}, {}".format(
                lhs.unit.system, rhs.unit.system)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( lhs.unit.multiplier*self.value, lhs.unit.reference_unit_for() ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( rhs.unit.multiplier*rhs.value, rhs.unit.reference_unit_for() ) 
        
        if lhs.unit is rhs.unit:
            return ValueUnit( lhs.value - rhs.value, lhs.unit )
            
        if lhs.unit.kind_of_quantity is rhs.unit.kind_of_quantity:
        
            ml = lhs.unit.multiplier
            mr = rhs.unit.multiplier 
            if ml < mr:
                return ValueUnit( lhs.value - (mr/ml)*rhs.value, lhs.unit )
            else:
                return ValueUnit( (ml/mr)*lhs.value - rhs.value, rhs.unit )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    lhs.unit.kind_of_quantity,rhs.unit.kind_of_quantity)
            )    
  
    def __rsub__(self,lhs):
        rhs = self
        # Can subtract numeric QVs from numbers
        if rhs.unit.kind_of_quantity is Numeric:
            return ValueUnit( lhs - rhs.value, rhs.unit )
        else:
            return NotImplemented
  
    # Multiplication, division and exponentiation create temporary ValueUnit 
    # objects that have not been resolved to a unit. 
    # These temporary objects have an interface that exposes
    # `multiplier`, `system` and `kind_of_quantity` attributes, 
    # which allow a kind_of_quantity and hence a unit to be resolved later.
    def __mul__(self,rhs):
        lhs = self
        if hasattr(rhs,'unit'):                      
            if not lhs.unit.system is rhs.unit.system:
                raise RuntimeError("operation requires the same unit system")

            return ValueUnit(lhs.value * rhs.value, lhs.unit * rhs.unit)
        else:
            # Assume that the `rhs` behaves as a number 
            return ValueUnit(
                rhs * lhs.value, 
                lhs.unit.system.unity * lhs.unit
            )
            
    def __rmul__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs * rhs.value, 
            rhs.unit.system.unity * rhs.unit
        )
            
    def __truediv__(self,rhs):
        lhs = self 
        if hasattr(rhs,'unit'):          
            if not lhs.unit.system is rhs.unit.system:
                raise RuntimeError("operation requires the same unit system")

            return ValueUnit(
                lhs.value / rhs.value,
                lhs.unit / rhs.unit
            )
            
        else:
            # Assume that the `rhs` behaves as a number 
            return ValueUnit(
                lhs.value / rhs, 
                lhs.unit / lhs.unit.system.unity 
            )
        
    def __rtruediv__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs / rhs.value, 
            rhs.unit.system.unity / rhs.unit
        )
        
    # # Python 2.x backward compatibility
    # def __div__(self,rhs):
        # return ValueUnit.__truediv__(self,rhs)
            
    # def __rdiv__(self,lhs):
        # return ValueUnit.__rtruediv__(self,lhs)
                        
    def __pow__(self,rhs):
        # work in progress!
        return NotImplemented
        
#----------------------------------------------------------------------------
def qvalue(value,unit):
    return ValueUnit(value,unit)
    
#----------------------------------------------------------------------------
def value(vu):
    try:
        return vu.value 
    except AttributeError:
        return vu 

#----------------------------------------------------------------------------
def unit(vu):
    try:
        return vu.unit 
    except AttributeError:
        # TODO: This must be interpreted as being  
        # equivalent to `unity`, the Numeric unit.
        return None 
       
#----------------------------------------------------------------------------
def result(value_unit, result_x_fn=lambda x,*arg,**kwarg:x, *arg,**kwarg):
    """
    Return a `qvalue` in which the unit has been 
    converted to the reference unit of the unit system. 
    A value result function `result_x_fn` can be supplied 
    to apply a final processing to the value.
    """
    return ValueUnit( 
        result_x_fn(
            value_unit.unit.multiplier*value_unit.value, 
            *arg, 
            **kwarg
        ), 
        value_unit.unit.reference_unit_for() 
    )
        
             

    
    
