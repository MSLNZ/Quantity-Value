from __future__ import division     # eval() needs this

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from QV.kind_of_quantity import KindOfQuantity, Number
from QV.dimension import Dimension

#----------------------------------------------------------------------------
class Context(object):

    """
    A Context keeps a register of :class:`.KindOfQuantity` instances,
    and associates each with a unique dimension.
    
    A Context is initialised by providing a set of :math:`n` 
    kinds of quantity that become the base quantities. 
    Other kinds of quantity can then be declared as products  
    and quotients of base quantities, or of other 
    derived quantities already declared. 
    
    The dimensions of all declared quantities must be unique
    in the context.
        
    Example::

        >>> context = Context( ("Length","L"),("Time","T") )
        >>> context.declare('Speed','V','Length/Time') 
        KindOfQuantity('Speed','V')
        
    """
    
    def __init__(self,*argv):
        assert len(argv) > 0,\
            "Provide a sequence of name-term tuples"
            
        self._basis = tuple( KindOfQuantity(n,t) for (n,t) in argv )
        
        self._koq = dict()
        for koq_i in self._basis:
            if self._valid_koq_name_or_term(koq_i._term):
                self._koq[koq_i._term] = koq_i
            if self._valid_koq_name_or_term(koq_i._name):
                self._koq[koq_i._name] = koq_i
        
        # # For conversions between different unit registers
        # self._conversion_factors = dict()
        
        self._koq_dimension = bidict()
        # Assign an independent dimension to each base quantity
        dimension = [0] * len(argv)
        
        # Dimensionless case is included by default
        self._koq_dimension[Number] = Dimension(self,dimension)
        self._koq.update( {'Number':Number, '1':Number} ) 
        
        for i,koq in enumerate( self._basis ):
            if koq in self._koq_dimension:
                raise RuntimeError(
                    "{!r} is allocated to {}".format(
                        koq,
                        self._koq_dimension[koq]
                    )
                )
            else:
                dimension[i] = 1
                self._koq_dimension[koq] = Dimension(self,dimension)
                dimension[i] = 0
        
    def __getitem__(self,name):
        if name in self._koq:
            return self._koq[name]
 
    def __getattr__(self,attr):
        try:
            return self._koq[attr]
        except KeyError:
            raise AttributeError
        
    def _koq_to_dim(self,koq):
        return self._koq_dimension[koq]
  
    def _dim_to_koq(self,dim):
        return self._koq_dimension.inverse[dim]
        
    def _valid_koq_name_or_term(self,koq_id):
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
             
  
    # `expression` is a sequence of binary multiplication
    # and division operations, represented as a tree of 
    # KindOfQuantity objects. 
    # `self._koq_to_dim()` resolves the dimension of  
    # KindOfQuantity objects at the leaves of this tree. 
    # Executing the expression results in the 
    # dimension for the resultant KindOfQuantity.
    def _evaluate_dimension(self,expression):
        stack = list()
        expression.execute(stack,self._koq_to_dim)
        
        assert len(stack) == 1
        return stack.pop()
    
    @property 
    def base_quantities(self):
        """Return the base quantities in this context"""
        return self._basis
        
    def declare(self,koq_name,koq_term,expression):
        """
        Declare a :class:`.KindOfQuantity` in the context
        with dimensions defined by the ``expression``
        
        The argument ``expression`` may be an arbitrary number of 
        multiplications and divisions among :obj:`.KindOfQuantity` objects, 
        or a string representing such a sequence of operations.
        
        A ``RuntimeError`` is raised if the dimensions of the 
        ``expression`` are already associated with a kind 
        of quantity in the context.
        
        """
        self._valid_koq_name_or_term(koq_name)
        self._valid_koq_name_or_term(koq_term)
            
        # Evaluates the KoQ expression using only those KoQ 
        # objects that have been declared. 
        if isinstance(expression,str):
            # Evaluates the KoQ expression using only those KoQ 
            # objects that have been declared in this context. 
            expression = eval(expression,{'__builtins__': None},self._koq)
        
        if isinstance(expression,KindOfQuantity):
            if expression in self._koq_dimension:
                raise RuntimeError(
                    "{!r} is already declared".format(expression)
                )
            else:
                # KoQ objects are only created by Context 
                # and hence should already be registered 
                assert False, 'unexpected'
        else:
            dim = self._evaluate_dimension(expression)
            
            koq = KindOfQuantity(koq_name,koq_term)

            self._koq_dimension[koq] = dim
            self._koq.update( {koq_name:koq, koq_term:koq} )
                
            return koq 
        
    def evaluate(self,expression):
        """
        Evaluate the kind of quantity represented by ``expression``
                
        The argument ``expression`` may be an arbitrary number of 
        multiplications and divisions among :obj:`.KindOfQuantity` objects, 
        or a string representing such a sequence of operations.
        
        A ``RuntimeError`` is raised if the dimensions of the result 
        of the expression are not associated with a kind of quantity 
        in the context.
        
        """
        if isinstance(expression,str):
            # Evaluates the KoQ expression using only those KoQ 
            # objects that have been declared in this context. 
            expression = eval(expression,{'__builtins__': None},self._koq)

        dim = self._evaluate_dimension(expression)
        
        try:
            return self._dim_to_koq(dim)
        except KeyError:
            raise RuntimeError(
                "No quantity is associated with {!r}".format(dim)
            )
            
    def dimensions(self,koq):
        """
        Return the dimensions of ``koq`` 
        
        """
        # Can be a name
        if isinstance(koq,str):
            koq = self._koq[koq] 
            
        return self._koq_dimension[koq]    
        
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