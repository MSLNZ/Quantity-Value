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
        metre = SI.unit( RatioScale( context['Length'],'metre','m' ) ) 
        for p_i in prefix.metric_prefixes: 
            SI.unit( p_i(metre.scale) )

        second = SI.unit( RatioScale( context['Time'],'second','s' ) )  
        for p_i in prefix.metric_prefixes: 
            SI.unit( p_i(second.scale) )

        # Doesn't matter that this is not the traditional 'base' unit
        gram = SI.unit( RatioScale( context['Mass'],'gram','g' ) )  
        for p_i in prefix.metric_prefixes: p_i(gram.scale) 
        
        self.assertRaises( AttributeError, getattr,SI,'Inductance')
        
        try:
            # SI.Mass.kilogram
            # SI.Time.microsecond
            SI.Time.picosecond
        except AttributeError:
            self.fail('Should not happen')
            
#============================================================================
if __name__ == '__main__':
    unittest.main()