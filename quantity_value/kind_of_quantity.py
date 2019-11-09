__all__ = ( 'KindOfQuantity', 'Numeric', )

#----------------------------------------------------------------------------
class KindOfQuantity(object):

    def __init__(self,name,term):
        self._name = name 
        self._term = term 
        self._context = None
     
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            self.__class__.__name__,
            self._name,
            self._term
        )

    def __str__(self):
        return str(self._term)

    def __eq__(self,other):
        dim_lhs = self._context.dimension(self)
        dim_rhs = self._context.dimension(other)
        
        return dim_lhs == dim_rhs        

    @property
    def context(self):
        return self._context 
        
    @context.setter
    def context(self,c):
        if self._context is None:
            self._context = c 
        else:
            raise RuntimeError(
                "Cannot change context setting"
            )
        
    @property 
    def name(self):
        return str(self._name) 
        
    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __div__(self,rhs):
        return Div(self,rhs)
        
    def __truediv__(self,rhs):
        return Div(self,rhs)

    def ratio(self,rhs):
        return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

    @property
    def is_dimensionless(self):
        return self._context.dimension(self).is_dimensionless

    @property
    def is_dimensionless_ratio(self):
        return self._context.dimension(self).is_dimensionless_ratio
        
    def is_ratio_of(self,other):
        """
        Return True when `other` has the same dimensions as 
        the numerator and denominator of this quantity-ratio object.
        
        """
        dim_lhs = self._context.dimension(self)
        dim_rhs = self._context.dimension(other)
        
        return dim_lhs.is_ratio_of(dim_rhs)
    
#----------------------------------------------------------------------------
# A representation for pure numbers
#
Numeric = KindOfQuantity('Numeric','1')

#----------------------------------------------------------------------------
class UnaryOp(object):   

    def __init__(self,arg):
        self.arg = arg

    @property
    def context(self):
        return self.arg.context
        
    def execute(self,stack,converter):
        if isinstance( self.arg,(BinaryOp,UnaryOp) ):
            self.arg.execute(stack,converter)
        else:
            stack.append( converter(self.arg) )
            
#----------------------------------------------------------------------------
class BinaryOp(object):   
    """
    Based class to build a simple parse tree and then evaluate it
    """
    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs 

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __rmul__(self,lhs):
        return Mul(lhs,self)

    def __truediv__(self,rhs):
        return Div(self,rhs)

    def __div__(self,rhs):
        return Div(self,rhs)

    def __rdiv__(self,lhs):
        return Div(lhs,self)

    @property
    def context(self):
        return self.lhs.context

    def ratio(self,rhs):
        return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)
        
    # Execution is a recursive process that reduces a tree 
    # of Mul and Div objects to a single dimension result.
    # The `stack` will hold dimensions. 
    # The `converter` argument is a `Context` method
    # that converts a KindOfQuantity object into a dimension.
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
class Mul(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def __repr__(self):
        return "Mul({!s},{!s})".format(self.lhs,self.rhs)
   
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

    def __repr__(self):
        return "Div({!s},{!s})".format(self.lhs,self.rhs)
    
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

    def __repr__(self):
        return "Ratio({!s},{!s})".format(self.lhs,self.rhs)
    
    def execute(self,stack,converter):
        super(Ratio,self).execute(stack,converter)    
        # The stack holds Dimension objects
        r = stack.pop()
        l = stack.pop()
        stack.append( l.ratio(r) )

