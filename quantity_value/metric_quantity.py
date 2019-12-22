from quantity import *

__all__ = ( 
    'MetricUnit',
)

#----------------------------------------------------------------------------
# The special feature of MetricUnit is that metric prefixes can be
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
    
    def __init__(self,kind_of_quantity,name,term,system,multiplier=1):
        super(MetricUnit,self).__init__(
            kind_of_quantity,
            name,
            term,
            system,
            multiplier
        )    

    def _apply_prefix(self,prefix):
        # Things like `centi(centi(metre))` are not permitted
        # So check that `self` is a reference unit in the system.
        if not self is self.system.reference_unit_for(self.kind_of_quantity):
            raise RuntimeError(
                "Illegal operation: '{}' already has a prefix".format(self.name)  
            )     
            
        name = "{!s}{!s}".format(
            prefix.name,
            self.name
        )
        
        if name in self.system:
            return self.system[name]
        else:
            term = "{!s}{!s}".format(
                prefix.term,
                self
            )
            
            pq = MetricUnit(
                self._kind_of_quantity,
                name,
                term,
                self.system,
                prefix.value
            )
            
            # Buffer related quantities        
            self.system._register_by_name(pq)
            
            return pq 
    
# #----------------------------------------------------------------------------
# class PrefixedMetricUnit(MetricUnit):

    # """
    # A PrefixedMetricUnit is related to a reference unit of the same 
    # kind of quantity in the unit system by a multiplier. 
    # Such as, centimetre to metre.
    
    # Instances are only created by MetricUnit
    # """
    
    # def __init__(self,kind_of_quantity,name,term,system,multiplier): 
        # super(PrefixedMetricUnit,self).__init__(
            # kind_of_quantity,
            # name,
            # term 
        # )
        # self._multiplier = multiplier
        # self.system = system        
                
    # def __repr__(self):
        # return "{!s}({!s},{!s},{!s},{})".format(
            # self.__class__.__name__,
            # self._kind_of_quantity.name,
            # self.name,
            # self,
            # self._multiplier
        # )
        
    # def _apply_prefix(self,prefix):
        # # Things like `centi(centi(metre))` are not permitted
        # raise RuntimeError(
            # "Illegal operation: '{}' already has a prefix".format(self.name)  
        # )
        


