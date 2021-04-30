.. _context:

*******
Context
*******

.. contents::
   :local:

The :mod:`.context` module provides support for calculations with quantities, in combination with the modules :mod:`.signature` and :mod:`.kind_of_quantity`. Kinds of quantity are associated with unique signatures in a context. 

A :class:`.Context` is initialised by a set of quantities, which become a basis for that context. Other kinds of quantity can be declared by providing an expression that describes quantity in terms of the base quantities and possibly other quantities already declared. 

For instance, in the following code block, resistance is declared in terms of voltage and current and power is declared in terms of voltage and resistance. The signature of power is :math:`\mathrm{I}^1\mathrm{V}^1\mathrm{T}^0`, which is displayed by the print statement as ``(1,1,0)``. 

.. code-block:: python 

    from QV import *
    
    context = Context(
        ("Current","I"),("Voltage","V"),("Time","T")
    )
    
    context.declare('Resistance','R','Voltage/Current')
    context.declare('Power','P','V*V/R')
    print( context.signature('P') )

:class:`.KindOfQuantity` objects can be retrieved from a context and used in expressions:

.. code-block:: python 

    Voltage = context['Voltage']
    Resistance = context['Resistance']
    
    tmp = Voltage/Resistance
    
    print( tmp )
    print( context.evaluate( tmp ) )

which displays 

.. code-block:: pycon 

    Div(V,R) 
    I 
    
Here ``tmp`` is an intermediate result obtained by dividing objects representing voltage and current. QV does not automatically try to resolve intermediate results. The method :meth:`.Context.evaluate` must be used explicitly to resolve the kind of quantity of a temporary object. 
 
.. _context_module:

.. automodule:: QV.context
    :members: 
    :inherited-members:
