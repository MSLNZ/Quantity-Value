.. _examples:

********
Examples
********

Simple kinematics
=================

When using the package, the first task is to select a set of base dimensions. This basis is immutable after definition. 

For instance, the basis :math:`LT` (distance and duration) may be used for a straight-line kinematics problems. Other kinds of quantity are then declared in terms of this basis, for example the dimensions of speed are :math:`LT^{-1}`. ::

    from QV import *
    
    context = Context( ("Length","L"),("Time","T") )
    context.declare('Speed','V','Length/Time')

Here, the object ``context`` maintains one-to-one relationships between the names, and short symbols, of kinds of quantities and the dimensions associated with measurements of them. So, after the declaration of speed, ``context`` will not allow any other quantity with the same dimensions to be declared. 

Units are defined in relation to kinds of quantity. In this case, we might write ::

    SI =  UnitRegister("SI",context)

    metre = SI.unit('Length','metre','m') 
    second = SI.unit('Time','second','s') 
    metre_per_second = SI.unit( 'Speed','metre_per_second','m/s' )

Here, the ``SI`` object is a register of units, each associated with the measurement of a kind of quantity and hence to the dimensions of that quantity in the context. The ``unit`` declaration creates a reference unit within the register; other units of the same kind of quantity can also be registered, but must be related to the reference unit by a conversion factor (see below, where a related unit, L/(100 km), is created for fuel consumption.)

Quantity values may be defined with the function ``qvalue()`` and used in calculations. For instance, ::

    d = qvalue(0.5,metre)
    t = qvalue(1.0,second)
    print( "average speed =", qresult(d/t) )

    x = qvalue(0.5,metre)
    t = qvalue(1.0,second)
    print( "displacement =", x0 + v0*t )

The output is ::

    average speed = 0.5 m/s
    displacement = 5.5 m

An interesting implementation detail is apparent here. The function ``qresult()`` is applied to ``d/t`` to resolve the units, but it is not used in the calculation of ``x0 + v0*t``. The reason is that individual multiplications or divisions are often just intermediate steps in a calculation. So, QV will not try to resolve the kind of quantity of an operation until signalled to do so. However, addition and subtraction of different kinds of quantity is forbidden by quantity calculus. So, the sum in ``x0 + v0*t`` must be validated before execution, and this requires QV to resolve the units of ``v0*t``. 

