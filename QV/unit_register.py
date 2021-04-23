from __future__ import division 

from functools import partial 

# `UnitRegister` does not represent the concept of a 'system of units'. 
# Different types of units belong in different systems, like the SI 
# would have m, cm, km, etc, and Imperial would have the foot, yard,
# etc. However, all those length scales are "self-similar" in the 
# sense that a scale factor converts from one to the other.
 
from QV.registered_unit import RegisteredUnit 
from QV.units_dict import UnitsDict

__all__ = (
    'UnitRegister', 
)

#----------------------------------------------------------------------------
class UnitRegister(object):

    """
    A UnitRegister holds associations between a kind-of-quantity and units.
    
    A distinction is made between a reference unit and other related units 
    for the same kind of quantity. There can be only one reference unit 
    in the register for each kind of quantity.  
    """ 
    
    def __init__(self,name,context):
        
        self._name = name
        
        # Needed to resolve KoQ objects from names
        self._context = context
        
        # KoQ objects - keys; UnitsDict() - values
        # The UnitsDict is a mapping of scale names 
        # and scale symbols to the corresponding 
        # RegisteredUnit object.
        self._koq_to_units_dict = dict()
        
        # A mapping of scale-symbol pairs to a 
        # function that converts between scales 
        self._conversion_fn = dict()            
                
        # # There must always be a unit for numbers and it is a 
        # # special case because the name and symbol are blank
        # Number = context['Number']
        # unity = RegisteredUnit(Number,'','',self,1)        
        # # self._koq_to_ref_unit[Number] = unity       
        # self._koq_to_units_dict[Number] = UnitsDict({ 'unity': unity })          
        
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
        
    def unit_for(self,expr):
        """
        Return the reference unit for `expr`
        
        `expr` can be a product or quotient of units, 
        a product or quotient of kind-of-quantity objects,
        or a kind-of-quantity object.
        
        """
        # If `expr` has the `kind_of_quantity` attribute then  
        # it is a unit or a unit expression. 
        # In the first case, we can obtain a kind-of-quantity  
        # directly so immediately look up the unit.
        # In the second case, the expression must be evaluated.
        # If `expr` has the `execute` attribute then it is a 
        # kind-of-quantity expression.
        
        if hasattr(expr,'kind_of_quantity'):
            koq = expr.kind_of_quantity
        else:
            koq = expr 
            
        if hasattr(koq,'execute'):
            # A koq expression
            koq = self.context._signature_to_koq( 
                self.context._evaluate_signature( koq ) 
            )
            
        return self._koq_to_ref_unit[koq]        

    def __getattr__(self,koq_name):
        # Convert koq_name to koq object
        koq = getattr(self._context,koq_name)
        # koq = self._context[koq_name]
        
        if koq in self._koq_to_units_dict:  
            return self._koq_to_units_dict[ koq ]
        else:
            raise AttributeError(
                "{!r} not found".format(koq)
            )
    
    def __getitem__(self,koq):
        if isinstance(koq,str):
            koq = self._context[koq]
            
        return self._koq_to_units_dict[koq]
                
    def get(self,koq):
        """
        Return a mapping of names and symbols to units for ``kind_of_quantity``
        """
        if isinstance(kind_of_quantity,str):
            kind_of_quantity = self._context[koq]
           
        return self._koq_to_units_dict.get(
            kind_of_quantity,
            UnitsDict({})
        )
            
    def __contains__(self,unit):
        
        units_dict = self._koq_to_units_dict.get(
            unit.scale.kind_of_quantity,
            UnitsDict({})
        )

        return (
            unit.scale.name in units_dict or 
            unit.scale.symbol in units_dict
        )
        
    def _register_unit(self,unit):
         
        # if unit in self:
            # raise RuntimeError(
                # "{!r} is already registered: {!r}".format(
                    # unit.scale.name,
                    # self._koq_to_units_dict[unit.scale.name]
                # )
            # )
        # else:
        koq = unit.scale.kind_of_quantity

        # Update or initialise the UnitsDict for koq
        if koq in self._koq_to_units_dict:
            units_dict = self._koq_to_units_dict[koq]           
            units_dict.update({ 
                unit.scale.name: unit, 
                unit.scale.symbol: unit 
            })
        else:
            self._koq_to_units_dict[koq] = UnitsDict({ 
                unit.scale.name: unit, 
                unit.scale.symbol: unit 
            })
                     
    def unit(self,scale):
        """
        
        """
        units_dict = self._koq_to_units_dict.get(
            scale.kind_of_quantity,
            UnitsDict({})
        )

        if (
            scale.name in units_dict or 
            scale.symbol in units_dict
        ):
            raise RuntimeError(
                "{!r} is already a registered unit for {!r}".format(
                    scale.name,
                    scale.kind_of_quantity
                )
            )

        u = RegisteredUnit(self,scale)
        self._register_unit( u ) 
        
        return u
  
    def conversion_function_values(self,A,B,*args):
        """
        Configure a function to convert from scale `A` to `B` 
        
        """
        src_koq = A.scale.kind_of_quantity
        dst_koq = B.scale.kind_of_quantity
        
        if not src_koq is dst_koq:
            raise RuntimeError(
                "{} and {} are different kinds of quantity".format(
                src_koq,dst_koq)
            )

        # Need to relax this constraint and allow 
        # conversion between interval and ratio scales
        # But put the control in the scales module.
        if not type(A.scale) is type(B.scale):
            raise RuntimeError(
                "{} and {} are different scale types".format(
                A.scale,B.scale)
            )

        full_fn = A.scale.conversion_function
        partial_fn = partial(full_fn,*args)
        self._conversion_fn[(A.scale.symbol,B.scale.symbol)] = partial_fn
        
    def conversion_from_A_to_B(self,A,B):
        """
        Return the conversion function from scale `A` to `B` 
        
        The function takes a single quantity-value argument `x` 
        and returns a quantity-value result
        
        """
        key = (A.scale.symbol,B.scale.symbol)            
        if key in self._conversion_fn:
            return self._conversion_fn[ key ]  
        else:
            raise RuntimeError(
                "no conversion available for {0[0]!r} to {0[1]!r}".format(key)
            ) 

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )