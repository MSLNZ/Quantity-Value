from functools import partial 

from QV.kind_of_quantity import KindOfQuantity
from QV.registered_unit import RegisteredUnit 
from QV.units_dict import UnitsDict
from QV.scale import RatioScale, IntervalScale

__all__ = (
    'UnitRegister', 'proportional_unit'
)

#----------------------------------------------------------------------------
class UnitRegister(object):

    """
    A UnitRegister holds mappings between a kind-of-quantity,
    a type of scale and a collection of units.
    
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
        
        # KoQ objects - keys; RegisteredUnit objects - values
        # The first registered unit for a koq is the reference 
        # unit: this may NOT be changed!!
        # Only ratio scales can be reference units 
        self._koq_to_ref_unit = dict()
        
        # A mapping of symbols for pairs of scales to a 
        # function that converts between those scales 
        self._conversion_fn = dict()            
                
        # There must always be a unit for numbers and it is a 
        # special case because the name and symbol are blank
        Number = context['Number']
        unity = RegisteredUnit( self, RatioScale(Number,'','') )        
        self._koq_to_ref_unit[Number] = unity       
        self._koq_to_units_dict[Number] = {
            RatioScale: UnitsDict({ 'unity': unity }) 
        }

        # Need to know if a unit has been registered 
        self._registered_units = set()
        
    def __str__(self):
        return self._name

    def __repr__(self):
        return "{!s}({!s})".format(
            self.__class__.__name__,
            self._name
        )

    def __contains__(self,u):
        return u in self._registered_units 
        
    @property
    def context(self):        
        return self._context     
    
    def reference_unit_for(self,expr):
        """
        Return the reference unit for `expr`
        
        `expr` can be a product or quotient of registered-units 
        or a product or quotient of kind-of-quantity objects
        or a registered-unit or a kind-of-quantity object.

        """  
        assert type(expr.scale) is RatioScale, repr(expr.scale) 
        
        if isinstance(expr,KindOfQuantity):
            return self._koq_to_ref_unit[expr] 
            
        elif isinstance(expr,RegisteredUnit):
            return self._koq_to_ref_unit[expr.kind_of_quantity]
            
        elif hasattr(expr,'kind_of_quantity'):
            # A registered-unit expression, so here we expose 
            # the corresponding koq expression
            expr = expr.kind_of_quantity
            
        if hasattr(expr,'execute'):
            # A kind-of-quantity expression so, we resolve the expression
            koq = self.context._signature_to_koq( 
                self.context._evaluate_signature( expr ) 
            )
            return self._koq_to_ref_unit[koq]
            
        else:
            raise RuntimeError(
                "{!r} unexpected".format(expr)
            )                      
        
    def unit_dict_for(self,expr):
        """
        Return the units associated with the kind of quantity of `expr`
        
        `expr` can be a product or quotient of registered-units, 
        a product or quotient of kind-of-quantity objects,
        or a registered-unit or a kind-of-quantity object.
        
        """
        scale_type = type(expr.scale) 

        # If `expr` has the `kind_of_quantity` attribute then  
        # it is a registered unit or a unit expression. 
        # In the first case, we can obtain a kind-of-quantity  
        # directly so immediately look up the unit.
        # In the second case, the expression must be evaluated.
        # If `expr` has the `execute` attribute then it is a 
        # kind-of-quantity expression.
        if isinstance(expr,KindOfQuantity):
            return self._koq_to_units_dict[expr] 
            
        elif isinstance(expr,RegisteredUnit):
            return self._koq_to_units_dict[expr.kind_of_quantity]
                  
        elif hasattr(expr,'kind_of_quantity'):
            expr = expr.kind_of_quantity
            
        if hasattr(expr,'execute'):
            # A kind-of-quantity expression so, we resolve the expression
            koq = self.context._signature_to_koq( 
                self.context._evaluate_signature( expr ) 
            )
            return self._koq_to_units_dict[koq]
            
        else:
            raise RuntimeError(
                "{!r} unexpected".format(expr)
            )        

    # These handy access methods have become problematic 
    # with the introduction of different types of scale. 
    # For now, get and getattr use RatioScale
    # and getitem is not available.
    
    # Only for RatioScales
    def __getattr__(self,koq_name):
        koq = getattr(self._context,koq_name)
        
        if koq in self._koq_to_units_dict:  
            return self._koq_to_units_dict[ koq ][RatioScale]
        else:
            raise AttributeError(
                "{!r} not found".format(koq)
            )
    
    # # Returns a dict, indexed by scale type, of UnitsDicts
    # def __getitem__(self,koq):
        # if isinstance(koq,str):
            # koq = self._context[koq]
            
        # return self._koq_to_units_dict[koq]
                
    def get(self,koq,scale_type=RatioScale):
        """
        """
        if isinstance(koq,str):
            koq = self._context[koq]
          
        default = {
            RatioScale: UnitsDict({}),
            IntervalScale: UnitsDict({})
        }
        
        return self._koq_to_units_dict.get(
            koq,
            default
        )[scale_type]
                    
    def _register_unit(self,unit):
         
        koq = unit.scale.kind_of_quantity
        scale_type = type(unit.scale)
        
        if koq not in self._koq_to_ref_unit and scale_type is RatioScale:
            self._koq_to_ref_unit[koq] = unit

        # Update or initialise the dict for koq
        if koq in self._koq_to_units_dict:           
            if scale_type in self._koq_to_units_dict[koq]:
                units_dict = self._koq_to_units_dict[koq][scale_type]
                units_dict.update({ 
                    unit.scale.name: unit, 
                    unit.scale.symbol: unit 
                })
            else:
                self._koq_to_units_dict[koq][scale_type] = UnitsDict({ 
                    unit.scale.name: unit, 
                    unit.scale.symbol: unit 
                })
        else:
            self._koq_to_units_dict[koq] = {
                scale_type: UnitsDict({ 
                    unit.scale.name: unit, 
                    unit.scale.symbol: unit 
                })
            }         
        self._registered_units.add(unit)
        
    def unit(self,scale):
        """
        Register a new scale as a unit 
        
        The associated kind of quantity must not 
        already have a scale with the same name or symbol 
        
        """
        scale_type = type(scale)
        
        units_dict = self._koq_to_units_dict.get(
            scale.kind_of_quantity,
            UnitsDict({})
        )

        if (
            scale.name in units_dict  
        or  scale.symbol in units_dict
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
        Register a function to convert from scale `A` to `B` 
        
        """
        src_koq = A.scale.kind_of_quantity
        dst_koq = B.scale.kind_of_quantity
        
        if not src_koq is dst_koq:
            raise RuntimeError(
                "{} and {} are different kinds of quantity".format(
                src_koq,dst_koq)
            )
            
        # If A and B are both ratio scales then a single value is needed.
        # If A or B two is an interval scale the offset values and a 
        # scale factor are needed.
        
        type_A = type(A.scale)
        type_B = type(B.scale)
        if type_A is RatioScale and type_B is RatioScale:
            full_fn = RatioScale.value_conversion_function()
            
        elif type_A is IntervalScale or type_B is IntervalScale:
            full_fn = IntervalScale.value_conversion_function()
            
        else:
            # Ordinal and nominal scales are not yet covered.
            raise RuntimeError(
                "{!r} or {!r} are not supported".format(A.scale,B.scale)
            )

        # This applies the conversion parameter values but leaves `x`
        partial_fn = partial(full_fn,*args)
        self._conversion_fn[(A.scale.symbol,B.scale.symbol)] = partial_fn        
        
    def conversion_from_A_to_B(self,A,B):
        """
        Return a conversion function for scale `A` to `B` 
        
        The function takes a single quantity-value argument `x` 
        on `A` and returns a quantity-value result on `B`
        
        """
        if A.scale.symbol == B.scale.symbol:
            return lambda x: x
            
        # For ratio scales we may use the `conversion_factor` information 
        # in the Scale objects to find the conversion factor.
        # This avoids the need to register lots of functions.
        if type(A.scale) is RatioScale and type(B.scale) is RatioScale:            
            factor = A.scale.conversion_factor / B.scale.conversion_factor
            return lambda x: factor*x 
            
        if not isinstance(A,RegisteredUnit):
            raise RuntimeError(
                "unregistered unit: {!r}".format(A)
            )
            
        return A.conversion_to(B)

#----------------------------------------------------------------------------
def proportional_unit(unit,name,symbol,conversion_factor):
    """
    Declare a scale proportional to a unit already registered 
    
    """
    register = unit.register 
    scale = unit.scale

    if not isinstance(scale,RatioScale):
        raise RuntimeError(
            "cannot apply a conversion factor to {!r}".format(scale) 
        )
        
    if not hasattr(unit,'register'):
        raise RuntimeError(
            "`unit` must be registered"
        )
    
    # The derived scale is the same type and quantity
    s = scale.__class__(scale.kind_of_quantity,name,symbol)

    if register.reference_unit_for(unit) is unit:
        # The multiplier converts to the reference scale 
        s.conversion_factor = conversion_factor 
        
    else:
        s.conversion_factor = conversion_factor / scale.conversion_factor 
    
    return s
        
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )