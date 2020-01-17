from __future__ import division 

__all__ = ( 'KindOfQuantity', 'Numeric' )

# KindOfQuantity is fundamental. 
# Using a Context, KoQs are associated with dimensions. 
# There could be different contexts that retain references 
# to the same KoQ objects. 

#----------------------------------------------------------------------------
class KindOfQuantity(object):

    """
    A quantity in the most general sense, 
    like Mass, Length, etc.
    
    When two objects have the same name and short name (term) 
    they are considered to be the same kind of quantity. 
    """

    def __init__(self,name,term):
        self._name = name 
        self._term = term 
     
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            self.__class__.__name__,
            self.name,
            self.term
        )

    def __str__(self):
        return str(self.term)

    def __eq__(self,other):
        return (
            self.name == other.name 
        and 
            self.term == other.term 
        ) 
        
    @property 
    def name(self):
        return str(self._name) 
        
    @property 
    def term(self):
        return str(self._term) 

    def __mul__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Mul(self,rhs)
            
    def __rmul__(self,lhs):
        # Assume that the lhs will behave as a number
        return Mul(Numeric,self)
            
    def __truediv__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Div(self,rhs)

    def __rtruediv__(self,lhs):
        # Assume that lhs behaves like a number
        return Div(Numeric,self)
        
    # def __div__(self,rhs):
        # return KindOfQuantity.__truediv__(self,rhs)
        
    # def __rdiv__(self,rhs):
        # return KindOfQuantity.__rtruediv__(self,rhs)
        
    def __floordiv__(self,rhs):
        # NB deliberately don't allow `rhs` to be numeric
        return Ratio(self,rhs)

    def __rfloordiv__(self,lhs):
        # Assume that lhs behaves like a number
        return Ratio(Numeric,self)
        
    def simplify(self):
        return Simplify(self)

#----------------------------------------------------------------------------
# KindOfQuantity objects can be multiplied and divided. Declaring a ratio 
# and simplifying a ratio is also supported.   
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
    Based class to build a simple parse tree and evaluate it
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

    # def __div__(self,rhs):
        # return BinaryOp.__truediv__(self,rhs)

    # def __rdiv__(self,lhs):
        # return BinaryOp.__rtruediv__(self,lhs)
            
    def __floordiv__(self,rhs):
        return Ratio(self,rhs)

    def __rfloordiv__(self,lhs):
        # rhs is not a KoQ
        return Ratio(lhs,self)

    def simplify(self):
        return Simplify(self)
        
    # Execution is a recursive process that reduces a tree 
    # of Mul and Div objects to a single result.
    # The `converter` argument is a `Context` method
    # that converts a KindOfQuantity object into a Dimension.
    # The `stack` holds dimensions. 
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
        # The stack holds Dimension objects
        x = stack.pop()
        stack.append( x.simplify() )

#----------------------------------------------------------------------------
class Pow(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Pow,self).execute(stack,converter)    
        # The stack holds Dimension objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l ** r )
        
#----------------------------------------------------------------------------
class Mul(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Mul,self).execute(stack,converter)    
        # The stack holds Dimension objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l * r )
        
#----------------------------------------------------------------------------
class Div(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 
    
    def execute(self,stack,converter):
        super(Div,self).execute(stack,converter)    
        # The stack holds Dimension objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l / r )
        
#----------------------------------------------------------------------------
class Ratio(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def execute(self,stack,converter):
        super(Ratio,self).execute(stack,converter)    
        # The stack holds Dimension objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l // r )

#----------------------------------------------------------------------------
Numeric = KindOfQuantity('Numeric','1')
