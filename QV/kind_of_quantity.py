__all__ = ( 'KindOfQuantity', 'Number' )

#----------------------------------------------------------------------------
class KindOfQuantity(object):

    """
    A type of quantity like mass, length, etc.
    
    KindOfQuantity objects can be multiplied and divided. Declaring a ratio 
    and simplifying a ratio is also supported.
    """

    def __init__(self,name,symbol):
        self._name = str(name) 
        self._symbol = str(symbol) 
     
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            self.__class__.__name__,
            self._name,
            self._symbol
        )

    def __str__(self):
        return self._symbol

    # __hash__ and __eq__ are required for mapping keys
    def __hash__(self):
        return hash( ( self._name, self._symbol ) )
        
    def __eq__(self,other):
        return (
            self._name == other.name 
        and 
            self._symbol == other.symbol 
        ) 
        
    @property 
    def name(self):
        return self._name
        
    @property 
    def symbol(self):
        return self._symbol

    def __mul__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Mul(self,rhs)
            
    def __rmul__(self,lhs):
        # Assume that the lhs will behave as a number
        return Mul(Number,self)
            
    def __truediv__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Div(self,rhs)

    def __rtruediv__(self,lhs):
        # Assume that lhs behaves like a number
        return Div(Number,self)
                
    def __floordiv__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Ratio(self,rhs)

    def __rfloordiv__(self,lhs):
        # Assume that lhs behaves like a number
        return Ratio(Number,self)
        
    def _simplify(self):
        return Simplify(self)

#----------------------------------------------------------------------------
# The `execute` method is defined in all operation classes and is used to  
# resolve expressions into a result, by executing the nodes of a parse tree.
# See `context._evaluate_signature`
#----------------------------------------------------------------------------
class UnaryOp(object):   

    def __init__(self,arg):
        self.arg = arg

    def execute(self,stack,converter):
        if isinstance( self.arg,(BinaryOp,UnaryOp) ):
            self.arg.execute(stack,converter)
        else:
            stack.append( converter(self.arg) )
            
#----------------------------------------------------------------------------
class BinaryOp(object):   
    """
    Base class to build a simple parse tree and evaluate it
    """
    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs 

    def __repr__(self):
        return "{!s}({!s},{!s})".format(
            self.__class__.__name__,
            self.lhs,
            self.rhs
        )            
        
    def __pow__(self,rhs):
        return Pow(self,rhs)
        
    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __rmul__(self,lhs):
        return Mul(lhs,self)

    def __truediv__(self,rhs):
        return Div(self,rhs)

    def __rtruediv__(self,lhs):
        return Div(lhs,self)

    def __floordiv__(self,rhs):
        return Ratio(self,rhs)

    def __rfloordiv__(self,lhs):
        # rhs is not a KoQ
        return Ratio(lhs,self)

    def _simplify(self):
        return Simplify(self)
        
    # Execution is a recursive process that reduces a tree 
    # of Mul and Div objects to a result.
    # The `converter` argument is a `Context` method
    # that converts a `KindOfQuantity` object into a Signature.
    # The `stack` holds signatures. 
    def execute(self,stack,converter):
        if isinstance( self.lhs,(BinaryOp,UnaryOp) ):
            self.lhs.execute(stack,converter)
        else:
            stack.append( converter(self.lhs) )
            
        if isinstance( self.rhs,(BinaryOp,UnaryOp) ):
            self.rhs.execute(stack,converter)
        else:
            stack.append( converter(self.rhs) )

#----------------------------------------------------------------------------
class Simplify(UnaryOp):

    def __init__(self,arg):
        UnaryOp.__init__(self,arg) 

    def execute(self,stack,converter):
        super(Simplify,self).execute(stack,converter)    
        # The stack holds Signature objects
        x = stack.pop()
        stack.append( x.simplify() )

#----------------------------------------------------------------------------
class Pow(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Pow,self).execute(stack,converter)    
        # The stack holds Signature objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l ** r )
        
#----------------------------------------------------------------------------
class Mul(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Mul,self).execute(stack,converter)    
        # The stack holds Signature objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l * r )
        
#----------------------------------------------------------------------------
class Div(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 
    
    def execute(self,stack,converter):
        super(Div,self).execute(stack,converter)    
        # The stack holds Signature objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l / r )
        
#----------------------------------------------------------------------------
class Ratio(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Ratio,self).execute(stack,converter)    
        # The stack holds Signature objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l // r )

#----------------------------------------------------------------------------
# The kind of quantity of all numbers
Number = KindOfQuantity('Number','1')

# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )