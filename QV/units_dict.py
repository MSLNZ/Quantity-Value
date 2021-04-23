from collections.abc import MutableMapping

class UnitsDict(MutableMapping):

    """
    A `dict`-like mapping of names, and short names (symbols), to 
    objects representing units.
    
    The names and short names are keys. They are unique and cannot be 
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
        # so we would need to find the other key using
        # the unit. This has not been implemented yet.
        del self._units[key]
            
    def __iter__(self):
        return iter(self._units)

    def __len__(self):
        return len(self._units)

    def __getattr__(self, attr):
        if attr in self._units:
            return self._units[attr]
        else:
            raise AttributeError( "{!r} not found".format(attr) )
                       
#============================================================================
if __name__ == '__main__':
    
    ud = UnitsDict(metre='m',kilogram='kg')
    ud.update( {'second':'s_unit', 's':'s_unit'} )
    print( repr(ud) )
    print( ud.s )
    del ud['s']
    print( repr(ud) )
    print( ud.second )
