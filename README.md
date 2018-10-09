# error-propagation
Quick and somewhat dirty library for error propagation of single values.

Bugfixes, extensions generally welcome.

# Basics
    In errors.py is defined a basic class intended for e.g. ipython use 
    which defines a value with associated error for error propagation with 
    constants and/or other Values. Floor division is not defined. Bitwise 
    addition (& operator) gives the weighted mean of two values, equivalent to
    combining two measurements.

    It can also be used for error propagation of numpy arrays in a similar manner
    
# Installation:
    To install, simply clone and add errors.py into your pythonpath. For more 
    global use, add directly into your python site-packages directory.
    
# Initialisation:
```
          from errors import Value
          x = Value(value, error)
```
# Example use:
```
          x = Value(1,3)         # Initialises value 1 +/- 2
          y = Value(2,4)         # Initialises value 2 +/- 4
          z = Value(1,3)         # Initialises value 1 +/- 2
          
          Expression -> Output
          -------------------------------------
          2*x        -> Value(2,6)
          x**2       -> Value(1,6)
          x + y      -> Value(3,5)
          x - y      -> Value(-1,5)
          x + 4      -> Value(5,3)
          x - 4      -> Value(-3,3)
          x*y        -> Value(2,7.21110255093)
          x/y        -> Value(0.5,1.80277563773)
          x == z     -> True
          x == y     -> False
          x == x     -> True
          x & y      -> Value(1.36, 2.4)

          >> x.percent_error
               300.0

    It is also possible to use the functionality for numpy arrays. If numpy
    is not available this functionality is not loaded.
    For example:
       x = Value(np.array([1,2]),np.array([3,2]))   # Initialises Values [1,2]
                                                    # Initialises Errors [3,2]
       x*2 -> Value([2,4],[6,4])
    and so on.
```
