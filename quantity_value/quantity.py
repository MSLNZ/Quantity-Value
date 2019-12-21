__all__ = (
    'Quantity',
    'Unit',
)
#----------------------------------------------------------------------------
class Quantity(object):

    """
    A Quantity is an specific KindOfQuantity. 
    Such as the metre is a specific Length.   
    """
    
    def __init__(self,kind_of_quantity,name,term):
        self._kind_of_quantity = kind_of_quantity
        self._name = name
        self._term = term

    def __repr__(self):
        return "{!s}({!r},{!r},{!r})".format(
            self.__class__.__name__,
            self._kind_of_quantity,
            self._name,
            self._term
        )
        
    def __str__(self):
        return str(self._term)
        
    @property 
    def name(self):
        return str(self._name)
        
    @property 
    def kind_of_quantity(self):
        return self._kind_of_quantity
        
#----------------------------------------------------------------------------
# TODO: There is similarity Unit and ValueUnit.
# If a unit has a multiplier, it might as well be a ValueUnit?
# Perhaps there is an opportunity to re-factor. However, a Unit  
# differs from a ValueUnit by:
#    * its association with a system of units 
#    * the properties `name` and `kind_of_quantity`
#    * the representation and string formating
#
class Unit(Quantity):

    """
    A Unit is a Quantity associated with a system of units.  
    For instance, the metre is the unit of length in the SI system.  
    Mathematical operations are defined between Unit objects.
    """

    def __init__(self,kind_of_quantity,name,term):
        super(Unit,self).__init__(kind_of_quantity,name,term)
        
        # We associate a unit system with a quantity because  
        # the realisation of a unit may differ between systems. 
        # Although this is rare, it suits our implementation to 
        # carry a reference to the unit system.
        
        self._system = None
        
    # Units of the same kind of quantity have different multipliers. 
    @property 
    def multiplier(self):
        try:
            return self._multiplier
        except AttributeError:
            return 1 

    @property 
    def system(self):
        return self._system
        
    @system.setter
    def system(self,system):
        if self._system is None:
            self._system = system
        else:
            raise RuntimeError(
                "System of units is assigned: {}".format(self.system)
            )
        
    def __repr__(self):
        return "{!s}({!r},{!r},{!r},{!r})".format(
            self.__class__.__name__,
            self._kind_of_quantity,
            self._name,
            self._term,
            self._system
        )     

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    def __div__(self,rhs):
        return self.__truediv__(rhs)
        
    def ratio(self,rhs):
        return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

    def reference_unit_for(self):
        return self.system.reference_unit_for( self.kind_of_quantity ) 

#----------------------------------------------------------------------------
# The following classes support simple manipulation of units by
# multiplication and division, declaring a ratio of units 
# and of simplifying a ratio of units is also supported. 
# The base classes  `UnaryOp` and `BinaryOp` establish the method 
# interface requirements.  
# These classes provide a temporary representation for 
# an equation involving units.
#
# Operations implement manipulations of multipliers and kinds
# of quantity simultaneously. The latter depends on 
# operations defined in kind_of_quantity.py, construct a tree
# of KoQ objects and then reduce it to a single resultant KoQ object.
#----------------------------------------------------------------------------
class UnaryOp(object):   

    def __init__(self,arg):
        self.arg = arg
        self._system = arg.system

    @property 
    def system(self):
        return self._system

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    def __div__(self,rhs):
        return self.__truediv__(rhs)
        
    def ratio(self,rhs):
        return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

    def reference_unit_for(self):
        return self.system.reference_unit_for( self.kind_of_quantity ) 
    
#----------------------------------------------------------------------------
class BinaryOp(object):   

    def __init__(self,lhs,rhs):
        self.lhs = lhs
        self.rhs = rhs
        
        assert lhs.system is rhs.system
        self._system = lhs.system
        
    @property 
    def system(self):
        return self._system

    def __mul__(self,rhs):
        return Mul(self,rhs)
            
    def __truediv__(self,rhs):
        return Div(self,rhs)

    def __div__(self,rhs):
        return self.__truediv__(rhs)
        
    def ratio(self,rhs):
        return Ratio(self,rhs)

    def simplify(self):
        return Simplify(self)

    def reference_unit_for(self):
        return self.system.reference_unit_for( self.kind_of_quantity ) 
       
#----------------------------------------------------------------------------
class Simplify(UnaryOp):

    def __init__(self,arg):
        UnaryOp.__init__(self,arg) 
        
    def __repr__(self):
        return "simplify({!r})".format(self.arg)

    def __str__(self):
        return "simplify({!s})".format(self.arg)
           
    @property 
    def kind_of_quantity(self):  
        return self.arg.kind_of_quantity.simplify()
        
    @property 
    def multiplier(self):
        return self.arg.multiplier

#----------------------------------------------------------------------------
class Ratio(BinaryOp):   

    def __init__(self,lhs,rhs):
        BinaryOp.__init__(self,lhs,rhs) 

    def __repr__(self):
        return "({!r}-|-{!r})".format(self.lhs,self.rhs)

    def __str__(self):
        return "({!s}|{!s})".format(self.lhs,self.rhs)
           
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity.ratio(self.rhs.kind_of_quantity)
        
    @property 
    def multiplier(self):
        return self.lhs.multiplier / self.rhs.multiplier

#----------------------------------------------------------------------------
class Mul(BinaryOp):   

    def __init__(self,lhs,rhs):
        super(Mul,self).__init__(lhs,rhs) 

    def __repr__(self):
        return "({!r}*{!r})".format(self.lhs,self.rhs)

    def __str__(self):
        return "({!s}*{!s})".format(self.lhs,self.rhs)
           
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity * self.rhs.kind_of_quantity
        
    @property 
    def multiplier(self):
        return self.lhs.multiplier * self.rhs.multiplier
        
#----------------------------------------------------------------------------
class Div(BinaryOp):   

    def __init__(self,lhs,rhs):
        super(Div,self).__init__(lhs,rhs) 

    def __repr__(self):
        return "({!r}/{!r})".format(self.lhs,self.rhs)

    def __str__(self):
        return "({!s}/{!s})".format(self.lhs,self.rhs)
    
    @property 
    def kind_of_quantity(self):  
        return self.lhs.kind_of_quantity / self.rhs.kind_of_quantity

    @property 
    def multiplier(self):
        return self.lhs.multiplier / self.rhs.multiplier
