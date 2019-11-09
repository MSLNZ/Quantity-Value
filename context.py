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
    A context tracks KindOfQuantity instances,
    and associates each each with a unique dimension.  
    A set of 'independent'  KindOfQuantity instances 
    form an n-dimensional basis. Other KindOfQuantity instances 
    are declared as products and quotients of the base quantities. Their
    dimensions are evaluated from the corresponding base-quantity dimensions.
    """
    
    def __init__(self,*argv):
        assert len(argv) > 0,\
            "Provide a sequence of `KindOfQuantity` instances for the basis"
            
        self._basis = tuple(argv)
        self._koq_dimension = bidict()
        
        # For conversions between different unit systems
        self._conversion_factors = dict()
        
        # Assign dimensions to base quantities
        dimension = [0] * len(argv)
        
        for i,koq in enumerate( self._basis ):
            if koq in self._koq_dimension:
                raise RuntimeError(
                    "{!r} is allocated to {}".format(
                        koq,
                        self._koq_dimension[koq]
                    )
                )
            else:
                # Each kind of quantity must refer to this context
                koq.context = self
                
                dimension[i] = 1
                self._koq_dimension[koq] = Dimension(dimension)
                dimension[i] = 0
  
        # Dimensionless case is always included
        self._koq_dimension[Numeric] = Dimension(dimension)
        
    # The `expression` is a sequence of binary multiplication
    # and division operations represented as a tree of objects.
    # The `self.dimension` method resolves `KindOfQuantity` objects 
    # at the leaves of this tree into their dimension. Execution 
    # of the expression reduces the tree into a single dimension result,
    # corresponding to the dimension for the resultant KindOfQuantity.
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
        Evaluate a quantity expression and return the corresponding quantity
        
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
        