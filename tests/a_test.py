from QV import *       

quantity = Context( ("Temperature","t") )
ureg = UnitRegister("ureg",quantity)

kelvin = ureg.unit( RatioScale(quantity.Temperature,'kelvin','K') ) 
Celsius = ureg.unit( IntervalScale(quantity.Temperature,'Celsius','C') ) 
Fahrenheit = ureg.unit( IntervalScale(quantity.Temperature,'Fahrenheit','F') ) 

ureg.conversion_function_values(kelvin,Celsius,1,-273.15)
ureg.conversion_function_values(kelvin,Fahrenheit,1.8,-459.67)
ureg.conversion_function_values(Fahrenheit,kelvin,1.0/1.8,459.67/1.8)

degrees_K = ureg.conversion_from_A_to_B(Fahrenheit,kelvin)
degrees_C = ureg.conversion_from_A_to_B(kelvin,Celsius)
degrees_F = ureg.conversion_from_A_to_B(kelvin,Fahrenheit)

x = qvalue( 65, Fahrenheit ) 
y = (x + x)
print( x, repr(x.unit.scale) )
print( qresult(x,preferred_unit=kelvin) )
