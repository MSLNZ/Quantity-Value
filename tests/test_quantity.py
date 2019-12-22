from __future__ import print_function
from __future__ import division 

import unittest

from quantity_value.kind_of_quantity import * 
from quantity_value.unit_system import *
from quantity_value.quantity import * 
from quantity_value.metric_prefix import *
from quantity_value.context import *

#----------------------------------------------------------------------------
class TestPrefix(unittest.TestCase):

    def test_construction(self):
        name = 'centi'
        abrev = 'c'
        value = 1E-2
        
        centi = MetricPrefix(name,abrev,value)
        
        self.assertTrue( type(centi) is MetricPrefix )
        self.assertEqual( centi.name, name )
        self.assertEqual( str(centi), abrev )
        self.assertAlmostEqual( value, centi.value, 15 )

#----------------------------------------------------------------------------
class TestQuantity(unittest.TestCase):

    def test_construction(self):
        Length = KindOfQuantity('Length','L') 
        
        name = 'metre'
        symbol = 'm' 
        
        metre = Quantity(Length,name,symbol)
        self.assertTrue( type(metre) is Quantity )
        self.assertEqual( str(metre), symbol )
        self.assertEqual( metre.name, name  )
        

#----------------------------------------------------------------------------
class TestMetricQuantity(unittest.TestCase):

    def test_construction(self):
        Length = KindOfQuantity('Length','L') 

        SIUnits =  UnitSystem("SI")

        name = 'metre'
        symbol = 'm' 
        metre = SIUnits.unit(Length,name,symbol)  

        self.assertTrue( type(metre) is Unit )
        self.assertEqual( str(metre), symbol )
        self.assertEqual( metre.name, name  )

        centimetre = centi( metre )

        self.assertTrue( isinstance(centimetre,Unit) )
        self.assertEqual( str(centimetre), 'cm' )
        self.assertEqual( centimetre.name, 'centimetre' )
        
        # Don't create a new object each time you change prefix
        centimetre_2 = centi( metre )
        self.assertTrue( centimetre is centimetre_2 )
        
        # Cannot apply a prefix to a PrefixedQuantity
        self.assertRaises( RuntimeError, deci, centimetre )
        

#============================================================================
if __name__ == '__main__':
    unittest.main()