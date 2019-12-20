from __future__ import print_function
from __future__ import division 

try:
    from itertools import zip_longest                   # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest   # Python 2

__all__ = (
    'Dimension',
)

#----------------------------------------------------------------------------
class Dimension(object):

    """
    Dimension holds the dimensional exponents of a KindOfQuantity instance. 
    
    Multiplication and division of Dimension adds and subtracts dimensional 
    exponents, but there is also provision made to retain the dimension 
    of 'dimensionless' quantities as a ratio.
    
    Dimension objects may be used as keys in Python dictionaries.
    """
    
    def __init__(self,numerator,denominator=()):
        self.numerator = tuple(numerator) 
        self.denominator = tuple(denominator)
       
    def __repr__(self):
        if not self.denominator:
            return "{!s}{!r}".format(
                self.__class__.__name__,
                self.numerator
            )
        else:
            return "{!s}{!r}/{!r}".format(
                self.__class__.__name__,
                self.numerator,
                self.denominator
            )
        
    def __str__(self):
        if not self.denominator:
            return str( self.numerator )
        else:
            return "{!s}/{!s}".format( 
                self.numerator, 
                self.denominator 
            )
        
    # __hash__ and __eq__ are required for mapping keys
    def __hash__(self):
        return hash(
            ( self.numerator, self.denominator )
        )
        
    def __eq__(self,other):
        return (    
            self.numerator == other.numerator
        and 
            self.denominator == other.denominator
        )
        
    def __len__(self):
        return len( self.numerator )

    @property
    def is_simplified(self):
        """
        Is in simplified form
        """
        return not self.denominator
        
    @property
    def is_dimensionless(self):
        return sum( self.simplify().numerator ) == 0

    @property
    def is_dimensionless_ratio(self):
        return self.numerator == self.denominator
        
    def is_ratio_of(self,other):
        """
        Return True when `other` is in simplified form and has 
        the same dimensions as the numerator and denominator
        of this dimensionless-ratio object.
        
        """
        if self.is_dimensionless_ratio and other.is_simplified:
            return self.numerator == other.numerator
            
        return False
        
    # Dimensions can be multiplied and divided
    def __mul__(self,rhs):
        return Dimension(
            tuple( 
                i+j for i,j in zip(
                    self.numerator,
                    rhs.numerator) 
            ),
            # the `denominator` may be empty,
            # using `zip_longest` will fill it with 0's
            tuple( 
                i+j for i,j in zip_longest(
                    self.denominator,
                    rhs.denominator,
                    fillvalue=0) 
            )
        )
            
    def __div__(self,rhs):
        return self.__truediv__(rhs)
    
    def __truediv__(self,rhs):
        return Dimension(
            tuple( 
                i-j for i,j in zip(
                    self.numerator,
                    rhs.numerator) 
            ),
            tuple( 
                i-j for i,j in zip_longest(
                    self.denominator,
                    rhs.denominator,
                    fillvalue=0) 
            )
        )

    def ratio(self,rhs):
        """
        Avoid simplifying the dimensions of `self` and `rhs`.
        Retain them as a ratio, with the dimension of `self` in 
        the numerator and the dimension of `rhs` in the denominator.
        
        """
        if not rhs.denominator:
            num = self.numerator
        else:
            num = tuple(
                i+j for i,j in zip(
                    self.numerator,
                    rhs.denominator)
            )
            
        if not self.denominator:
            den = rhs.numerator
        else:
            den = tuple(
                i+j for i,j in zip_longest(
                    self.denominator,
                    rhs.numerator)
            )
            
        return Dimension(num,den)

    def simplify(self):
        """
        Return the dimension of the object. 
        If there are dimensions for both the numerator and
        denominator they will be combined and simplified. 
        
        """
        return Dimension(
            tuple( 
                i-j for i,j in zip_longest(
                    self.numerator,
                    self.denominator,
                    fillvalue=0) 
            )
        )
  
        
#============================================================================
if __name__ == '__main__':
    
    import quantity_value as QV
    from context import *

    Length = QV.KindOfQuantity('Length','L') 
    context = Context(Length)
    
    LengthRatio = QV.KindOfQuantity('LengthRatio','L/L') 
    context.declare( LengthRatio,Length.ratio(Length) )
    
    print( context.evaluate( (LengthRatio*Length).simplify() ) )