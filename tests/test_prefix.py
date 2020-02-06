from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 

from QV.prefix import * 

#----------------------------------------------------------------------------
class TestPrefix(unittest.TestCase):

    # See also test_scale.py
    
    def test(self):
        name = 'centi'
        abrev = 'c'
        value = 1E-2
        
        centi = Prefix(name,abrev,value)
        
        self.assertTrue( type(centi) is Prefix )
        self.assertEqual( centi.name, name )
        self.assertEqual( str(centi), abrev )
        self.assertAlmostEqual( value, centi.value, 15 )

    def test_prefixes_collection(self):

        context = Context(('Length','L'),('Time','T'),('Mass','M') )
        SI =  UnitRegister("SI",context)

        # Create complete sets of prefixed units
        metre = SI.reference_unit('Length','metre','m') 
        for p_i in prefix.metric_prefixes: p_i(metre)

        second = SI.reference_unit('Time','second','s')  
        for p_i in prefix.metric_prefixes: p_i(second)

        # Doesn't matter that this is not the traditional 'base' unit
        gram = SI.reference_unit('Mass','gram','g')  
        for p_i in prefix.metric_prefixes: p_i(gram) 
        
        self.assertRaises( AttributeError, getattr,SI,'millihenry')
        try:
            SI.kilogram
            SI.microsecond
            SI.picosecond
        except AttributeError:
            self.fail('Should not happen')
            
#============================================================================
if __name__ == '__main__':
    unittest.main()