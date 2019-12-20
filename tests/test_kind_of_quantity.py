from __future__ import print_function
from __future__ import division 

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import ValueDuplicationError

import unittest
 
from quantity_value.kind_of_quantity import * 

#----------------------------------------------------------------------------
class TestKindOfQuantity(unittest.TestCase):

    def test_construction(self):
        name = 'Length'
        term = 'L'
        
        Length = KindOfQuantity(name,term) 
        
        self.assertTrue( type(Length) is KindOfQuantity )
        self.assertEqual( Length.name, name )
        self.assertEqual( str(Length), term )
 
#============================================================================
if __name__ == '__main__':
    unittest.main()