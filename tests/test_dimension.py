from __future__ import division 

import unittest
 
from QV import *
from QV.dimension import Dimension 

#----------------------------------------------------------------------------
class TestDimension(unittest.TestCase):

    def test_construction(self):
        # Basis
        context = Context(
            ('Length','L'),
            ('Mass','M'),
            ('Time','T')
        )
        
        Length = context['Length'] 
        Mass = context['Mass'] 
        Time = context['Time'] 
        
        self.assertEqual( str(context._koq_to_dim(Length)), str( (1,0,0) ) )
        self.assertEqual( str(context._koq_to_dim(Mass)), str( (0,1,0) ) )
        self.assertEqual( str(context._koq_to_dim(Time)), str( (0,0,1) ) )
        
        self.assertEqual( len(context._koq_to_dim(Mass) ), 3 )
        
        self.assertTrue( Dimension( context, (0,0,0) ).is_dimensionless )
        # Default - always present
        Numeric = context['Numeric']
        self.assertTrue( context._koq_to_dim(Numeric).is_dimensionless )
        
        # Derived KoQ
        Speed = context.declare('Speed','V','Length/Time')
        self.assertEqual( str(context._koq_to_dim(Speed)), str( (1,0,-1) ) )
        
        LengthRatio = context.declare( 'LengthRatio','L//L','L//L' )
        self.assertEqual( 
            str(context._koq_to_dim(LengthRatio)), 
            "{}//{}".format( (1,0,0), (1,0,0) )  
        )

        self.assertTrue( not context._koq_to_dim(LengthRatio).is_simplified )
        self.assertTrue( context._koq_to_dim(LengthRatio).is_dimensionless )
        # self.assertTrue( context._koq_to_dim(LengthRatio).is_dimensionless_ratio ) 
        self.assertTrue( context._koq_to_dim(LengthRatio).is_ratio_of(context._koq_to_dim(Length)) ) 

        self.assertTrue( context.dimensions('LengthRatio').is_dimensionless )
        # self.assertTrue( context.dimensions('LengthRatio').is_dimensionless_ratio ) 
        self.assertTrue( context.dimensions('LengthRatio').is_ratio_of(context.dimensions('Length') ) )
  
        # Although the simplified dimension is that of Length, 
        # the temporary ratio (L*L)/L is not recognised. 
        self.assertRaises(RuntimeError,context.evaluate, 'LengthRatio*Length' )
  
        koq = context.evaluate( '(LengthRatio*Length)._simplify()' )
        self.assertTrue( koq is Length )     
        self.assertEqual( koq, Length )     

    def test_operations(self):
    
        context = None 
        
        t1 = (1,0)
        t2 = (0,1)
        
        d1 = Dimension( context, t1 )
        d2 = Dimension( context, t2 )
        
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

        self.assertEqual( context._koq_to_dim(Length), Dimension( context, (1,0) ) )
        self.assertEqual( context._koq_to_dim(Time), Dimension( context, (0,1) ) )
        self.assertEqual( context._koq_to_dim(Speed), Dimension( context, (1,-1) ) )

        self.assertTrue( context._dim_to_koq( Dimension( context, (1,-1) ) ) is Speed)
        self.assertTrue( context._dim_to_koq( Dimension( context, (1,0) ) ) is Length)

    def test_as_dict_key(self):
    
        context = None 

        t1 = (1,0)
        d1 = Dimension( context, t1 )
        d = {d1:t1}
        self.assertEqual( d[d1], t1 )

#============================================================================
if __name__ == '__main__':
    unittest.main()