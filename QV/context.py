from bidict import bidict 

from QV.kind_of_quantity import KindOfQuantity, Number
from QV.signature import Signature

#----------------------------------------------------------------------------
class Context(object):

    """
    A Context keeps a register of :class:`.KindOfQuantity` instances,
    and associates each with a unique signature.
    
    A Context is initialised by a set of quantities. 
    Other quantities can then be declared as products  
    and quotients of these 'base' quantities, or of other 
    derived quantities already declared. 
    
    The signature of declared quantities must be unique.
        
    Example::

        >>> context = Context( ("Length","L"),("Time","T") )
        >>> context.declare('Speed','V','Length/Time') 
        KindOfQuantity('Speed','V')
        
    """
    
    def __init__(self,*argv):
        assert len(argv) > 0,\
            "Provide a sequence of name-symbol tuples"
            
        self._basis = tuple( KindOfQuantity(n,t) for (n,t) in argv )
        
        self._koq = dict()
        for koq_i in self._basis:
            if self._valid_koq_name_or_symbol(koq_i._symbol):
                self._koq[koq_i._symbol] = koq_i
            if self._valid_koq_name_or_symbol(koq_i._name):
                self._koq[koq_i._name] = koq_i
                
        self._koq_signature = bidict()
        
        # Assign an independent exponent to each base quantity
        exponents = [0] * len(argv)
        
        # The class of numbers is included by default
        self._koq_signature[Number] = Signature(self,exponents)
        self._koq.update( {'Number':Number, '1':Number} ) 
        
        for i,koq in enumerate( self._basis ):
            if koq in self._koq_signature:
                raise RuntimeError(
                    "{!r} is allocated to {}".format(
                        koq,
                        self._koq_signature[koq]
                    )
                )
            else:
                exponents[i] = 1
                self._koq_signature[koq] = Signature(self,exponents)
                exponents[i] = 0

    def __contains__(self,koq_name):
        return koq_name in self._koq
    
    def __getitem__(self,koq_name):
        if koq_name in self:
            return self._koq[koq_name]
        else:
            raise KeyError(
                "{!r} not found".format(koq_name)
            )
          
    def __getattr__(self,koq_name):
        if koq_name in self:
            return self._koq[koq_name]
        else:
            raise AttributeError(
                "{!r} not found".format(koq_name)
            )
        
    def _koq_to_signature(self,koq):
        return self._koq_signature[koq]
  
    def _signature_to_koq(self,sig):
        return self._koq_signature.inverse[sig]
            
        
    def _valid_koq_name_or_symbol(self,koq_id):
        if hasattr(self,koq_id):     
            if koq_id in self._koq:
                raise RuntimeError(
                    "{!r} is used for {!r}".format(
                        koq_id,
                        self._koq[koq_id]
                    )
                )
            else:
                # Must not conflict with class attributes too
                raise RuntimeError(
                    "{!r} is used as an attribute of {!s}".format(
                        koq_id,
                        self.__class__.__name__
                    )
                )
                
        else:
            return True 
             
  
    # `expression` is a sequence of binary multiplication
    # and division operation objects, linked in a tree. 
    # Executing `expression` results in the 
    # signature for the resultant KindOfQuantity.
    # `_koq_to_signature` resolves the KindOfQuantity objects
    # corresponding to signatures at the leaves of this tree. 
    def _evaluate_signature(self,expression):
        stack = list()
        expression.execute(stack,self._koq_to_signature)
        
        assert len(stack) == 1
        return stack.pop()
    
    @property 
    def base_quantities(self):
        """Return the base quantities in this context"""
        return self._basis
        
    def declare(self,koq_name,koq_symbol,expression):
        """
        Declare a :class:`.KindOfQuantity` defined by ``expression``
        
        The ``expression`` may be products  
        and quotients of :obj:`.KindOfQuantity` objects, 
        or a string representing these operations.
        
        A ``RuntimeError`` is raised if the signature 
        resulting from ``expression`` is already associated 
        with a kind of quantity.
        
        """
        self._valid_koq_name_or_symbol(koq_name)
        self._valid_koq_name_or_symbol(koq_symbol)
            
        if isinstance(expression,str):
            # Evaluates the string using KoQ objects 
            # that have been declared in this context. 
            expression = eval(expression,{'__builtins__': None},self._koq)
        
        if isinstance(expression,KindOfQuantity):
            if expression in self._koq_signature:
                raise RuntimeError(
                    "{!r} is already declared".format(expression)
                )
            else:
                # KoQ objects are only created by Context 
                # and hence should already be registered 
                assert False, 'unexpected'
        else:
            sig = self._evaluate_signature(expression)
            
            koq = KindOfQuantity(koq_name,koq_symbol)

            self._koq_signature[koq] = sig
            self._koq.update( {koq_name:koq, koq_symbol:koq} )
                
            return koq 
        
    def evaluate(self,expression):
        """
        Return the quantity represented by ``expression``
                
        The argument ``expression`` may be products 
        and quotients of :obj:`.KindOfQuantity` objects, 
        or a string representing these operations.
        
        A ``RuntimeError`` is raised if the signature of the result 
        is not associated with a kind of quantity in the context.
        
        """
        if isinstance(expression,str):
            # Evaluates the KoQ expression using only those KoQ 
            # objects that have been declared in this context. 
            expression = eval(expression,{'__builtins__': None},self._koq)

        sig = self._evaluate_signature(expression)
        
        try:
            return self._signature_to_koq(sig)
        except KeyError:
            raise RuntimeError(
                "No quantity is associated with {!r}".format(sig)
            )
            
    def signature(self,koq):
        """
        Return the signature associated with ``koq`` 
        
        """
        # Can be a name
        if isinstance(koq,str):
            koq = self._koq[koq] 
            
        return self._koq_signature[koq]    
   
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )