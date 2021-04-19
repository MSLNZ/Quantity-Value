from __future__ import division 
import numbers 
 
__all__ = ( 'Scale', )

#----------------------------------------------------------------------------
class Scale(object):

    """
    Measured values of a quantity are reported on a scale.  
    For example, the SI scale for length measurement is the metre.   
        
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
    def name(self):
        """The quantity name"""
        return self._name
        
    @property 
    def symbol(self):
        """Short name for the quantity"""
        return self._symbol
        
    @property 
    def kind_of_quantity(self):
        """The associated kind of quantity"""
        return self._kind_of_quantity
  


# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )