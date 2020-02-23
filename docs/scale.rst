.. _scale:

*****
Scale
*****

The :mod:`.scale` module contains the classes :class:`.Scale` and :class:`.Unit`, which implement unit behaviour. 

The :class:`.Scale` class represents the conventional notion of a measurement scale (commonly called a unit). The :class:`.Unit` class extends this notion by associating a particular kind of quantity with a scale. 

At present, all scales associated with the same kind of quantity are proportional to one another (conversion from one scale to another requires only a multiplicative scale factor). However, this may change in future. We will probably implement support for 'interval' scales (for which a scale factor and an offset are needed to convert from one scale to another).

The :class:`.UnitRegister` class handles the creation of :class:`.Scale` and :class:`.Unit` instances.

.. contents::
   :local:


.. _scale_module:

.. automodule:: QV.scale
    :members: 
    :inherited-members:
