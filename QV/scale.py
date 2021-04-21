from __future__ import division 
import numbers 
 
__all__ = ( 'Scale', 'OrdinalScale', 'IntervalScale', 'RatioScale',)

#----------------------------------------------------------------------------
# In Stevens' classification 'Scale' is the nominal scale 
#
class Scale(object):

    """
    A Scale object has a name (and a short name, or symbol) 
    and contains a reference to the associated kind of quantity.
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        self._kind_of_quantity = kind_of_quantity
        self._name = str(name)
        self._symbol = str(symbol)

    def __repr__(self):
        return "{!s}({!r},{!r},{!r})".format(
            self.__class__.__name__,
            self.kind_of_quantity,
            self._name,
            self._symbol
        )
        
    # __hash__ and __eq__ are required for mapping keys
    # __eq__ also needed as a nominal scale property 
    def __hash__(self):
        return hash( ( self._name, self._symbol ) )
        
    def __eq__(self,other):
        return (
            self._name == other.name 
        and 
            self._symbol == other.symbol 
        ) 
        
    def __str__(self):
        return self._symbol
        
    @property 
    def conversion_function(self):
        raise NotImplementedError()

    @property 
    def name(self):
        return self._name
        
    @property 
    def symbol(self):
        return self._symbol
        
    @property 
    def kind_of_quantity(self):
        return self._kind_of_quantity
  
#----------------------------------------------------------------------------
class OrdinalScale(Scale):

    """
    
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        Scale.__init__(self,kind_of_quantity,name,symbol)

    @property 
    def conversion_function(self):
        raise NotImplementedError()
        
#----------------------------------------------------------------------------
class IntervalScale(OrdinalScale):

    """
    
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        OrdinalScale.__init__(self,kind_of_quantity,name,symbol)

    @property 
    def conversion_function(self):
        """
        Return a generic conversion function from one scale to another 
        
        """
        # `k` is a conversion factor, 
        # `o_A` is the offset on the source scale and 
        # `o_B` is the offset on the target scale,  
        # `x` is a value on the source scale 
        return lambda k,o_A,o_B,x: k*(x - o_A) + o_B
        
#----------------------------------------------------------------------------

# TODO: allow a scale to carry a flag that can be prefixed? 
# By default no, but base SI units could be?


class RatioScale(IntervalScale):

    """
    
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        IntervalScale.__init__(self,kind_of_quantity,name,symbol)
        
    @property 
    def conversion_function(self):
        """
        Return a generic conversion function from one scale to another 
        
        """
        # `k` is a conversion factor from the source to target scale, 
        # `x` is a value on the scale 
        return lambda k,x: k*x 
        
    def __mul__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )
        
    def __div__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )

    def __floordiv__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )