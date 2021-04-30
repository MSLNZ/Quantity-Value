from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 

from QV.registered_unit import RegisteredUnit as Unit
from QV import registered_unit 
from QV.prefix import * 

#----------------------------------------------------------------------------
class TestUnit(unittest.TestCase):

    def test(self):
        # construction
        context = Context( ('Length','L'),('Time','T') )
        SI =  UnitRegister("SI",context)

        Length = 'Length'
        name = 'metre'
        symbol = 'm' 
        metre = SI.unit( RatioScale(context['Length'],name,symbol) )  

        self.assertTrue( type(metre) is Unit )
        self.assertEqual( str(metre.scale), symbol )
        self.assertEqual( metre.scale.name, name  )
        self.assertTrue( metre.scale.kind_of_quantity is context['Length']  )
    
        # related unit
        centimetre = SI.unit( centi( metre ) )

        self.assertTrue( isinstance(centimetre,Unit) )
        self.assertEqual( str(centimetre.scale), 'cm' )
        self.assertEqual( centimetre.scale.name, 'centimetre' )
        self.assertEqual( centimetre.scale.kind_of_quantity, context['Length']  )
        self.assertEqual( centimetre.scale.conversion_factor, 0.01 )
        self.assertTrue( centimetre.register is SI )
        
        # Don't create two equivalent scales
        self.assertRaises( RuntimeError, SI.unit, centi( metre ) )
        
        # Cannot apply a prefix to a PrefixedQuantity
        self.assertRaises( RuntimeError, deci, centimetre )
        
        # operations 
        # NB, the resolution of unit expressions is handled 
        # in quantity_value.py 
        second = SI.unit( RatioScale(context['Time'],'second','s') ) 
        
        tmp = metre * second
        self.assertTrue( isinstance(tmp,registered_unit.Mul) )

        try: 
            10 * second 
        except TypeError:
            pass 
        else:
            assert False
        
        tmp = metre / second
        self.assertTrue( isinstance(tmp,registered_unit.Div) )

        try: 
            10 / second 
        except TypeError:
            pass 
        else:
            assert False

        tmp = metre // second
        self.assertTrue( isinstance(tmp,registered_unit.Ratio) )

        try: 
            10 // second 
        except TypeError:
            pass 
        else:
            assert False 
            
#============================================================================
if __name__ == '__main__':
    unittest.main()