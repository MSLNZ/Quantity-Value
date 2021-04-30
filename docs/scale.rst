.. _scale:

*****
Scale
*****

The :mod:`.scale` module contains the class :class:`.Scale` which implements generic scale behaviour. This class represents the conventional notion of a measurement scale (also commonly called a unit).  

Different categories of scale are implemented as classes derived from :class:`.Scale`: 

    * Instances of :class:`.RatioScale` scales have an absolute zero, like the metre scale for length or the kelvin scale for thermodynamic temperature. 
    
    * :class:`.IntervalScale` scales are measurement scales with an arbitrary zero, like the Fahrenheit and Celsius temperature scales. 

.. contents::
   :local:


.. _scale_module:

.. automodule:: QV.scale
    :members: 
    :inherited-members:
