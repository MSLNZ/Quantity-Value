from QV.registered_unit import RegisteredUnit as Unit
from QV.registered_unit import RegisteredUnitExpression
from QV.kind_of_quantity import Number
from QV.scale import RatioScale, IntervalScale

__all__ = ('qvalue','value','unit','qresult','qratio')

#----------------------------------------------------------------------------
#
# The name comes from the idea that a quantity is fully expressed
# as a value and a unit (Maxwell).

class ValueUnit(object):
    """
    A number and an associated unit.
    
    A ``ValueUnit`` class represents a quantity value, 
    as that term is used in metrology.
    
    """
    __slots__ = ("value", "unit")
    
    def __init__(self,value,unit):
        self.value = value     
        self.unit = unit
        
    # We want this object to appear to be a ``qvalue``,
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
            self.unit.scale.symbol 
        )
        
    def __add__(self,rhs):  
        lhs = self  
        register = lhs.unit.register  
        
        assert register is rhs.unit.register, "different unit registers"
        
        if (
            type(lhs.unit.scale) is RatioScale
        and type(rhs.unit.scale) is RatioScale  
        ): 
        
            # The calculation is done in the reference unit 
            # unless both units are the same 
            if lhs.unit is rhs.unit:
                return ValueUnit(   
                    lhs.value + rhs.value, 
                    rhs.unit 
                )
                
            elif (
                isinstance(lhs.unit,RegisteredUnitExpression) 
            or  isinstance(rhs.unit,RegisteredUnitExpression) 
            or  lhs.unit in register and rhs.unit in register
            ):

                # `unit` may be a unit expression, or the units 
                # may not be the same but both are registered, 
                # in either case we must resolve the unit   
                # and convert before proceeding.
                ref_u_l = register.reference_unit_for( lhs.unit ) 
                ref_u_r = register.reference_unit_for( rhs.unit ) 
                
                # For ratio scales there could be a conversion 
                # factor to get from the resolved unit to the 
                # reference unit.
                
                l_to_ref_fn = register.conversion_from_A_to_B(lhs.unit,ref_u_l)
                r_to_ref_fn = register.conversion_from_A_to_B(rhs.unit,ref_u_r)
                
                assert ref_u_r is ref_u_l, "different units"
                    
                return ValueUnit(   
                    l_to_ref_fn(lhs.value) + r_to_ref_fn(rhs.value), 
                    ref_u_r 
                ) 
            else:
                assert False, "unexpected"
                
        else:
            raise RuntimeError(
                "cannot add {!r} and {!r}".format(lhs.unit.scale,rhs.unit.scale)
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
        
        assert register is rhs.unit.register, "different unit registers"
            
        if (
            type(lhs.unit.scale) is RatioScale
        and type(rhs.unit.scale) is RatioScale  
        ): 
                     
            if lhs.unit is rhs.unit:
                # The case of interval scales is different
                # if type(lhs.unit.scale) is IntervalScale:
                return ValueUnit(   
                    lhs.value - rhs.value, 
                    rhs.unit 
                )
                
            elif (
                isinstance(lhs.unit,RegisteredUnitExpression) 
            or  isinstance(rhs.unit,RegisteredUnitExpression) 
            or  lhs.unit in register and rhs.unit in register
            ):

                # `unit` may be a unit expression, or the units 
                # may not be the same but both are registered, 
                # in either case we must resolve the unit   
                # and convert before proceeding.

                ref_u_l = register.reference_unit_for( lhs.unit ) 
                ref_u_r = register.reference_unit_for( rhs.unit ) 
                
                # For ratio scales there could be a conversion 
                # factor to get from the resolved unit to the 
                # reference unit.

                l_to_ref_fn = register.conversion_from_A_to_B(lhs.unit,ref_u_l)
                r_to_ref_fn = register.conversion_from_A_to_B(rhs.unit,ref_u_r)
                
                assert ref_u_r is ref_u_l, "different units"
                    
                return ValueUnit(   
                    l_to_ref_fn(lhs.value) - r_to_ref_fn(rhs.value), 
                    ref_u_r 
                )   
                
            else:
                assert False, "unexpected"
        else:
            raise RuntimeError(
                "cannot subtract {!r} and {!r}".format(lhs.unit.scale,rhs.unit.scale)
            )

  
    def __rsub__(self,lhs):
        rhs = self
        # Can subtract numeric QVs from numbers
        if rhs.unit.scale.kind_of_quantity is Number:
            return ValueUnit( lhs - rhs.value, rhs.unit )
        else:
            return NotImplemented
  
    # Multiplication, division and exponentiation 
    # create temporary ValueUnit objects. 
    # These expose an interface with 
    # `register` and `kind_of_quantity` attributes, 
    # which allow a kind_of_quantity and hence a unit to be resolved.
    
    def __mul__(self,rhs):
        lhs = self
        if hasattr(rhs,'unit'):                      
            assert lhs.unit.register is rhs.unit.register, "different unit registers"
            
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
            assert lhs.unit.register is rhs.unit.register, "different unit registers"

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
        >>> metre = si.unit( RatioScale(context['Length'],'metre','m') ) 
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
    unit=None, 
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
    
    If ``simplify`` is ``True``, unit signatures will be simplified.
    
    The function ``value_result`` is applied to the value as a final processing step.
    
    Example ::
    
        >>> context = Context( ("Length","L"), ("Time","T") )
        >>> Speed = context.declare('Speed','V','Length/Time')
        >>> si =  UnitRegister("si",context)
        >>> metre = si.unit( RatioScale(context['Length'],'metre','m') )
        >>> second = si.unit( RatioScale(context['Time'],'second','s') )
        >>> metre_per_second = si.unit( RatioScale(context['Speed'],'metre_per_second','m*s-1') )
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
    
    if simplify and not value_unit.unit.is_simplified:
        u = value_unit.unit.simplify()
    else:
        u = value_unit.unit
        
    u_scale_type = type(u.scale)

    # This can find the ref unit, but if we are dealing 
    # with a unit expression, we don't know how to 
    # convert to that ref unit! The same applies to 
    # a preferred unit. 
    ref_unit = register.reference_unit_for( u )
    
    # ``unit`` may be a string.
    if unit:
    
        koq = ref_unit.scale.kind_of_quantity
        ref_scale_type = type(ref_unit.scale)
        
        units_dict = register.get(koq,ref_scale_type)
        
        if isinstance(unit,str):
            if unit in units_dict:
                unit = units_dict[unit]
            else:
                raise RuntimeError(
                    "{} is not a unit for {!r}".format(
                        unit,
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
                
        # Note `unit` may be a temporary RatioScale object and hence unregistered
        fn = register.conversion_from_A_to_B(u,unit)
        return ValueUnit( 
            value_result(
                fn( value_unit.value ), 
                *arg, 
                **kwarg
            ), 
            unit 
        )
    else:       
        fn = register.conversion_from_A_to_B(u,ref_unit)
        return ValueUnit( 
            value_result(
                fn( value_unit.value ), 
                *arg, 
                **kwarg
            ), 
            ref_unit  
        )
        
#----------------------------------------------------------------------------
def qratio(value_unit_1, value_unit_2, unit=None ):
    """
    Return a quantity value for ``value_unit_1/value_unit_2``.
    If the signature of the associated units are in simplified form,
    signature information is retained in the quotient.

    When ``unit`` is None, the reference unit is used. 

    Example ::
    
        >>> context = Context( ("Current","I"),("Voltage","V") )
        >>> ureg = UnitRegister("ureg",context)
        >>> volt = ureg.unit( RatioScale(context['Voltage'],'volt','V') ) 
        >>> voltage_ratio = context.declare('voltage_ratio','V/V','Voltage//Voltage')
        >>> volt_per_volt = ureg.unit( RatioScale(context['voltage_ratio'],'volt_per_volt','V/V') )
        >>> v1 = qvalue(1.23, volt)
        >>> v2 = qvalue(9.51, volt)
        >>> qratio( v2,v1 )
        qvalue(7.73170731...,volt_per_volt)

    """
    register = value_unit_1.unit.register 
    if not register is value_unit_1.unit.register :
        raise RuntimeError("different unit registers")
    
    ref_unit = register.reference_unit_for(
        value_unit_1.unit//value_unit_2.unit
    )
    
    if unit:
        # Check that the user-supplied unit is compatible 
        koq_1 = ref_unit.scale.kind_of_quantity 
        koq_2 = unit.scale.kind_of_quantity 
        
        if koq_1 != koq_2:
            raise RuntimeError(
                "Different kinds of quantity: {} and {}".format(
                    koq_1,koq_2
                )
            )

        value = (
            value_unit_1.unit.scale.conversion_factor*value_unit_1.value /
            (value_unit_2.unit.scale.conversion_factor*value_unit_2.value) 
        )/unit.scale.conversion_factor
        
        return ValueUnit( value, unit )    
    else:
        value = (
            value_unit_1.unit.scale.conversion_factor*value_unit_1.value /
            (value_unit_2.unit.scale.conversion_factor*value_unit_2.value) 
        )

        return ValueUnit( value, ref_unit )
        
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )    
