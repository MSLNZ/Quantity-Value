from __future__ import print_function
from __future__ import division 

import warnings
warnings.filterwarnings(
    "ignore", 
    message="Python 2 support will be dropped in a future release."
)
from bidict import ValueDuplicationError

import unittest
 
from quantity_value.kind_of_quantity import * 
from quantity_value.dimension import * 
from quantity_value.context import *

#----------------------------------------------------------------------------
class TestKindOfQuantity(unittest.TestCase):

    def test_construction(self):
        name = 'Length'
        term = 'L'
        
        Length = KindOfQuantity(name,term) 
        
        self.assertTrue( type(Length) is KindOfQuantity )
        self.assertEqual( Length.name, name )
        self.assertEqual( str(Length), term )

#----------------------------------------------------------------------------
class TestDimension(unittest.TestCase):

    def test_construction(self):

        Length = KindOfQuantity('Length','L') 
        Time = KindOfQuantity('Time','T')
    
        context = Context(Length,Time)
        
        self.assertEqual( len(context._koq_dimension[Length]), 2 )
        
        d1 = context.dimension(Length)
        self.assertEqual( d1, Dimension( (1,0) ) )
        d2 = context.dimension(Time)
        self.assertEqual( d2, Dimension( (0,1) ) )

        self.assertTrue( Length is context.kind_of_quantity( d1 ) ) 
        self.assertTrue( Time is context.kind_of_quantity( d2 ) )
   
    def test_decalare(self):
    
        Length = KindOfQuantity('Length','L') 
        Time = KindOfQuantity('Time','T')
    
        context = Context(Length,Time)
 
        Speed = KindOfQuantity('Speed','V')
        context.declare(Speed,Length/Time)
 
        self.assertTrue( Speed is context.kind_of_quantity( Dimension( (1,-1) ) ) ) 
        self.assertEqual( context.dimension(Speed), Dimension( (1,-1) ) )

        SpeedRatio = KindOfQuantity('SpeedRatio','V/V')
        context.declare(SpeedRatio,(Speed).ratio(Speed))

        self.assertEqual( context.dimension(SpeedRatio), Dimension( (1,-1), (1,-1)) )
        self.assertTrue( SpeedRatio is context.kind_of_quantity( Dimension( (1,-1), (1,-1)) ) ) 
        self.assertTrue( 
            context.dimension(SpeedRatio).simplify().is_dimensionless
        )

    def test_evaluate(self):

        Length = KindOfQuantity('Length','L') 
        Time = KindOfQuantity('Time','T')
        Mass = KindOfQuantity('Mass','M')
    
        context = Context(Length,Time,Mass)
        
        Speed = KindOfQuantity('Speed','V')
        context.declare(Speed,Length/Time)
 
        SpeedRatio = KindOfQuantity('SpeedRatio','V/V')
        context.declare(SpeedRatio,(Speed).ratio(Speed))

        self.assertTrue( Speed is context.evaluate(Length/Time) )
        self.assertTrue( SpeedRatio is context.evaluate( (Length/Time).ratio(Length/Time) ) )
        
    def test_failures(self):

        Length = KindOfQuantity('Length','L') 
        Time = KindOfQuantity('Time','T')
        Mass = KindOfQuantity('Mass','M')
    
        context = Context(Length,Time)

        # Cannot define something that already exists
        self.assertRaises(RuntimeError,context.declare,Length,Length)
        
        # Cannot just declare a new dimension 
        self.assertRaises(AttributeError,context.declare,Mass,Length)

        # Cannot associate a new kind of quantity with an existing dimension
        self.assertRaises(
            ValueDuplicationError,
            context.declare,
            Mass,                   # Mass has not yet been declared, so OK
            Length*Length/Length    # reduces to Length, which is already in use
        )
        
        # The dimension must resolve to a base or declared quantity 
        self.assertRaises(
            RuntimeError,
            context.evaluate,
            Length*Length
        )
 
        # Arguments must have been declared or be in the basis
        self.assertRaises(
            KeyError,
            context.evaluate,
            Length*Mass
        )
 
#============================================================================
if __name__ == '__main__':
    unittest.main()