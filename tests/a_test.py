from QV import *

context = Context( ("Length","L"),("Time","T"), ('Mass','M'), ('Data','D') )

SI =  UnitRegister("SI",context)

metre = SI.unit( RatioScale(context['Length'],'metre','m') )
second = SI.unit( RatioScale(context['Time'],'second','s') )
kilogram = SI.unit( RatioScale(context['Mass'],'kilogram','kg') )

centimetre = SI.unit( prefix.centi(metre.scale) ) 
SI.conversion_function_values(metre,centimetre,1.0/prefix.centi.value)

m_2_cm = SI.conversion_from_A_to_B(metre,centimetre)

# print( m_2_cm(10) )

# for p_i in prefix.metric_prefixes: 
     # prefixed_scale = p_i(second.scale)
     # print( "{0.name} ({0.symbol}): {0.prefix:.1E}".format(prefixed_scale) )
     

# byte_scale = RatioScale('Data','byte','b') 
# for p_i in prefix.binary_prefixes: 
    # prefixed_scale = p_i(byte_scale)
    # print( "{0.name} ({0.symbol}): {0.prefix}".format(prefixed_scale) )
    
print( SI.Length )