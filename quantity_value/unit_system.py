from __future__ import division 

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from fractions import *

from quantity import Unit 

__all__ = (
    'UnitSystem', 'rational_unit'
)

#----------------------------------------------------------------------------
class UnitSystem(object):

    """
    A unit system holds a 1-to-1 bi-directional map between KindOfQuantity 
    instances and reference Unit instances. Such as Length <-> metre.
    UnitSystem objects also behave like a map from unit names to unit objects. 
    Such as, `SI.metre` or `SI['metre']` or `'metre' in SI`.
    """
    
    def __init__(self,name,context):
        self._name = name
        self._context = context
        
        self._register = bidict()   # koq <-> unit
        self._name_to_unit = dict() # unit name -> unit
        
        # There must be a unit for numbers
        unity = Unit(context['Numeric'],'','',self,1)        
        self._register[context['Numeric']] = unity
        self._name_to_unit['unity'] = unity
        self.__dict__['unity'] = unity 
            
    def __str__(self):
        return self._name

    def __repr__(self):
        return "{!s}({!s})".format(
            self.__class__.__name__,
            self._name
        )

    def has_unit_for(self,kind_of_quantity):
        return kind_of_quantity in self._register 
        
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
        # In the second case, we obtain a kind-of-quantity
        # expression that must be evaluated first.
        # If `expr` has `execute` it is a kind-of-quantity
        # expression that must be evaluated.
        if hasattr(expr,'kind_of_quantity'):
            koq = expr.kind_of_quantity
        else:
            # Assume a koq or a koq expression
            koq = expr 
            
        context = koq.context
        if hasattr(koq,'execute'):
            koq = context.evaluate( koq )
            
        return self._register.get(koq,None)        
  
    def __contains__(self,name):
        return name in self._name_to_unit 
        
    def __getitem__(self,name):
        return self._name_to_unit[name]
        
    def get(self,name,default=None):
            return self._name_to_unit.get(name,default)
            
    def _register_reference_unit(self,unit):
        # key: koq; value: unit
        koq = unit._kind_of_quantity
        
        if koq in self._register: 
            if not self._register[koq] is unit:
                raise RuntimeError(
                    "{!r} is already registered".format(koq)
                )
        else:
            self._register[koq] = unit 
            self._register_by_name(unit)
            
    def _register_by_name(self,unit):
        # This can contain all units, not just reference ones,
        # provided their names are distinct dictionary keys
        if unit.name in self._name_to_unit:
            raise RuntimeError(
                "The name {!s} registered to {!r}".format(
                    unit.name,
                    self._name_to_unit[unit.name]
                )
            )
            
        assert not unit.name in self.__dict__,\
            "{!s} is a reserved name".format(unit.name)
 
        self._name_to_unit[unit.name] = unit
        self.__dict__[unit.name] = unit 
 
    def kind_of_quantity(self,unit):
        return self._register.inverse[unit]
            
    def unit(self,koq_name,unit_name,unit_term):
        """
        Create a reference unit in this system for `kind_of_quantity`
        The unit will be identified by `name`, and abbreviation `term`.
        """
        koq = self._context._koq_name[koq_name]
        
        # Reference units all have multiplier = 1
        u = Unit(koq,unit_name,unit_term,self,multiplier=1)
        self._register_reference_unit(u) 
        
        return u
  
    def from_to(self,source_unit,target_unit):
        """
        Return a multiplier to convert from `source_unit` to `target_unit`
        """
        assert source_unit.name in self,\
            "{!r} is not registered".format(source_unit)
            
        assert target_unit.name in self,\
            "{!r} is not registered".format(target_unit)
            
        src_koq = source_unit._kind_of_quantity
        dst_koq = target_unit._kind_of_quantity
        if not src_koq is dst_koq:
            raise RuntimeError(
                "{} and {} are different kinds of quantity".format(src_koq,dst_koq)
            )
            
        multiplier = target_unit.multiplier         # ref * k_dst -> unit_dst
        multiplier /= source_unit.multiplier        # unit_dst / unit_src -> k_dst / k_src
        
        return multiplier 
       
#----------------------------------------------------------------------------
def rational_unit(unit,fraction,name,term):
    """
    Define and register a rational multiple of a system  
    reference unit for the same quantity.
    
    """
    kind_of_quantity = unit._kind_of_quantity
    system = unit._system 

    if not unit is system.reference_unit_for(unit.kind_of_quantity):
        raise RuntimeError(
            "Illegal operation: '{}' is not a reference unit in this system".format(unit.name)  
        )     

    if name in system:
        return system[name]
    else:
        rational_unit = Unit(
            kind_of_quantity,
            name,
            term,
            system,
            Fraction( fraction )
        )
        system._register_by_name(rational_unit)
        
        return rational_unit
        
#----------------------------------------------------------------------------
def metric_unit(prefix,unit):
    """
    Define a metric multiple of a system  
    reference unit for the same quantity.
    
    """
    kind_of_quantity = unit._kind_of_quantity
    system = unit._system 

    # Things like `centi(centi(metre))` are not permitted
    # So check that `self` is a reference unit in the system.
    if not unit is system.reference_unit_for(unit.kind_of_quantity):
        raise RuntimeError(
            "Illegal operation: '{}' is not a reference unit in this system".format(unit.name)  
        )     

    name = "{!s}{!s}".format(
        prefix.name,
        unit.name
    )
    
    if name in system:
        return system[name]
    else:
        term = "{!s}{!s}".format(
            prefix.term,
            unit
        )
        
        pq = Unit(
            kind_of_quantity,
            name,
            term,
            system,
            prefix.value
        )
        
        # Buffer related quantities        
        system._register_by_name(pq)
        
        return pq 