from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 
from QV.prefix import *
from QV.quantity_value import ValueUnit

#----------------------------------------------------------------------------
class TestQuantityValue(unittest.TestCase):

    def test_construction(self):
    
        context = Context( ('Length','L') )
        SI =  UnitRegister("SI",context)
        Length = 'Length'
        metre = SI.reference_unit(Length,'metre','m')
        
        x = 1.234
        vu = qvalue(x,metre)
        
        self.assertTrue( isinstance(vu,ValueUnit) )
        self.assertTrue( unit(vu) is metre )
        self.assertAlmostEqual( value(vu), x, 15 )       
        self.assertTrue( vu.unit is metre )
        self.assertAlmostEqual( vu.value, x, 15 )       
 
    def test_simple_addition_subtraction(self):
        
        context = Context( ('Length','L') )
        SI =  UnitRegister("SI",context)
        Length = 'Length'
        
        metre = SI.reference_unit(Length,'metre','m')

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
        
        # When units have different prefixes ...
        qv2 = qvalue(x2,centi(metre))
        vu = qv1 + qv2 
        # ... the result will be expressed in the lesser of the units 
        self.assertAlmostEqual( value(vu), x1*100 + x2, 15 )       
        self.assertTrue( unit(vu) is centi(metre) )

        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.value, x1*100 - x2, 15 )       
        self.assertTrue( vu.unit is centi(metre) )

        # Illegal case 
        Imperial = UnitRegister("Imperial",context)
        foot = Imperial.reference_unit(Length,'foot','ft')
        qv3 = qvalue(x1,foot)
        
        # When QVs use different unit registers, they cannot be combined
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

    def test_simple_kinematics(self):
        # tests multiplication and addition 
        context = Context( ("Length","L"), ("Time","T") )

        Speed = context.declare('Speed','V','Length/Time')
        Acceleration = context.declare('Acceleration','A','Speed/Time')

        si =  UnitRegister("si",context)

        metre = si.reference_unit('Length','metre','m') 
        second = si.reference_unit('Time','second','s') 
        metre_per_second = si.reference_unit('Speed','metre_per_second','m*s-1')
        metre_per_second_per_second = si.reference_unit(
            'Acceleration',
            'metre_per_second_per_second',
            'm*s-2'
        )

        d = qvalue(0.5,metre)
        t = qvalue(1.0,second)

        # average speed 
        self.assertAlmostEqual( qresult(d/t).value, d.value/t.value, 15 )
        self.assertEqual( qresult(d/t).unit, metre_per_second )
        
        # acceleration
        self.assertAlmostEqual( qresult(d/t/t).value, d.value/t.value**2, 15  )
        self.assertEqual( qresult(d/t/t).unit, metre_per_second_per_second )
        
        # displacement
        a0 = qvalue(9.8,metre_per_second_per_second)
        v0 = qvalue(5.2,metre_per_second)
        x0 = qvalue(.3,metre)
        
        displacement = x0 + (v0*t) + (0.5*a0*t*t) 
        self.assertAlmostEqual( 
            displacement.value, 
            x0.value + v0.value*t.value + (a0.value*t.value**2)/2,
            15            
        )

    def test_simple_fuel_consumption(self):
    
        from fractions import Fraction

        context = Context( ("Distance","L"), ("Volume","V")  )
        FuelConsumption = context.declare('FuelConsumption','FC','Volume/Distance')

        ureg =  UnitRegister("ureg",context)

        # Reference units 
        kilometre = ureg.reference_unit('Distance','kilometre','km') 
        litre = ureg.reference_unit('Volume','litre','L')

        ureg.reference_unit('FuelConsumption','litres_per_km','L/km')
        litres_per_100_km = related_unit(
            ureg.litres_per_km,
            Fraction(1,100),
            'litres_per_100_km','L/(100 km)'
        )
         
        # consumption in ad hoc units 
        distance = qvalue(25.6,kilometre)
        fuel = qvalue(2.2,litre)
        consumes = qresult(  fuel/distance, 'L/(100 km)' ) 
        self.assertTrue( consumes.unit is litres_per_100_km )
        self.assertAlmostEqual( consumes.value, 2.2/(25.6/100), 15 )
        
        # further calculation
        distance = qvalue(155,kilometre)
        required = qresult( consumes * distance ) 
        self.assertTrue( required.unit is litre )
        self.assertAlmostEqual( required.value, distance.value * 2.2/25.6, 15 )

    def test_dimensionless(self):
    
        context = Context( ("Current","I"),("Voltage","V") )
        context.declare('Resistance','R','Voltage/Current')
        ureg =  UnitRegister("ureg",context)

        volt = ureg.reference_unit('Voltage','volt','V') 
        ampere = ureg.reference_unit('Current','ampere','A') 
        ohm = ureg.reference_unit('Resistance','Ohm','Ohm')

        v1 = qvalue(0.5,volt)
        i1 = qvalue(1.E-3,ampere)

        r1 = qresult( v1/i1 )
        r2 = qvalue(2.48E3,ohm)
        
        parallel_resistance = qresult( (r1*r2)/(r1 + r2) ) 
        self.assertTrue( parallel_resistance.unit is ohm )
        self.assertAlmostEqual( 
            parallel_resistance.value,
            (r1.value*r2.value)/(r1.value + r2.value)
        )

        Resistance_ratio = context.declare('Resistance_ratio','R/R','Resistance//Resistance')
        r_ratio = ureg.reference_unit('Resistance_ratio','ohm_per_ohm','Ohm/Ohm')

        v_divider = qratio( r2,(r1+r2) )    
        
        self.assertTrue( v_divider.unit.is_dimensionless )
        self.assertTrue( v_divider.unit.is_ratio_of(ohm.kind_of_quantity) )

#============================================================================
if __name__ == '__main__':
    unittest.main()