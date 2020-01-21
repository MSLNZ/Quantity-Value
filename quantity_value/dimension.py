try:
    from itertools import zip_longest                   # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest   # Python 2

#----------------------------------------------------------------------------
class Dimension(object):

    """
    A Dimension keeps track of dimensional exponents. 
    
    Multiplication and division of dimensions adds and subtracts their 
    exponents, respectively. There is also provision to retain the  
    dimensions of a 'dimensionless' quantity.
    
    A Dimension contains a reference to a :class:`.Context`, which has 
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
        return self._context 
        
    @property
    def is_simplified(self):
        """
        True when the denominator is empty
        """
        return not self.denominator
        
    @property
    def is_dimensionless(self):
        """
        True when all dimensional exponents are zero 
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
        True when this object and `other` 
        have the same dimensions.
        
        """
        if self.is_dimensionless_ratio and other.is_simplified:
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
        Return the simplified dimensions of the object.
        
        If there are dimensions in both the numerator and
        the denominator they will be combined in the
        numerator of the object returned leaving the 
        denominator zero. 
        
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
  
