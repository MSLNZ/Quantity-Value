from __future__ import division     # eval() needs this

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from kind_of_quantity import KindOfQuantity, Numeric

from dimension import Dimension

#----------------------------------------------------------------------------
class Context(object):

    """
    A Context keeps a register of :class:`.KindOfQuantity` instances,
    and associates each instance with a unique dimension.
    
    A Context may be used to look up a kind of quantity by
    name or by short-name (term).
    
    A Context is initialised by defining a set of 'independent' 
    kinds of quantity to form an n-dimensional basis. 
    Other kinds of quantity can then be declared as products  
    and quotients of this basis. Only derived quantities 
    with unique dimensions are permitted.
    """
    
    def __init__(self,*argv):
        assert len(argv) > 0,\
            "Provide a sequence of name-term tuples"
            
        self._basis = tuple( KindOfQuantity(n,t) for (n,t) in argv )
        
        self._koq = { koq_i._term: koq_i for koq_i in self._basis }
        self._koq.update( { koq_i._name: koq_i for koq_i in self._basis } )
        
        # # For conversions between different unit registers
        # self._conversion_factors = dict()
        
        self._koq_dimension = bidict()
        # Assign an independent dimension to each base quantity
        dimension = [0] * len(argv)
        
        # Dimensionless case is included by default
        self._koq_dimension[Numeric] = Dimension(self,dimension)
        self._koq.update( {'Numeric':Numeric, '1':Numeric} ) 
        
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
    
    def _koq_to_dim(self,koq):
        """
        Return the dimension associated with `koq`
        
        """
        return self._koq_dimension[koq]
  
    def _dim_to_koq(self,dim):
        """
        Return the kind of quantity associated with `dim`
        
        """
        return self._koq_dimension.inverse[dim]
  
    def declare(self,koq_name,koq_term,expression):
        """
        Associate `kog` with the quantity expression `expression`
        
        """
        if koq_name in self._koq:
            raise RuntimeError(
                "{!r} is already declared".format(koq_name)
            )

        if koq_term in self._koq:
            raise RuntimeError(
                "{!r} is already declared".format(koq_term)
            )
            
        # Evaluates the KoQ expression using only those KoQ 
        # objects that have been declared. 
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
        Evaluate the kind of quantity for `expression`
        
        """
        if isinstance(expression,str):
            # Evaluates the KoQ expression using only those KoQ 
            # objects that have been declared in this context. 
            expression = eval(expression,{'__builtins__': None},self._koq)

        dim = self._evaluate_dimension(expression)
        
        try:
            return self._koq_dimension.inverse[dim]
        except KeyError:
            raise RuntimeError(
                "No quantity is associated with {!r}".format(dim)
            )

    def is_dimensionless(self,koq_name):
        """
        True when ``koq_name`` is dimensionless
        
        """
        return self._koq_to_dim(self[koq_name]).is_dimensionless

    def is_dimensionless_ratio(self,koq_name):
        """
        True when ``koq_name`` is a a dimensionless ratio
        
        """
        return self._koq_to_dim(self[koq_name]).is_dimensionless_ratio
        
    def is_ratio_of(self,koq_ratio_name,koq_name):
        """
        Return True when ``koq_name`` has the same dimensions as 
        the numerator and denominator of `koq_ratio`.
        
        """
        dim_lhs = self._koq_to_dim( self[koq_ratio_name] )
        dim_rhs = self._koq_to_dim( self[koq_name] )
        
        return dim_lhs.is_ratio_of(dim_rhs)
    
        
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
        