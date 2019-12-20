import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import bidict 

from kind_of_quantity import Numeric
from dimension import Dimension

#----------------------------------------------------------------------------
class Context(object):

    """
    A Context keeps track of KindOfQuantity instances,
    and associates each instance with a unique dimension.  
    A set of 'independent' KindOfQuantity instances will
    form an n-dimensional basis. Other KindOfQuantity instances 
    can be declared as products and quotients of the base quantities. 
    """
    
    def __init__(self,*argv):
        assert len(argv) > 0,\
            "Provide a sequence of `KindOfQuantity` instances"
            
        self._basis = tuple(argv)
        self._koq_dimension = bidict()
        
        # For conversions between different unit systems
        self._conversion_factors = dict()
        
        # Assign an independent dimension to each base quantity
        dimension = [0] * len(argv)
        
        # Dimensionless case is included by default
        self._koq_dimension[Numeric] = Dimension(dimension)
        
        for i,koq in enumerate( self._basis ):
            if koq in self._koq_dimension:
                raise RuntimeError(
                    "{!r} is allocated to {}".format(
                        koq,
                        self._koq_dimension[koq]
                    )
                )
            else:
                # Every kind of quantity known to the context 
                # must carry a reference to it.
                koq.context = self
                
                dimension[i] = 1
                self._koq_dimension[koq] = Dimension(dimension)
                dimension[i] = 0
        
    # The `expression` is a sequence of binary multiplication
    # and division operations, represented as a tree of 
    # KindOfQuantity objects. 
    # The `self.dimension` method resolves 
    # the dimension of KindOfQuantity objects at the leaves of this tree. 
    # Executing the expression produces a single 
    # dimension, corresponding to the dimension for the 
    # resultant KindOfQuantity.
    def _evaluate_dimension(self,expression):
        stack = list()
        expression.execute(stack,self.dimension)
        
        assert len(stack) == 1
        return stack.pop()
    
    def dimension(self,koq):
        """
        Return the dimension associated with `koq`
        
        """
        return self._koq_dimension[koq]
  
    def kind_of_quantity(self,dim):
        """
        Return the kind of quantity associated with `dim`
        
        """
        return self._koq_dimension.inverse[dim]
  
    def declare(self,koq,expression):
        """
        Associate `kog` with the quantity expression `expression`
        
        """
        if koq in self._koq_dimension:
            raise RuntimeError(
                "{!r} is already declared".format(koq)
            )
        else:
            dim = self._evaluate_dimension(expression)
            
            # Each kind of quantity must refer to this context
            koq.context = self
            self._koq_dimension[koq] = dim
        
    def evaluate(self,expression):
        """
        Evaluate `expression` and return the corresponding kind of quantity
        
        """
        dim = self._evaluate_dimension(expression)
        
        try:
            return self._koq_dimension.inverse[dim]
        except KeyError:
            raise RuntimeError(
                "No quantity is associated with {!r}".format(dim)
            )
        
    def conversion_from_to(self,ref_unit_1,ref_unit_2,factor):
        """
        Register a factor to convert from `ref_unit_1`, in  
        one unit system, to `ref_unit_2` in another
        """
        koq_1 = ref_unit_1._kind_of_quantity
        koq_2 = ref_unit_2._kind_of_quantity
        assert koq_1 is koq_2,\
            "{} and {} are different quantities".format(koq_1,koq_2)
            
        if (ref_unit_1,ref_unit_2) in self._conversion_factors:
                raise RuntimeError(
                    "There is already an entry for {} and {}".format(
                        ref_unit_1,
                        ref_unit_2
                    )
                )
        else:
            self._conversion_factors[(ref_unit_1,ref_unit_2)] = factor

    def from_to(self,ref_unit_1,ref_unit_2):
        """
        """
        koq_1 = ref_unit_1._kind_of_quantity
        koq_2 = ref_unit_2._kind_of_quantity
        assert koq_1 is koq_2,\
            "{} and {} are different quantities".format(koq_1,koq_2)

        return self._conversion_factors[(ref_unit_1,ref_unit_2)]
        