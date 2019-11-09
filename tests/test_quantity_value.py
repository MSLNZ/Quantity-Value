from __future__ import print_function
from __future__ import division 

import unittest

from quantity_value.kind_of_quantity import * 
from quantity_value.unit_system import *
from quantity_value.quantity import * 
from quantity_value.metric_quantity import *
from quantity_value.metric_prefix import *
from quantity_value.context import *
from quantity_value.quantity_value import *

#----------------------------------------------------------------------------
class TestQuantityValue(unittest.TestCase):

    def test_construction(self):
        SIUnits =  UnitSystem("SI",MetricUnit)
        Length = KindOfQuantity('Length','L') 
        metre = SIUnits.unit(Length,'metre','m')
        
        x = 1.234
        qv = QuantityValue(x,metre)
        
        self.assertTrue( isinstance(qv,QuantityValue) )
        self.assertTrue( quantity(qv) is metre )
        self.assertAlmostEqual( value(qv), x, 15 )       
 
    def test_simple_addition_subtraction(self):
        
        SIUnits = UnitSystem("SI",MetricUnit)
        Length = KindOfQuantity('Length','L') 
        metre = SIUnits.unit(Length,'metre','m')

        x1 = 1.2 
        x2 = 3.4 
        
        qv1 = QuantityValue(x1,metre)
        qv2 = QuantityValue(x2,metre)
        
        qv = qv1 + qv2 
        self.assertAlmostEqual( qv.x, x1 + x2, 15 )       
        self.assertTrue( qv.q is metre )
  
        qv = qv1 - qv2 
        self.assertAlmostEqual( qv.x, x1 - x2, 15 )       
        self.assertTrue( qv.q is metre )
        
        # When the units have different prefixes
        qv2 = QuantityValue(x2,centi(metre))
        qv = qv1 + qv2 
        # The result will be expressed in the lesser of the units 
        self.assertAlmostEqual( value(qv), x1*100 + x2, 15 )       
        self.assertTrue( quantity(qv) is centi(metre) )

        qv = qv1 - qv2 
        self.assertAlmostEqual( qv.x, x1*100 - x2, 15 )       
        self.assertTrue( qv.q is centi(metre) )

        # Illegal case 
        Imperial = UnitSystem("Imperial",Unit)
        foot = Imperial.unit(Length,'foot','ft')
        qv3 = QuantityValue(x1,foot)
        
        # When QVs use different systems of units,  
        # addition and subtraction is not permitted
        self.assertRaises(
            RuntimeError,
            QuantityValue.__add__,
            qv1,
            qv3
        ) 
  
        self.assertRaises(
            RuntimeError,
            QuantityValue.__sub__,
            qv1,
            qv3
        ) 
  
#============================================================================
if __name__ == '__main__':
    unittest.main()