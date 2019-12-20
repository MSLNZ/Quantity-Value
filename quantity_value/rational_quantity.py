from fractions import Fraction 

from quantity import *

__all__ = ( 
    'RationalUnit',
    'alternative_unit',
)

#----------------------------------------------------------------------------
class RationalUnit(Unit):

    """
    A rational unit is related to a reference unit by a rational multiplier. 
    Such as, feet to inches.
    """
    
    def __init__(self,kind_of_quantity,name,term):
        super(RationalUnit,self).__init__(
            kind_of_quantity,
            name,
            term
        )    
        
        self._prefixed_quantities = dict() 
        self._multiplier = Fraction(1)        

#----------------------------------------------------------------------------
def alternative_unit(unit,fraction,name,term):
    """
    Define and register a rational multiple of the system  
    reference unit for the same quantity.
    
    """
    kind_of_quantity = unit._kind_of_quantity
    system = unit._system 
    
    if not system.has_unit_for(kind_of_quantity):
        raise RuntimeError(
            "{!r} is not a reference unit".format(unit)
        )

    fraction = Fraction( fraction )
    
    alt_rational_unit = AltRationalUnit(
        kind_of_quantity,
        name,
        term,
        system,
        fraction
    )
    system._register_by_name(alt_rational_unit)
    
    return alt_rational_unit
    
#----------------------------------------------------------------------------
class AltRationalUnit(RationalUnit):

    """
    Instances are only created by RationalUnit
    """
    
    def __init__(self,kind_of_quantity,name,term,system,fraction): 
        super(AltRationalUnit,self).__init__(
            kind_of_quantity,
            name,
            term 
        )
        self._multiplier = fraction
        self.system = system        

    def __repr__(self):
        return "{!s}({!r},{!s},{!s},{!s})".format(
            self.__class__.__name__,
            self.name,
            self,
            self.system,       
            self._multiplier
        )
        
