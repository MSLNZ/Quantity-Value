import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from kind_of_quantity import Numeric 
from quantity import Unit 

__all__ = (
    'UnitSystem',
)
#----------------------------------------------------------------------------
class UnitSystem(object):

    """
    A unit system holds a 1-to-1 bi-directional map between KindOfQuantity 
    instances and Unit instances. Such as Length <-> metre.
    It also maps 1-to-1 between unit names and unit objects. Such as, 
    `SI.centimetre` or `SI['centimetre']`
    """
    
    def __init__(self,name,unit_class):
        self._name = name
        
        self._register = bidict()   # koq <-> unit
        self._name_to_unit = dict() # unit name -> unit
        
        self._unit_cls = unit_class
            
        # There must be a unit for numbers
        unity = unit_class(Numeric,'','')
        
        # Do registration explicitly, because unit.name = ""
        unity.system = self 
        self._register[Numeric] = unity
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
            # Assume a koq or koq expression
            koq = expr 
            
        context = koq.context
        if hasattr(koq,'execute'):
            koq = context.evaluate( koq )
            
        return self._register.get(koq,None)        
  
    def __contains__(self,name):
        return name in self._name_to_unit 
        
    def __getitem__(self,name):
        return self._name_to_unit[name]
        
    def get(self,kind_of_quantity,default=None):
        try:
            return self.__getitem__(kind_of_quantity)
        except KeyError:
            return default 
            
    def register(self,unit):
        # key: koq; value: unit
        koq = unit._kind_of_quantity
        
        if koq in self._register: 
            if not self._register[koq] is unit:
                raise RuntimeError(
                    "{!r} is already registered".format(koq)
                )
        else:
            unit.system = self 
            self._register[koq] = unit 
            self._register_by_name(unit)
            
    def _register_by_name(self,unit):
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
        
    def unit(self,kind_of_quantity,name,term):
        """
        Create a reference unit for `kind_of_quantity`
        """
        u = self._unit_cls(kind_of_quantity,name,term)
        self.register(u) 
        return u
  
    def from_to(self,source_unit,target_unit):
        """
        Conversion factor for `source_unit` to `target_unit`
        """
        assert source_unit.name in self,\
            "{!r} is not registered in this system".format(source_unit)
        assert target_unit.name in self,\
            "{!r} is not registered in this system".format(target_unit)
            
        src_koq = source_unit._kind_of_quantity
        dst_koq = target_unit._kind_of_quantity
        if not src_koq is dst_koq:
            raise RuntimeError(
                "{} and {} are different quantities".format(src_koq,dst_koq)
            )
            
        multiplier = target_unit.multiplier         # ref * k_dst -> unit_dst
        multiplier /= source_unit.multiplier        # unit_dst / unit_src -> k_dst / k_src
        
        return multiplier 
       