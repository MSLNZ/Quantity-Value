from QV import *

# context = Context( ("Length","L"),("Time","T"), ('Mass','M'), ('Data','D') )

# SI =  UnitRegister("SI",context)

# metre = SI.unit( RatioScale(context['Length'],'metre','m') )
# second = SI.unit( RatioScale(context['Time'],'second','s') )
# kilogram = SI.unit( RatioScale(context['Mass'],'kilogram','kg') )

# centimetre = SI.unit( prefix.centi(metre.scale) ) 

# SI.conversion_function_values(centimetre,metre,prefix.centi.value)

# print( qvalue(1,centimetre) + qvalue(1,centimetre) )

# print( qresult( qvalue(1,centimetre) + qvalue(1,centimetre), preferred_unit=SI.Length.metre ) )
# print( qresult( qvalue(1,centimetre) + qvalue(1,centimetre) ) )
# m_2_cm = SI.conversion_from_A_to_B(metre,centimetre)

# print( m_2_cm(10) )

# for p_i in prefix.metric_prefixes: 
     # prefixed_scale = p_i(second.scale)
     # print( "{0.name} ({0.symbol}): {0.prefix:.1E}".format(prefixed_scale) )
     

# byte_scale = RatioScale('Data','byte','b') 
# for p_i in prefix.binary_prefixes: 
    # prefixed_scale = p_i(byte_scale)
    # print( "{0.name} ({0.symbol}): {0.prefix}".format(prefixed_scale) )
    
# context = Context( ("Current","I"),("Voltage","V") )
# context.declare('Resistance','R','Voltage/Current')
# ureg =  UnitRegister("ureg",context)

# volt = ureg.unit( RatioScale(context['Voltage'],'volt','V') )
# ampere = ureg.unit( RatioScale(context['Current'],'ampere','A') )
# milliampere = ureg.unit( prefix.milli(ampere) )
# ohm = ureg.unit( RatioScale(context['Resistance'],'Ohm','Ohm') )

# v1 = qvalue(0.5,volt)
# i1 = qvalue(1,milliampere)

# print( qresult( v1/i1 ) )

# from fractions import Fraction

# context = Context( ("Distance","L"), ("Volume","V")  )
# FuelConsumption = context.declare('FuelConsumption','FC','Volume/Distance')

# ureg =  UnitRegister("ureg",context)

# # Reference units 
# kilometre = ureg.unit( RatioScale(context['Distance'],'kilometre','km') )
# litre = ureg.unit( RatioScale(context['Volume'],'litre','L') )

# litres_per_km = ureg.unit( RatioScale(context['FuelConsumption'],'litres_per_km','L/km)') )

# litres_per_100_km = ureg.unit( 
    # proportional_unit(
        # ureg.FuelConsumption.litres_per_km,
        # 'litres_per_100_km','L/(100 km)',
        # Fraction(1,100)
    # )
# )
 
# # consumption in ad hoc units 
# distance = qvalue(25.6,kilometre)
# fuel = qvalue(2.2,litre)
# consumes = qresult(  fuel/distance, 'L/(100 km)' )
# print((consumes))        

quantity = Context( ("Temperature","t") )
ureg = UnitRegister("ureg",quantity)
kelvin = ureg.unit( RatioScale(quantity.Temperature,'kelvin','K') ) 
Celsius = ureg.unit( IntervalScale(quantity.Temperature,'Celsius','C') ) 

ureg.conversion_function_values(kelvin,Celsius,1,0,-273.15)
degrees_C = ureg.conversion_from_A_to_B(kelvin,Celsius)
print( degrees_C( 273.15 ), Celsius )
