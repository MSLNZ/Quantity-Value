from .quantity import Unit

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
        if isinstance(self.unit,Unit):
            unit_l = self.unit
        else:   
            assert False,'automatic resolution not implemented'
        if isinstance(rhs.unit,Unit):
            unit_r = rhs.unit
        else:   
            assert False,'automatic resolution not implemented'

        if not unit_l.system is unit_r.system:
            raise RuntimeError("Different unit systems: {}, {}".format(
                unit_l.system,unit_r.system)
            )
            
        if unit_l is unit_r:
            return ValueUnit( self.value + rhs.value, unit_l )
         
        if unit_l.kind_of_quantity is unit_r.kind_of_quantity:
            ml = unit_l.multiplier
            mr = unit_r.multiplier 
            if ml < mr:
                return ValueUnit( self.value + (mr/ml)*rhs.value, unit_l )
            else:
                return ValueUnit( (ml/mr)*self.value + rhs.value, unit_r )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    unit_l.kind_of_quantity,unit_r.kind_of_quantity)
            )    

    def __radd__(self,lhs):
        # Can add numbers to numeric QVs
        if isinstance(self.unit,Unit):
            unit_r = self.unit
        else:   
            assert False,'automatic resolution not implemented'

        if unit_r.kind_of_quantity is Numeric:
            return ValueUnit( lhs + self.value, unit_r )
        else:
            return NotImplemented
  
    def __sub__(self,rhs):
        if isinstance(self.unit,Unit):
            unit_l = self.unit
        else:   
            assert False,'automatic resolution not implemented'
        if isinstance(rhs.unit,Unit):
            unit_r = rhs.unit
        else:   
            assert False,'automatic resolution not implemented'

        if not unit_l.system is unit_r.system:
            raise RuntimeError("Different unit systems: {}, {}".format(
                unit_l.system,unit_r.system)
            )
        
        if unit_l is unit_r:
            return ValueUnit( self.value - rhs.value, unit_l )
            
        if unit_l.kind_of_quantity is unit_r.kind_of_quantity:
        
            ml = unit_l.multiplier
            mr = unit_r.multiplier 
            if ml < mr:
                return ValueUnit( self.value - (mr/ml)*rhs.value, unit_l )
            else:
                return ValueUnit( (ml/mr)*self.value - rhs.value, unit_r )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    unit_l.kind_of_quantity,unit_r.kind_of_quantity)
            )    
  
    def __rsub__(self,lhs):
        # Can subtract numeric QVs from numbers
        if isinstance(self.unit,Unit):
            unit_r = self.unit
        else:   
            assert False,'automatic resolution not implemented'

        if unit_r.kind_of_quantity is Numeric:
            return ValueUnit( lhs - self.value, unit_r )
        else:
            return NotImplemented
  
    # Multiplication and division create ValueUnit 
    # objects in which the unit is a temporary 
    # object that has not not been resolved to a unit. 
    # This temporary object has an interface that exposes
    # `multiplier`, `system` and `kind_of_quantity` attributes. 
    # These allow a unit to be resolved later.
    def __mul__(self,rhs):
        if hasattr(rhs,'unit'):          
            unit_l = self.unit
            unit_r = rhs.unit
            if not unit_l.system is unit_r.system:
                raise RuntimeError("operation requires the same unit system")

            tmp = self.unit * rhs.unit 
            v = self.value * rhs.value 

            return ValueUnit(v,tmp)
        else:
            # Assume that the `rhs` behaves as a number 
            q = self.unit.system.unity * self.unit
            return ValueUnit(rhs * self.value, q)
            
    def __div__(self,rhs):
        if hasattr(rhs,'unit'):          
            unit_l = self.unit
            unit_r = rhs.unit
            if not unit_l.system is unit_r.system:
                raise RuntimeError("operation requires the same unit system")

            return self.__truediv__(rhs) 
            
        else:
            # Assume that the `rhs` behaves as a number 
            q = self.unit.system.unity / self.unit
            return ValueUnit(self.value /  rhs, q)
            
    def __truediv__(self,rhs):
        unit_l = self.unit
        unit_r = rhs.unit
        if not unit_l.system is unit_r.system:
            raise RuntimeError("operation requires the same unit system")

        tmp = self.unit / rhs.unit 
        v = self.value / rhs.value 
        
        return ValueUnit(v,tmp)
        
    def __rmul__(self,lhs):
        # Assume that the `lhs` behaves as a number 
        q = self.unit.system.unity * self.unit
        return ValueUnit(lhs * self.value, q)
            
    def __rdiv__(self,lhs):
        # Assume that the `lhs` behaves as a number 
        q = self.unit.system.unity / self.unit
        return ValueUnit(lhs / self.value, q)

    def __rtruediv__(self,lhs):
        # Assume that the `lhs` behaves as a number 
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
# TODO: `value_unit` can only consist of product/quotient terms. 
# Need to resolve these before addition and subtraction with 
# other terms can be allowed.
# Hence:: 
#   x0 + result(v0*t) + result(0.5*a0*t*t)
# rather than::
#   result(x0 + v0*t + 0.5*a0*t*t)
# This could be changed by using the __add__ and __sub__ 
# methods to trigger resolution of their arguments. 
# In that case, we could often do without `result`, 
# e.g., this would auto-evaluate::
#   x0 + v0*t + 0.5*a0*t*t
# We would need a different way to declare `result_x_fn`. It 
# could be a callback function assigned to ValueUnit.
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
        
             

    
    
