from __future__ import print_function
from __future__ import division 

import unittest

from QV import * 
from QV.prefix import *
from QV.kind_of_quantity import Number
from QV.quantity_value import ValueUnit

#----------------------------------------------------------------------------
class TestQuantityValue(unittest.TestCase):

    def test_construction(self):
    
        context = Context( ('Length','L') )
        SI =  UnitRegister("SI",context)
        metre = SI.unit( RatioScale(context['Length'],'metre','m') )
        
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
        
        metre = SI.unit( RatioScale(context['Length'],'metre','m') )
        centimetre = SI.unit( centi(metre) )
        SI.conversion_function_values(centimetre,metre,centi.value)
        
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
        qv2 = qvalue(x2,centimetre)
        vu = qv1 + qv2 
        # ... the result will be expressed in reference units
        self.assertAlmostEqual( value(vu), x1 + x2/100, 15 )       
        self.assertTrue( unit(vu) is metre )

        vu = qv1 - qv2 
        self.assertAlmostEqual( vu.value, x1 - x2/100, 15 )       
        self.assertTrue( vu.unit is metre )
        
        # QV object on the right
        qv4 = 1 + qvalue( 2, SI.Number.unity )
        self.assertAlmostEqual(qv4.value,3)
        self.assertEqual(qv4.unit,SI.Number.unity)

        qv5 = 1 - qvalue( 2, SI.Number.unity )
        self.assertAlmostEqual(qv5.value,-1)
        self.assertEqual(qv5.unit,SI.Number.unity)

        # Illegal case 
        Imperial = UnitRegister("Imperial",context)
        foot = Imperial.unit( RatioScale(context['Length'],'foot','ft') )
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

        metre = si.unit( RatioScale(context['Length'],'metre','m') )
        second = si.unit( RatioScale(context['Time'],'second','s') )
        metre_per_second = si.unit( RatioScale(context['Speed'],'metre_per_second','m*s-1') )
        metre_per_second_per_second = si.unit( RatioScale(
            context['Acceleration'],
            'metre_per_second_per_second',
            'm*s-2'
        ))

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
        kilometre = ureg.unit( RatioScale(context['Distance'],'kilometre','km') )
        litre = ureg.unit( RatioScale(context['Volume'],'litre','L') )

        litres_per_km = ureg.unit( RatioScale(context['FuelConsumption'],'litres_per_km','L/km)') )
        
        litres_per_100_km = ureg.unit( 
            proportional_unit(
                ureg.FuelConsumption.litres_per_km,
                'litres_per_100_km','L/(100 km)',
                Fraction(1,100)
            )
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
        self.assertAlmostEqual( required.value, distance.value * 2.2/(25.6), 15 )

    def test_dimensionless(self):
    
        context = Context( ("Current","I"),("Voltage","V") )
        context.declare('Resistance','R','Voltage/Current')
        ureg =  UnitRegister("ureg",context)

        volt = ureg.unit( RatioScale(context['Voltage'],'volt','V') )
        microvolt = ureg.unit( micro(volt) )

        ampere = ureg.unit( RatioScale(context['Current'],'ampere','A') )
        ohm = ureg.unit( RatioScale(context['Resistance'],'Ohm','Ohm') )

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
        r_ratio = ureg.unit( RatioScale(context['Resistance_ratio'],'ohm_per_ohm','Ohm/Ohm') )

        v_divider = qratio( r2,(r1+r2) )    
        
        self.assertTrue( v_divider.unit.is_dimensionless )
        self.assertTrue( v_divider.unit.is_ratio_of(ohm.kind_of_quantity) )

        # Voltage divider
        context.declare('Voltage_ratio','V/V','Voltage//Voltage')
        volt_per_volt= ureg.unit( RatioScale(context['Voltage_ratio'],'volt_per_volt','V/V') )
        volt_per_millivolt = ureg.unit(
            proportional_unit(volt_per_volt,'volt_per_millivolt','V/mV',1E3)
        )
        volt_per_microvolt = ureg.unit( 
            proportional_unit(volt_per_volt,'volt_per_micovolt','V/uV',1E6)
        )
        
        v1 = qvalue(0.5,volt)
        v2 = qvalue(0.5,microvolt)
        gain = qratio( v1, v2 )
        
        self.assertAlmostEqual( 1000000.0, qresult(gain).value )
        self.assertEqual( "1.0 V/uV", str( qresult(gain,volt_per_microvolt) ) )
        self.assertEqual( "1000.0 V/mV", str( qresult(gain,volt_per_millivolt) ) )
        self.assertEqual( "1000000.0 V/V", str( qresult(gain,volt_per_volt) ) )
        # Inappropriate unit
        self.assertRaises( RuntimeError, qratio, v1, v2, unit = volt  )
        
#============================================================================
if __name__ == '__main__':
    unittest.main()