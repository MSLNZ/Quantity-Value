from __future__ import print_function
from __future__ import division 

import unittest

from QV.units_dict import *

"""
The UnitsDict class is based on collections.MutableMapping and inherits most of 
the functionality of a mapping object from it. Our implementation must only supply 
__setitem__, __getitem__, __delitem__, __iter__, __len__. 

We have also defined __str__ and __repr__.

The only special feature in our implementation is to use __getattr__ to 
make stored units accessible via object attributes.

The implementation does not in anyway rely on the design of QV. 
It is merely an ad hoc mapping object between names and Python objects. 
"""
#----------------------------------------------------------------------------
class TestUnitDict(unittest.TestCase):

    def test_1(self):
    
        # Simple construction then set, get and del items
        ud = UnitsDict()
        
        self.assertEqual( len(ud) , 0 )
 
        name = 'metre'
        term = 'm' 
        metre = object()
        
        ud[name] = metre
        ud[term] = metre
        
        self.assertEqual( len(ud) , 2 )
        self.assertTrue( ud.metre is metre )
        self.assertTrue( ud.m is metre  )
        self.assertTrue( ud['metre'] is metre )
        self.assertTrue( ud['m'] is metre  )
        
        del ud[name] 
        self.assertRaises(KeyError,ud.__getitem__,name)
        self.assertRaises(AttributeError,ud.__getattr__,name)
        
        self.assertEqual( len(ud) , 1 )
        self.assertTrue( ud.m is metre  )
        self.assertTrue( ud['m'] is metre  )
 
        del ud[term] 
 
        self.assertEqual( len(ud) , 0 )

    def test_2(self):
    
        metre = object()
        second = object() 
        
        # Simple construction from sequence
        seq = [('metre',metre),('m',metre),('second',second),('s',second)]
        ud = UnitsDict( seq )
        
        self.assertEqual( len(ud) , 4 )

        self.assertTrue( ud.metre is metre )
        self.assertTrue( ud.m is metre  )
        self.assertTrue( ud['metre'] is metre )
        self.assertTrue( ud['m'] is metre  )

        self.assertTrue( ud.second is second )
        self.assertTrue( ud.s is second  )
        self.assertTrue( ud['second'] is second )
        self.assertTrue( ud['s'] is second  )

        # Simple construction from dict
        d = dict(metre=metre,m=metre,second=second,s=second)
        ud = UnitsDict( d )
        
        self.assertTrue( ud.metre is metre )
        self.assertTrue( ud.m is metre  )
        self.assertTrue( ud['metre'] is metre )
        self.assertTrue( ud['m'] is metre  )

        self.assertTrue( ud.second is second )
        self.assertTrue( ud.s is second  )
        self.assertTrue( ud['second'] is second )
        self.assertTrue( ud['s'] is second  )

        # Simple construction from keywords
        ud = UnitsDict( metre=metre,m=metre,second=second,s=second )
        
        self.assertTrue( ud.metre is metre )
        self.assertTrue( ud.m is metre  )
        self.assertTrue( ud['metre'] is metre )
        self.assertTrue( ud['m'] is metre  )

        self.assertTrue( ud.second is second )
        self.assertTrue( ud.s is second  )
        self.assertTrue( ud['second'] is second )
        self.assertTrue( ud['s'] is second  )
        
        names = ['metre','m','second','s']
        keys = ud.keys() 
        for n_i in names:
            self.assertTrue( n_i in keys )
            
        objects = [metre,second]
        values = ud.values()
        for v_i in values: 
            self.assertTrue(v_i in objects)

    def test_3(self):
    
        ud = UnitsDict()
        
        metre = object()
        second = object() 
        
        ud['metre'] = metre
        
        # Things that should not work
        self.assertRaises(AttributeError,ud.__setitem__,'keys',metre)
        self.assertRaises(RuntimeError,ud.__setitem__,'metre',second)
        self.assertRaises(AttributeError,ud.__getattr__,'second')
        
#============================================================================
if __name__ == '__main__':
    unittest.main()