from quantity import *

__all__ = ( 
    'MetricUnit',
)

#----------------------------------------------------------------------------
# The only special feature of MetricUnit is that the metric prefixes can be
# applied to create related units. Those related units cannot have the 
# same prefixes applied. This functionality could be implemented in the same 
# way as in rational_unit.py, with a function instead of methods.
#
class MetricUnit(Unit):

    """
    A MetricUnit will represent the reference unit for a kind of quantity.
    A metric prefix may be applied to a MetricUnit object to define related  
    (PrefixedMetricUnit) units. Such as decilitre, centimetre, etc.
    """
    
    def __init__(self,kind_of_quantity,name,term):
        super(MetricUnit,self).__init__(
            kind_of_quantity,
            name,
            term
        )    
        
        self._prefixed_quantities = dict() 
        self._multiplier = 1        

    def _apply_prefix(self,prefix):
            
        try:
            return self._prefixed_quantities[prefix]
            
        except KeyError:
            
            term = "{!s}{!s}".format(
                prefix,
                self
            )
            name = "{!s}{!s}".format(
                prefix.name,
                self.name
            )
            
            pq = PrefixedMetricUnit(
                self._kind_of_quantity,
                name,
                term,
                self.system,
                prefix.value
            )
            
            # Buffer related quantities        
            self._prefixed_quantities[prefix] = pq 
            self.system._register_by_name(pq)
            
            return pq 
    
#----------------------------------------------------------------------------
class PrefixedMetricUnit(MetricUnit):

    """
    A PrefixedMetricUnit is related to a reference unit of the same 
    kind of quantity in the unit system by a multiplier. 
    Such as, centimetre to metre.
    
    Instances are only created by MetricUnit
    """
    
    def __init__(self,kind_of_quantity,name,term,system,multiplier): 
        super(PrefixedMetricUnit,self).__init__(
            kind_of_quantity,
            name,
            term 
        )
        self._multiplier = multiplier
        self.system = system        
                
    def __repr__(self):
        return "{!s}({!s},{!s},{!s},{})".format(
            self.__class__.__name__,
            self._kind_of_quantity.name,
            self.name,
            self,
            self._multiplier
        )
        
    def _apply_prefix(self,prefix):
        # Things like `centi(centi(metre))` are not permitted
        raise RuntimeError(
            "Illegal operation: '{}' already has a prefix".format(self.name)  
        )
        


