from __future__ import division     # eval() needs this

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from QV.kind_of_quantity import KindOfQuantity, Number
from QV.signature import Signature

#----------------------------------------------------------------------------
class Context(object):

    """
    A Context keeps a register of :class:`.KindOfQuantity` instances,
    and associates each with a unique signature.
    
    A Context is initialised by a set of base quantities. 
    Other quantities can then be declared as products  
    and quotients of these base quantities, or of other 
    derived quantities already declared. 
    
    The signature of declared quantities must be unique
    in the context.
        
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
        
        # # For conversions between different unit registers
        # self._conversion_factors = dict()
        
        self._koq_signature = bidict()
        # Assign an independent exponent to each base quantity
        exponents = [0] * len(argv)
        
        # Dimensionless case is included by default
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
        
    def _kog_to_signature(self,koq):
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
                raise RuntimeError(
                    "{!r} is an attribute of {!s}".format(
                        koq_id,
                        self.__class__.__name__
                    )
                )
                
        else:
            return True 
             
  
    # Executing the expression results in the 
    # signature for the resultant KindOfQuantity.
    # `expression` is a sequence of binary multiplication
    # and division operations, represented as a tree of 
    # KindOfQuantity objects. 
    # `_kog_to_signature` resolves the signature of  
    # the KindOfQuantity objects at the leaves of this tree. 
    def _evaluate_signature(self,expression):
        stack = list()
        expression.execute(stack,self._kog_to_signature)
        
        assert len(stack) == 1
        return stack.pop()
    
    @property 
    def base_quantities(self):
        """Return the base quantities in this context"""
        return self._basis
        
    def declare(self,koq_name,koq_symbol,expression):
        """
        Declare a :class:`.KindOfQuantity`
        with signature defined by ``expression``
        
        The argument ``expression`` may be multiplications 
        and divisions of :obj:`.KindOfQuantity` objects, 
        or a string representing such a sequence of operations.
        
        A ``RuntimeError`` is raised if the signature of the 
        ``expression`` is already associated with a kind 
        of quantity in the context.
        
        """
        self._valid_koq_name_or_symbol(koq_name)
        self._valid_koq_name_or_symbol(koq_symbol)
            
        # Evaluates the KoQ expression using only those KoQ 
        # objects that have been declared. 
        if isinstance(expression,str):
            # Evaluates the KoQ expression using only those KoQ 
            # objects that have been declared in this context. 
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
        Evaluate the quantity represented by ``expression``
                
        The argument ``expression`` may be multiplications 
        and divisions of :obj:`.KindOfQuantity` objects, 
        or a string representing such a sequence of operations.
        
        A ``RuntimeError`` is raised if the signature of the result 
        of the expression are not associated with a kind of quantity 
        in the context.
        
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
        
    # def conversion_from_to(self,ref_unit_1,ref_unit_2,factor):
        # """
        # Register a factor to convert from `ref_unit_1`, in  
        # one unit register, to `ref_unit_2` in another
        # """
        # koq_1 = ref_unit_1._kind_of_quantity
        # koq_2 = ref_unit_2._kind_of_quantity
        # assert koq_1 is koq_2,\
            # "{} and {} are different quantities".format(koq_1,koq_2)
            
        # if (ref_unit_1,ref_unit_2) in self._conversion_factors:
                # raise RuntimeError(
                    # "There is already an entry for {} and {}".format(
                        # ref_unit_1,
                        # ref_unit_2
                    # )
                # )
        # else:
            # self._conversion_factors[(ref_unit_1,ref_unit_2)] = factor

    # def from_to(self,ref_unit_1,ref_unit_2):
        # """
        # """
        # koq_1 = ref_unit_1._kind_of_quantity
        # koq_2 = ref_unit_2._kind_of_quantity
        # assert koq_1 is koq_2,\
            # "{} and {} are different quantities".format(koq_1,koq_2)

        # return self._conversion_factors[(ref_unit_1,ref_unit_2)]
   
# ===========================================================================    
if __name__ == "__main__":
    import doctest
    from QV import *
    doctest.testmod(  optionflags= doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  )