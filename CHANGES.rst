=============
Release Notes
=============

Version 0.2.0 (30 April 2021)
=============================

    * Terminology has changed substantially. Use of the term 'dimension' in version 0.1.0 has been reconsidered and in many cases we now write 'signature' instead. This allows us to use the term 'dimension' correctly.

    * The :class:`Dimension` class has been renamed :class:`.Signature`. The structure of a Signature class is now described in terms of a ratio of tuples containing numerical elements (rather than a ratio of dimensions composed of exponents).

    * The :class:`Unit` class has been renamed :class:`.RegisteredUnit` and placed in its own module, :mod:`.registered_unit`.

    * A hierarchy of scales classes is now provided: :class:`.Scale`, :class:`.OrdinalScale`, :class:`.IntervalScale` and :class:`.RatioScale` The :class:`.RatioScale` represents the behaviour of the units that were represented in the previous release (metric units).

    * Both :class:`.IntervalScale` and :class:`.RatioScale` have :meth:`conversion_function` methods that return a generic function for conversion between different scales for the same quantities. A new method :meth:`.UnitRegister.conversion_function_values` can be used to register the specific parameters required for value conversion between two scales using the `conversion_function`.

    * Support for Python 2 has been dropped.

Version 0.1.0 (24 Feb 2020)
===========================

    * First release.

    
    
    
    

