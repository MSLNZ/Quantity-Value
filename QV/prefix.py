from QV.unit_register import metric_unit

#----------------------------------------------------------------------------
class Prefix(object):
    
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
        
    def __call__(self,metric_reference_unit):
        return metric_unit(self,metric_reference_unit)
        
#============================================================================
# Common metric prefixes
#
pico =      Prefix('pico','p',1E-12)
nano =      Prefix('nano','n',1E-9)
micro =     Prefix('micro','u',1E-6)
milli =     Prefix('milli','m',1E-3)
centi =     Prefix('centi','c',1E-2)
deci =      Prefix('deci','d',1E-1)
deka =      Prefix('deka','da',1E1)
hecto =     Prefix('hecto','h',1E2)
kilo =      Prefix('kilo','k',1E3)
mega =      Prefix('mega','M',1E6)
giga =      Prefix('giga','G',1E9)
tera =      Prefix('tera','T',1E12)

# Useful to iterate over all prefixes
metric_prefixes = (
    pico,
    nano,
    micro,
    milli,
    centi,
    deci,
    deka,
    hecto,
    kilo,
    mega,
    giga,
    tera
)
