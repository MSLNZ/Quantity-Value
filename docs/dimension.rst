.. _dimension:

*********
Dimension
*********

The :class:`.Dimension` class defines objects that encapsulate the dimensional exponents associated with the measure of a quantity. 

Every :class:`.Dimension` object is associated with a :class:`.Context` object, in which the base quantities are defined.

:class:`.Dimension` objects can be multiplied or divided, which adds or subtracts the dimensional exponents, respectively.

Each object ``numerator`` and ``denominator`` members which hold tuples of dimensional exponents. Usually, the denominator will contain only zero exponents and in that case the object is said to be in `simplified` form. However, the 'floor division' operator ``\\`` is defined for :class:`.Dimension`, as well as regular division, and can be used to retain information about the dimensions of a 'dimensionless' quantity. 

When floor division is used, the denominator of dimensions of the right-hand operand is added to the numerator of the left-hand operand and the numerator of the right-hand operand is added to the denominator of the left-hand operand. So, when the right and left-hand arguments have the same dimensions, and both are in simplified form, a dimensionless ratio created by ``\\`` retains dimensional information about the original arguments. Regular division, on the other hand, subtracts the numerator of the right-hand operand from the numerator of the left-hand operand, and similarly for the denominator. So, when the right and left-hand arguments have the same dimensions, the result is dimensionless but information about the dimensions of the original arguments is lost.

.. contents::
    :local:

.. _dimension_module:

.. automodule:: QV.dimension
    :members: 
    :inherited-members:
