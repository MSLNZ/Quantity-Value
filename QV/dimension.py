try:
    from itertools import zip_longest                   # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest   # Python 2

#----------------------------------------------------------------------------
class Dimension(object):

    """
    A Dimension holds dimensional exponents. 
    
    Multiplication and division of dimensions adds and subtracts the 
    dimensional exponents, respectively. 
    
    The numerator and denominator of a Dimension object 
    are tuples of dimensional exponents. This   
    allows the dimensions of a 'dimensionless' 
    quantity to be retained. 
    
    A Dimension object is in 'simplified' form when the 
    denominator is empty (or contains only zeros). 
    A Dimension object may be converted
    to 'simplified' form by setting the numerator to the 
    difference between the numerator and the denominator and setting the 
    exponents in the denominator to zero.
    
    A Dimension holds a reference to a :class:`.Context`, which has 
    a 1-to-1 mapping between dimensions and kinds of quantity.
    """
    
    def __init__(self,context,numerator,denominator=()):
        self._context = context
        self.numerator = tuple(numerator) 
        self.denominator = tuple(denominator)
       
    def __repr__(self):
        if not self.denominator:
            return "{!s}{!r}".format(
                self.__class__.__name__,
                self.numerator
            )
        else:
            return "{!s}({!r}//{!r})".format(
                self.__class__.__name__,
                self.numerator,
                self.denominator
            )
        
    def __str__(self):
        if not self.denominator:
            return str( self.numerator )
        else:
            return "{!s}//{!s}".format( 
                self.numerator, 
                self.denominator 
            )
        
    # __hash__ and __eq__ are required for mapping keys
    # Dimensions are used as keys in Python dictionaries.
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
    def context(self):        
        """The associated Context"""
        return self._context 
        
    @property
    def is_simplified(self):
        """True when dimensional exponents in the denominator are all zero"""
        return not self.denominator
        
    @property
    def is_dimensionless(self):
        """True when the dimensional exponents in simplified form are all zero"""
        return sum( self.simplify().numerator ) == 0

    # @property
    # def is_dimensionless_ratio(self):
        # """True when the numerator equals the denominator"""
        # return self.numerator == self.denominator
        
    def is_ratio_of(self,other):
        """
        True when the object is a dimensionless ratio and the
        numerator has the same dimensions as the``other`` object.
        
        """
        if self.numerator == self.denominator and other.is_simplified:
            return self.numerator == other.numerator
            
        return False
        
    # Dimensions can be multiplied and divided
    def __mul__(self,rhs):
        return Dimension(
            self.context,
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

    def __pow__(self,rhs):
        return Dimension(
            self.context,
            tuple(i*rhs for i in self.numerator),
            tuple(i*rhs for i in self.denominator)
        )
            
    # def __div__(self,rhs):
        # return self.__truediv__(rhs)
    
    def __truediv__(self,rhs):
        return Dimension(
            self.context,
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

    def __floordiv__(self,rhs):
        """
        Divide the dimensions of `self` by `rhs`,
        but retain the result as a ratio of dimensions.

        The numerator will contain the dimensions of `self` 
        and the denominator the dimensions of `rhs` 
        if both arguments are in simplified form.
                
        If the arguments are not simplified, the 
        more general calculation will be performed.
        
        """
        if rhs.is_simplified:
            num = self.numerator
        else:
            num = tuple(
                i+j for i,j in zip(
                    self.numerator,
                    rhs.denominator)
            )
            
        if self.is_simplified:
            den = rhs.numerator
        else:
            den = tuple(
                i+j for i,j in zip_longest(
                    self.denominator,
                    rhs.numerator)
            )
            
        return Dimension(self.context,num,den)

    def simplify(self):
        """
        Return the dimensions in simplified form.
        
        The numerator in the Dimension object returned is the 
        difference between the numerator and the denominator
        of this object, the dimensional exponents in the 
        denominator of the object returned are all zero.
        
        """
        return Dimension(
            self.context,
            tuple( 
                i-j for i,j in zip_longest(
                    self.numerator,
                    self.denominator,
                    fillvalue=0) 
            )
        )

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )
