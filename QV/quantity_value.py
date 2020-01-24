from __future__ import division 

from QV.scale import Unit

__all__ = ('qvalue','value','unit','qresult','qratio')

#----------------------------------------------------------------------------
#
class ValueUnit(object):
    """
    A number and an associated unit.
    
    A ``ValueUnit`` class is intended to represent the notion of a
    quantity value, as that term is used formally in metrology.
    """
    __slots__ = ("value", "unit")
    
    def __init__(self,value,unit):
        self.value = value     
        self.unit = unit
        
    # We want the object to appear to be ``qvalue``,
    # because that is how we would create such an object.
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
        register = lhs.unit.register
        if not register is rhs.unit.register:
            raise RuntimeError("Different unit systems: {}, {}".format(
                register, rhs.unit.register)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( 
                lhs.unit.multiplier*self.value, 
                register.reference_unit_for( lhs.unit ) 
            ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( 
                rhs.unit.multiplier*rhs.value, 
                register.reference_unit_for( rhs.unit ) 
        ) 
            
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
        register = lhs.unit.register
        if not register is rhs.unit.register:
            raise RuntimeError("Different unit systems: {}, {}".format(
                register, rhs.unit.register)
            )
            
        if not isinstance(lhs.unit,Unit):
            # Must resolve the unit before proceeding
            lhs = ValueUnit( 
                lhs.unit.multiplier*self.value, 
                register.reference_unit_for( lhs.unit ) 
            ) 
        
        if not isinstance(rhs.unit,Unit):
            # Must resolve the unit before proceeding
            rhs = ValueUnit( 
                rhs.unit.multiplier*rhs.value, 
                register.reference_unit_for( rhs.unit ) 
            ) 
        
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
    """
    Create a new quantity value object.
    
    ``value`` is the measure,
    ``unit`` is the measurement scale
    
    """
    return ValueUnit(value,unit)
    
#----------------------------------------------------------------------------
def value(quantity_value):
    """
    Return the value of a quantity value object.
    
    """
    try:
        return quantity_value.value 
    except AttributeError:
        return quantity_value 

#----------------------------------------------------------------------------
def unit(quantity_value):
    """
    Return the measurement unit (scale) of a quantity value object.
    
    """
    try:
        return quantity_value.unit 
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
    Return a ``qvalue``.
    
    ``value_unit`` is a ``qvalue`` object or expression of ``qvalue`` objects. 
    
    
    If a ``unit`` is supplied it will be used to report the measure. If  
    not the measure will be converted to the reference unit.
    
    If ``simplify`` is ``True`` the unit dimensions will be simplified.
    
    A ``value_result`` function can be applied 
    to the value as a final processing step.
    """
    if unit:
        # Use a preferred unit 
        register = value_unit.unit.register
        if isinstance(unit,str):
            # `unit` is the name of a unit, so look up the object
            unit = register[unit]
            
        if simplify:
            ref_unit = register.reference_unit_for( 
                value_unit.unit.simplify() 
            ) 
        else:
            ref_unit = register.reference_unit_for( value_unit.unit )
                
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
            unit = value_unit.unit.simplify()
        else:
            unit = value_unit.unit
            
        register = value_unit.unit.register 
        unit = register.reference_unit_for( unit )
        
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
    Return a quantity value for ``value_unit_1/value_unit_2``  keeping   
    while the dimensions of the numerator and denominator separate.

    If no ``unit`` is supplied the reference unit is used. 

    """
    register = value_unit_1.unit.register 
    if not register is value_unit_1.unit.register :
        raise RuntimeError("Different unit systems: {}, {}".format(
            register, value_unit_1.unit.register)
        )
    
    koq_1 = register.reference_unit_for( value_unit_1.unit ).scale.kind_of_quantity 
    koq_2 = register.reference_unit_for( value_unit_2.unit ).scale.kind_of_quantity 
    
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

        ureg = value_unit_1.unit.register
        unit = register.reference_unit_for(value_unit_1.unit//value_unit_2.unit)
        return ValueUnit( 
            value, 
            unit
        )
    
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )    
