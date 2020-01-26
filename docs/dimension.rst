.. _dimension:

*********
Dimension
*********

The :class:`.Dimension` class defines objects that hold the dimensional exponents associated with the measure of a quantity. 

Every :class:`.Dimension` is associated with a :class:`.Context`, in which a set of base quantities is defined.

:class:`.Dimension` objects can be multiplied or divided, which adds or subtracts the dimensional exponents, respectively.

Each :class:`.Dimension` has ``numerator`` and ``denominator`` members, which hold tuples of dimensional exponents. Usually, the denominator will contain only zero exponents, in which case the object is in `simplified` form. 

The 'floor division' operator ``\\`` is defined for :class:`.Dimension`. This is an alternative to regular division, which can be used to retain information about the dimensions of a 'dimensionless' quantity. When floor division is used, the denominator of the :class:`.Dimension` of the right-hand operand is added to the numerator of the left-hand operand and the numerator of the right-hand operand is added to the denominator of the left-hand operand. So, when the right and left-hand arguments have the same dimensions, and both are in simplified form, a dimensionless ratio created by ``\\`` retains information about the dimensions of the original arguments. Regular division, on the other hand, subtracts the numerator of the right-hand operand from the numerator of the left-hand operand, and similarly for the denominator. So, when the right and left-hand arguments have the same dimensions, the numerator and denominator of the resulting :class:`.Dimension` will contain only zeros; the result is dimensionless with no information about the dimensions of the original arguments.

.. contents::
    :local:

.. _dimension_module:

.. automodule:: QV.dimension
    :members: 
    :inherited-members:
