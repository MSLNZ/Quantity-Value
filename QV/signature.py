from itertools import zip_longest                   

#----------------------------------------------------------------------------
class Signature(object):

    """
    A Signature has a pair of tuples that identify a kind of quantity. 
    
    Multiplication and division of signatures adds and subtracts the 
    tuple elements, respectively. 
    
    The numerator and denominator of a Signature object 
    are the tuples. This allows the signature of a 'dimensionless' 
    quantity to be retained. 
    
    A Signature object is in 'simplified' form when the 
    denominator is empty (or contains only zeros).
    
    A Signature object may be converted to 'simplified' form by setting 
    the numerator to the difference between the numerator and the  
    denominator and setting the exponents in the denominator to zero.
    
    A Signature refers to a :class:`.Context`, which contains 
    a 1-to-1 mapping between signatures and kinds of quantity.
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
    # Signatures are used as keys in Python dictionaries.
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
        """When elements in the denominator are all zero"""
        return not self.denominator
        
    @property
    def is_dimensionless(self):
        """When elements in simplified form are all zero"""
        return sum( self.simplify().numerator ) == 0

    # @property
    # def is_dimensionless_ratio(self):
        # """True when the numerator equals the denominator"""
        # return self.numerator == self.denominator
        
    def is_ratio_of(self,other):
        """
        True when the object is a dimensionless ratio and the
        numerator has the same signature as the``other`` object.
        
        """
        if self.numerator == self.denominator and other.is_simplified:
            return self.numerator == other.numerator
            
        return False
        
    # Signatures can be multiplied and divided
    def __mul__(self,rhs):
        return Signature(
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
        return Signature(
            self.context,
            tuple(i*rhs for i in self.numerator),
            tuple(i*rhs for i in self.denominator)
        )
            
    def __truediv__(self,rhs):
        return Signature(
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
        Divide the elements of `self` by `rhs`,
        but retain the result as a ratio of tuples.

        The numerator will contain the signature of `self` 
        and the denominator the signature of `rhs` 
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
            
        return Signature(self.context,num,den)

    def simplify(self):
        """
        Return the signature in simplified form.
        
        The numerator returned is the difference between 
        the numerator and the denominator of this object, 
        the elements in the denominator returned are all zero.
        
        """
        return Signature(
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
