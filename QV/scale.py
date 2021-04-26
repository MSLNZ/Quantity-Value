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
    An :class:`.IntervalScale` has an arbitrary origin.
    Units associated with an interval scale may not be 
    multiplied or divided.
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        OrdinalScale.__init__(self,kind_of_quantity,name,symbol)

    @property 
    def conversion_function(self):
        """
        The generic conversion function from one interval scale to another 
  
        Example::
        
            >>> quantity = Context( ("Temperature","t") )
            >>> ureg = UnitRegister("ureg",quantity)
            >>> kelvin = ureg.unit( RatioScale(quantity.Temperature,'kelvin','K') ) 
            >>> Celsius = ureg.unit( RatioScale(quantity.Temperature,'Celsius','C') ) 
            >>> ureg.conversion_function_values(kelvin,Celsius,1,0,-273.15)
            >>> degrees_C = ureg.conversion_from_A_to_B(kelvin,Celsius)
            >>> print( degrees_C( 273.15 ), Celsius )
            0.0 C
  
        """
        # `k` is a conversion factor, 
        # `o_A` is the offset on the source scale and 
        # `o_B` is the offset on the target scale,  
        # `x` is a value on the source scale 
        return lambda k,o_A,o_B,x: k*(x - o_A) + o_B
        
#----------------------------------------------------------------------------
class RatioScale(IntervalScale):

    """
    A :class:`.RatioScale` is a metric scale. 
    Units associated with a ratio scale may be multiplied and divided, 
    resulting in derived units. 
    """
    
    def __init__(self,kind_of_quantity,name,symbol,conversion_factor=None):
        IntervalScale.__init__(self,kind_of_quantity,name,symbol)
        
        if conversion_factor is not None: 
            self._conversion_factor = conversion_factor 
 
    # The conversion factor relates to a designated reference 
    # scale for the same quantity. It is immutable. 
    @property 
    def conversion_factor(self):
        """
        Return a conversion factor for a value 
        on this scale to one on the reference scale 
        
        """
        try:
            return self._conversion_factor
        except AttributeError:
            return 1.0 
            
    @conversion_factor.setter 
    def conversion_factor(self,value):
        if not hasattr(self,'_conversion_factor'):
            self._conversion_factor = value
        else:
            raise RuntimeError(
                "{!r} already has a conversion factor: {}".format(
                    self,self._conversion_factor
                )
            )
            
    @property 
    def conversion_function(self):
        """
        The generic conversion function from one ratio scale to another 
        
        """
        # `k` is a conversion factor from the source to target scale, 
        # `x` is a value on the scale 
        return lambda k,x: k*x 
        
    def __mul__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )
        
        koq = self.kind_of_quantity*rhs.kind_of_quantity
        name = self.name+"*{!s}".format(rhs.name)
        symbol = self.symbol+"*{!s}".format(rhs.symbol)
        factor = self.conversion_factor*rhs.conversion_factor 
        
        return RatioScale(koq,name,symbol,factor)
        
    def __truediv__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )

        koq = self.kind_of_quantity/rhs.kind_of_quantity
        name = self.name+"/({!s})".format(rhs.name)
        symbol = self.symbol+"/({!s})".format(rhs.symbol)
        factor = self.conversion_factor/rhs.conversion_factor 
        
        return RatioScale(koq,name,symbol,factor)
        
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