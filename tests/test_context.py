from __future__ import print_function
from __future__ import division 

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import ValueDuplicationError

import unittest
 
from QV import * 
from QV.dimension import Dimension 

#----------------------------------------------------------------------------
class TestContext(unittest.TestCase):

    def test_construction(self):

        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        Length = context['Length'] 
        Time = context['Time']
    
        self.assertEqual( len(context._koq_dimension[Length]), 2 )
        
        d1 = context._koq_to_dim(Length)
        self.assertEqual( d1, Dimension( context, (1,0) ) )
        
        d2 = context._koq_to_dim(Time)
        self.assertEqual( d2, Dimension( context, (0,1) ) )

        self.assertTrue( Length is context._dim_to_koq( d1 ) ) 
        self.assertTrue( Time is context._dim_to_koq( d2 ) )
   
    def test_decalare(self):
    
        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        Speed = context.declare('Speed','V','Length/Time')
        
        self.assertTrue( Speed is context['Speed'] )
        self.assertTrue( Speed is context['V'] )
        self.assertTrue( context._koq_to_dim(Speed) == Dimension( context, (1,-1), () ) )
        
        # Multiplication by a number of the left is OK
        self.assertTrue( Speed is context.evaluate('1*Length/Time') )
        # Multiplication by a number on the right is not tolerated
        self.assertRaises( KeyError, context.evaluate,'Length*1/Time' )
        # Division by a number on the left is OK
        self.assertTrue( Speed is context.evaluate('Length*(1/Time)') )
        # Division by by a number on the right is not tolerated
        self.assertRaises( KeyError, context.evaluate,'Length/Time/1' )
 
        self.assertTrue( Speed is context._dim_to_koq( Dimension( context, (1,-1) ) ) ) 
        self.assertEqual( context._koq_to_dim(Speed), Dimension( context, (1,-1) ) )

        SpeedRatio = context.declare('SpeedRatio','V/V','Speed//Speed')

        self.assertEqual( context._koq_to_dim(SpeedRatio), Dimension( context, (1,-1), (1,-1)) )
        self.assertTrue( SpeedRatio is context._dim_to_koq( Dimension( context, (1,-1), (1,-1)) ) )
        
        self.assertTrue( context.dimensions('SpeedRatio').is_dimensionless )

    def test_evaluate(self):

        context = Context(
            ('Length','L'),
            ('Time','T'),
            ('Mass','M')
        )
        
        Speed = context.declare('Speed','V','Length/Time')
 
        SpeedRatio = context.declare('SpeedRatio','V//V','Speed//Speed')

        self.assertTrue( Speed is context.evaluate('Length/Time') )
        self.assertTrue( SpeedRatio is context.evaluate( '(Length/Time)//(Length/Time)' ) )
        
    def test_failures(self):

        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        # Cannot define something that already exists
        self.assertRaises(RuntimeError,context.declare,"Length","L",'Length')
        
        # Cannot just declare a new dimension 
        self.assertRaises(RuntimeError,context.declare,"Mass","M",'Length')

        # Cannot associate a new kind of quantity with an existing dimension
        self.assertRaises(
            ValueDuplicationError,
            context.declare,
            'Mass','M',             # Mass has not yet been declared, so OK
            'Length*Length/Length'  # reduces to Length, which is already in use
        )
        
        # The dimension must be resolved to a base or declared quantity 
        self.assertRaises(
            RuntimeError,
            context.evaluate,
            'Length*Length'
        )
 
    def test_simple_quantity_calculus(self):
        
        context = Context( ("Current","I"),("Voltage","V"),("Time","T") )

        context.declare('Resistance','R','Voltage/Current')
        context.declare('Power','P','V*V/R')

        Voltage = context['Voltage']
        Resistance = context['Resistance']

        I = context.evaluate(  Voltage/Resistance )
        self.assertEqual( 
            context.dimensions(I), context.dimensions('Current') 
        )
        tmp = context.evaluate( I*Voltage )
        self.assertEqual( 
            context.dimensions(tmp), context.dimensions('Power') 
        )
#============================================================================
if __name__ == '__main__':
    unittest.main()