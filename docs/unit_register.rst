.. _unit_register:

*************
Unit register
*************

The unit register holds a collection of :class:`.RegisteredUnit` objects, which are a generalisation of the conventional notion of a measurement unit. Some :class:`.RegisteredUnit` objects are considered as reference units, the others are called related units. There can be only one reference unit for each kind of quantity, but any number of related units. Each related unit has a multiplier that can be used to convert a measure expressed in the related unit to a measure expressed in the reference unit. 

The :mod:`.unit_register` is associated with a :class:`.Context` to allow the validity of unit expressions to be checked by quantity calculus. 

Units are declared by providing the name of the kind of quantity, the name of a scale (unit) and a term symbol (short name for the unit), for example 

.. code-block:: python

    from QV import *
    
    context = Context(('Length','L'))

    SI =  UnitRegister("SI",context)
    metre = SI.unit( RatioScale(context.Length,'metre','m') )   # reference unit
    centimetre = SI.unit( prefix.centi(metre) ) # related unit 

.. contents::
   :local:

.. _unit_register_module:

.. automodule:: QV.unit_register
    :members: 
    :inherited-members:
