from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 

from QV.kind_of_quantity import * 
from QV.scale import * 

#----------------------------------------------------------------------------
class TestScale(unittest.TestCase):

    def test(self):
    
        # construction
        Length = KindOfQuantity('Length','L') 
        
        name = 'metre'
        symbol = 'm' 
        
        metre = Scale(Length,name,symbol)
        self.assertTrue( type(metre) is Scale )
        self.assertEqual( str(metre), symbol )
        self.assertEqual( metre.name, name  )
        self.assertEqual( metre.kind_of_quantity, Length  )
        
        # Should work as a dict key 
        d = { metre: 1 }
        self.assertTrue( d[metre] == 1 )


        
#============================================================================
if __name__ == '__main__':
    unittest.main()