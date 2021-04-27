from QV.scale import RatioScale 
from QV.unit_register import proportional_unit

#----------------------------------------------------------------------------
class Prefix(object):

    """
    Holds the name, short name (symbol) and scale factor 
    for a prefix. It can be called to generate a new unit.
   
    For example::
    
        >>> context = Context( ('Length','L') )
        >>> SI =  UnitRegister("SI",context)
        >>> metre = SI.unit( RatioScale(context['Length'],'metre','m') )
        >>> centimetre = SI.unit( prefix.centi(metre) )
        >>> SI.conversion_function_values(metre,centimetre,prefix.centi.value)
        >>> print( centimetre )
        cm
        
    """
    
    def __init__(self,name,symbol,value):
        self.name = name 
        self.symbol = symbol 
        self.value = value
        
    def __repr__(self):
        return "{!s}({!r},{!r},{:.0E})".format(
            self.__class__.__name__,
            self.name,
            self.symbol,
            self.value
        )
        
    def __str__(self):
        return str(self.symbol) 
        
    def __call__(self,unit):
        register = unit.register 
        scale = unit.scale
        
        if not isinstance(scale,RatioScale):
            raise RuntimeError(
                "cannot apply a conversion factor to {!r}".format(scale) 
            )
            
        # Must be applied to a reference unit
        if register.reference_unit_for(unit) is not unit:
            raise RuntimeError(
                "{!r} is a derived scale".format(scale)
            )

        name = "{!s}{!s}".format(
            self.name,
            scale.name
        )
 
        symbol = "{!s}{!s}".format(
            self.symbol,
            scale.symbol
        )
         
        # Note the scale is returned unregistered         
        return proportional_unit(unit,name,symbol,self.value)
              
            
#============================================================================
# Metric prefixes (multiples and sub-multiples of 10) 
#
yocto =         Prefix('yocto','y',1E-24)
zepto =         Prefix('zepto','z',1E-21)
atto =          Prefix('atto','a',1E-18)
femto =         Prefix('femto','f',1E-15)
pico =          Prefix('pico','p',1E-12)
nano =          Prefix('nano','n',1E-9)
micro =         Prefix('micro','u',1E-6)
milli =         Prefix('milli','m',1E-3)
centi =         Prefix('centi','c',1E-2)
deci =          Prefix('deci','d',1E-1)
deka =          Prefix('deka','da',1E1)
hecto =         Prefix('hecto','h',1E2)
kilo =          Prefix('kilo','k',1E3)
mega =          Prefix('mega','M',1E6)
giga =          Prefix('giga','G',1E9)
tera =          Prefix('tera','T',1E12)
peta =          Prefix('peta','P',1E15)
exa =           Prefix('exa','E',1E18)
zetta =         Prefix('zetta','Z',1E21)
yotta =         Prefix('yotta','Y',1E24)

# Useful to iterate over 
metric_prefixes = (
    yocto, zepto, atto, femto,
    pico, nano, micro, milli,
    centi, deci,
    deka, hecto,
    kilo, mega, giga, tera,
    peta, exa, zetta, yotta
)
"""A collection of all metric prefixes. 

    Useful for generating all related units by iteration::
    
        >>> context = Context( ('Time','T') )
        >>> second = SI.unit( RatioScale(context['Time'],'second','s') )  
        >>> for p_i in prefix.metric_prefixes: 
        ...     prefixed_scale = p_i(second.scale)
        ...     print( "{0.name} ({0.symbol}): {0.prefix:.1E}".format(prefixed_scale) )
        ...
        yoctosecond (ys): 1.00E-24
        zeptosecond (zs): 1.00E-21
        attosecond (as): 1.00E-18
        femtosecond (fs): 1.00E-15
        picosecond (ps): 1.00E-12
        nanosecond (ns): 1.00E-09
        microsecond (us): 1.00E-06
        millisecond (ms): 1.00E-03
        centisecond (cs): 1.00E-02
        decisecond (ds): 1.00E-01
        dekasecond (das): 1.00E+01
        hectosecond (hs): 1.00E+02
        kilosecond (ks): 1.00E+03
        megasecond (Ms): 1.00E+06
        gigasecond (Gs): 1.00E+09
        terasecond (Ts): 1.00E+12
        petasecond (Ps): 1.00E+15
        exasecond (Es): 1.00E+18
        zettasecond (Zs): 1.00E+21
        yottasecond (Ys): 1.00E+24
"""

# The kilogram is a special case. 
def si_mass_units(kg_unit):
    """
    Generate multiples and sub-multiples for SI mass units
    
    ``kg_unit`` must be defined, with 
    name ``kilogram`` and symbol ``kg``
    
    Example::
    
        >>> context = Context( ('Mass','M') )
        >>> SI =  UnitRegister("SI",context)        
        >>> kilogram = SI.unit( RatioScale(context['Mass'],'kilogram','kg') )  
        >>> prefix.si_mass_units(kilogram)
        >>> print( SI.Mass.gram.scale.name )
        gram
        >>> print( repr(SI.Mass.gram) )
        RegisteredUnit(KindOfQuantity('Mass','M'),'gram','g')        


    """
    if (
        kg_unit.scale.name != 'kilogram' and 
        kg_unit.scale.symbol != 'kg'
    ):
        raise RuntimeError(
            "conventional name required, got {0.name} and{0.symbol}".format(
                kg_unit.scale
            )
        )
        
    register = kg_unit.register
    
    gram = register.unit( 
        proportional_unit(kg_unit,
                    'gram',
                    'g', 
                    1.0 / 1000.0,
        )
    )
      
    for p_i in metric_prefixes:
        if p_i.value != 1E3: 
            register.unit( 
                proportional_unit(kg_unit,
                    p_i.name+'gram',
                    p_i.symbol+'g', 
                    p_i.value / 1000.0
                )
            )
    
#============================================================================
# Binary prefixes 
#
kibi =          Prefix('kibi','ki',1048)        
mebi =          Prefix('mebi','Mi',1048**2)
gibi =          Prefix('gibi','Gi',1048**3)
tebi =          Prefix('tebi','Ti',1048**4)
pebi =          Prefix('pebi','Pi',1048**5)
exbi =          Prefix('exbi','Ei',1048**6)
zebi=           Prefix('zebi','Zi',1048**7)
yobi =          Prefix('yotta','Yi',1048**8)

# Useful to iterate over 
binary_prefixes = (
    kibi, mebi, gibi, tebi,
    pebi, exbi, zebi, yobi
)
"""A collection of binary prefixes. 

    Useful for generating all related units by iteration::
    
        >>> byte_scale = RatioScale('Data','byte','b')
        >>> for p_i in prefix.binary_prefixes: 
        ...     prefixed_scale = p_i(byte_scale)
        ...     print( "{0.name} ({0.symbol}): {0.prefix}".format(prefixed_scale) )
        ...        
        kibibyte (kib): 1048
        mebibyte (Mib): 1098304
        gibibyte (Gib): 1151022592
        tebibyte (Tib): 1206271676416
        pebibyte (Pib): 1264172716883968
        exbibyte (Eib): 1324853007294398464
        zebibyte (Zib): 1388445951644529590272
        yottabyte (Yib): 1455091357323467010605056

"""