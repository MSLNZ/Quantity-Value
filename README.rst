==============
Quantity-Value
==============

|docs| |github tests| |pypi| |zenodo|

This package provides Python support for physical quantities used in mathematical equations. 

Python objects called quantity-values are used to associate a measured value with a unit of measurement. Calculations involving these objects follow the rules of quantity calculus.

The package can be used to define the quantities, and associated units of measurement, of interest in a specific problem. In that way the context in which quantity calculations are performed is well defined.

Example
=======

Calculations involving electrical measurements can be described in terms of a simple set of base quantities, here we declare current and voltage and the dependent quantity resistance

.. invisible-code-block: pycon

    >>> from __future__ import division

.. code-block:: pycon 

    >>> from QV import *
    >>> context = Context( ("Current","I"),("Voltage","V") )
    >>> Resistance = context.declare('Resistance','R','Voltage/Current')

Units can be declared in terms of these quantities 

.. code-block:: pycon 

    >>> ureg = UnitRegister("ureg",context)
    >>>
    >>> volt = ureg.unit( RatioScale(context['Voltage'],'volt','V') ) 
    >>> amp = ureg.unit( RatioScale(context['Current'],'amp','A') )
    >>> milliamp = ureg.unit( prefix.milli(amp) )
    >>> ohm = ureg.unit( RatioScale(context['Resistance'],'Ohm','Ohm') )
    
and then quantity-values can be created and manipulated

.. code-block:: pycon 
   
    >>> v1 = qvalue(0.10,volt)
    >>> i1 = qvalue(15,milliamp) 
    >>> print( qresult( v1/i1 ) )
    6.6666666666... Ohm
 
Status
======

The Quantity-Value package is part of a research project at the Measurement Standards Laboratory of New Zealand looking at issues in Digital Metrology. 

Quantity-Value is intended as an exemplar for software that supports the concept of a physical quantity and physical quantity calculations.

The project is on-going and should not yet be considered stable. There may be substantial changes in later versions.

Documentation
=============

The documentation for **Quantity-Value** can be found `here <https://quantity-value.readthedocs.io/en/stable/>`_.


.. |docs| image:: https://readthedocs.org/projects/quantity-value/badge/?version=stable
   :target: https://quantity-value.readthedocs.io/en/stable/
   :alt: Documentation Status

.. |github tests| image:: https://github.com/MSLNZ/Quantity-Value/actions/workflows/run-tests.yml/badge.svg
   :target: https://github.com/MSLNZ/Quantity-Value/actions/workflows/run-tests.yml

.. |pypi| image:: https://badge.fury.io/py/Quantity-Value.svg
   :target: https://badge.fury.io/py/Quantity-Value

.. |zenodo| image:: https://zenodo.org/badge/220706236.svg
   :target: https://zenodo.org/badge/latestdoi/220706236
