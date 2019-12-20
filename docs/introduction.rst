.. _introduction:

************
Introduction
************

The ``quantity_value`` package supports the representation of physical quantities as a value paired with a unit of measurement, for example 10.5 kg. Using ``quantity_value``, it is possible to define this quantity ::

    >>> m = quantity_value(10.5,kg) 
    
and manipulate it in mathematical expressions. The semantics of quantities and rules governing calculations are handled by the package.

The package will become a tool to ensure quantity correctness in calculations that manipulate physical quantities, but that is not an easy goal. It is in the early stages of development, exploring a novel approach to solve this problem. 