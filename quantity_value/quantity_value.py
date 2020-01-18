from __future__ import division 

from scale import Unit

#----------------------------------------------------------------------------
#
class ValueUnit(object):
    """
    A ValueUnit pairs a number and a unit.
    The unit must be associated with a register of units.
    Arithmetic expressions involving ValueUnit objects 
    apply the rules of quantity calculus to the associated units.
    In general, this will create a temporary object representing 
    the unit expression, which must be explicitly resolved to the 
    corresponding unit in the unit register.
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
        if not lhs.unit.register is rhs.unit.register:
            raise RuntimeError("Different unit systems: {}, {}".format(
                lhs.unit.register, rhs.unit.register)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( lhs.unit.multiplier*self.value, lhs.unit.reference_unit() ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( rhs.unit.multiplier*rhs.value, rhs.unit.reference_unit() ) 
            
        if lhs.unit is rhs.unit:
            return ValueUnit( lhs.value + rhs.value, lhs.unit )
         
        if lhs.unit.scale.kind_of_quantity is rhs.unit.scale.kind_of_quantity:
            ml = lhs.unit.multiplier
            mr = rhs.unit.multiplier 
            if ml < mr:
                return ValueUnit( lhs.value + (mr/ml)*rhs.value, lhs.unit )
            else:
                return ValueUnit( (ml/mr)*lhs.value + rhs.value, rhs.unit )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    lhs.unit.scale.kind_of_quantity,rhs.unit.scale.kind_of_quantity)
            )    

    def __radd__(self,lhs):
        rhs = self
        # Can add numbers to numeric QVs
        if rhs.unit.scale.kind_of_quantity is Numeric:
            return ValueUnit( lhs + rhs.value, rhs.unit )
        else:
            return NotImplemented
  
    def __sub__(self,rhs):
        lhs = self
        if not lhs.unit.register is rhs.unit.register:
            raise RuntimeError("Different unit systems: {}, {}".format(
                lhs.unit.register, rhs.unit.register)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( lhs.unit.multiplier*self.value, lhs.unit.reference_unit() ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( rhs.unit.multiplier*rhs.value, rhs.unit.reference_unit() ) 
        
        if lhs.unit is rhs.unit:
            return ValueUnit( lhs.value - rhs.value, lhs.unit )
            
        if lhs.unit.scale.kind_of_quantity is rhs.unit.scale.kind_of_quantity:
        
            ml = lhs.unit.multiplier
            mr = rhs.unit.multiplier 
            if ml < mr:
                return ValueUnit( lhs.value - (mr/ml)*rhs.value, lhs.unit )
            else:
                return ValueUnit( (ml/mr)*lhs.value - rhs.value, rhs.unit )
        else:
            raise RuntimeError(
                "Different kinds of quantity: {}, {}".format(
                    lhs.unit.scale.kind_of_quantity,rhs.unit.scale.kind_of_quantity)
            )    
  
    def __rsub__(self,lhs):
        rhs = self
        # Can subtract numeric QVs from numbers
        if rhs.unit.scale.kind_of_quantity is Numeric:
            return ValueUnit( lhs - rhs.value, rhs.unit )
        else:
            return NotImplemented
  
    # Multiplication, division and exponentiation create temporary ValueUnit 
    # objects that have not been resolved to a unit. 
    # These temporary objects have an interface that exposes
    # `multiplier`, `register` and `kind_of_quantity` attributes, 
    # which allow a kind_of_quantity and hence a unit to be resolved later.
    def __mul__(self,rhs):
        lhs = self
        if hasattr(rhs,'unit'):                      
            if not lhs.unit.register is rhs.unit.register:
                raise RuntimeError("operation requires the same unit register")

            return ValueUnit(lhs.value * rhs.value, lhs.unit * rhs.unit)
        else:
            # Assume that the `rhs` behaves as a number 
            return ValueUnit(
                rhs * lhs.value, 
                lhs.unit.register.unity * lhs.unit
            )
            
    def __rmul__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs * rhs.value, 
            rhs.unit.register.unity * rhs.unit
        )
            
    def __truediv__(self,rhs):
        lhs = self 
        if hasattr(rhs,'unit'):          
            if not lhs.unit.register is rhs.unit.register:
                raise RuntimeError("operation requires the same unit register")

            return ValueUnit(
                lhs.value / rhs.value,
                lhs.unit / rhs.unit
            )
            
        else:
            # Assume that the `rhs` behaves as a number 
            return ValueUnit(
                lhs.value / rhs, 
                lhs.unit / lhs.unit.register.unity 
            )
        
    def __rtruediv__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs / rhs.value, 
            rhs.unit.register.unity / rhs.unit
        )
        
    # def __floordiv__(self,rhs):
        # lhs = self 
        # if hasattr(rhs,'unit'):          
            # if not lhs.unit.register is rhs.unit.register:
                # raise RuntimeError("operation requires the same unit register")

            # return ValueUnit(
                # lhs.value / rhs.value,
                # lhs.unit // rhs.unit
            # )
        # else:
            # # Assume that the `rhs` behaves as a number 
            # return ValueUnit(
                # lhs.value / rhs, 
                # lhs.unit // lhs.unit.register.unity 
            # )

    # def __rfloordiv__(self,lhs):
        # rhs = self 
        # # Assume that the `lhs` behaves as a number 
        # return ValueUnit(
            # lhs.value / rhs.value, 
            # rhs.unit.register.unity // rhs.unit   
        # )
        
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
def qresult(
    value_unit, 
    unit=None, 
    simplify=True, 
    value_result = lambda x, *arg, **kwarg: x, 
    *arg,
    **kwarg
    ):
    """
    Return a `qvalue`.
    
    `unit` may be the name of a unit, or a unit object. The measure will be 
    converted to this unit.
    
    `simplify` controls when the unit dimensions will be simplified.
    
    If no `unit` is given the measure will be converted to the reference 
    unit of the register. 
    
    A function `value_result` can be supplied 
    to apply a final processing to the value.
    """
    if unit:
        # Use a preferred unit 

        if isinstance(unit,str):
            # `unit` is the name of a unit, so look up the object
            unit = value_unit.unit.register[unit]
            
        if simplify:
            ref_unit = value_unit.unit.simplify().reference_unit() 
        else:
            ref_unit = value_unit.unit.reference_unit()
                
        if unit.scale.kind_of_quantity != ref_unit.scale.kind_of_quantity:
            raise RuntimeError(
                "{} are incompatible with {}".format(
                    unit,
                    ref_unit
                )
            )
            
        multiplier = value_unit.unit.multiplier/unit.multiplier
        return ValueUnit( 
            value_result(
                value_unit.value*multiplier , 
                *arg, 
                **kwarg
            ), 
            unit 
        )
    else:
        if simplify:
            unit = value_unit.unit.simplify().reference_unit() 
        else:
            unit = value_unit.unit.reference_unit()
            
        return ValueUnit( 
            value_result(
                value_unit.unit.multiplier*value_unit.value, 
                *arg, 
                **kwarg
            ), 
            unit  
        )
        
#----------------------------------------------------------------------------
def qratio(value_unit_1, value_unit_2, unit=None ):
    """
    Return a quantity-value for the ratio keeping the dimensions 
    of the numerator and denominator separate.

    If no `unit` is given the ratio will be converted to the reference 
    unit of the register. 

    """
    # Return a qvalue with units that are appropriate for the ratio
    
    koq_1 = value_unit_1.unit.reference_unit().scale.kind_of_quantity 
    koq_2 = value_unit_2.unit.reference_unit().scale.kind_of_quantity 
    
    if koq_1 != koq_2:
        raise RuntimeError(
            "Different kinds of quantity: {} and {}".format(
                koq_1,koq_2
            )
        )
    
    if unit and koq_1 != unit.scale.kind_of_quantity:
        raise RuntimeError(
            "Different kinds of quantity: {} and {}".format(
                koq_1, unit.scale.kind_of_quantity
            )
        )
   
    if unit:
        value = (
            value_unit_1.unit.multiplier*value_unit_1.value /
            (value_unit_2.unit.multiplier*value_unit_2.value) 
        )/unit.multiplier
        
        return ValueUnit( 
            value_unit.unit.multiplier*value_unit.value, 
            unit
        )    
    else:
        value = (
            value_unit_1.unit.multiplier*value_unit_1.value /
            (value_unit_2.unit.multiplier*value_unit_2.value) 
        )

        return ValueUnit( 
            value, 
            (value_unit_1.unit//value_unit_2.unit).reference_unit()
        )
    
    
