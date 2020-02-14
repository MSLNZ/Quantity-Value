==============
Quantity-Value
==============

|docs| |travis| |appveyor| |pypi|

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
    >>> volt = ureg.reference_unit('Voltage','volt','V') 
    >>> amp = ureg.reference_unit('Current','amp','A') 
    >>> milliamp = prefix.milli(amp)
    >>> ohm = ureg.reference_unit('Resistance','Ohm','Ohm')
    
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


.. |docs| image:: https://readthedocs.org/projects/quantity-value/badge/?version=latest
    :target: https://quantity-value.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/MSLNZ/Quantity-Value/master.svg?label=Travis-CI
    :target: https://travis-ci.org/MSLNZ/Quantity-Value

.. |appveyor| image:: https://img.shields.io/appveyor/ci/jborbely/Quantity-Value/master.svg?label=AppVeyor
    :target: https://ci.appveyor.com/project/jborbely/Quantity-Value/branch/master

.. |pypi| image:: https://badge.fury.io/py/Quantity-Value.svg
    :target: https://badge.fury.io/py/Quantity-Value

