from __future__ import division 
from __future__ import print_function 

from QV.scale import Unit
from QV.kind_of_quantity import Number

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
        return "{!s}({!s},{!s})".format(
            'qvalue',
            self.value,
            self.unit.scale.name 
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
        if rhs.unit.scale.kind_of_quantity is Number:
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
        if rhs.unit.scale.kind_of_quantity is Number:
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
                lhs.unit.register.Number.unity * lhs.unit
            )
            
    def __rmul__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs * rhs.value, 
            rhs.unit.register.Number.unity * rhs.unit
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
                lhs.unit / lhs.unit.register.Number.unity 
            )
        
    def __rtruediv__(self,lhs):
        rhs = self
        # Assume that the `lhs` behaves as a number 
        return ValueUnit(
            lhs / rhs.value, 
            rhs.unit.register.Number.unity / rhs.unit
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
    
    Example ::
    
        >>> context = Context( ("Length","L"), ("Time","T") )
        >>> si = UnitRegister("si",context)
        >>> metre = si.reference_unit('Length','metre','m') 
        >>> qvalue( 1.84, metre )
        qvalue(1.84,metre)
        
    """
    return ValueUnit(value,unit)
    
#----------------------------------------------------------------------------
def value(quantity_value):
    """
    Return the value
    
    """
    try:
        return quantity_value.value 
    except AttributeError:
        return quantity_value 

#----------------------------------------------------------------------------
def unit(quantity_value):
    """
    Return the unit (measurement scale)
    
    """
    try:
        return quantity_value.unit 
    except AttributeError:
        # TODO: This must be interpreted as being  
        # equivalent to `unity`, the Number unit.
        return None 
       
#----------------------------------------------------------------------------
def qresult(
    value_unit, 
    preferred_unit=None, 
    simplify=True, 
    value_result = lambda x, *arg, **kwarg: x, 
    *arg,
    **kwarg
    ):
    """
    Return a ``qvalue``.
    
    ``value_unit`` is a quantity-value or expression of quantity-values. 
    
    If a ``unit`` is supplied, it is used to report the measure. If  
    not, the measure is reported in the reference unit for that quantity.
    
    If ``simplify`` is ``True``, unit dimensions are simplified.
    
    The function ``value_result`` is applied to the value as a final processing step.
    
    Example ::
    
        >>> context = Context( ("Length","L"), ("Time","T") )
        >>> Speed = context.declare('Speed','V','Length/Time')
        >>> si =  UnitRegister("si",context)
        >>> metre = si.reference_unit('Length','metre','m') 
        >>> second = si.reference_unit('Time','second','s') 
        >>> metre_per_second = si.reference_unit('Speed','metre_per_second','m*s-1')
        >>> d = qvalue(0.5,metre)
        >>> t = qvalue(1.0,second)
        >>> v0 = qresult(d/t)
        >>> print( "average speed =", v0 )
        average speed = 0.5 m*s-1
        >>> x0 = qvalue(.3,metre)
        >>> print( "displacement =", x0 + v0*t )
        displacement = 0.8 m
        
    """
    register = value_unit.unit.register 
    
    if simplify:
        unit = value_unit.unit.simplify()
    else:
        unit = value_unit.unit
        
    ref_unit = register.reference_unit_for( unit )
    
    if preferred_unit:
    
        koq = ref_unit.scale.kind_of_quantity
        units_dict = register[koq]
        
        if isinstance(preferred_unit,str):
            if preferred_unit in units_dict:
                preferred_unit = units_dict[preferred_unit]
            else:
                raise RuntimeError(
                    "{} is not a unit for {!r}".format(
                        preferred_unit,
                        koq
                    )
                )
            
        # # Do not simplify dimensionless units 
        # simplify = not preferred_unit.is_dimensionless and simplify 
        
        # if simplify:
            # ref_unit = register.reference_unit_for( 
                # value_unit.unit.simplify() 
            # ) 
        # else:
            # ref_unit = register.reference_unit_for( value_unit.unit )
                
            
        multiplier = value_unit.unit.multiplier/preferred_unit.multiplier
        return ValueUnit( 
            value_result(
                multiplier*value_unit.value, 
                *arg, 
                **kwarg
            ), 
            preferred_unit 
        )
    else:       
        return ValueUnit( 
            value_result(
                value_unit.unit.multiplier*value_unit.value, 
                *arg, 
                **kwarg
            ), 
            ref_unit  
        )
        
#----------------------------------------------------------------------------
def qratio(value_unit_1, value_unit_2, unit=None ):
    """
    Return a quantity value for ``value_unit_1/value_unit_2``.
    If the dimensions of the associated units are in simplified form,
    dimensional information will be retained in the quotient.

    If no ``unit`` is supplied the reference unit is used. 

    Example ::
    
        >>> context = Context( ("Current","I"),("Voltage","V") )
        >>> ureg = UnitRegister("ureg",context)
        >>> volt = ureg.reference_unit('Voltage','volt','V') 
        >>> voltage_ratio = context.declare('voltage_ratio','V/V','Voltage//Voltage')
        >>> volt_per_volt = ureg.reference_unit('voltage_ratio','volt_per_volt','V/V')
        >>> v1 = qvalue(1.23, volt)
        >>> v2 = qvalue(9.51, volt)
        >>> qratio( v2,v1 )
        qvalue(7.73170731...,volt_per_volt)

    """
    register = value_unit_1.unit.register 
    if not register is value_unit_1.unit.register :
        raise RuntimeError("Different unit registers: {}, {}".format(
            register, value_unit_1.unit.register)
        )
    
    default_unit = register.reference_unit_for(value_unit_1.unit//value_unit_2.unit)
    # Check that the user-supplied unit is compatible wit the quantity 
    if unit:
        koq_1 = default_unit.scale.kind_of_quantity 
        koq_2 = unit.scale.kind_of_quantity 
        
        if koq_1 != koq_2:
            raise RuntimeError(
                "Different kinds of quantity: {} and {}".format(
                    koq_1,koq_2
                )
            )

        value = (
            value_unit_1.unit.multiplier*value_unit_1.value /
            (value_unit_2.unit.multiplier*value_unit_2.value) 
        )/unit.multiplier
        
        return ValueUnit( value, unit )    
    else:
        value = (
            value_unit_1.unit.multiplier*value_unit_1.value /
            (value_unit_2.unit.multiplier*value_unit_2.value) 
        )

        return ValueUnit( value, default_unit )
    
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )    
