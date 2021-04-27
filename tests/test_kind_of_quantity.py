from bidict import ValueDuplicationError

import unittest
 
from QV.kind_of_quantity import * 
from QV import kind_of_quantity as koq 
 
#----------------------------------------------------------------------------
class TestKindOfQuantity(unittest.TestCase):

    def tests(self):
        # Construction
        name = 'Length'
        symbol = 'L'
        
        Length = KindOfQuantity(name,symbol) 
        
        self.assertTrue( type(Length) is KindOfQuantity )
        self.assertEqual( Length.name, name )
        self.assertEqual( str(Length), symbol )
        
        Time = KindOfQuantity('Time','T') 

        # Must work as a dict key
        d = { Length: 'Length', Time: 'Time' }
        self.assertEqual( d[Length], 'Length' )
        self.assertEqual( d[Time], 'Time' )
        
        # Equality
        self.assertTrue( Length == Length )
        self.assertTrue( Length != Number )
        self.assertTrue( Length != Time )
        
        # operations'
        # NB, the functionality of the MUL, Div etc classes
        # is tested in association with Context.
        tmp = Length * Time 
        self.assertTrue( isinstance(tmp, koq.Mul) )
 
        tmp = 10 * Time 
        self.assertTrue( isinstance(tmp, koq.Mul) )
 
        tmp = Length / Time 
        self.assertTrue( isinstance(tmp, koq.Div) )

        tmp = 10 / Time 
        self.assertTrue( isinstance(tmp, koq.Div) )

        tmp = Length // Time 
        self.assertTrue( isinstance(tmp, koq.Ratio) )

        tmp = 10 // Time 
        self.assertTrue( isinstance(tmp, koq.Ratio) )

#============================================================================
if __name__ == '__main__':
    unittest.main()