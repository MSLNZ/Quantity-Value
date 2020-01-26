.. _unit_register:

*************
Unit register
*************

The :mod:`.unit_register` combines with the :mod:`.scale` module and the :mod:`.context` module to provide support for units. A :class:`.UnitRegister` is associated with a :class:`.Context`, which allows the validity of unit expressions to be checked by quantity calculus. The unit register holds a collection of :class:`.Unit` objects, which are classified as reference units or related units. There can be only one reference unit for each kind of quantity, but any number of related units. Each related unit has a multiplier that can be used to convert a measure expressed in the related unit to a measure expressed in the reference unit. 

Units are declared by providing the name of the kind of quantity, the unit name and a term symbol (short name) for the unit, for example ::

    SI =  UnitRegister("SI",context)
    metre = SI.unit('Length','metre','m')   # reference unit
    centimetre = metric_prefix.centi(metre) # related unit 
    
Units can be looked up in the register by name or by term, or the name may be used as an attribute of the register. These expressions return the ``metre`` unit ::

    SI['metre'] 
    SI['m']
    SI.metre
    

.. contents::
   :local:


.. _unit_register_module:

.. automodule:: QV.unit_register
    :members: 
    :inherited-members:
