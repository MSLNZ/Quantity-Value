.. _introduction:

************
Introduction
************

This package supports the representation of physical quantities as a measured value paired with a unit, for example 10.5 kg. It is possible to declare quantities like ``m = qvalue(10.5,kg)`` and then use ``m`` in mathematical expressions. The rules governing calculations with quantities are handled by the software.

The package intended to become a tool to ensure quantity correctness in calculations that manipulate physical quantities, but it is still in the early stages of development. 

Background
==========

The correct way to express a physical quantity, such as the mass 940 kg, is as a measure (a number) paired with a unit, where the unit is associated with the same kind of quantity as is being measured  (the unit is in fact the name of the measurement scale used). Writing the measure alone is not acceptable, because information about what can be done with the measure is lost. The rules of quantity calculus are not the same as pure numbers. For instance, only quantities of the same kind may be added; so, 940 kg + 60 kg is permitted, and evaluates to 1000 kg, but 940 kg + 60 cannot be evaluated. 

When digital systems handle data representing physical quantities, one might expect software support for physical quantities to be used. However, this is rarely the case. Why this should be so is not clear, perhaps no need is perceived; but if so, that would be wishful thinking. Famous failures to handle physical data correctly include the loss of NASA's Mars Climate Observer, in 1999, and the so-called Gimli Glider incident, in 1983, when a commercial Air Canada flight ran out of fuel. Support is needed now more than ever, because there is a huge increase in the amount of measurement data being generated and processed automatically by digital systems. 

From early days of general-purpose computing in the 1970s to the present, many suggestions have been made about how to support quantities, but no general solution has emerged. It appears that the challenge of encoding the semantics of physical quantity data in software is harder than it appears. This project is trying to use contextual information about a problem to tailor support to the context. The approach is similar to what happens in scientific writing. Careful attention must be given to a description of terms in calculations when quantities are involved. Without this, a text becomes obscure and only a reader familiar with the missing contextual information can make sense of it. Similar principles should apply to software representations of quantities. 

Our work addresses the difficulties encountered when units are encoded by their dimensional exponents in a conventional basis. When quantity calculus is then used to track quantities, there are inevitably problems of ambiguity and difficulties of expression. For instance, fuel consumption is conventionally expressed in L/(100 km) but has the dimensions of area (in the SI), whereas rainfall, when measured as a volume divided by a cross-sectional area, is conventionally simplified and reported as a length. There are also the many so-called 'dimensionless' quantities which are effectively unit-less, but certainly should not be considered pure numbers. And then there is the problem of disambiguating quantities like torque and energy, which have the SI dimensions :math:`M^2LT^{-2}`, because the choice of base quantities is inadequate. 

Kind of quantity, individual quantity and quantity value
--------------------------------------------------------
A distinction is made between a `kind of quantity` and an `individual quantity`. Kind of quantity is the more general concept, for example: `length`, `mass`, etc, [VIM_S1.2]_. Whereas, an individual quantity is specific, for example: the mass of a particular car, :math:`m_\mathrm{car}`, 940 kilograms, etc. Also, when an individual quantity is presented as a measure paired with a unit, it may be called a `quantity value` [VIM_S1.19]_. When the intended meaning is clear in the context,  we will simply use `quantity` for any of: 'kind of quantity', 'individual quantity' or 'quantity value'.

Dimensions and dimensional exponents
------------------------------------
Dimensions were introduced by Joseph Fourier, in 1822, as a way to calculate the scale factor to adjust a measure when units are changed. Dimensions are usually expressed as a product of variables (one for each base quantity) that may be exponentiated. The symbols chosen recall the kind of quantity on which the measure depends (so they often `appear` to be associated with the kind of quantity, when really they are associated with the particular scale used). For example, the dimensions for a measure of speed in the SI are :math:`{L}{T}^{-1}`, where :math:`{L}` is the variable (dimension) associated with length and :math:`{T}` the variable (dimension) associated with time. The dimensional exponent -1 applied to :math:`{T}` means that :math:`{L}` is divided by :math:`{T}`. So, to transform a speed of 50 km/h into metres per second, 50 will be multiplied by 1000/3600, giving a speed of approximately 13.89 m/s.

Quantity calculus
-----------------
The rules of quantity calculus are usually presented as arithmetic operations applied to dimensions. Such as: the dimensions of a product of quantity values is obtained as the products of the corresponding dimensions of each factor (so the exponents of the same dimensional variable are added). For example, the distance covered by a body, initially at rest, moving with a constant acceleration, :math:`a`, for a time, :math:`t`, is :math:`s = \frac{1}{2}at^2`. In the SI, the dimensions for a measure of :math:`a` are :math:`{L}{T}^{-2}` and the dimensions of an elapsed time squared are :math:`{T}^2`. So, on the right-hand side of the equation, the product of dimensions, :math:`{L}`, matches the dimension of the distance, :math:`s`. (When dimensions balance on either side of an equation it is called `dimensional homogeneity` and is a necessary condition for equality. Homogeneity ensures that the equation remains true even when the measurement units change.)

Dimensional analysis
--------------------
Dimensional analysis is based on the idea that physical laws do not depend on the units in which quantities are measured. It is an analytical technique used to study relationships among quantities subject to a physical laws. 

The seven familiar SI base units and the convention of representing other units as a product of base-unit symbols, possibly exponentiated, is an application of dimensional analysis [SI_brochure]_. Hoverer, it is important to remember that the choice of SI dimensions is conventional. There is still freedom to choose the most convenient set of dimensions for a particular problem. It is also useful to remember that SI symbols are really just names for scales. The process of generating a name (by multiplying and dividing the names of base units) does not guarantee the existence of a meaningful physical quantity to be measured.  

.. rubric:: Footnotes

.. [VIM_S1.2] The international vocabulary of metrology—basic and general concepts and associated terms (section 1.2), online: https://www.bipm.org/en/publications/guides/.
.. [VIM_S1.19] The international vocabulary of metrology—basic and general concepts and associated terms (section 1.19), online: https://www.bipm.org/en/publications/guides/.
.. [SI_brochure] The International System of Units (SI): https://www.bipm.org/en/publications/si-brochure/