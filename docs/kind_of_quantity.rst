.. _kind_of_quantity:

****************
Kind of Quantity
****************

.. contents::
   :local:

A :class:`.KindOfQuantity` represents the general notion of a quantity, such as: a length, mass, speed, etc. This can be contrasted with more specific quantity definitions, like: my height, your weight, etc. 

:class:`.KindOfQuantity` objects are defined (and identified) by a name and a term (a short name). For example, this code creates a new context with the base kinds of quantity Length and Time ::

    context = Context( ("Length","L"), ("Time","T") )
    Length, Time = context.base_quantities
    
Quantity calculus is defined for :class:`.KindOfQuantity` objects (see, :mod:`.context`).

.. _kind_of_quantity_module:

.. automodule:: QV.kind_of_quantity
    :members: 
    :inherited-members:
