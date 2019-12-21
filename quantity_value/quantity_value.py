#----------------------------------------------------------------------------
#
class ValueUnit(object):
    """
    A ValueUnit object pairs a number and a unit.
    The unit must be associated with a system of units.
    Arithmetic expressions involving ValueUnit objects 
    apply the rules of quantity calculus to the associated units.
    In general, this will create a temporary object representing 
    the unit expression, which must be explicitly resolved to the 
    corresponding unit in the unit system.
    """
    __slots__ = ("x", "u")
    
    def __init__(self,value,unit):
        self.x = value     
        self.u = unit
        
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            self.__class__.__name__,
            self.x,
            self.u 
        )
        
    def __str__(self):
        return "{!s} {!s}".format(
            self.x,
            self.u 
        )
        
    def __add__(self,rhs):
        unit_l = self.u
        unit_r = rhs.u
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")
            
        if unit_l is unit_r:
            return ValueUnit( self.x + rhs.x, unit_l )
         
        if unit_l._kind_of_quantity is unit_r._kind_of_quantity:
            ml = unit_l.multiplier
            mr = unit_r.multiplier 
            if ml < mr:
                return ValueUnit( self.x + (mr/ml)*rhs.x, unit_l )
            else:
                return ValueUnit( (ml/mr)*self.x + rhs.x, unit_r )
        else:
            raise RuntimeError("operation requires the same kind of quantity")    

    def __radd__(self,lhs):
        # Can add numbers to numeric QVs
        unit_r = self.u

        if unit_r.kind_of_quantity is Numeric:
            return ValueUnit( lhs + self.x, unit_r )
        else:
            raise NotImplemented
  
    def __sub__(self,rhs):
        unit_l = self.u
        unit_r = rhs.u
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")
        
        if unit_l is unit_r:
            return ValueUnit( self.x - rhs.x, unit_l )
            
        if (    unit_l.system is unit_r.system 
            and unit_l._kind_of_quantity is unit_r._kind_of_quantity
        ):
            ml = unit_l.multiplier
            mr = unit_r.multiplier 
            if ml < mr:
                return ValueUnit( self.x - (mr/ml)*rhs.x, unit_l )
            else:
                return ValueUnit( (ml/mr)*self.x - rhs.x, unit_r )
        else:
            raise RuntimeError("operation requires the same kind of quantity")    
  
    def __rsub__(self,lhs):
        # Can subtract numeric QVs from numbers
        unit_r = self.u
        if unit_r.kind_of_quantity is Numeric:
            return ValueUnit( lhs - self.x, unit_r )
        else:
            raise NotImplemented
  
    # Multiplication and division create ValueUnit 
    # objects in which the unit is a temporary 
    # object that has not not been resolved to a unit. 
    # This temporary object has an interface that exposes
    # `multiplier`, `system` and `kind_of_quantity` attributes. 
    # These allow a unit to be resolved later.
    def __mul__(self,rhs):
        unit_l = self.u
        unit_r = rhs.u
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")

        tmp = self.u * rhs.u 
        v = self.x * rhs.x 
        
        return ValueUnit(v,tmp)
            
    def __div__(self,rhs):
        unit_l = self.u
        unit_r = rhs.u
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")

        return self.__truediv__(rhs) 
        
        return ValueUnit(v,tmp)
            
    def __truediv__(self,rhs):
        unit_l = self.u
        unit_r = rhs.u
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")

        tmp = self.u / rhs.u 
        v = self.x / rhs.x 
        
        return ValueUnit(v,tmp)
        
    def __rmul__(self,lhs):
        # Assume that the `lhs` behaves as a number 
        q = self.u.system.unity * self.u
        return ValueUnit(lhs * self.x, q)
            
    def __rdiv__(self,lhs):
        # Assume that the `lhs` behaves as a number 
        q = self.u.system.unity / self.u
        return ValueUnit(lhs / self.x, q)
                        
#----------------------------------------------------------------------------
def value(vu):
    try:
        return vu.x 
    except AttributeError:
        return vu 

#----------------------------------------------------------------------------
def unit(vu):
    try:
        return vu.u 
    except AttributeError:
        # TODO: This must be interpreted as being  
        # equivalent to `unity`, the Numeric unit.
        return None 
       
#----------------------------------------------------------------------------
#
def result(value_unit, result_x_fn=lambda x,*arg:x, *arg):
    """
    Return a `ValueUnit` in which the unit has been 
    converted to the reference unit of the unit system. 
    A value result function `result_x_fn` can be supplied 
    to apply a final processing to the value.
    """
    return ValueUnit( 
        result_x_fn(value_unit.u.multiplier*value_unit.x, *arg), 
        value_unit.u.reference_unit_for() 
    )
        
             

    
    
