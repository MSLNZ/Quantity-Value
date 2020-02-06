# from QV.unit_register import _prefixed_unit
from QV.scale import Unit 

#----------------------------------------------------------------------------
class Prefix(object):

    """
    Holds the name, term and scale factor for a prefix
    and can be called to generate a new related unit.
    """
    
    def __init__(self,name,term,value):
        self.name = name 
        self.term = term 
        self.value = value
        
    def __repr__(self):
        return "{!s}({!r},{!r},{:.0E})".format(
            self.__class__.__name__,
            self.name,
            self.term,
            self.value
        )
        
    def __str__(self):
        return str(self.term) 
        
    def __call__(self,reference_unit):
        """Return a new unit related to reference unit"""
        
        kind_of_quantity = reference_unit.scale.kind_of_quantity
        register = reference_unit._register 

        # Check that `reference_unit` is in the register,
        # because things like `centi(centi(metre))` are not permitted.
        if not reference_unit is register.reference_unit_for(
            reference_unit.scale.kind_of_quantity
        ):
            raise RuntimeError(
                "{!r} is not a reference unit".format(
                    reference_unit.scale.name
                )  
            )     

        name = "{!s}{!s}".format(
            self.name,
            reference_unit.scale.name
        )
        
        if name in register:
            return register[name]
        else:
            term = "{!s}{!s}".format(
                self.term,
                reference_unit.scale
            )
            
            pq = Unit(
                kind_of_quantity,
                name,
                term,
                register,
                self.value
            )
            
            # Buffer related quantities        
            register._register_by_name(pq)
            
            return pq         
            
#============================================================================
# Metric prefixes (multiples and sub-multiples of 10) 
#
yocto =         Prefix('yocto','5',1E-24)
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