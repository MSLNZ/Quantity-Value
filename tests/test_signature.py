from __future__ import division 

import unittest
 
from QV import *
from QV.signature import Signature 

#----------------------------------------------------------------------------
class TestSignature(unittest.TestCase):

    def test(self):
        # construction 
        context = None 
        
        t1 = (1,0)
        d1 = Signature( context, t1 )
        
        self.assertTrue( d1.context is None )
        self.assertEqual( d1, d1 )
        self.assertEqual( len(d1), 2 )
        self.assertTrue( d1.is_simplified )
        self.assertFalse( d1.is_dimensionless ) 
        self.assertFalse( d1.is_ratio_of(d1) ) 
        
        # works as dict key
        d = {d1:t1}
        self.assertEqual( d[d1], t1 )

    def test_operations(self):
    
        context = None 
        
        t1 = (1,0)
        t2 = (0,1)
        
        d1 = Signature( context, t1 )
        d2 = Signature( context, t2 )
        
        d_add = d1 * d2
        self.assertEqual( (1,1), d_add.numerator ) 
        self.assertEqual( (), d_add.denominator ) 
        
        d_sub = d1 / d2 
        self.assertEqual( (1,-1), d_sub.numerator ) 
        self.assertEqual( (), d_sub.denominator ) 
        
        d_ratio = d1 // d2 
        self.assertEqual( (1,0), d_ratio.numerator ) 
        self.assertEqual( (0,1), d_ratio.denominator ) 
        
        d_simple = d_ratio.simplify() 
        self.assertEqual( (1,-1), d_simple.numerator ) 
        self.assertEqual( (), d_simple.denominator ) 
        
    def test_in_context(self):
    
        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        Length = context['Length'] 
        Time = context['Time'] 
    
        Speed = context.declare('Speed','V','Length/Time')

        self.assertEqual( context._koq_to_signature(Length), Signature( context, (1,0) ) )
        self.assertEqual( context._koq_to_signature(Time), Signature( context, (0,1) ) )
        self.assertEqual( context._koq_to_signature(Speed), Signature( context, (1,-1) ) )

        self.assertTrue( context._signature_to_koq( Signature( context, (1,-1) ) ) is Speed)
        self.assertTrue( context._signature_to_koq( Signature( context, (1,0) ) ) is Length)

        LengthRatio = context.declare( 'LengthRatio','L//L','L//L' )
        self.assertEqual( 
            str(context._koq_to_signature(LengthRatio)), 
            "{}//{}".format( (1,0), (1,0) )  
        )

        self.assertTrue( not context._koq_to_signature(LengthRatio).is_simplified )
        self.assertTrue( context._koq_to_signature(LengthRatio).is_dimensionless )
        self.assertTrue( 
            context._koq_to_signature(LengthRatio).is_ratio_of(context._koq_to_signature(Length)) 
        ) 

        self.assertTrue( context.signature('LengthRatio').is_dimensionless )
        self.assertTrue( 
            context.signature('LengthRatio').is_ratio_of(context.signature('Length') ) 
        )

        # Although the simplified dimension is that of Length, 
        # the temporary ratio (L*L)/L is not recognised. 
        self.assertRaises(RuntimeError,context.evaluate, 'LengthRatio*Length' )
  
        koq = context.evaluate( '(LengthRatio*Length)._simplify()' )
        self.assertTrue( koq is Length )     
        self.assertEqual( koq, Length )     

#============================================================================
if __name__ == '__main__':
    unittest.main()