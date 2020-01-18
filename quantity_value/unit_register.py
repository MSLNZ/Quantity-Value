from __future__ import division 

# Note, mappings from KoQ to unit can be many-to-one. 
#
# `UnitRegister` does not represent the concept of a 'system of units'. 
# Different types of units belong in different systems, like the SI 
# would have m, cm, km, etc, and Imperial would have the foot, yard,
# etc. However, all those length scales are "similar" in the 
# sense that a simple multiplier converts from one to the other.
 
from fractions import *

from scale import Unit 

__all__ = (
    'UnitRegister', 'related_unit', 'metric_unit'
)

#----------------------------------------------------------------------------
class UnitRegister(object):

    """
    A unit register can declare a reference unit for a 
    kind of quantity. Other related units can be declared as 
    a multiple of the reference unit.
    
    Units can be looked up by name or by term (short name),
    such as `SI['metre']` or `'metre' in SI`. Unit names 
    can also be used as an attribute to access the unit,
    for example, `SI.metre`.
    
    """
    
    def __init__(self,name,context):
        self._name = name
        self._context = context
        
        self._koq_to_unit = dict()  # koq -> unit
        self._name_to_unit = dict() # unit name -> unit
        
        # There must always be a unit for numbers
        Numeric = context['Numeric']
        unity = Unit(Numeric,'','',self,1)        
        self._koq_to_unit[Numeric] = unity
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
        or simply a kind-of-quantity object.
        
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
        Create a reference unit in the register for `koq_name`
        The unit will be identified by `unit_name`, 
        and the abbreviation `unit_term`.
        
        """
        koq = self.context._koq[koq_name]
        
        # Reference units all have multiplier = 1
        u = Unit(koq,unit_name,unit_term,self,multiplier=1)
        self._register_reference_unit(u) 
        
        return u
  
    def from_to(self,source_unit,target_unit):
        """
        Return a multiplier to convert from `source_unit` to `target_unit`
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
def related_unit(unit,fraction,name,term):
    """
    Define and register a multiple of a
    reference unit for the same quantity.
    
    """
    kind_of_quantity = unit.scale.kind_of_quantity
    register = unit._register 

    if not unit is register.reference_unit_for(unit.scale.kind_of_quantity):
        raise RuntimeError(
            "{!r} is not a reference unit".format(unit.scale.name)  
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
        
#----------------------------------------------------------------------------
def metric_unit(prefix,unit):
    """
    Define a metric multiple of a
    reference unit for the same quantity.
    
    """
    kind_of_quantity = unit.scale.kind_of_quantity
    register = unit._register 

    # Check that `self` is a reference unit in the register,
    # because things like `centi(centi(metre))` are not permitted.
    if not unit is register.reference_unit_for(unit.scale.kind_of_quantity):
        raise RuntimeError(
            "{!r} is not a reference unit".format(unit.scale.name)  
        )     

    name = "{!s}{!s}".format(
        prefix.name,
        unit.scale.name
    )
    
    if name in register:
        return register[name]
    else:
        term = "{!s}{!s}".format(
            prefix.term,
            unit.scale
        )
        
        pq = Unit(
            kind_of_quantity,
            name,
            term,
            register,
            prefix.value
        )
        
        # Buffer related quantities        
        register._register_by_name(pq)
        
        return pq 