from __future__ import division 

# `UnitRegister` does not represent the concept of a 'system of units'. 
# Different types of units belong in different systems, like the SI 
# would have m, cm, km, etc, and Imperial would have the foot, yard,
# etc. However, all those length scales are "self-similar" in the 
# sense that a scale factor converts from one to the other.
 
from QV.scale import Unit 
from QV.units_dict import UnitsDict

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
        
        self._koq_to_ref_unit = dict()          # koq -> unit
        self._koq_to_units_dict = dict()         # Length.metre -> Unit 
                
        # There must always be a unit for numbers and it is a 
        # special case because the name and term are blank
        Number = context['Number']
        unity = Unit(Number,'','',self,1)        
        self._koq_to_ref_unit[Number] = unity       
        self._koq_to_units_dict[Number] = UnitsDict({ 'unity': unity })        
        
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
            
        return self._koq_to_ref_unit[koq]        

    def __getattr__(self,attr):
        # Convert koq name to koq object
        attr = getattr(self._context,attr)
        try:  
            return self._koq_to_units_dict[ attr ]
        except KeyError:
            raise AttributeError
    
    def __getitem__(self,koq):
        if isinstance(koq,str):
            koq = self._context[koq]
            
        return self._koq_to_units_dict[koq]
        
    def get(self,kind_of_quantity):
        """
        Return a mapping of names and terms to units for ``kind_of_quantity``
        """
        if isinstance(kind_of_quantity,str):
            kind_of_quantity = self._context[kind_of_quantity]
           
        return self._koq_to_units_dict.get(
            kind_of_quantity,
            UnitsDict({})
        )
            
    def _register_reference_unit(self,unit):
        # key: koq; value: unit
        koq = unit.scale.kind_of_quantity
        
        if koq in self._koq_to_ref_unit: 
            if not self._koq_to_ref_unit[koq] is unit:
                raise RuntimeError(
                    "{!r} is already registered".format(koq)
                )
        else:
            self._koq_to_ref_unit[koq] = unit 
            self._set_units_dict(koq,unit)
            
    def _set_units_dict(self,koq,unit):
        if koq in self._koq_to_units_dict:
            koq_units = self._koq_to_units_dict[koq]           
            koq_units.update({ 
                unit.scale.name: unit, unit.scale.term: unit 
            })
        else:
            self._koq_to_units_dict[koq] = UnitsDict({ 
                unit.scale.name: unit, unit.scale.term: unit 
            })
            
    def _register_related_unit(self,unit):
        
        # The same unit names can be used with different KoQs,
        # but the mapping koq -> unit must be unique.
        koq = unit.scale.kind_of_quantity
        if koq in self._koq_to_ref_unit:
            self._set_units_dict(koq,unit)
        else:
            raise RuntimeError(
                "No reference unit defined for {!s}".format(koq)
            )
         
    def reference_unit(self,koq_name,unit_name,unit_term):
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
        src_koq = source_unit.scale.kind_of_quantity
        dst_koq = target_unit.scale.kind_of_quantity
        
        if src_koq not in self._koq_to_units_dict:
            raise RuntimeError(
                "{!r} is not registered".format(source_unit)
            )
        if dst_koq not in self._koq_to_units_dict:
            raise RuntimeError(
                "{!r} is not registered".format(target_unit)
            )
        
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
    Register a unit that is multiple or submultiple of the
    reference unit for the same kind of quantity.
    
    Example::
        >>> context = Context( ("Distance","L"), ("Volume","V") )
        >>> FuelConsumption = context.declare('FuelConsumption','FC','Volume/Distance')
        >>> ureg =  UnitRegister("ureg",context)
        >>> kilometre = ureg.reference_unit('Distance','kilometre','km') 
        >>> litre = ureg.reference_unit('Volume','litre','L')
        >>> litres_per_km = ureg.reference_unit('FuelConsumption','litres_per_km','L/km')
        >>> litres_per_100_km = related_unit(
        ...     ureg.FuelConsumption.litres_per_km,
        ...     1E-2,
        ...     'litres_per_100_km','L/(100 km)'
        ... )
        >>> print( litres_per_100_km )
        L/(100 km)
        
    """
    koq = reference_unit.scale.kind_of_quantity
    register = reference_unit._register 

    if not reference_unit is register.reference_unit_for(koq):
        raise RuntimeError(
            "{!r} is not a reference unit".format(reference_unit.scale.name)  
        )     

    units_dict = register[koq]
    if name in units_dict:
        return units_dict[name]
    else:
        unit = Unit(
            koq,
            name,
            term,
            register,
            fraction
        )
        register._register_related_unit(unit)
        
        return unit
        

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )