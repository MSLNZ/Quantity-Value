.. _scale:

*****
Scale
*****

The :mod:`.scale` module contains classes :class:`.Scale` and :class:`.Unit` which implement the behaviour of units in ``QV``. 

At present the scale type is always 'metric', or 'rational', which means that all scales for the same kind of quantity are proportional (conversion from one scale to another requires only a multiplicative scale factor). This will change in future. We will extend the implementation to support 'interval' scales (to convert from one interval scale to another requires a scale factor and an offset).

The :class:`.UnitRegister` class handles the creation of :class:`.Scale` and :class:`.Unit` instances.

.. contents::
   :local:


.. _scale_module:

.. automodule:: QV.scale
    :members: 
    :inherited-members:
