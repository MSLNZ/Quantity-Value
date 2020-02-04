.. _scale:

*****
Scale
*****

The :mod:`.scale` module contains classes :class:`.Scale` and :class:`.Unit` which implement unit behaviour. 

At present the type of scale is always what is called 'metric', or 'rational', which means that scales for the same kind of quantity are proportional to one another (conversion from one scale to another requires only a multiplicative scale factor). However, this is likely to change in future. We will probably extend the implementation to support 'interval' scales (to convert from one interval scale to another requires a scale factor and an offset).

The :class:`.UnitRegister` class handles the creation of :class:`.Scale` and :class:`.Unit` instances.

.. contents::
   :local:


.. _scale_module:

.. automodule:: QV.scale
    :members: 
    :inherited-members:
