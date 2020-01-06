try:
    from itertools import zip_longest                   # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest   # Python 2

#----------------------------------------------------------------------------
class Dimension(object):

    """
    Dimension holds the dimensional exponents of a KindOfQuantity. 
    
    Multiplication and division of Dimension adds and subtracts dimensional 
    exponents. There is also provision made to retain the dimension 
    of 'dimensionless' quantities as a ratio.
    
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
    def is_simplified(self):
        """
        True when the denominator is empty
        """
        return not self.denominator
        
    @property
    def is_dimensionless(self):
        """
        True when there are no non-zero dimensional exponents 
        """
        return sum( self.simplify().numerator ) == 0

    @property
    def is_dimensionless_ratio(self):
        """
        True when the numerator and denominator are the same 
        """
        return self.numerator == self.denominator
        
    def is_ratio_of(self,other):
        """
        True when `other` is in simplified form and
        `self` is a dimensionless ratio of the
        dimensions of `other`.
        
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
            
    # def __div__(self,rhs):
        # return self.__truediv__(rhs)
    
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
  
