__all__ = ( 'Scale', 'OrdinalScale', 'IntervalScale', 'RatioScale', )

#----------------------------------------------------------------------------
# 'Scale' is a nominal scale 
#
class Scale(object):

    """
    A Scale has a name (and a short name, or symbol) 
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
        return hash( 
            ( self._name, self._symbol, id(self.__class__) ) 
        )
        
    # Equality of scales means their names and types agree
    # So, Celsius on a ratio scale is different from 
    # an interval scale.
    def __eq__(self,other):
        return (
            self._name == other.name 
        and 
            self._symbol == other.symbol 
        and
            self.__class__ is other.__class__
        ) 
        
    def __str__(self):
        return self._symbol
       
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
        
#----------------------------------------------------------------------------
class IntervalScale(OrdinalScale):

    """
    An :class:`.IntervalScale` has an arbitrary origin.
    Units associated with an interval scale may not be 
    multiplied or divided.
    """
    
    def __init__(self,kind_of_quantity,name,symbol):
        OrdinalScale.__init__(self,kind_of_quantity,name,symbol)

    @staticmethod
    def value_conversion_function():
        """
        Generic conversion function from one interval scale to another 
        
        """     
        return lambda factor,offset,x: factor*x + offset
        
#----------------------------------------------------------------------------
# Quantity calculus applies to entities measured on ratio scales, so we 
# may arbitrarily generate products and quotients, which are derived scales.
# The mechanics of KindOfQuantity and Signature are used to resolve 
# the derived quantity; no attempt is made to keep track of the 
# corresponding unit. Instead, values are re-scaled to a reference unit 
# for each term and the scale factor for the final conversion is built up
# as the calculation proceeds, using `conversion_factor`. At the same time, 
# a string of the unit  names and symbols is assembled, so that it will be 
# possible to read  how a temporary object has been constructed, 
# before being converted to a registered unit of the appropriate kind.
#
class RatioScale(IntervalScale):

    """
    A :class:`.RatioScale` is a metric scale. 
    Units may be multiplied and divided. 
    """
    
    def __init__(self,kind_of_quantity,name,symbol,conversion_factor=None):
        IntervalScale.__init__(self,kind_of_quantity,name,symbol)
        
        if conversion_factor is not None: 
            self._conversion_factor = conversion_factor 
 
    # The conversion factor converts to the reference 
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
 
    @staticmethod
    def value_conversion_function():
        """
        Generic conversion function from one ratio scale to another 
        
        """
        return lambda factor,x: factor*x
   
    def __mul__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )
        
        koq = self.kind_of_quantity*rhs.kind_of_quantity
        name = "({!s}*{!s})".format(self.name,rhs.name)
        symbol = "({!s}*{!s})".format(self.symbol,rhs.symbol)
        factor = self.conversion_factor*rhs.conversion_factor 
        
        return RatioScale(koq,name,symbol,factor)
        
    def __truediv__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )

        koq = self.kind_of_quantity/rhs.kind_of_quantity
        name = "({!s}/{!s})".format(self.name,rhs.name)
        symbol = "({!s}/{!s})".format(self.symbol,rhs.symbol)
        factor = self.conversion_factor/rhs.conversion_factor 
        
        return RatioScale(koq,name,symbol,factor)
        
    def __floordiv__(self,rhs):
        if not isinstance(rhs,RatioScale): 
            raise RuntimeError(
                "Incompatible scales: {!r} and {!r}".format(self,rhs)
            )
 
        koq = self.kind_of_quantity//rhs.kind_of_quantity
        name = "({!s}//{!s})".format(self.name,rhs.name)
        symbol = "({!s}//{!s})".format(self.symbol,rhs.symbol)
        factor = self.conversion_factor/rhs.conversion_factor 
 
        return RatioScale(koq,name,symbol,factor)

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )