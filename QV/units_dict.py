from collections import MutableMapping

class UnitsDict(MutableMapping):

    """
    Holds a mapping of names and short names (terms) to units.
    The names and short names are unique and cannot be 
    overwritten once defined (but, they can be deleted).
    """
    
    def __init__(self,*args,**kwargs):
        
        self._units = dict()
        self.update(*args, **kwargs)
 
    def __str__(self):
        return str(self._units) 
        
    def __repr__(self):
        return "{0.__class__.__name__}({0!s})".format(self)
        
    def __getitem__(self, key):
        return self._units[key]

    def __setitem__(self, key, value):
        # Use the fact that keys are also attributes
        if hasattr(self,key):           
            if key in self._units:
                # Require unique keys
                raise RuntimeError(
                    "'{!s}' is the used by {!r} ".format(
                        key,
                        self._units[key]
                    )
                )
            else:
                # Cannot use object attribute names, like 'update'
                raise AttributeError( 
                    "'{!s}' is an attribute of {}".format(
                        key,self.__class__.__name__
                    ) 
                )                
        else:
            self._units[key] = value

    def __delitem__(self, key):
        # NB, usually two keys refer to the same unit 
        del self._units[key]
            
    def __iter__(self):
        return iter(self._units)

    def __len__(self):
        return len(self._units)

    def __getattr__(self, attr):
        try:
            return self._units[attr]
        except KeyError:
            raise AttributeError
                       
#============================================================================
if __name__ == '__main__':
    
    ud = UnitsDict(metre='m',kilogram='kg')
    ud.update( {'second':'s', 's':'s'} )
    print( repr(ud) )
    del ud['s']
    print( repr(ud) )
    print( ud.second )
