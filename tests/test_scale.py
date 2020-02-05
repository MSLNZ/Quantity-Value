from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 

from QV.kind_of_quantity import * 
from QV.scale import * 
from QV import scale 
from QV.prefix import * 

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

#----------------------------------------------------------------------------
class TestUnit(unittest.TestCase):

    def test(self):
        # construction
        context = Context( ('Length','L'),('Time','T') )
        SI =  UnitRegister("SI",context)

        Length = 'Length'
        name = 'metre'
        symbol = 'm' 
        metre = SI.unit(Length,name,symbol)  

        self.assertTrue( type(metre) is Unit )
        self.assertEqual( str(metre.scale), symbol )
        self.assertEqual( metre.scale.name, name  )
        self.assertEqual( metre.kind_of_quantity, context['Length']  )
    
        # related unit
        centimetre = centi( metre )

        self.assertTrue( isinstance(centimetre,Unit) )
        self.assertEqual( str(centimetre.scale), 'cm' )
        self.assertEqual( centimetre.scale.name, 'centimetre' )
        self.assertEqual( centimetre.kind_of_quantity, context['Length']  )
        self.assertEqual( centimetre.multiplier, 0.01 )
        self.assertTrue( centimetre.register is SI )
        
        # Don't create a new object each time you change prefix
        centimetre_2 = centi( metre )
        self.assertTrue( centimetre is centimetre_2 )
        
        # Cannot apply a prefix to a PrefixedQuantity
        self.assertRaises( RuntimeError, deci, centimetre )
        
        # operations 
        # NB, the resolution of unit expressions is handled 
        # in quantity_value.py 
        second = SI.unit('Time','second','s')  
        
        tmp = metre * second
        self.assertTrue( isinstance(tmp,scale.Mul) )

        try: 
            10 * second 
        except TypeError:
            pass 
        else:
            assert False
        
        tmp = metre / second
        self.assertTrue( isinstance(tmp,scale.Div) )

        try: 
            10 / second 
        except TypeError:
            pass 
        else:
            assert False

        tmp = metre // second
        self.assertTrue( isinstance(tmp,scale.Ratio) )

        try: 
            10 // second 
        except TypeError:
            pass 
        else:
            assert False
        
#============================================================================
if __name__ == '__main__':
    unittest.main()