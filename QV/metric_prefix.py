from QV.unit_register import metric_unit

#----------------------------------------------------------------------------
class MetricPrefix(object):
    
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
pico =      MetricPrefix('pico','p',1E-12)
nano =      MetricPrefix('nano','n',1E-9)
micro =     MetricPrefix('micro','u',1E-6)
milli =     MetricPrefix('milli','m',1E-3)
centi =     MetricPrefix('centi','c',1E-2)
deci =      MetricPrefix('deci','d',1E-1)
deka =      MetricPrefix('deka','da',1E1)
hecto =     MetricPrefix('hecto','h',1E2)
kilo =      MetricPrefix('kilo','k',1E3)
mega =      MetricPrefix('mega','M',1E6)
giga =      MetricPrefix('giga','G',1E9)
tera =      MetricPrefix('tera','T',1E12)

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

# Common numerical postfixes
#
percent = MetricPrefix('per-cent','%',1E-2)
per_mille = MetricPrefix('per-mille','%%',1E-3)
per_million = MetricPrefix('per-million','ppm',1E-6)
per_billion = MetricPrefix('per-billion','ppb',1E-9)

# Useful to iterate over all postfixes
number_postfixes = (
    percent,
    per_mille,
    per_million,
    per_billion,
)