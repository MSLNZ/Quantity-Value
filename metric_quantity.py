from quantity import *

__all__ = ( 
    'MetricUnit',
    'MetricPrefix',
)

#----------------------------------------------------------------------------
class MetricUnit(Unit):

    """
    A metric unit may have a metric prefix applied. Such as decilitre, 
    centimetre, etc.
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
        
#----------------------------------------------------------------------------
class MetricPrefix(object):
    
    def __init__(self,name,term,value):
        self.name = name 
        self.term = term 
        self.value = value
        
    def __repr__(self):
        return "{!s}({!r},{!r},{:.0E})".format(
            self.__class__.__name__,
            self.name,
            self.term,
            self.value
        )
        
    def __str__(self):
        return str(self.term) 
        
    def __call__(self,quantity):
        return quantity._apply_prefix(self)
        
        


