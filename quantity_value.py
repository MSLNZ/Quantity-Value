__all__ = (
    'QuantityValue',
    'value',
    'quantity',
)

#----------------------------------------------------------------------------
class QuantityValue(object):

    __slots__ = ("x", "q")
    
    def __init__(self,value,quantity):
        self.x = value     
        self.q = quantity
        
    def __repr__(self):
        return "{!s}({!r},{!r})".format(
            self.__class__.__name__,
            self.x,
            self.q 
        )
        
    def __str__(self):
        return "{!s} {!s}".format(
            self.x,
            self.q 
        )
        
    def __add__(self,rhs):
        ql = self.q
        qr = rhs.q
        
        if ql is qr:
            return QuantityValue( self.x + rhs.x, ql )
         
        if (    ql.system is qr.system 
            and ql._kind_of_quantity is qr._kind_of_quantity
        ):
            ml = ql.multiplier
            mr = qr.multiplier 
            if ml < mr:
                return QuantityValue( self.x + (mr/ml)*rhs.x, ql )
            else:
                return QuantityValue( (ml/mr)*self.x + rhs.x, qr )
        else:
            raise RuntimeError(
                "addition or subtraction of quantity values requires "
                "the same kind of quantity and the same unit system"
            )    

    def __radd__(self,lhs):
        # Can add numbers to numeric QVs
        qr = self.q
        if qr.kind_of_quantity is Numeric:
            return QuantityValue( lhs + self.x, qr )
        else:
            raise NotImplemented
  
    def __sub__(self,rhs):
        ql = self.q
        qr = rhs.q
        
        if ql is qr:
            return QuantityValue( self.x - rhs.x, ql )
            
        if (    ql.system is qr.system 
            and ql._kind_of_quantity is qr._kind_of_quantity
        ):
            ml = ql.multiplier
            mr = qr.multiplier 
            if ml < mr:
                return QuantityValue( self.x - (mr/ml)*rhs.x, ql )
            else:
                return QuantityValue( (ml/mr)*self.x - rhs.x, qr )
        else:
            raise RuntimeError(
                "addition or subtraction of quantity values requires "
                "the same kind of quantity and the same unit system"
            )    
  
    def __rsub__(self,lhs):
        # Can subtract numeric QVs from numbers
        qr = self.q
        if qr.kind_of_quantity is Numeric:
            return QuantityValue( lhs - self.x, qr )
        else:
            raise NotImplemented
  
    # Multiplication and division create QuantityValue 
    # objects in which the quantity attribute is an 
    # expression that has not not been
    # resolved to a single unit within the system. 
    # This temporary object has an interface that exposes
    # `multiplier`, `system` and `kind_of_quantity` attributes, 
    # which are also present in the Unit interface. 
    # These allow a unit to be resolved later.
    def __mul__(self,rhs):
        tmp = self.q * rhs.q 
        v = self.x * rhs.x 
        
        return QuantityValue(v,tmp)
            
    def __div__(self,rhs):
        return self.__truediv__(rhs) 
        
        return QuantityValue(v,tmp)
            
    def __truediv__(self,rhs):
        tmp = self.q / rhs.q 
        v = self.x / rhs.x 
        
        return QuantityValue(v,tmp)
        
    def __rmul__(self,lhs):
        # Assume that the `lhs` behaves as a numeric 
        q = self.q.system.unity * self.q
        return QuantityValue(lhs * self.x, q)
            
    def __rdiv__(self,lhs):
        # Assume that the `lhs` behaves as a numeric 
        q = self.q.system.unity / self.q
        return QuantityValue(lhs / self.x, q)
        
    def resolve(self):
        """
        Return a `QuantityValue` with the reference  
        unit of the unit system. 
        """
        quantity = self.q
        us = quantity.system 
        koq_expression = quantity.kind_of_quantity
        c = koq_expression.context
        
        unit = us.reference_unit_for( koq_expression ) 
        
        return QuantityValue(self.q.multiplier*self.x,unit)
        
#----------------------------------------------------------------------------
def value(qv):
    try:
        return qv.x 
    except AttributeError:
        return qv 

#----------------------------------------------------------------------------
def quantity(qv):
    try:
        return qv.q 
    except AttributeError:
        return None 
       
             

    
    
