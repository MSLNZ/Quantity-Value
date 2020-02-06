from __future__ import division 

# Note, mappings from KoQ to unit can be many-to-one. 
#
# `UnitRegister` does not represent the concept of a 'system of units'. 
# Different types of units belong in different systems, like the SI 
# would have m, cm, km, etc, and Imperial would have the foot, yard,
# etc. However, all those length scales are "self-similar" in the 
# sense that a scale factor converts from one to the other.
 
from fractions import *

from QV.scale import Unit 

__all__ = (
    'UnitRegister', 'related_unit'
)

#----------------------------------------------------------------------------
class UnitRegister(object):

    """
    A UnitRegister holds associations between kinds of quantities and units.
    
    A distinction is made between a reference unit and other related units 
    for the same kind of quantity. There can be only one reference unit 
    in the register for each kind of quantity.
    
    """ 
    
    def __init__(self,name,context):
        self._name = name
        self._context = context
        
        self._koq_to_unit = dict()  # koq -> unit
        self._name_to_unit = dict() # unit name -> unit
        
        # There must always be a unit for numbers
        Number = context['Number']
        unity = Unit(Number,'','',self,1)        
        self._koq_to_unit[Number] = unity
        self._name_to_unit['unity'] = unity
        self.__dict__['unity'] = unity 
            
    def __str__(self):
        return self._name

    def __repr__(self):
        return "{!s}({!s})".format(
            self.__class__.__name__,
            self._name
        )

    @property
    def context(self):        
        return self._context 
        
    def reference_unit_for(self,expr):
        """
        Return the reference unit for `expr`
        
        `expr` can be a product or quotient of units, 
        a product or quotient of kind-of-quantity objects,
        or a kind-of-quantity object.
        
        """
        # If `expr` has `kind_of_quantity` then `expr` is 
        # a unit or a unit expression. In the first case, 
        # we obtain a kind-of-quantity directly and should
        # immediately look up the unit.
        # In the second case, a kind-of-quantity
        # expression must be evaluated.
        # If `expr` has `execute` it is a kind-of-quantity
        # expression that must be evaluated.
        if hasattr(expr,'kind_of_quantity'):
            koq = expr.kind_of_quantity
        else:
            # Assume a koq or a koq expression
            koq = expr 
            
        if hasattr(koq,'execute'):
            koq = self.context._dim_to_koq( 
                self.context._evaluate_dimension( koq ) 
            )
            
        return self._koq_to_unit[koq]        
  
    def __contains__(self,name_or_term):
        return name_or_term in self._name_to_unit 
        
    def __getitem__(self,name_or_term):
        return self._name_to_unit[name_or_term]
        
    def get(self,name_or_term,default=None):
        # unit name -> unit
        return self._name_to_unit.get(name_or_term,default)
            
    def _register_reference_unit(self,unit):
        # key: koq; value: unit
        koq = unit.scale.kind_of_quantity
        
        if koq in self._koq_to_unit: 
            if not self._koq_to_unit[koq] is unit:
                raise RuntimeError(
                    "{!r} is already registered".format(koq)
                )
        else:
            self._koq_to_unit[koq] = unit 
            self._register_by_name(unit)
            
    def _register_by_name(self,unit):
        # `_name_to_unit` can refer to any units, not just reference ones,
        # provided their names and terms are distinct dictionary keys
        if unit.scale.name in self._name_to_unit:
            raise RuntimeError(
                "The name {!s} registered to {!r}".format(
                    unit.scale.name,
                    self._name_to_unit[unit.scale.name]
                )
            ) 
        if unit.scale.term in self._name_to_unit:
            raise RuntimeError(
                "The name {!s} registered to {!r}".format(
                    unit.scale.term,
                    self._name_to_unit[unit.scale.term]
                )
            ) 
            
        assert not unit.scale.name in self.__dict__,\
            "{!s} is a reserved name".format(unit.scale.name)

        self._name_to_unit[unit.scale.name] = unit
        self._name_to_unit[unit.scale.term] = unit
        self.__dict__[unit.scale.name] = unit 
        
        # # Don't express terms as object attributes 
        # # because they usually aren't valid identifiers 
        # assert not term in self.__dict__,\
            # "{!s} is a reserved name".format(term)
        # self.__dict__[term] = unit 
 
    def unit(self,koq_name,unit_name,unit_term):
        """
        Create a reference unit for ``koq_name``
        
        """
        koq = self.context._koq[koq_name]
        
        # Reference units all have multiplier = 1
        u = Unit(koq,unit_name,unit_term,self,multiplier=1)
        self._register_reference_unit(u) 
        
        return u
  
    def from_to(self,source_unit,target_unit):
        """
        Return the scale factor to convert from `source_unit` to `target_unit`
        """
        assert source_unit.scale.name in self,\
            "{!r} is not registered".format(source_unit)
            
        assert target_unit.scale.name in self,\
            "{!r} is not registered".format(target_unit)
            
        src_koq = source_unit.scale.kind_of_quantity
        dst_koq = target_unit.scale.kind_of_quantity
        if not src_koq is dst_koq:
            raise RuntimeError(
                "{} and {} are different kinds of quantity".format(
                src_koq,dst_koq)
            )
            
        # ref * k_dst -> unit_dst
        multiplier = target_unit.multiplier

        # unit_dst / unit_src -> k_dst / k_src
        multiplier /= source_unit.multiplier    
        
        return multiplier 
       
