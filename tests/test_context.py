from bidict import ValueDuplicationError

import unittest
 
from QV import * 
from QV.signature import Signature 

#----------------------------------------------------------------------------
class TestContext(unittest.TestCase):

    def test_construction(self):

        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        Length = context['Length'] 
        Time = context['Time']
    
        self.assertEqual( len(context._koq_signature[Length]), 2 )
        
        d1 = context._koq_to_signature(Length)
        self.assertEqual( d1, Signature( context, (1,0) ) )
        
        d2 = context._koq_to_signature(Time)
        self.assertEqual( d2, Signature( context, (0,1) ) )

        self.assertTrue( Length is context._signature_to_koq( d1 ) ) 
        self.assertTrue( Time is context._signature_to_koq( d2 ) )
        
        self.assertRaises(RuntimeError,Context,('Length','L'), ('Length','T'))
        self.assertRaises(RuntimeError,Context,('Length','L'), ('Time','L'))
   
    def test_decalare(self):
    
        context = Context(
            ('Length','L'),
            ('Time','T')
        )
        
        Speed = context.declare('Speed','V','Length/Time')
        
        self.assertTrue( Speed is context['Speed'] )
        self.assertTrue( Speed is context['V'] )
        self.assertTrue( context._koq_to_signature(Speed) == Signature( context, (1,-1), () ) )
        
        # Multiplication by a number of the left is OK
        self.assertTrue( Speed is context.evaluate('1*Length/Time') )
        # Multiplication by a number on the right is not tolerated
        self.assertRaises( KeyError, context.evaluate,'Length*1/Time' )
        # Division by a number on the left is OK
        self.assertTrue( Speed is context.evaluate('Length*(1/Time)') )
        # Division by by a number on the right is not tolerated
        self.assertRaises( KeyError, context.evaluate,'Length/Time/1' )
 
        self.assertTrue( Speed is context._signature_to_koq( Signature( context, (1,-1) ) ) ) 
        self.assertEqual( context._koq_to_signature(Speed), Signature( context, (1,-1) ) )

        SpeedRatio = context.declare('SpeedRatio','V/V','Speed//Speed')

        self.assertEqual( context._koq_to_signature(SpeedRatio), Signature( context, (1,-1), (1,-1)) )
        self.assertTrue( SpeedRatio is context._signature_to_koq( Signature( context, (1,-1), (1,-1)) ) )
        
        self.assertTrue( context.signature('SpeedRatio').is_dimensionless )

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
            context.signature(I), context.signature('Current') 
        )
        tmp = context.evaluate( I*Voltage )
        self.assertEqual( 
            context.signature(tmp), context.signature('Power') 
        )
#============================================================================
if __name__ == '__main__':
    unittest.main()