Fuel consumption
================
When `ad hoc` units are preferred, this package facilitates their use. For example, fuel consumption is typically stated in units of litres per 100 km. This can be handled as follows [#FN1]_  ::

    context = Context( ("Distance","L"), ("Volume","V") )
    FuelConsumption = context.declare( 'FuelConsumption','FC','Volume/Distance' )
    
    ureg =  UnitRegister("ureg",context)

    # Reference units 
    kilometre = ureg.unit('Distance','kilometre','km') 
    litre = ureg.unit('Volume','litre','L')
    litres_per_km = ureg.unit( 'FuelConsumption','litres_per_km','L/km' )
    
    litres_per_100_km = related_unit(
    ...     litres_per_km,
    ...     Fraction(1,100),
    ...     'litres_per_100_km','L/(100 km)'
    ...     )

Calculations proceed as might be expected

    distance = qvalue(25.6,kilometre)
    fuel = qvalue(2.2,litre)
    
    consumes = fuel/distance
    print( "average consumption =", qresult( fuel/distance, litres_per_100_km ) )
    
    distance = qvalue(155,kilometre)
    print( 'fuel required =', qresult( consumes * distance ) )

which gives the following results [#FN2]_.  ::

    average consumption = 8.59375 L/(100 km)
    fuel required = 13.3203125 L
    
It is interesting that QV is able to treat distance and volume as quite distinct quantities, whereas they share the dimension of length in the SI [#FN3]_. 

Electrical quantities
=====================
Electrical problems use particular quantities, and associated units. With basis dimensions :math:`VIT`, for potential difference, current and duration, respectively, additional kinds of quantity of interest include: resistance, capacitance, inductance, energy, power and angular frequency. The context can be configured, as follows :: 

    context = Context( ("Current","I"),("Voltage","V"),("Time","T") )
    
    context.declare('Resistance','R','Voltage/Current')
    context.declare('Capacitance','C','I*T/V')
    context.declare('Inductance','L','V*T/I')
    context.declare('Angular_frequency','F','1/T')
    context.declare('Energy','E','P*T')
    context.declare('Power','P','V*I')

Suitable units are:

    ureg =  UnitRegister("Reg",context)
    
    volt = ureg.unit('Voltage','volt','V') 
    second = ureg.unit('Time','second','s') 
    ampere = ureg.unit('Current','ampere','A') 
    ohm = ureg.unit('Resistance','Ohm','Ohm')
    henry = ureg.unit('Inductance','henry','H')
    rad_per_s = ureg.unit( 'Angular_frequency','radian_per_second','rad/s' )
    joule = ureg.unit('Energy','joule','J')
    watt = ureg.unit('Power','watt','W')

Calculations are then straightforward. For example, ::

    v1 = qvalue(0.5,volt)
    i1 = qvalue(1.E-3,ampere)
    l1 = qvalue(0.3E-3,henry)
    w1 = qvalue(2*PI*2.3E3,rad_per_s)
    
    r1 = v1/i1
    
    print( "resistance =", qresult(r1) )
    print( "reactance =", qresult(w1*l1) )
    print( "energy =", qresult(0.5*l1*i1*i1) )
    print( "power =", qresult(v1*i1) )
    
    r2 = qvalue(2.48E3,ohm)
    print(  "parallel resistance =",  qresult( (r1*r2)/(r1 + r2) ) )

Which produces ::

    resistance = 500.0 Ohm
    reactance = 4.33539786195 Ohm
    energy = 1.5e-10 J
    power = 0.0005 W
    parallel resistance = 416.10738255 Ohm


Dimensionless ratios
--------------------

Ratios of quantities of the same kind often arise in physical calculations. They are usually described as `dimensionless` quantities, because the ratio is independent of the choice of units. Nonetheless, they are not plain numbers; the quantities involved should not be ignored. 

In this package, dimensionless quantity ratios retain quantity information when they are defined using the function ``qratio``. A typical example of a dimensionless quantity in the electrical context, considered above, is a resistance ratio (potential divider). Adding to the code shown above (where ``r1`` is evaluated), ::

    context.declare( 'Resistance_ratio','R/R', 'Resistance//Resistance' )
    ureg.unit('Resistance_ratio','ohm_per_ohm','Ohm/Ohm')
    
    r2 = qvalue(2.48E3,ohm)
    divider = qratio( r2,(r1+r2) )
    
    v_in = qvalue( 5.12, volt) 
    
    koq_dim = context.dimensions( divider.unit.kind_of_quantity.name )
    if koq_dim.is_ratio_of( context.dimensions('Resistance') ):
        print( "Resistive divider" )
        print( "  ratio =",divider )
        print( "  v_out =", qresult(v_divider * v_in) )

produces the output ::
  
    Resistive divider
      ratio = 0.832214765101 Ohm/Ohm
      v_out = 4.26093959732 V

.. [#FN1] The distance reference unit could have been chosen as  100 km, instead of 1 km, but it seems more natural to proceed as shown. The reference unit for consumption, ``litres_per_km``, is determined by the reference units for volume and distance. The related unit of ``litres_per_100_km`` must be introduced with an appropriate scale factor.
.. [#FN2] The argument ``litres_per_100_km`` is passed to ``qresult()``  to obtain results in the required unit. The default would be the reference unit declared for the kind of quantity (``litres_per_km`` in this case). 
.. [#FN3] Reduced to SI base units, the consumption is about :math:`8.6 \times 10^{-8}\,m^2`. This area, multiplied by the distance travelled, is the volume of fuel required.



