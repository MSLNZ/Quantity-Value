.. _signature:

*********
Signature
*********

The :class:`.Signature` class defines objects that hold a signature associated with a kind of quantity. 

Every :class:`.Signature` is associated with a :class:`.Context`, in which a set of base quantities is defined.

:class:`.Signature` objects can be multiplied or divided. 

Every :class:`.Signature` object has ``numerator`` and ``denominator`` members, which hold tuples of elements. Usually, the denominator contains zero values, and the object is said to be in `simplified` form. However, the denominator can be loaded with non-trivial element values by using the 'floor division' operator ``\\``. 

The 'floor division' operator ``\\`` is an alternative to regular division. When floor division is used, the denominator of the :class:`.Signature` of the right-hand operand is added to the numerator of the left-hand operand and the numerator of the right-hand operand is added to the denominator of the left-hand operand. So, when the right and left-hand arguments have the same signatures, and both are in simplified form, a dimensionless ratio created by ``\\`` retains information about the signatures of the original arguments. Regular division, on the other hand, subtracts the numerator of the right-hand operand from the numerator of the left-hand operand, and similarly for the denominator. So, when the right and left-hand arguments have the same signatures, the numerator and denominator of the resulting :class:`.Signature` will result in only zeros; the result is dimensionless with no information about the signatures of the original arguments.

.. contents::
    :local:

.. _dimension_module:

.. automodule:: QV.signature
    :members: 
    :inherited-members:
