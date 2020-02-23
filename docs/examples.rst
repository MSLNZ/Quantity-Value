.. _examples:

********
Examples
********

Simple kinematics
=================

When using the package, the first task is to select a set of base dimensions. 

For instance, the basis :math:`LT` (distance and duration) may be used for a straight-line kinematics problems. Other kinds of quantity are then declared in terms of this basis, for example the dimensions of speed are :math:`LT^{-1}`. 

.. code-block:: python 

    from QV import *
    
    context = Context( ("Length","L"),("Time","T") )
    context.declare('Speed','V','Length/Time')

Here, the object ``context`` maintains one-to-one relationships between the names, and short symbols, of kinds of quantities and the dimensions associated with measurements of them. So, after the declaration of speed, ``context`` will not allow any other quantity with the same dimensions to be declared. 

Units are defined in relation to kinds of quantity. In this case, we might write 

.. code-block:: python 

    SI =  UnitRegister("SI",context)

    metre = SI.reference_unit('Length','metre','m') 
    second = SI.reference_unit('Time','second','s') 
    metre_per_second = SI.reference_unit( 'Speed','metre_per_second','m/s' )

Here, the ``SI`` object is a register of units, each associated with the measurement of a kind of quantity and hence to the dimensions of that quantity in the context. The ``unit`` declaration creates a reference unit within the register; other units of the same kind of quantity can also be registered, but must be related to the reference unit by a conversion factor (see below, where a related unit, L/(100 km), is created for fuel consumption.)

Quantity values may be defined with the function ``qvalue()`` and used in calculations. For instance, 

.. code-block:: python 

    d = qvalue(0.5,metre)
    t = qvalue(1.0,second)
    print( "average speed =", qresult(d/t) )

    v0 = qvalue(5.2,metre_per_second)
    x0 = qvalue(0.3,metre)
    print( "displacement =", x0 + v0*t )

The output is 

.. code-block:: pycon 

    average speed = 0.5 m/s
    displacement = 5.5 m

An interesting implementation detail is apparent here. The function ``qresult()`` is applied to ``d/t`` to resolve the units, but it is not used in the calculation of ``x0 + v0*t``. The reason is that individual multiplications or divisions are often just intermediate steps in a calculation. So, QV will not try to resolve the kind of quantity of an operation until signalled to do so. However, addition and subtraction of different kinds of quantity is forbidden by quantity calculus. So, the sum in ``x0 + v0*t`` must be validated before execution, and this requires QV to resolve the units of ``v0*t``. 