#----------------------------------------------------------------------------
def related_unit(reference_unit,fraction,name,term):
    """
    Define and register a unit that is multiple of the
    reference unit for the same kind of quantity.
    
    Example::
        >>> context = Context( ("Distance","L"), ("Volume","V") )
        >>> FuelConsumption = context.declare('FuelConsumption','FC','Volume/Distance')
        >>> ureg =  UnitRegister("ureg",context)
        >>> kilometre = ureg.unit('Distance','kilometre','km') 
        >>> litre = ureg.unit('Volume','litre','L')
        >>> litres_per_km = ureg.unit('FuelConsumption','litres_per_km','L/km')
        >>> litres_per_100_km = related_unit(
        ...     ureg.litres_per_km,
        ...     Fraction(1,100),
        ...     'litres_per_100_km','L/(100 km)'
        ... )
        >>> print( litres_per_100_km )
        L/(100 km)
        
    """
    kind_of_quantity = reference_unit.scale.kind_of_quantity
    register = reference_unit._register 

    if not reference_unit is register.reference_unit_for(
        reference_unit.scale.kind_of_quantity
    ):
        raise RuntimeError(
            "{!r} is not a reference unit".format(reference_unit.scale.name)  
        )     

    if name in register:
        return register[name]
    else:
        rational_unit = Unit(
            kind_of_quantity,
            name,
            term,
            register,
            fraction
        )
        register._register_by_name(rational_unit)
        
        return rational_unit
        
# #----------------------------------------------------------------------------
# def _prefixed_unit(prefix,reference_unit):
    # """
    # Define and register a multiple or sub-multiple of a
    # reference unit for the same quantity.
    
    # Example ::
        # >>> context = Context(('Length','L')) 
        # >>> SI =  UnitRegister("SI",context)
        # >>> metre = SI.unit('Length','metre','m')  
        # >>> centimetre = prefix.centi(metre) 
        # >>> print( centimetre )
        # cm

    # """
    # kind_of_quantity = reference_unit.scale.kind_of_quantity
    # register = reference_unit._register 

    # # Check that `self` is a reference unit in the register,
    # # because things like `centi(centi(metre))` are not permitted.
    # if not reference_unit is register.reference_unit_for(
        # reference_unit.scale.kind_of_quantity
    # ):
        # raise RuntimeError(
            # "{!r} is not a reference unit".format(reference_unit.scale.name)  
        # )     

    # name = "{!s}{!s}".format(
        # prefix.name,
        # reference_unit.scale.name
    # )
    
    # if name in register:
        # return register[name]
    # else:
        # term = "{!s}{!s}".format(
            # prefix.term,
            # reference_unit.scale
        # )
        
        # pq = Unit(
            # kind_of_quantity,
            # name,
            # term,
            # register,
            # prefix.value
        # )
        
        # # Buffer related quantities        
        # register._register_by_name(pq)
        
        # return pq 
        
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )