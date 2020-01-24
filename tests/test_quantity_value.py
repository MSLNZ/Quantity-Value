from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 
from QV.metric_prefix import *
from QV.quantity_value import ValueUnit

#----------------------------------------------------------------------------
class TestQuantityValue(unittest.TestCase):

    def test_construction(self):
        context = Context( ('Length','L') )
        SIUnits =  UnitRegister("SI",context)
        Length = 'Length'
        metre = SIUnits.unit(Length,'metre','m')
        
        x = 1.234
        vu = qvalue(x,metre)
        
        self.assertTrue( isinstance(vu,ValueUnit) )
        self.assertTrue( unit(vu) is metre )
        self.assertAlmostEqual( value(vu), x, 15 )       
 
    def test_simple_addition_subtraction(self):
        
        context = Context( ('Length','L') )
        SI =  UnitRegister("SI",context)
        Length = 'Length'
        
        metre = SI.unit(Length,'metre','m')

        x1 = 1.2 
        x2 = 3.4 
        
        qv1 = qvalue(x1,metre)
        qv2 = qvalue(x2,metre)
        
        vu = qv1 + qv2 
        self.assertAlmostEqual( vu.value, x1 + x2, 15 )       
        self.assertTrue( vu.unit is metre )
  
        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.value, x1 - x2, 15 )       
        self.assertTrue( vu.unit is metre )
        
        # When the units have different prefixes
        qv2 = qvalue(x2,centi(metre))
        vu = qv1 + qv2 
        # The result will be expressed in the lesser of the units 
        self.assertAlmostEqual( value(vu), x1*100 + x2, 15 )       
        self.assertTrue( unit(vu) is centi(metre) )

        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.value, x1*100 - x2, 15 )       
        self.assertTrue( vu.unit is centi(metre) )

        # Illegal case 
        Imperial = UnitRegister("Imperial",context)
        foot = Imperial.unit(Length,'foot','ft')
        qv3 = qvalue(x1,foot)
        
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