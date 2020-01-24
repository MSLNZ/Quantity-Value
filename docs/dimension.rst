.. _dimension:

*********
Dimension
*********

The :class:`.Dimension` class defines objects that encapsulate the dimensions associated with the measure of a quantity. 

Every :class:`.Dimension` object is associated with a :class:`.Context` object, in which the base quantities are defined.

:class:`.Dimension` objects can be multiplied or divided, which adds or subtracts the encapsulated dimensional exponents, respectively.

Each object has ``numerator`` and ``denominator`` members that hold tuples of dimensional exponents.
This structure allows the dimensions of a 'dimensionless' quantity to be retained. 

There is a difference in the way the ``numerator`` and ``denominator`` members are manipulated by the division operation compared to the 'floor division' operation (the operator ``\\``). When the division operator is used, the numerator of the right-hand operand is subtracted from the numerator of the left-hand operand, and similarly for the denominator. However, when floor division is used, the denominator of the right-hand operand is added to the numerator of the left-hand operand and the numerator of the right-hand operand is added to the denominator of the left-hand operand. Thus, a dimensionless ratio created using the operator ``\\`` retains information about the dimensions of the quantity. 

For instance ::

    
.. contents::
   :local:


.. _dimension_module:

.. automodule:: QV.dimension
    :members: 
    :inherited-members:
