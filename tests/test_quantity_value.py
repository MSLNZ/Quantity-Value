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
        vu = ValueUnit(x,metre)
        
        self.assertTrue( isinstance(vu,ValueUnit) )
        self.assertTrue( unit(vu) is metre )
        self.assertAlmostEqual( value(vu), x, 15 )       
 
    def test_simple_addition_subtraction(self):
        
        SIUnits = UnitSystem("SI",MetricUnit)
        Length = KindOfQuantity('Length','L') 
        metre = SIUnits.unit(Length,'metre','m')

        x1 = 1.2 
        x2 = 3.4 
        
        qv1 = ValueUnit(x1,metre)
        qv2 = ValueUnit(x2,metre)
        
        vu = qv1 + qv2 
        self.assertAlmostEqual( vu.x, x1 + x2, 15 )       
        self.assertTrue( vu.u is metre )
  
        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.x, x1 - x2, 15 )       
        self.assertTrue( vu.u is metre )
        
        # When the units have different prefixes
        qv2 = ValueUnit(x2,centi(metre))
        vu = qv1 + qv2 
        # The result will be expressed in the lesser of the units 
        self.assertAlmostEqual( value(vu), x1*100 + x2, 15 )       
        self.assertTrue( unit(vu) is centi(metre) )

        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.x, x1*100 - x2, 15 )       
        self.assertTrue( vu.u is centi(metre) )

        # Illegal case 
        Imperial = UnitSystem("Imperial",Unit)
        foot = Imperial.unit(Length,'foot','ft')
        qv3 = ValueUnit(x1,foot)
        
        # When QVs use different systems of units,  
        # addition and subtraction is not permitted
        self.assertRaises(
            RuntimeError,
            ValueUnit.__add__,
            qv1,
            qv3
        ) 
  
        self.assertRaises(
            RuntimeError,
            ValueUnit.__sub__,
            qv1,
            qv3
        ) 
  
#============================================================================
if __name__ == '__main__':
    unittest.main()