Fuel consumption
================
When `ad hoc` units are preferred, this package facilitates their use. For example, fuel consumption is typically stated in units of litres per 100 km. This can be handled as follows [#FN1]_  

.. code-block:: python 

    from fractions import Fraction
    
    context = Context( ("Distance","L"), ("Volume","V") )
    FuelConsumption = context.declare( 'FuelConsumption','FC','Volume/Distance' )
    
    ureg =  UnitRegister("ureg",context)

    # Reference units 
    kilometre = ureg.reference_unit('Distance','kilometre','km') 
    litre = ureg.reference_unit('Volume','litre','L')
    litres_per_km = ureg.reference_unit( 'FuelConsumption','litres_per_km','L/km' )
    
    litres_per_100_km = related_unit(
         litres_per_km,
         Fraction(1,100),
         'litres_per_100_km','L/(100 km)'
    )

Calculations proceed as might be expected 

.. code-block:: python 

    distance = qvalue(25.6,kilometre)
    fuel = qvalue(2.2,litre)
    
    consumes = fuel/distance
    print( "average consumption =", qresult( consumes, litres_per_100_km ) )
    
    distance = qvalue(155,kilometre)
    print( 'fuel required =', qresult( consumes * distance ) )

which gives the following results [#FN2]_.  

.. code-block:: pycon 

    average consumption = 8.59375 L/(100 km)
    fuel required = 13.3203125 L
    
It is interesting that QV can treat distance and volume as quite distinct quantities, although they share the dimension of length in the SI [#FN3]_. 

Electrical quantities
=====================

Electrical measurements involve particular quantities, and associated units. We can use base dimensions :math:`V`, :math:`I` and :math:`T`, for potential difference, current and duration, respectively. Then additional kinds of quantity of interest include: resistance, capacitance, inductance, energy, power and angular frequency. The context can be configured, as follows 

.. code-block:: python  

    context = Context( ("Current","I"),("Voltage","V"),("Time","T") )
    
    context.declare('Resistance','R','Voltage/Current')
    context.declare('Capacitance','C','I*T/V')
    context.declare('Inductance','L','V*T/I')
    context.declare('Angular_frequency','F','1/T')
    context.declare('Power','P','V*I')
    context.declare('Energy','E','P*T')

Suitable units are:

.. code-block:: python 

    ureg =  UnitRegister("Reg",context)
    
    volt = ureg.reference_unit('Voltage','volt','V') 
    second = ureg.reference_unit('Time','second','s') 
    ampere = ureg.reference_unit('Current','ampere','A') 
    ohm = ureg.reference_unit('Resistance','Ohm','Ohm')
    henry = ureg.reference_unit('Inductance','henry','H')
    rad_per_s = ureg.reference_unit( 'Angular_frequency','radian_per_second','rad/s' )
    watt = ureg.reference_unit('Power','watt','W')
    joule = ureg.reference_unit('Energy','joule','J')

Calculations are then straightforward. For example, 

.. code-block:: python 

    from math import pi

    v1 = qvalue(0.5,volt)
    i1 = qvalue(1.E-3,ampere)
    l1 = qvalue(0.3E-3,henry)
    w1 = qvalue(2*pi*2.3E3,rad_per_s)
    
    r1 = v1/i1
    
    print( "resistance =", qresult(r1) )
    print( "reactance =", qresult(w1*l1) )
    print( "energy =", qresult(0.5*l1*i1*i1) )
    print( "power =", qresult(v1*i1) )
    
    r2 = qvalue(2.48E3,ohm)
    print(  "parallel resistance =",  qresult( (r1*r2)/(r1 + r2) ) )

Which produces 

.. code-block:: pycon 

    resistance = 500.0 Ohm
    reactance = 4.33539786195 Ohm
    energy = 1.5e-10 J
    power = 0.0005 W
    parallel resistance = 416.10738255 Ohm

Ratios
======

Ratios of the same kind of quantities arise frequently in calculations. These ratios are often described as `dimensionless` quantities, but they are not plain numbers and the quantities involved should not be ignored. 

Dimensionless ratios can retain quantity information if defined using the function ``qratio``. 

For example, continuing the electrical case above (where ``r1`` and ``r2`` were evaluated), a resistor network may be used to scale down a voltage by some fraction (often called a potential, or resistive, divider). The resistance ratio can be defined as a dimensionless quantity in this way

.. code-block:: python 

    context.declare( 'Resistance_ratio','R/R', 'Resistance//Resistance' )
    ureg.reference_unit('Resistance_ratio','ohm_per_ohm','Ohm/Ohm')
    
    divider = qratio( r2,(r1+r2) )
    
    v_in = qvalue( 5.12, volt) 
    v_out = qresult(divider * v_in)
    
    if divider.unit.is_ratio_of(ohm.kind_of_quantity):
        print( "Resistive divider" )
        print( "  ratio =", divider )
        print( "  v_out =", v_out )

which produces the output 

.. code-block:: pycon 
  
    Resistive divider
      ratio = 0.832214765101 Ohm/Ohm
      v_out = 4.26093959732 V 

Note, we use the operator ``//`` when declaring a dimensionless ratio as a kind of quantity. This is necessary to preserve information about the quantities in the ratio.

Another example is the voltage gain of an amplifying stage 

.. code-block:: python 

    from QV.prefix import micro
    
    context.declare('Voltage_ratio','V/V','Voltage//Voltage')
    volt_per_volt= ureg.reference_unit('Voltage_ratio','volt_per_volt','V/V')

    volt_per_millivolt = related_unit(volt_per_volt,1E3,'volt_per_millivolt','V/mV')
    volt_per_microvolt = related_unit(volt_per_volt,1E6,'volt_per_micovolt','V/uV')
        
    v1 = qvalue(0.5,volt)
    v2 = qvalue(0.5,micro(volt))
    gain = qratio( v1, v2 )    
    
    print( "Gain =", qresult(gain) )
    print( "Gain =", qresult(gain,volt_per_microvolt) )
    print( "Gain =", qresult(gain,volt_per_millivolt) )
    print( "Gain =", qresult(gain,volt_per_volt) )

The output is (Note, when no preferred unit is given (the first case), units are simplified to a dimensionless quantity.) 

.. code-block:: pycon 

    Gain = 1000000.0
    Gain = 1.0 V/uV
    Gain = 1000.0 V/mV
    Gain = 1000000.0 V/V
 
Angles
======

It is well known that some SI quantities cannot be distinguished by dimensional analysis because they have the same dimensions [Brownstein]_. This ambiguity can be removed by introducing a base dimension for angle, and a new dimensional constant :math:`\eta`, but then some of the basic equations of physics also have to be changed [Quincey]_. 

It is not as bad as it sounds. For example, the well-known equation 

.. math::

    s = r \cdot \theta \;,

for the length of arc subtended by an angle :math:`\theta` on a circle of radius :math:`r`, becomes 

.. math::

    s = \eta \cdot r \cdot \theta \;.

In this equation, :math:`\theta` has the dimension :math:`A` and the constant :math:`\eta` has the dimension :math:`A^{-1}`, so :math:`s` has the dimension of length, as expected (references [Brownstein]_ and [Quincey]_ should be consulted for more detail).

No one is suggesting that a dimension for angle should be added to the SI, however, a number of authors have remarked that using an extra dimension in computer systems would obtain more reliable dimensional homogeneity checks. The quantity-value package is perfect for this. The following simple example shows how the arc length calculation can be coded. More particularly, it shows how to introduce the dimension for angle and define the dimensional constant :math:`\eta`. 

.. code-block:: python 

    context = Context( ("Length","L"), ("Time","T"), ("Angle","A") )
    InverseAngle = context.declare('InverseAngle','1/A','1/A')

    xi = UnitRegister("xi",context)

    metre = xi.reference_unit('Length','metre','m') 
    second = xi.reference_unit('Time','second','s') 
    radian = xi.reference_unit('Angle','radian','rad') 
    inv_radian = xi.reference_unit('InverseAngle','per radian','1/rad') 

    from math import pi

    # Constants
    PI = qvalue( pi, radian )
    ETA = qresult( 1.0 / PI )
    
    print( "pi =", PI)
    print( "eta =", ETA )    

    radius = qvalue( 0.1, metre )
    angle = qresult( PI/8 )
    arc_length = qresult( ETA * angle * radius )

    print( "arc length =", arc_length )

The output displays 

.. code-block:: pycon 

    pi = 3.14159265359 rad
    eta = 0.318309886184 1/rad
    arc length = 0.0125 m
    
.. rubric:: Footnotes

.. [#FN1] The distance reference unit could have been chosen as  100 km, instead of 1 km, but it seems more natural to proceed as shown. The reference unit for consumption, ``litres_per_km``, is determined by the reference units for volume and distance. The related unit of ``litres_per_100_km`` must be introduced with an appropriate scale factor.
.. [#FN2] The argument ``litres_per_100_km`` is passed to ``qresult()``  to obtain results in the required unit. The default would be the reference unit declared for the kind of quantity (``litres_per_km`` in this case). 
.. [#FN3] Reduced to SI base units, the consumption is about :math:`8.6 \times 10^{-8}\,m^2`. This area, multiplied by the distance travelled, is the volume of fuel required.

.. [Brownstein] K. R. Brownstein, *Angles - lets treat them squarely*, `Am. J. Phys. 65(7), July 1997, pp 605-614 <https://doi.org/10.1119/1.18616>`_ .
.. [Quincey] P. Quincey and R. J. C. Brown, *Implications of adopting plane angle as a base quantity in the SI*, `Metrologia 53, 2016, pp 998-1002 <https://doi.org/10.1088/0026-1394/53/3/998>`_.

